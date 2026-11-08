/* Draws one recorded step: variables, arrays, maps, lists, trees, graphs, call stack… */
import { isRef, isStr, prim, fmt, kindOf, attr, nodeLabel, esc } from './values.js';
import { roots, changedIdx, sameVal } from './diff.js';

const PTR = /^(i|j|k|l|r|m|lo|hi|low|high|mid|left|right|start|end|begin|slow|fast|p|q|p1|p2|idx|index|ptr|pos|w|write|read|insert|top|L|R|a_i|b_i|ii|jj|first|last|col|row|c|x|y)$|(_idx|_i|_ptr|Idx|_pos|_index)$/;
const COLORS = ['#ff7eb6', '#5fa8ff', '#ffb547', '#3ccf91', '#a88bff', '#ff8a5c', '#33c4d6', '#e86bd8'];
const FIXED = { i: 0, l: 0, left: 0, lo: 0, low: 0, slow: 0, start: 0, p1: 0, j: 1, r: 1, right: 1, hi: 1, high: 1, fast: 1, end: 1, p2: 1, mid: 2, m: 2, k: 3, row: 3, col: 4 };
export function tagColor(name) {
  if (name in FIXED) return COLORS[FIXED[name]];
  let h = 0;
  for (const c of name) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return COLORS[h % COLORS.length];
}
const tag = (n) => `<span class="ptag" style="--c:${tagColor(n)}">${esc(n)}</span>`;
const pretty = (v, h) => esc(fmt(v, h));
const cellText = (v, h) => {
  if (isStr(v)) return esc(v.s.length > 6 ? v.s.slice(0, 6) + '…' : v.s);
  const o = isRef(v) ? h[v.r] : null;
  if (o && ['lnode', 'tnode', 'gnode'].includes(kindOf(o))) return '•' + esc(nodeLabel(o, h));
  const s = fmt(v, h);
  return esc(s.length > 9 ? s.slice(0, 8) + '…' : s);
};

