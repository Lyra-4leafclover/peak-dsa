/* Problem bank: list with filters + a detail page (read it, watch it run, code it yourself). */
import { PROBLEMS } from '../data/problems.js';
import { TOPICS, topicInfo, XP } from '../data/topics.js';
import { store } from '../store.js';
import { esc } from '../viz/values.js';
import { splitNotes } from '../ui/code.js';
import { createEditor, waitForCM } from '../ui/editor.js';
import { renderResults, short } from '../ui/results.js';
import { showTrace } from '../ui/theater.js';
import { pyStatus } from '../ui/pystatus.js';
import * as py from '../engine/py.js';
import { toast } from '../app.js';

export const bySlug = Object.fromEntries(PROBLEMS.map(p => [p.slug, p]));
export function payloadOf(p) {
  const o = { mode: p.mode };
  for (const k of ['fn', 'params', 'types', 'cmp', 'inplace', 'cycle', 'nodeMode']) if (p[k] !== undefined) o[k] = p[k];
  return o;
}
export function argNames(p) {
  if (p.mode === 'design') return ['operations', 'arguments'];
  const n = p.tests[0][0].length;
  const names = [...(p.params || [])];
  if (p.cycle !== undefined) names.splice(p.cycle, 0, 'pos (loop links back to)');
  if (p.types && Object.values(p.types).includes('joined')) return ['listA', 'listB', 'skipA', 'skipB'];
  while (names.length < n) names.push(`arg${names.length}`);
  return names.slice(0, n);
}

export async function render(el, slug) {
  if (slug && bySlug[slug]) return detail(el, bySlug[slug]);
  return list(el);
}

function list(el) {
  const st = { q: store.get('pq', ''), topic: store.get('ptopic', 'All'), diff: store.get('pdiff', 'All'), show: 'all' };
  const total = PROBLEMS.length, solved = PROBLEMS.filter(p => store.isSolved(p.slug)).length;
  el.innerHTML = `<div class="wrap">
    <div class="phead"><img src="assets/art/challenges.webp" alt=""><div class="txt">
      <h1>Problem Bank</h1>
      <p>${total} classic interview problems, each written in plain words with a step-by-step animated solution. Pick one, watch it run, then try it yourself in Python.</p>
      <div class="progress-strip"><div class="bar"><i style="width:${(solved / total * 100).toFixed(1)}%"></i></div><b>${solved} / ${total} solved</b></div>
    </div></div>
    <div class="filters card">
      <input class="search" type="search" placeholder="🔎 Search problems (e.g. 'tree', 'two sum', '206')" value="${esc(st.q)}">
      <div class="row"><span class="tiny muted">Difficulty</span><div class="seg diffs">${['All', 'Easy', 'Medium', 'Hard'].map(d => `<button data-d="${d}">${d}</button>`).join('')}</div>
      <div class="seg shows"><button data-s="all">All</button><button data-s="todo">To do</button><button data-s="done">Solved ✅</button></div></div>
      <div class="topic-chips"><button class="chipbtn" data-t="All">🌈 All topics</button>${TOPICS.map(t => `<button class="chipbtn" data-t="${t[0]}">${t[2]} ${t[0]}</button>`).join('')}</div>
    </div>
    <div class="plist"></div></div>`;
  const plist = el.querySelector('.plist');
  function paint() {
    el.querySelectorAll('.diffs button').forEach(b => b.classList.toggle('on', b.dataset.d === st.diff));
    el.querySelectorAll('.shows button').forEach(b => b.classList.toggle('on', b.dataset.s === st.show));
    el.querySelectorAll('.topic-chips button').forEach(b => b.classList.toggle('on', b.dataset.t === st.topic));
    const q = st.q.toLowerCase().trim();
    const match = p => (st.topic === 'All' || p.topic === st.topic) && (st.diff === 'All' || p.diff === st.diff)
      && (st.show === 'all' || (st.show === 'done') === store.isSolved(p.slug))
      && (!q || `${p.title} ${p.slug} ${p.topic} ${p.lc || ''} ${p.story}`.toLowerCase().includes(q));
    let html = '';
    for (const t of TOPICS) {
      const ps = PROBLEMS.filter(p => p.topic === t[0] && match(p));
      if (!ps.length) continue;
      const done = PROBLEMS.filter(p => p.topic === t[0] && store.isSolved(p.slug)).length;
      const all = PROBLEMS.filter(p => p.topic === t[0]).length;
      html += `<section class="ptopic"><div class="ptopic-h"><img src="assets/art/${t[1]}.webp" alt=""><div><h3>${t[2]} ${t[0]}</h3><p class="muted tiny">${t[3]}</p></div><span class="tiny muted">${done}/${all} ✅</span><a class="tiny" href="#/learn">learn it first →</a></div>
      <div class="prows">${ps.map(p => `<a class="prow ${store.isSolved(p.slug) ? 'solved' : ''}" href="#/problems/${p.slug}">
        <span class="chk">${store.isSolved(p.slug) ? '✅' : '○'}</span><span class="pt">${esc(p.title)}</span>
        ${p.lc ? `<span class="lcn">#${p.lc}</span>` : '<span class="lcn">classic</span>'}<span class="tag ${p.diff}">${p.diff}</span></a>`).join('')}</div></section>`;
    }
    plist.innerHTML = html || '<div class="card center muted">No problems match. Try clearing the filters 🙂</div>';
  }
  el.querySelector('.search').addEventListener('input', e => { st.q = e.target.value; store.set('pq', st.q); paint(); });
  el.querySelector('.filters').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.d) { st.diff = b.dataset.d; store.set('pdiff', st.diff); }
    if (b.dataset.s) st.show = b.dataset.s;
    if (b.dataset.t) { st.topic = b.dataset.t; store.set('ptopic', st.topic); }
    paint();
  });
  paint();
}

