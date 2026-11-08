/* Helpers for reading values recorded by the tracer. */
export const isRef = v => v && typeof v === 'object' && 'r' in v;
export const isStr = v => v && typeof v === 'object' && 's' in v;
export const obj = (heap, v) => (isRef(v) ? heap[v.r] : null);

export function attr(o, name) {
  if (!o || o.k !== 'obj') return undefined;
  const a = o.a.find(x => x[0] === name);
  return a ? a[1] : undefined;
}
export const hasAttr = (o, n) => !!(o && o.k === 'obj' && o.a.some(x => x[0] === n));

export function kindOf(o) {
  if (!o) return null;
  if (o.k !== 'obj') return o.k;
  if (hasAttr(o, 'neighbors')) return 'gnode';
  if (hasAttr(o, 'children')) return 'trie';
  if (hasAttr(o, 'left') || hasAttr(o, 'right')) return 'tnode';
  if (hasAttr(o, 'next') || hasAttr(o, 'prev')) return 'lnode';
  return 'obj';
}

function num(n) {
  if (Number.isInteger(n)) return String(n);
  const s = n.toFixed(4).replace(/0+$/, '').replace(/\.$/, '');
  return s;
}

export function prim(v) {
  return v === null || typeof v !== 'object' || isStr(v) || 'f' in v || 'big' in v;
}

/* Short text for any value, Python-style. */
export function fmt(v, heap, depth = 0) {
  if (v === null || v === undefined) return 'None';
  if (v === true) return 'True';
  if (v === false) return 'False';
  if (typeof v === 'number') return num(v);
  if (isStr(v)) return v.q ? v.s : `'${v.s}'`;
  if ('f' in v) return v.f;
  if ('big' in v) return v.big;
  const o = obj(heap, v);
  if (!o) return '…';
  if (depth > 2) return o.k === 'list' ? '[…]' : '…';
  const items = (arr, n = 8) => {
    const parts = arr.slice(0, n).map(x => fmt(x, heap, depth + 1));
    if (arr.length > n || (o.n || 0) > arr.length) parts.push('…');
    return parts.join(', ');
  };
  switch (o.k) {
    case 'list': return `[${items(o.v)}]`;
    case 'tuple': return o.v.length === 1 ? `(${items(o.v)},)` : `(${items(o.v)})`;
    case 'set': return o.v.length ? `{${items(o.v)}}` : 'set()';
    case 'deque': return `deque([${items(o.v)}])`;
    case 'dict': return `{${o.v.slice(0, 6).map(([a, b]) => `${fmt(a, heap, depth + 1)}: ${fmt(b, heap, depth + 1)}`).join(', ')}${o.v.length > 6 ? ', …' : ''}}`;
    case 'func': return `ƒ ${o.name}`;
    case 'class': return `class ${o.name}`;
    case 'other': return o.repr;
    case 'obj': {
      const val = attr(o, 'val') ?? attr(o, 'key') ?? attr(o, 'value');
      return val !== undefined ? `${o.cls}(${fmt(val, heap, depth + 1)})` : `${o.cls}`;
    }
  }
  return '?';
}

/* Label shown inside a node bubble (list / tree / graph node). */
export function nodeLabel(o, heap) {
  for (const k of ['val', 'key', 'value', 'data', 'label']) {
    const v = attr(o, k);
    if (v !== undefined && prim(v)) {
      if (k === 'key' && attr(o, 'val') !== undefined) break;
      return fmt(v, heap).replace(/^'(.*)'$/, '$1');
    }
  }
  const key = attr(o, 'key');
  const val = attr(o, 'val') ?? attr(o, 'value');
  if (key !== undefined) return `${fmt(key, heap)}:${fmt(val, heap)}`.replace(/'/g, '');
  const p = o.a.find(x => prim(x[1]));
  return p ? fmt(p[1], heap) : o.cls;
}

export const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
export const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