/* ---------------- main ---------------- */
export function renderState(el, step, prev, trace, opts = {}) {
  if (!step) { el.innerHTML = '<div class="viz-empty">Nothing to show yet.</div>'; return; }
  const h = step.h, ph = prev ? prev.h : {};
  const all = roots(step);
  const top = step.st[step.st.length - 1];
  const topVars = top ? top.v : [];

  const namesOf = new Map();
  for (const r of all) if (isRef(r.v)) {
    if (!namesOf.has(r.v.r)) namesOf.set(r.v.r, []);
    const arr = namesOf.get(r.v.r);
    if (!arr.includes(r.name) && arr.length < 4) arr.push(r.name);
  }
  const ptrs = [];
  for (const r of all) {
    if (!r.top || typeof r.v !== 'number' || !Number.isInteger(r.v)) continue;
    if (PTR.test(r.name) || (opts.pointers || []).includes(r.name)) ptrs.push([r.name, r.v]);
  }

  const prevTop = new Map();
  if (prev) for (const f of prev.st) if (top && f.u === top.u) for (const [n, v] of f.v) prevTop.set(n, v);

  const parts = [];
  // 1) variable cards
  const cards = [];
  for (const [n, v] of topVars) {
    if (n === 'self') continue;
    const changed = prev && (!prevTop.has(n) || !sameVal(prevTop.get(n), v, ph, h));
    let val;
    if (prim(v)) val = pretty(v, h);
    else {
      const o = h[v.r];
      const kind = kindOf(o);
      const icon = { list: '▦', dict: '▤', set: '◇', deque: '⇄', tuple: '▦', lnode: '○', tnode: '○', gnode: '○', trie: '○', obj: '▣' }[kind] || '•';
      val = kind === 'lnode' || kind === 'tnode' || kind === 'gnode' ? `${icon} node(${esc(nodeLabel(o, h))})` : `${icon} <span class="see">${esc(kind === 'obj' ? o.cls : kind)} ↓</span>`;
    }
    cards.push(`<div class="vcard${changed ? ' flash' : ''}"><div class="vname">${esc(n)}</div><div class="vval">${val}</div></div>`);
  }
  if (cards.length) parts.push(section('Variables', 'vars', `<div class="vcards">${cards.join('')}</div>`));

  // 2) structures
  const shown = new Set();
  const structs = [];
  for (const r of all) {
    if (isStr(r.v) && r.top && ptrs.length && r.v.s.length >= 2 && r.v.s.length <= 60) {
      if (shown.has('s:' + r.name)) continue;
      shown.add('s:' + r.name);
      const fake = { k: 'list', v: [...r.v.s].map(c => ({ s: c })), n: r.v.s.length };
      structs.push(card(r.name, `string · ${r.v.s.length} chars`, arrayView(fake, h, ptrs, new Set(), false)));
      continue;
    }
    if (!isRef(r.v) || shown.has(r.v.r)) continue;
    const o = h[r.v.r];
    if (!o) continue;
    const kind = kindOf(o);
    if (['lnode', 'tnode', 'gnode', 'trie', 'func', 'class', 'other'].includes(kind)) continue;
    if (r.name === 'self') continue;
    shown.add(r.v.r);
    const names = namesOf.get(r.v.r) || [r.name];
    const html = structView(names[0], o, h, ph[r.v.r], ph, ptrs, opts, r.v.r);
    if (html) structs.push(card(names.join(' = '), html.sub, html.body));
  }
  if (structs.length) parts.push(section('Data structures', 'structs', structs.join('')));

  // 3) node-based structures (linked lists / trees / graphs / tries)
  const nodes = { lnode: [], tnode: [], gnode: [], trie: [] };
  for (const [id, o] of Object.entries(h)) {
    const k = kindOf(o);
    if (k in nodes) nodes[k].push(+id);
  }
  const varLabels = new Map();
  for (const r of all) if (isRef(r.v)) {
    if (!varLabels.has(r.v.r)) varLabels.set(r.v.r, []);
    const arr = varLabels.get(r.v.r);
    if (!arr.includes(r.name) && arr.length < 3 && (r.top || !arr.length)) arr.push(r.name);
  }
  if (nodes.lnode.length) parts.push(section('Linked list', 'll', linkedView(nodes.lnode, h, varLabels, trace)));
  if (nodes.tnode.length) parts.push(section('Tree', 'tree', treeView(nodes.tnode, h, varLabels, ph)));
  if (nodes.gnode.length) parts.push(section('Graph', 'graph', nodeGraphView(nodes.gnode, h, varLabels)));
  if (nodes.trie.length) parts.push(section('Trie (letter tree)', 'trie', trieView(nodes.trie, h, varLabels)));

  // 4) call stack + recursion tree
  if (step.st.length > 1 || opts.alwaysStack) parts.push(section('Call stack', 'stack', callStack(step)));
  const rec = recursionTree(trace, opts.stepIndex ?? 0, step);
  if (rec) parts.push(section('Recursion tree', 'rec', rec));

  // 5) printed output
  const out = (trace.out || '').slice(0, step.o);
  if (out) parts.push(section('Printed output', 'out', `<pre class="stdout">${esc(out.slice(-1500))}</pre>`));

  if (step.ret !== undefined && step.e === 'return') {
    parts.unshift(`<div class="retbox">↩ <b>${esc(top ? top.f : '')}</b> gives back <code>${pretty(step.ret, h)}</code></div>`);
  }
  if (step.exc) parts.unshift(`<div class="retbox err">${esc(step.exc)}</div>`);
  el.innerHTML = parts.join('') || '<div class="viz-empty">No variables yet. Press ▶ to start.</div>';
  const cur = el.querySelector('.rec-cur');
  if (cur && cur.scrollIntoView) {
    const box = cur.closest('.scrollx');
    if (box) box.scrollLeft = Math.max(0, cur.getBoundingClientRect().left - box.getBoundingClientRect().left + box.scrollLeft - box.clientWidth / 2);
  }
}

const section = (title, cls, body) => `<section class="vsec vsec-${cls}"><h4>${title}</h4>${body}</section>`;
const card = (title, sub, body) => `<div class="scard"><div class="stitle"><b>${esc(title)}</b><span>${esc(sub)}</span></div>${body}</div>`;

