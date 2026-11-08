/* Works out "what changed" between two recorded steps, in plain words. */
import { isRef, prim, fmt, same, kindOf, attr } from './values.js';

export function frameVars(step) {
  const top = step.st[step.st.length - 1];
  return top ? top.v : [];
}

/* All (name, value) roots visible in a step, top frame first, plus self.<attr>. */
export function roots(step) {
  const out = [];
  const st = step.st || [];
  for (let i = st.length - 1; i >= 0; i--) {
    for (const [n, v] of st[i].v) {
      out.push({ name: n, v, frame: i, top: i === st.length - 1 });
      if (n === 'self' && isRef(v)) {
        const o = step.h[v.r];
        if (o && o.k === 'obj') for (const [an, av] of o.a) out.push({ name: `self.${an}`, v: av, frame: i, top: i === st.length - 1 });
      }
    }
  }
  return out;
}

export function changedIdx(a, b, heapA, heapB) {
  const ch = new Set();
  for (let i = 0; i < b.v.length; i++) {
    if (i >= a.v.length || !sameVal(a.v[i], b.v[i], heapA, heapB)) ch.add(i);
  }
  return ch;
}

export function sameVal(x, y, hx, hy, d = 0) {
  if (isRef(x) && isRef(y)) {
    if (x.r !== y.r) return false;
    if (d > 1) return true;
    const a = hx[x.r], b = hy[y.r];
    if (!a || !b) return a === b;
    if (a.k !== b.k) return false;
    if (a.k === 'obj') return same(a.a, b.a);
    if (!a.v || !b.v) return same(a, b);
    if (a.v.length !== b.v.length) return false;
    return a.v.every((e, i) => (a.k === 'dict' ? same(e, b.v[i]) : sameVal(e, b.v[i], hx, hy, d + 1)));
  }
  return same(x, y);
}

const keyStr = (k, h) => fmt(k, h);

/* Describe the changes from step a to step b (the effect of running a line). */
export function describe(a, b) {
  if (!a || !b) return [];
  const msgs = [];
  const done = new Set();
  const topA = a.st[a.st.length - 1], topB = b.st[b.st.length - 1];
  if (!topB) return msgs;
  const prevVars = new Map();
  for (const f of a.st) if (f.u === topB.u) for (const [n, v] of f.v) prevVars.set(n, v);
  const fresh = topA && topA.u !== topB.u && !a.st.some(f => f.u === topB.u);
  for (const [n, v] of topB.v) {
    if (n === 'self') continue;
    const had = prevVars.has(n);
    const old = prevVars.get(n);
    if (!had) {
      if (!fresh) msgs.push({ t: 'new', html: `<b>${n}</b> is born = <code>${fmt(v, b.h)}</code>` });
      continue;
    }
    if (isRef(v) && isRef(old) && v.r === old.r) {
      if (done.has(v.r)) continue;
      done.add(v.r);
      const m = structChange(n, a.h[v.r], b.h[v.r], a.h, b.h);
      if (m) msgs.push(m);
      continue;
    }
    if (!sameVal(old, v, a.h, b.h)) {
      msgs.push({ t: 'chg', html: `<b>${n}</b>: <code>${fmt(old, a.h)}</code> → <code>${fmt(v, b.h)}</code>` });
    }
  }
  // structures reached through other frames / object fields (e.g. self.stack, node.next)
  for (const id of Object.keys(b.h)) {
    if (done.has(+id) || !a.h[id]) continue;
    const o = b.h[id], p = a.h[id];
    if (o.k === 'obj' && p.k === 'obj' && !same(o.a, p.a)) {
      for (const [an, av] of o.a) {
        const pv = p.a.find(x => x[0] === an);
        if (!pv || !sameVal(pv[1], av, a.h, b.h, 2)) {
          const who = kindOf(o) === 'obj' ? o.cls : `node(${fmt(attr(o, 'val') ?? attr(o, 'key'), b.h)})`;
          msgs.push({ t: 'chg', html: `<b>${who}.${an}</b> now points to <code>${fmt(av, b.h)}</code>` });
        }
      }
      done.add(+id);
    }
  }
  const named = new Map();
  for (const r of roots(b)) if (isRef(r.v) && !named.has(r.v.r)) named.set(r.v.r, r.name);
  for (const [id, name] of named) {
    if (done.has(id) || !a.h[id] || !b.h[id]) continue;
    done.add(id);
    const m = structChange(name, a.h[id], b.h[id], a.h, b.h);
    if (m) msgs.push(m);
  }
  return msgs.slice(0, 6);
}