function detail(el, p) {
  const sol = splitNotes(p.solution);
  const names = argNames(p);
  const idx = PROBLEMS.indexOf(p);
  const prev = PROBLEMS[idx - 1], next = PROBLEMS[idx + 1];
  const [, art, emo] = topicInfo(p.topic);
  let player = null, myPlayer = null, editor = null;
  let caseIdx = 0;
  el.innerHTML = `<div class="wrap pdetail">
    <a class="crumb" href="#/problems">← All problems</a>
    <div class="ptitle"><h1>${esc(p.title)}</h1>
      <div class="row"><span class="tag ${p.diff}">${p.diff}</span><span class="tag">${emo} ${p.topic}</span>
      ${p.lc ? `<a class="tag lc" href="https://leetcode.com/problemset/?search=${p.lc}" target="_blank" rel="noopener">LeetCode #${p.lc} ↗</a>` : '<span class="tag">classic algorithm</span>'}
      <span class="tag bg-butter">+${XP[p.diff]} XP</span>${store.isSolved(p.slug) ? '<span class="tag bg-mint">✅ Solved</span>' : ''}</div></div>
    <div class="pgrid">
      <aside class="pinfo">
        <div class="card story"><img class="sart" src="assets/art/${art}.webp" alt=""><h3>📖 The problem, in plain words</h3><p>${esc(p.story)}</p>
          <div class="examples">${p.tests.slice(0, 2).map((t, i) => `<div class="ex"><b>Example ${i + 1}</b><div><code>${esc(p.mode === 'design' ? short(t[0][0], 120) : t[0].map((a, j) => `${names[j]} = ${short(a, 80)}`).join(', '))}</code></div><div>→ <code>${esc(short(t[1], 120))}</code></div></div>`).join('')}</div>
        </div>
        <div class="card"><h3>💡 Hints</h3><div class="hints">${p.hints.map((h, i) => `<details><summary>Hint ${i + 1}</summary><p>${esc(h)}</p></details>`).join('')}
          <details class="trick"><summary>🔑 The big trick (spoiler!)</summary><p>${esc(p.trick)}</p></details></div>
          <div class="bigo"><span>⏱ Time <b>${esc(p.time)}</b></span><span>📦 Memory <b>${esc(p.space)}</b></span></div>
        </div>
        <div class="row navpn">${prev ? `<a class="btn ghost small" href="#/problems/${prev.slug}">← ${esc(prev.title)}</a>` : ''}<span class="grow"></span>${next ? `<a class="btn ghost small" href="#/problems/${next.slug}">${esc(next.title)} →</a>` : ''}</div>
      </aside>
      <section class="pmain">
        <div class="tabs"><button data-tab="watch" class="on">🎬 Watch the solution</button><button data-tab="code">✏️ Code it yourself</button><span class="grow"></span><span class="pys"></span></div>
        <div class="tab tab-watch">
          <div class="cases card"><b>Pick an input:</b> ${p.tests.map((t, i) => `<button class="chipbtn" data-case="${i}">Example ${i + 1}</button>`).join('')}<button class="chipbtn" data-case="custom">✍️ My own input</button>
            <div class="custom hide">${names.map((n, i) => `<label><span>${esc(n)}</span><input data-arg="${i}" value="${esc(JSON.stringify(p.tests[0][0][i]))}"></label>`).join('')}<button class="btn small go-custom">▶ Run with my input</button><div class="tiny muted">Use Python or JSON style: [1, 2, 3], "hello", [[1, 2], [3]], None/null.</div></div>
          </div>
          <div class="watch-out"></div>
        </div>
        <div class="tab tab-code hide">
          <div class="card code-card">
            <div class="row"><b>Your solution</b><span class="grow"></span><button class="btn small ghost reset">↺ Reset</button><button class="btn small ghost peek">👀 Peek at solution</button></div>
            <div class="ed"></div>
            <div class="row actions"><button class="btn green runtests">▶ Run tests</button><button class="btn soft watchmine">🎬 Watch MY code run (Example ${1})</button><span class="tiny muted">Ctrl/⌘ + Enter runs tests</span></div>
          </div>
          <div class="results"></div>
          <div class="mine-out"></div>
        </div>
      </section>
    </div></div>`;
  const $ = s => el.querySelector(s);
  const offPy = pyStatus($('.pys'));
  const base = payloadOf(p);
  const opts = { bars: p.bars };

  async function watch(args, raw) {
    player?.destroy?.();
    el.querySelectorAll('[data-case]').forEach(b => b.classList.toggle('on', b.dataset.case === String(raw ? 'custom' : caseIdx)));
    const payload = { ...base, ...(raw ? { rawArgs: raw } : { args }) };
    player = await showTrace($('.watch-out'), { code: sol.code, notes: sol.notes, payload, opts, onDone: () => { if (store.mark('watched:' + p.slug)) store.addXP(3, 'watched'); } });
  }
  $('.cases').addEventListener('click', e => {
    const b = e.target.closest('[data-case]');
    if (b) {
      if (b.dataset.case === 'custom') { $('.custom').classList.toggle('hide'); return; }
      caseIdx = +b.dataset.case; watch(p.tests[caseIdx][0]);
    }
    if (e.target.closest('.go-custom')) {
      const raw = [...el.querySelectorAll('[data-arg]')].map(i => i.value);
      if (p.mode === 'design') { try { watch([JSON.parse(raw[0]), JSON.parse(raw[1])]); } catch { toast('Those need to be JSON lists, like ["push","pop"] and [[1],[]]'); } return; }
      watch(null, raw);
    }
  });
  watch(p.tests[0][0]);

  let editorReady = false;
  async function initEditor() {
    if (editorReady) return; editorReady = true;
    await waitForCM();
    editor = createEditor($('.ed'), store.code(p.slug) || p.starter, { onChange: v => store.saveCode(p.slug, v), minLines: 14 });
  }
  el.querySelector('.tabs').addEventListener('click', e => {
    const b = e.target.closest('[data-tab]'); if (!b) return;
    el.querySelectorAll('.tabs [data-tab]').forEach(x => x.classList.toggle('on', x === b));
    $('.tab-watch').classList.toggle('hide', b.dataset.tab !== 'watch');
    $('.tab-code').classList.toggle('hide', b.dataset.tab !== 'code');
    if (b.dataset.tab === 'code') { player?.stop?.(); initEditor().then(() => editor?.refresh()); }
  });
  async function runTests() {
    const r = $('.results');
    r.innerHTML = '<div class="loadbox"><span class="spinner"></span> Running tests…</div>';
    try {
      const res = await py.run('test', { ...base, code: editor.get(), tests: p.tests }, 15000);
      const out = renderResults(r, res, { names });
      editor.mark(out.line);
      if (out.total && out.pass === out.total) {
        const first = store.solve(p.slug, XP[p.diff]);
        if (first) toast(`🎉 Solved! +${XP[p.diff]} XP`);
        const n = Object.keys(store.data().solved).length;
        if (n >= 1) store.badge('First Solve 🐣'); if (n >= 10) store.badge('Ten Down 🔟'); if (n >= 50) store.badge('Half-Century 🏏');
        if (p.diff === 'Hard') store.badge('Hard Hitter 💪');
      }
    } catch (e) {
      r.innerHTML = `<div class="res-banner bad">${e.message === 'TIMEOUT' ? '⏰ Your code ran for too long. Probably an infinite loop (a while loop that never ends?).' : esc(e.message)}</div>`;
    }
  }
  $('.runtests').onclick = runTests;
  el.addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && editor) { e.preventDefault(); runTests(); } });
  $('.watchmine').onclick = async () => {
    myPlayer?.destroy?.();
    myPlayer = await showTrace($('.mine-out'), { code: editor.get(), payload: { ...base, args: p.tests[0][0] }, opts });
    $('.mine-out').scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
  $('.reset').onclick = () => { if (confirm('Throw away your code and start fresh?')) { editor.set(p.starter); } };
  $('.peek').onclick = () => {
    if (!confirm('Peek at the full solution? (Try the hints first! 🙈)')) return;
    editor.set(sol.code + '\n');
    toast('Solution loaded. Read it, then try writing it again from memory!');
  };
  return () => { offPy(); player?.destroy?.(); myPlayer?.destroy?.(); };
}