/* ---------------- structures ---------------- */
function structView(name, o, h, p, ph, ptrs, opts, id) {
  const ch = p && p.k === o.k && p.v ? changedIdx(p, o, ph, h) : new Set();
  const n = o.n ?? (o.v ? o.v.length : 0);
  if (o.k === 'list' || o.k === 'tuple') {
    const allPrim = o.v.every(prim);
    const rows = o.v.map(v => (isRef(v) ? h[v.r] : null));
    const isGrid = o.v.length > 0 && rows.every(r => r && (r.k === 'list' || r.k === 'tuple') && r.v.every(prim));
    if (isGrid && /^(graph|adj|g|adjlist|adj_list|neighbors|nei|edges_of)$/i.test(name) && looksAdj(rows, o.v.length)) {
      return { sub: `graph · ${n} nodes`, body: adjGraph(rows.map((r, i) => [i, r.v]), h, ptrs) };
    }
    if (isGrid) return { sub: `grid · ${n}×${rows[0] ? rows[0].n : 0}`, body: gridView(o, rows, h, p, ph, ptrs, name) };
    if (/heap|pq|minh|maxh|^h$/i.test(name) && allPrim) return { sub: `heap · ${n} items (smallest on top)`, body: heapView(o, h, ch) };
    if (/stack|^stk$|^st$/i.test(name)) return { sub: `stack · ${n} items`, body: stackView(o, h, ch) };
    if (/queue|^q$/i.test(name)) return { sub: `queue · ${n} items`, body: queueView(o, h) };
    const bars = allPrim && o.v.length > 1 && o.v.every(v => typeof v === 'number') && (opts.bars === true || (opts.bars || []).includes?.(name));
    return { sub: `${o.k} · ${n} item${n === 1 ? '' : 's'}`, body: arrayView(o, h, ptrs, ch, bars) };
  }
  if (o.k === 'deque') return { sub: `deque (queue) · ${n} items`, body: queueView(o, h) };
  if (o.k === 'set') return { sub: `set · ${n} items`, body: setView(o, h, p, ph) };
  if (o.k === 'dict') {
    const adj = o.v.length > 1 && dictAdj(o, h);
    const body = dictView(o, h, p, ph);
    if (adj) return { sub: `graph as dict · ${n} nodes`, body: adjGraph(adj, h, ptrs) + body };
    return { sub: `${o.cls || 'dict'} · ${n} key${n === 1 ? '' : 's'}`, body };
  }
  if (o.k === 'obj') {
    const rows = o.a.map(([a, v]) => `<tr><td>${esc(a)}</td><td><code>${pretty(v, h)}</code></td></tr>`).join('');
    return { sub: `${o.cls} object`, body: `<table class="dict">${rows}</table>` };
  }
  return null;
}

function arrayView(o, h, ptrs, ch, bars) {
  const len = o.v.length;
  const nums = o.v.filter(v => typeof v === 'number');
  const max = Math.max(1, ...nums.map(Math.abs));
  const ptrAt = new Map();
  for (const [n, v] of ptrs) if (v >= 0 && v <= len) {
    if (!ptrAt.has(v)) ptrAt.set(v, []);
    ptrAt.get(v).push(n);
  }
  const cells = o.v.map((v, i) => {
    const pt = ptrAt.get(i) || [];
    const style = pt.length ? ` style="--c:${tagColor(pt[0])}"` : '';
    const bar = bars ? `<div class="bar" style="height:${Math.max(6, Math.abs(v) / max * 90)}px"></div>` : '';
    return `<div class="cell${ch.has(i) ? ' chg' : ''}${pt.length ? ' on' : ''}${bars ? ' barcell' : ''}"${style}>${bar}<div class="box">${cellText(v, h)}</div><div class="idx">${i}</div><div class="ptrs">${pt.map(tag).join('')}</div></div>`;
  });
  const end = ptrAt.get(len);
  if (end) cells.push(`<div class="cell ghost on" style="--c:${tagColor(end[0])}"><div class="box">·</div><div class="idx">${len}</div><div class="ptrs">${end.map(tag).join('')}</div></div>`);
  const more = (o.n || len) > len ? `<div class="more">+${o.n - len} more</div>` : '';
  if (!len) return '<div class="emptyarr">[ ] empty</div>';
  return `<div class="arr scrollx">${cells.join('')}${more}</div>`;
}

function gridView(o, rows, h, p, ph, ptrs, name) {
  const pv = Object.fromEntries(ptrs);
  const pairs = [['r', 'c'], ['i', 'j'], ['row', 'col'], ['x', 'y'], ['nr', 'nc'], ['rr', 'cc']];
  const hits = new Map();
  for (const [a, b] of pairs) if (a in pv && b in pv) hits.set(`${pv[a]},${pv[b]}`, `${a},${b}`);
  const prows = p && p.k === o.k ? p.v.map(v => (isRef(v) ? ph[v.r] : null)) : [];
  const vals = new Set();
  rows.forEach(r => r.v.forEach(v => vals.add(fmt(v, h))));
  const cat = vals.size <= 5;
  const palette = ['#fff4d6', '#d9f5e5', '#e3ecff', '#ffe0ea', '#efe5ff'];
  const valColor = new Map([...vals].sort().map((v, i) => [v, palette[i % palette.length]]));
  let html = `<div class="scrollx"><table class="grid"><tr><th></th>${rows[0].v.map((_, j) => `<th>${j}</th>`).join('')}</tr>`;
  rows.forEach((r, i) => {
    html += `<tr><th>${i}</th>`;
    r.v.forEach((v, j) => {
      const pr = prows[i];
      const chg = pr && (j >= pr.v.length || !sameVal(pr.v[j], v, ph, h));
      const hit = hits.get(`${i},${j}`);
      const t = fmt(v, h);
      const bg = cat ? `background:${valColor.get(t)}` : '';
      html += `<td class="${chg ? 'chg' : ''}${hit ? ' on' : ''}" style="${bg}">${cellText(v, h)}${hit ? `<span class="gtag">${esc(hit)}</span>` : ''}</td>`;
    });
    html += '</tr>';
  });
  return html + '</table></div>';
}

