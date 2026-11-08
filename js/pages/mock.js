/* Mock interviews: a timed coding round (secret tests) and a timed concept round. */
import { PROBLEMS } from '../data/problems.js';
import { CONCEPTS, PREDICT } from '../data/quizzes.js';
import { payloadOf } from './problems.js';
import { runQuiz } from './challenges.js';
import { createEditor, waitForCM } from '../ui/editor.js';
import { renderResults } from '../ui/results.js';
import { pyStatus } from '../ui/pystatus.js';
import * as py from '../engine/py.js';
import { store } from '../store.js';
import { esc } from '../viz/values.js';

const pick = (arr, n) => [...arr].sort(() => Math.random() - .5).slice(0, n);
const LEVELS = { warmup: ['🌱 Warm-up', ['Easy', 'Easy'], 30], real: ['💼 Real interview', ['Easy', 'Medium'], 45], hard: ['🔥 Big-tech', ['Medium', 'Hard'], 60] };

export function render(el, kind, lvl) {
  if (kind === 'code' && LEVELS[lvl]) return coding(el, lvl);
  if (kind === 'concepts') return concepts(el);
  el.innerHTML = `<div class="wrap"><div class="phead"><img src="assets/art/mock.webp" alt=""><div class="txt"><h1>Mock Interviews</h1><p>Practise the real thing. A timer runs, tests are <b>secret</b> (you only see examples), and you get a score card at the end. Talk out loud as you code, like you would to an interviewer!</p></div></div>
    <div class="grid g3">${Object.entries(LEVELS).map(([k, [t, d, m]]) => `<a class="tile" href="#/mock/code/${k}"><div class="body"><h3>${t}</h3><p>2 random problems (${d.join(' + ')}), ${m} minutes, secret tests.</p><span class="btn small" style="align-self:flex-start;margin-top:8px">Start →</span></div></a>`).join('')}
      <a class="tile" href="#/mock/concepts"><div class="body"><h3>🧠 Concept round</h3><p>12 quick-fire theory questions in 6 minutes, like a phone screen.</p><span class="btn small" style="align-self:flex-start;margin-top:8px">Start →</span></div></a></div>
    <div class="card" style="margin-top:18px"><h3>📋 Interview recipe (say these out loud)</h3><ol><li>Repeat the problem in your own words. Ask about edge cases (empty? negatives? duplicates?).</li><li>Say the slow, obvious solution first and its Big-O.</li><li>Find the bottleneck. Which pattern helps? (hash map, two pointers, window, heap…)</li><li>Code it cleanly. Name variables well.</li><li>Walk through an example by hand. Then test edge cases.</li><li>State the final time and memory complexity.</li></ol></div></div>`;
}

function concepts(el) {
  el.innerHTML = '<div class="wrap" style="padding-top:22px"><a class="crumb" href="#/mock">← Mocks</a><h1>🧠 Concept round</h1><div class="arena"></div></div>';
  const go = () => runQuiz(el.querySelector('.arena'), pick([...CONCEPTS, ...PREDICT], 12), { title: 'Concept round', timeLimit: 360, onEnd: (s, again) => { if (again) return go(); store.addMock({ date: new Date().toLocaleDateString(), kind: 'Concept round', score: `${s}/12` }); store.badge('Mock Survivor 🎤'); } });
  return go();
}

