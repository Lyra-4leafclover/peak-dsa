/* Pretty test-result cards. */
import { esc } from '../viz/values.js';
const show = v => esc(typeof v === 'string' ? JSON.stringify(v) : JSON.stringify(v));
export function short(v, n = 90) { const s = JSON.stringify(v); return s && s.length > n ? s.slice(0, n) + '…' : s; }
export function renderResults(el, res, { hidden = 0, names = [] } = {}) {
  if (res.error) {
    el.innerHTML = `<div class="res-banner bad">Your code didn't even start: <code>${esc(res.error.error)}</code>${res.error.line ? ` on line ${res.error.line}` : ''}</div>`;
    return { pass: 0, total: 0, line: res.error.line };
  }
  const R = res.results;
  const pass = R.filter(r => r.pass).length;
  const firstErr = R.find(r => r.error);
  el.innerHTML = `<div class="res-banner ${pass === R.length ? 'good' : 'bad'}">${pass === R.length ? 'All tests passed!' : `${pass} / ${R.length} tests passed`}</div>
  <div class="res-list">${R.map((r, i) => {
    const hid = i >= R.length - hidden;
    return `<details class="res ${r.pass ? 'ok' : 'no'}" ${!r.pass && !hid && !el.dataset.opened ? 'open' : ''}><summary>${r.pass ? '✓' : '✗'} ${hid ? `Secret test ${i - (R.length - hidden) + 1}` : `Test ${i + 1}`}<span class="tiny muted"> · ${r.ms} ms</span></summary>
    ${hid && !r.pass ? '<div class="tiny muted">This one is a secret! Think about edge cases: empty input, one item, negatives, duplicates…</div>' : hid ? '' : `
      <div class="kv"><b>Input</b><code>${esc((names.length ? r.args.map((a, j) => `${names[j] || 'arg' + j} = ${short(a, 200)}`) : r.args.map(a => short(a, 200))).join(', '))}</code></div>
      <div class="kv"><b>Expected</b><code>${show(r.exp)}</code></div>
      ${r.error ? `<div class="kv"><b>Error</b><code class="err">${esc(r.error)}${r.line ? ` (line ${r.line})` : ''}</code></div>` : `<div class="kv"><b>You gave</b><code>${show(r.got)}</code></div>`}
      ${r.out ? `<div class="kv"><b>Printed</b><pre class="stdout">${esc(r.out)}</pre></div>` : ''}`}
    </details>`;
  }).join('')}</div>`;
  return { pass, total: R.length, line: firstErr?.line };
}