function dictView(o, h, p, ph) {
  const old = new Map(p && p.k === 'dict' ? p.v.map(([k, v]) => [fmt(k, ph), v]) : []);
  if (!o.v.length) return '<div class="emptyarr">{ } empty</div>';
  const rows = o.v.map(([k, v]) => {
    const ks = fmt(k, h);
    const isNew = p && !old.has(ks);
    const chg = p && !isNew && !sameVal(old.get(ks), v, ph, h);
    return `<tr class="${isNew ? 'new' : chg ? 'chg' : ''}"><td class="k">${esc(ks)}</td><td class="arrow">→</td><td><code>${pretty(v, h)}</code></td></tr>`;
  }).join('');
  const more = o.n > o.v.length ? `<tr><td colspan=3 class="more">+${o.n - o.v.length} more</td></tr>` : '';
  return `<table class="dict">${rows}${more}</table>`;
}

function setView(o, h, p, ph) {
  const old = new Set(p && p.k === 'set' ? p.v.map(v => fmt(v, ph)) : []);
  if (!o.v.length) return '<div class="emptyarr">{ } empty set</div>';
  return `<div class="chips">${o.v.map(v => `<span class="chip${p && !old.has(fmt(v, h)) ? ' new' : ''}">${pretty(v, h)}</span>`).join('')}${o.n > o.v.length ? `<span class="more">+${o.n - o.v.length}</span>` : ''}</div>`;
}

function stackView(o, h, ch) {
  if (!o.v.length) return '<div class="emptyarr">empty stack</div>';
  const items = o.v.map((v, i) => `<div class="sitem${ch.has(i) ? ' chg' : ''}">${i === o.v.length - 1 ? '<span class="toptag">top</span>' : ''}${pretty(v, h)}</div>`).reverse();
  return `<div class="stackv">${items.join('')}<div class="sbase"></div></div>`;
}

function queueView(o, h) {
  if (!o.v.length) return '<div class="emptyarr">empty queue</div>';
  return `<div class="queuev scrollx"><span class="qend">front ⟵</span>${o.v.map(v => `<div class="qitem">${pretty(v, h)}</div>`).join('')}<span class="qend">⟵ back</span></div>`;
}

function heapView(o, h, ch) {
  const n = o.v.length;
  if (!n) return '<div class="emptyarr">empty heap</div>';
  const pos = [];
  const depth = Math.floor(Math.log2(n)) + 1;
  const W = Math.max(260, Math.pow(2, depth - 1) * 46);
  for (let i = 0; i < n; i++) {
    const d = Math.floor(Math.log2(i + 1));
    const idx = i + 1 - Math.pow(2, d);
    const slots = Math.pow(2, d);
    pos.push({ x: (idx + 0.5) * W / slots, y: 26 + d * 56 });
  }
  let svg = '';
  for (let i = 1; i < n; i++) {
    const a = pos[Math.floor((i - 1) / 2)], b = pos[i];
    svg += `<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" class="edge"/>`;
  }
  for (let i = 0; i < n; i++) {
    svg += `<g class="tn${ch.has(i) ? ' chg' : ''}${i === 0 ? ' root' : ''}"><circle cx="${pos[i].x}" cy="${pos[i].y}" r="18"/><text x="${pos[i].x}" y="${pos[i].y + 5}">${cellText(o.v[i], h)}</text></g>`;
  }
  return `<div class="scrollx"><svg class="treesvg" width="${W}" height="${depth * 56 + 10}">${svg}</svg></div>` + arrayView(o, h, [], ch, false);
}