async function coding(el, lvl) {
  const [title, diffs, mins] = LEVELS[lvl];
  const probs = diffs.map((d, i) => pick(PROBLEMS.filter(p => p.diff === d && p.mode !== 'design'), 2)[i % 2]);
  let left = mins * 60, cur = 0, over = false;
  const codes = probs.map(p => p.starter), results = probs.map(() => null);
  el.innerHTML = `<div class="wrap" style="padding-top:22px"><div class="row"><a class="crumb" href="#/mock">← Quit mock</a><span class="grow"></span><span class="pys"></span><span class="bigtimer"></span></div>
    <h1>${title}</h1><div class="tabs">${probs.map((p, i) => `<button data-i="${i}">Q${i + 1}: ${esc(p.title)}</button>`).join('')}<span class="grow"></span><button class="finish" style="background:var(--red);color:#fff">🏁 Finish</button></div>
    <div class="pgrid"><aside class="card qinfo"></aside><section><div class="card code-card"><div class="ed"></div><div class="row"><button class="btn green run">▶ Run secret tests</button><span class="tiny muted">You may run as often as you like.</span></div></div><div class="results"></div></section></div></div>`;
  const $ = s => el.querySelector(s);
  const off = pyStatus($('.pys'));
  await waitForCM();
  const ed = createEditor($('.ed'), codes[0], { minLines: 16, onChange: v => { codes[cur] = v; } });
  function show(i) {
    cur = i; const p = probs[i];
    el.querySelectorAll('.tabs [data-i]').forEach(b => b.classList.toggle('on', +b.dataset.i === i));
    $('.qinfo').innerHTML = `<span class="tag ${p.diff}">${p.diff}</span> <span class="tag">${p.topic}</span><h3 style="margin-top:8px">${esc(p.title)}</h3><p>${esc(p.story)}</p><div class="ex"><b>Example</b><div><code>${esc(JSON.stringify(p.tests[0][0]))}</code> → <code>${esc(JSON.stringify(p.tests[0][1]))}</code></div></div><p class="tiny muted" style="margin-top:10px">No hints in a mock 😉 Trust yourself!</p>`;
    ed.set(codes[i]); $('.results').innerHTML = results[i] ? `<div class="res-banner ${results[i].pass === results[i].total ? 'good' : 'bad'}">Last run: ${results[i].pass}/${results[i].total} secret tests</div>` : '';
  }
  el.querySelector('.tabs').onclick = e => { const b = e.target.closest('[data-i]'); if (b) show(+b.dataset.i); if (e.target.closest('.finish')) finish(); };
  $('.run').onclick = async () => {
    const p = probs[cur], r = $('.results');
    r.innerHTML = '<div class="loadbox"><span class="spinner"></span> Running secret tests…</div>';
    try { const res = await py.run('test', { ...payloadOf(p), code: ed.get(), tests: p.tests }, 15000); results[cur] = renderResults(r, res, { hidden: p.tests.length - 1 }); }
    catch (e) { r.innerHTML = `<div class="res-banner bad">${e.message === 'TIMEOUT' ? '⏰ Timed out (infinite loop?)' : esc(e.message)}</div>`; }
  };
  const tick = setInterval(() => { left--; const t = $('.bigtimer'); if (t) { t.textContent = `⏱ ${Math.floor(left / 60)}:${String(left % 60).padStart(2, '0')}`; t.classList.toggle('low', left < 300); } if (left <= 0) finish(); }, 1000);
  function finish() {
    if (over) return; over = true; clearInterval(tick);
    const pts = results.map(r => (r && r.total ? r.pass / r.total : 0));
    const score = Math.round(pts.reduce((a, b) => a + b, 0) / probs.length * 100);
    const used = mins * 60 - left;
    store.addMock({ date: new Date().toLocaleDateString(), kind: title, score: `${score}%` });
    store.badge('Mock Survivor 🎤');
    store.addXP(Math.round(score / 4), 'mock');
    el.querySelector('.wrap').innerHTML = `<div class="card scorecard"><img src="assets/art/mock.webp" alt="" style="width:160px;margin:0 auto 10px;border-radius:24px"><div class="big">${score}%</div><p>${score === 100 ? '🏆 Hired! (in our hearts)' : score >= 60 ? '🌟 Strong performance!' : '💪 Good practice. Review the solutions below and try again.'}</p><p class="muted">Time used: ${Math.floor(used / 60)}m ${used % 60}s</p>
      <div class="pcards" style="text-align:left;margin:16px 0">${probs.map((p, i) => `<a class="prow" href="#/problems/${p.slug}"><span class="chk">${pts[i] === 1 ? '✅' : pts[i] > 0 ? '🟡' : '❌'}</span><span class="pt">${esc(p.title)}</span><span class="tiny">${Math.round(pts[i] * 100)}% · watch solution →</span></a>`).join('')}</div>
      <a class="btn" href="#/mock">Back to mocks</a></div>`;
  }
  show(0);
  return () => { clearInterval(tick); off(); };
}