function structChange(n, p, o, ha, hb) {
  if (!p || !o || p.k !== o.k) return null;
  const f = v => fmt(v, hb), fa = v => fmt(v, ha);
  if (['list', 'deque', 'tuple'].includes(o.k)) {
    const A = p.v, B = o.v;
    if (B.length === A.length + 1 && A.every((x, i) => sameVal(x, B[i], ha, hb))) return { t: 'add', html: `added <code>${f(B[B.length - 1])}</code> to the end of <b>${n}</b>` };
    if (B.length === A.length + 1 && A.every((x, i) => sameVal(x, B[i + 1], ha, hb))) return { t: 'add', html: `added <code>${f(B[0])}</code> to the front of <b>${n}</b>` };
    if (B.length === A.length - 1 && B.every((x, i) => sameVal(x, A[i], ha, hb))) return { t: 'del', html: `removed <code>${fa(A[A.length - 1])}</code> from the end of <b>${n}</b>` };
    if (B.length === A.length - 1 && B.every((x, i) => sameVal(x, A[i + 1], ha, hb))) return { t: 'del', html: `removed <code>${fa(A[0])}</code> from the front of <b>${n}</b>` };
    if (B.length === A.length) {
      const ch = [...changedIdx(p, o, ha, hb)];
      if (!ch.length) return null;
      if (ch.length === 2 && sameVal(A[ch[0]], B[ch[1]], ha, hb) && sameVal(A[ch[1]], B[ch[0]], ha, hb)) return { t: 'swap', html: `swapped <b>${n}[${ch[0]}]</b> and <b>${n}[${ch[1]}]</b> (${fa(A[ch[0]])} ⇄ ${fa(A[ch[1]])})` };
      return { t: 'chg', html: ch.slice(0, 3).map(i => `<b>${n}[${i}]</b>: <code>${fa(A[i])}</code> → <code>${f(B[i])}</code>`).join(', ') + (ch.length > 3 ? ' …' : '') };
    }
    if (o.n !== p.n) return { t: 'chg', html: `<b>${n}</b> now has ${o.n} items` };
    return null;
  }
  if (o.k === 'set') {
    const A = new Set(p.v.map(fa)), B = new Set(o.v.map(f));
    const add = [...B].filter(x => !A.has(x)), del = [...A].filter(x => !B.has(x));
    if (add.length) return { t: 'add', html: `put <code>${add.slice(0, 3).join(', ')}</code> into <b>${n}</b>` };
    if (del.length) return { t: 'del', html: `took <code>${del.slice(0, 3).join(', ')}</code> out of <b>${n}</b>` };
    return null;
  }
  if (o.k === 'dict') {
    const A = new Map(p.v.map(([k, v]) => [keyStr(k, ha), v]));
    const out = [];
    for (const [k, v] of o.v) {
      const ks = keyStr(k, hb);
      if (!A.has(ks)) out.push(`new key <b>${n}[${ks}]</b> = <code>${f(v)}</code>`);
      else if (!sameVal(A.get(ks), v, ha, hb)) out.push(`<b>${n}[${ks}]</b>: <code>${fa(A.get(ks))}</code> → <code>${f(v)}</code>`);
      A.delete(ks);
    }
    for (const k of A.keys()) out.push(`deleted key <b>${n}[${k}]</b>`);
    return out.length ? { t: 'chg', html: out.slice(0, 3).join(', ') } : null;
  }
  return null;
}