/* ---------------- graphs from dict / list adjacency ---------------- */
function looksAdj(rows, n) {
  let ok = 0, tot = 0;
  for (const r of rows) for (const v of r.v) { tot++; if (Number.isInteger(v) && v >= 0 && v < n) ok++; }
  return tot > 0 && ok / tot > 0.9;
}
function dictAdj(o, h) {
  const keys = new Set(o.v.map(([k]) => fmt(k, h)));
  const res = [];
  let ok = 0, tot = 0;
  for (const [k, v] of o.v) {
    if (!prim(k) || !isRef(v)) return null;
    const lst = h[v.r];
    if (!lst || !['list', 'set', 'tuple'].includes(lst.k) || !lst.v.every(prim)) return null;
    for (const x of lst.v) { tot++; if (keys.has(fmt(x, h))) ok++; }
    res.push([k, lst.v]);
  }
  return tot >= 2 && ok / tot >= 0.6 ? res : null;
}
function adjGraph(adj, h, ptrs) {
  const ids = [];
  const seen = new Set();
  const add = k => { const s = fmt(k, h); if (!seen.has(s)) { seen.add(s); ids.push(s); } };
  adj.forEach(([k, lst]) => { add(k); lst.forEach(add); });
  if (ids.length > 40) return '';
  const pos = circle(ids.length);
  const at = new Map(ids.map((s, i) => [s, pos[i]]));
  const ptrHit = new Map();
  for (const [n, v] of ptrs) ptrHit.set(String(v), n);
  const edges = new Set();
  let svg = '';
  adj.forEach(([k, lst]) => lst.forEach(x => {
    const a = fmt(k, h), b = fmt(x, h);
    const key = [a, b].sort().join('|');
    if (edges.has(key)) return;
    edges.add(key);
    const A = at.get(a), B = at.get(b);
    svg += `<line x1="${A.x}" y1="${A.y}" x2="${B.x}" y2="${B.y}" class="edge"/>`;
  }));
  ids.forEach(s => {
    const P = at.get(s);
    const p = ptrHit.get(s.replace(/'/g, ''));
    svg += `<g class="tn${p ? ' cur' : ''}"><circle cx="${P.x}" cy="${P.y}" r="17"/><text x="${P.x}" y="${P.y + 5}">${esc(s.replace(/'/g, '').slice(0, 4))}</text>${p ? `<text class="lbl" x="${P.x}" y="${P.y - 24}">${esc(p)}</text>` : ''}</g>`;
  });
  return `<svg class="treesvg graphsvg" viewBox="0 0 300 300" width="300" height="300">${svg}</svg>`;
}
function circle(n) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const a = -Math.PI / 2 + i * 2 * Math.PI / n;
    const R = n === 1 ? 0 : 115;
    out.push({ x: 150 + R * Math.cos(a), y: 150 + R * Math.sin(a) });
  }
  return out;
}

/* ---------------- linked lists ---------------- */
function listLayout(trace) {
  if (trace._ll) return trace._ll;
  const pos = new Map();
  let nextRow = 0, createdRow = -1, createdCol = 0;
  const used = new Set();
  const place = (id, r, c) => { pos.set(id, { r, c }); used.add(`${r},${c}`); };
  for (const st of trace.steps) {
    const fresh = [];
    for (const [id, o] of Object.entries(st.h)) if (kindOf(o) === 'lnode' && !pos.has(+id)) fresh.push(+id);
    if (!fresh.length) continue;
    const nextOf = id => { const v = attr(st.h[id], 'next'); return isRef(v) ? v.r : null; };
    const freshSet = new Set(fresh);
    const pointed = new Set(fresh.map(nextOf).filter(x => x !== null && freshSet.has(x)));
    for (const id of fresh.filter(x => !pointed.has(x))) {
      if (pos.has(id)) continue;
      // predecessor already placed?
      let pred = null;
      for (const [pid] of pos) if (st.h[pid] && nextOf(pid) === id) pred = pos.get(pid);
      let chain = [], cur = id;
      while (cur !== null && freshSet.has(cur) && !pos.has(cur) && !chain.includes(cur)) { chain.push(cur); cur = nextOf(cur); }
      if (pred && !used.has(`${pred.r},${pred.c + 1}`)) chain.forEach((x, i) => place(x, pred.r, pred.c + 1 + i));
      else if (chain.length === 1 && trace.steps[0] !== st) {
        if (createdRow < 0) createdRow = nextRow++;
        while (used.has(`${createdRow},${createdCol}`)) createdCol++;
        place(chain[0], createdRow, createdCol++);
      } else { const r = nextRow++; chain.forEach((x, i) => place(x, r, i)); }
    }
    for (const id of fresh) if (!pos.has(id)) { const r = nextRow++; place(id, r, 0); }
  }
  trace._ll = pos;
  return pos;
}

function linkedView(ids, h, labels, trace) {
  const pos = listLayout(trace);
  const BW = 50, BH = 34, GX = 40, GY = 74, PAD = 24;
  const present = ids.filter(id => pos.has(id));
  if (!present.length) return '';
  const rows = [...new Set(present.map(id => pos.get(id).r))].sort((a, b) => a - b);
  const rowY = new Map(rows.map((r, i) => [r, PAD + 18 + i * GY]));
  const maxC = Math.max(...present.map(id => pos.get(id).c));
  const X = id => PAD + pos.get(id).c * (BW + GX);
  const Y = id => rowY.get(pos.get(id).r);
  const W = PAD * 2 + (maxC + 1) * (BW + GX), H = PAD + rows.length * GY + 10;
  let svg = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#2b2b3a"/></marker><marker id="ahp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#a88bff"/></marker><marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#ff8a5c"/></marker></defs>';
  const arrow = (a, b, cls, mk, bend) => {
    const x1 = X(a) + BW, y1 = Y(a) + BH / 2, x2 = X(b), y2 = Y(b) + BH / 2;
    if (Y(a) === Y(b) && pos.get(b).c === pos.get(a).c + 1 && !bend) return `<line x1="${x1}" y1="${y1}" x2="${x2 - 2}" y2="${y2}" class="${cls}" marker-end="url(#${mk})"/>`;
    if (a === b) return `<path d="M${X(a) + BW / 2},${Y(a)} c 30,-40 -30,-40 -8,0" class="${cls}" marker-end="url(#${mk})"/>`;
    const back = X(b) <= X(a);
    const sx = back ? X(a) + BW / 2 : x1, ex = back ? X(b) + BW / 2 : x2;
    const sy = back ? Y(a) + BH : y1, ey = back ? Y(b) + BH : y2;
    const dy = (back ? 34 : -30) + (bend || 0);
    return `<path d="M${sx},${sy} C${sx},${sy + dy} ${ex},${ey + dy} ${ex},${ey + (back ? 2 : 0)}" class="${cls}" fill="none" marker-end="url(#${mk})"/>`;
  };
  for (const id of present) {
    const o = h[id];
    const nx = attr(o, 'next'), pv = attr(o, 'prev'), rd = attr(o, 'random');
    if (isRef(nx) && pos.has(nx.r) && h[nx.r]) svg += arrow(id, nx.r, 'edge', 'ah');
    else if (nx === null) svg += `<text class="nil" x="${X(id) + BW + 6}" y="${Y(id) + BH / 2 + 4}">∅</text>`;
    if (isRef(pv) && pos.has(pv.r) && h[pv.r]) svg += arrow(id, pv.r, 'edge prev', 'ahp', 16);
    if (isRef(rd) && pos.has(rd.r) && h[rd.r]) svg += arrow(id, rd.r, 'edge rand', 'ahr', -18);
  }
  for (const id of present) {
    const lb = labels.get(id) || [];
    const x = X(id), y = Y(id);
    svg += `<g class="ln${lb.length ? ' on' : ''}" ${lb.length ? `style="--c:${tagColor(lb[0])}"` : ''}><rect x="${x}" y="${y}" width="${BW}" height="${BH}" rx="9"/><text x="${x + BW / 2}" y="${y + BH / 2 + 5}">${esc(nodeLabel(h[id], h).slice(0, 6))}</text>`;
    lb.forEach((n, i) => { svg += `<text class="lbl" style="fill:${tagColor(n)}" x="${x + BW / 2}" y="${y - 6 - i * 13}">${esc(n)}</text>`; });
    svg += '</g>';
  }
  return `<div class="scrollx"><svg class="llsvg" width="${W}" height="${H + 20}" viewBox="0 -20 ${W} ${H + 20}">${svg}</svg></div><div class="legend">→ next${present.some(id => attr(h[id], 'prev') !== undefined) ? ' · <span style="color:#a88bff">→ prev</span>' : ''}${present.some(id => attr(h[id], 'random') !== undefined) ? ' · <span style="color:#ff8a5c">→ random</span>' : ''} · ∅ = None (end)</div>`;
}

/* ---------------- binary trees ---------------- */
function treeView(ids, h, labels, ph) {
  const kids = id => {
    const o = h[id];
    const l = attr(o, 'left'), r = attr(o, 'right');
    return [isRef(l) && h[l.r] ? l.r : null, isRef(r) && h[r.r] ? r.r : null];
  };
  const child = new Set();
  ids.forEach(id => kids(id).forEach(c => c !== null && child.add(c)));
  const rootsList = ids.filter(id => !child.has(id)).sort((a, b) => a - b);
  const pos = new Map();
  let x = 0, maxD = 0;
  const visit = (id, d) => {
    if (id === null || pos.has(id) || pos.size > 200) return;
    pos.set(id, null);
    const [l, r] = kids(id);
    visit(l, d + 1);
    pos.set(id, { x: x++, d });
    maxD = Math.max(maxD, d);
    visit(r, d + 1);
  };
  rootsList.forEach(r => { visit(r, 0); x += 0.6; });
  const SX = 44, SY = 58, P = 30;
  const W = Math.max(200, x * SX + P * 2), H = (maxD + 1) * SY + P + 10;
  const px = id => P + pos.get(id).x * SX, py = id => P + 8 + pos.get(id).d * SY;
  let svg = '';
  for (const [id, p] of pos) if (p) {
    const [l, r] = kids(id);
    for (const c of [l, r]) if (c !== null && pos.get(c)) svg += `<line x1="${px(id)}" y1="${py(id)}" x2="${px(c)}" y2="${py(c)}" class="edge"/>`;
  }
  for (const [id, p] of pos) if (p) {
    const lb = labels.get(id) || [];
    const isNew = ph && !ph[id];
    svg += `<g class="tn${lb.length ? ' cur' : ''}${isNew ? ' chg' : ''}" ${lb.length ? `style="--c:${tagColor(lb[0])}"` : ''}><circle cx="${px(id)}" cy="${py(id)}" r="17"/><text x="${px(id)}" y="${py(id) + 5}">${esc(nodeLabel(h[id], h).slice(0, 4))}</text>`;
    lb.forEach((n, i) => { svg += `<text class="lbl" style="fill:${tagColor(n)}" x="${px(id) + 21}" y="${py(id) - 14 - i * 12}" text-anchor="start">${esc(n)}</text>`; });
    svg += '</g>';
  }
  return `<div class="scrollx"><svg class="treesvg" width="${W}" height="${H}">${svg}</svg></div>`;
}

/* ---------------- graph nodes (Node.neighbors) ---------------- */
function nodeGraphView(ids, h, labels) {
  ids = ids.slice(0, 40).sort((a, b) => a - b);
  const pos = circle(ids.length);
  const at = new Map(ids.map((id, i) => [id, pos[i]]));
  let svg = '<defs><marker id="ahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0L10,5L0,10z" fill="#9a9ab0"/></marker></defs>';
  for (const id of ids) {
    const nb = attr(h[id], 'neighbors');
    const lst = isRef(nb) ? h[nb.r] : null;
    if (!lst || !lst.v) continue;
    for (const v of lst.v) if (isRef(v) && at.has(v.r)) {
      const A = at.get(id), B = at.get(v.r);
      const dx = B.x - A.x, dy = B.y - A.y, L = Math.hypot(dx, dy) || 1;
      svg += `<line x1="${A.x + dx / L * 18}" y1="${A.y + dy / L * 18}" x2="${B.x - dx / L * 20}" y2="${B.y - dy / L * 20}" class="edge" marker-end="url(#ahg)"/>`;
    }
  }
  for (const id of ids) {
    const P = at.get(id), lb = labels.get(id) || [];
    svg += `<g class="tn${lb.length ? ' cur' : ''}" ${lb.length ? `style="--c:${tagColor(lb[0])}"` : ''}><circle cx="${P.x}" cy="${P.y}" r="17"/><text x="${P.x}" y="${P.y + 5}">${esc(nodeLabel(h[id], h))}</text>${lb.map((n, i) => `<text class="lbl" style="fill:${tagColor(n)}" x="${P.x}" y="${P.y - 24 - i * 12}">${esc(n)}</text>`).join('')}</g>`;
  }
  return `<svg class="treesvg graphsvg" viewBox="0 0 300 300" width="300" height="300">${svg}</svg>`;
}

/* ---------------- tries ---------------- */
function trieView(ids, h, labels) {
  const kids = id => {
    const ch = attr(h[id], 'children');
    const d = isRef(ch) ? h[ch.r] : null;
    if (!d) return [];
    if (d.k === 'dict') return d.v.filter(([, v]) => isRef(v) && h[v.r]).map(([k, v]) => [fmt(k, h).replace(/'/g, ''), v.r]);
    if (d.k === 'list') return d.v.map((v, i) => [String.fromCharCode(97 + i), v]).filter(([, v]) => isRef(v) && h[v.r]).map(([k, v]) => [k, v.r]);
    return [];
  };
  const child = new Set();
  ids.forEach(id => kids(id).forEach(([, c]) => child.add(c)));
  const rootsList = ids.filter(id => !child.has(id));
  const pos = new Map(); let x = 0, maxD = 0;
  const place = (id, d) => {
    if (pos.has(id) || pos.size > 150) return;
    pos.set(id, null);
    const ch = kids(id);
    ch.forEach(([, c]) => place(c, d + 1));
    const xs = ch.map(([, c]) => pos.get(c)).filter(Boolean).map(p => p.x);
    pos.set(id, { x: xs.length ? (Math.min(...xs) + Math.max(...xs)) / 2 : x++, d });
    maxD = Math.max(maxD, d);
  };
  rootsList.forEach(r => place(r, 0));
  const SX = 40, SY = 54, P = 26;
  const W = Math.max(200, x * SX + P * 2), H = (maxD + 1) * SY + P;
  const px = id => P + pos.get(id).x * SX, py = id => P + pos.get(id).d * SY;
  let svg = '';
  for (const [id, p] of pos) if (p) for (const [k, c] of kids(id)) if (pos.get(c)) {
    svg += `<line x1="${px(id)}" y1="${py(id)}" x2="${px(c)}" y2="${py(c)}" class="edge"/><text class="elbl" x="${(px(id) + px(c)) / 2 - 7}" y="${(py(id) + py(c)) / 2}">${esc(k)}</text>`;
  }
  for (const [id, p] of pos) if (p) {
    const o = h[id];
    const end = attr(o, 'is_end') ?? attr(o, 'end') ?? attr(o, 'isEnd') ?? attr(o, 'is_word') ?? attr(o, 'word') ?? attr(o, 'isWord');
    const lb = labels.get(id) || [];
    const done = end === true || (isStr(end) && end.s);
    svg += `<g class="tn${lb.length ? ' cur' : ''}${done ? ' end' : ''}" ${lb.length ? `style="--c:${tagColor(lb[0])}"` : ''}><circle cx="${px(id)}" cy="${py(id)}" r="12"/>${done ? `<text x="${px(id)}" y="${py(id) + 4}">★</text>` : ''}${lb.map((n, i) => `<text class="lbl" style="fill:${tagColor(n)}" x="${px(id) + 16}" y="${py(id) - 8 - i * 12}" text-anchor="start">${esc(n)}</text>`).join('')}</g>`;
  }
  return `<div class="scrollx"><svg class="treesvg" width="${W}" height="${H}">${svg}</svg></div><div class="legend">★ = a word ends here</div>`;
}

/* ---------------- call stack & recursion ---------------- */
function callStack(step) {
  return `<div class="cstack">${step.st.map((f, i) => {
    const vars = f.v.filter(([n, v]) => n !== 'self' && prim(v)).slice(0, 6).map(([n, v]) => `${esc(n)}=${pretty(v, step.h)}`).join(' · ');
    return `<div class="cframe${i === step.st.length - 1 ? ' top' : ''}"><b>${esc(f.f === '<module>' ? 'main program' : f.f + '()')}</b><span>${vars}</span></div>`;
  }).reverse().join('')}</div>`;
}

function recursionTree(trace, k, step) {
  const calls = trace.calls || [];
  if (!calls.length) return '';
  const byId = new Map(calls.map(c => [c.id, c]));
  const recursive = calls.some(c => c.p && byId.get(c.p) && byId.get(c.p).f === c.f);
  if (!recursive) return '';
  const visible = calls.filter(c => c.s <= k && c.f !== '<module>');
  if (visible.length < 2) return '';
  const kids = new Map();
  visible.forEach(c => { if (!kids.has(c.p)) kids.set(c.p, []); kids.get(c.p).push(c.id); });
  const active = new Set();
  for (let c = byId.get(step.c); c; c = byId.get(c.p)) active.add(c.id);
  const vis = new Set(visible.map(c => c.id));
  const top = visible.filter(c => !vis.has(c.p));
  const pos = new Map(); let x = 0, maxD = 0;
  const place = (id, d) => {
    const ch = kids.get(id) || [];
    ch.forEach(c => place(c, d + 1));
    const xs = ch.map(c => pos.get(c).x);
    pos.set(id, { x: xs.length ? (Math.min(...xs) + Math.max(...xs)) / 2 : x++, d });
    maxD = Math.max(maxD, d);
  };
  top.forEach(c => place(c.id, 0));
  const SX = 92, SY = 62, P = 50;
  const W = x * SX + P, H = (maxD + 1) * SY + 30;
  const px = id => P + pos.get(id).x * SX - 20, py = id => 24 + pos.get(id).d * SY;
  let svg = '';
  visible.forEach(c => { if (pos.has(c.p)) svg += `<line x1="${px(c.p)}" y1="${py(c.p)}" x2="${px(c.id)}" y2="${py(c.id)}" class="edge${active.has(c.id) ? ' act' : ''}"/>`; });
  visible.forEach(c => {
    const done = c.e !== undefined && c.e <= k;
    const cur = c.id === step.c;
    const label = `${c.f}(${c.a.replace(/\w+=/g, '')})`;
    svg += `<g class="rn${cur ? ' rec-cur' : active.has(c.id) ? ' act' : done ? ' done' : ''}"><rect x="${px(c.id) - 42}" y="${py(c.id) - 14}" width="84" height="26" rx="13"/><text x="${px(c.id)}" y="${py(c.id) + 4}">${esc(label.length > 13 ? label.slice(0, 12) + '…' : label)}</text>${done ? `<text class="rv" x="${px(c.id)}" y="${py(c.id) + 26}">= ${esc(c.r)}</text>` : ''}</g>`;
  });
  return `<div class="scrollx"><svg class="recsvg" width="${Math.max(W, 200)}" height="${H}">${svg}</svg></div><div class="legend"><span class="lg cur"></span> running now <span class="lg act"></span> waiting for an answer <span class="lg done"></span> finished</div>`;
}
