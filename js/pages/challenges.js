import { art, icon } from '../ui/icons.js';
/* Challenges: daily problem, predict the output, Big-O quiz, bug hunt, speed round. */
import { PROBLEMS } from '../data/problems.js';
import { PREDICT, BIGO, BIGO_OPTS, CONCEPTS, BUGS } from '../data/quizzes.js';
import { bySlug, payloadOf, argNames } from './problems.js';
import { createEditor, waitForCM } from '../ui/editor.js';
import { renderResults } from '../ui/results.js';
import { highlight } from '../ui/code.js';
import { pyStatus } from '../ui/pystatus.js';
import * as py from '../engine/py.js';
import { store } from '../store.js';
import { esc } from '../viz/values.js';
import { toast } from '../app.js';

const shuffle = a => { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const today = () => new Date().toISOString().slice(0, 10);
export function dailyProblem() { const d = today(); let h = 0; for (const c of d) h = (h * 31 + c.charCodeAt(0)) >>> 0; return PROBLEMS[h % PROBLEMS.length]; }
const codeBlock = c => `<pre class="qcode">${c.split('\n').map(highlight).join('\n')}</pre>`;

/* Generic multiple-choice runner. items: [q, code, options, correct, why]. */
export function runQuiz(el, items, { title, timeLimit = 0, perQ = 0, onEnd, xpEach = 2 }) {
  let i = 0, score = 0, left = timeLimit, timer = null, answered = false;
  const end = () => { clearInterval(timer); el.innerHTML = `<div class="card scorecard"><div class="big">${score} / ${items.length}</div><p>${score === items.length ? 'PERFECT!' : score >= items.length * .7 ? 'Great job!' : 'Keep practising, you\'re getting there!'}</p><button class="btn again">Play again</button></div>`; el.querySelector('.again').onclick = () => onEnd?.(score, true); onEnd?.(score, false); };
  function show() {
    if (i >= items.length) return end();
    answered = false;
    const [q, code, opts, , ] = items[i];
    el.innerHTML = `<div class="card quiz"><div class="row"><b>${esc(title)}</b><span class="tag">Question ${i + 1} / ${items.length}</span><span class="tag bg-mint">Score ${score}</span><span class="grow"></span>${timeLimit ? `<span class="bigtimer">${fmtT(left)}</span>` : ''}</div>
      <h3>${esc(q)}</h3>${code ? codeBlock(code) : ''}<div class="qopts">${opts.map((o, k) => `<button class="qopt" data-k="${k}">${esc(o)}</button>`).join('')}</div><div class="why"></div></div>`;
    el.querySelector('.qopts').onclick = e => {
      const b = e.target.closest('[data-k]'); if (!b || answered) return; answered = true;
      const k = +b.dataset.k, ok = k === items[i][3];
      el.querySelectorAll('.qopt').forEach((x, j) => { if (j === items[i][3]) x.classList.add('right'); else if (j === k) x.classList.add('wrong'); });
      if (ok) { score++; store.addXP(xpEach, 'quiz'); }
      el.querySelector('.why').innerHTML = `<div class="res-banner ${ok ? 'good' : 'bad'}">${ok ? 'Correct!' : 'Not quite.'} ${esc(items[i][4])}</div><button class="btn small nextq">Next →</button>`;
      el.querySelector('.nextq').onclick = () => { i++; show(); };
    };
  }
  const fmtT = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  if (timeLimit) timer = setInterval(() => { left--; const t = el.querySelector('.bigtimer'); if (t) { t.textContent = fmtT(left); t.classList.toggle('low', left < 15); } if (left <= 0) end(); }, 1000);
  show();
  return () => clearInterval(timer);
}

const MODES = {
  predict: ['Predict the Output', 'Read tiny programs and guess what they print.', 'predict'],
  bigo: ['Big-O Quiz', 'How fast is this code? Pick its Big-O.', 'bigo'],
  bugs: ['Bug Hunt', 'Each solution has ONE sneaky bug. Find it and fix it until tests pass.', 'bugs'],
  speed: ['Speed Round', '60 seconds. As many concept questions as you can.', 'speed'],
};

export function render(el, mode, arg) {
  if (mode && MODES[mode]) return play(el, mode, arg);
  const d = dailyProblem();
  const dailyDone = store.isDone('daily:' + today());
  el.innerHTML = `<div class="wrap">
    <div class="phead">${art('challenges', 'ph')}<div class="txt"><h1>Challenges</h1><p>Short, fun games that make the ideas stick. Every right answer earns XP. Streak: <b>${store.streak()} day(s)</b></p></div></div>
    <div class="card daily"><div class="minirow"><div style="font-size:2.4rem"></div><div class="grow"><h3 style="margin:0">Daily Challenge · ${today()}</h3><p style="margin:0">Today's problem: <b>${esc(d.title)}</b> <span class="tag ${d.diff}">${d.diff}</span> · solve it today for a <b>+25 XP bonus</b></p></div>
      ${dailyDone ? '<span class="tag bg-mint">Done today</span>' : `<a class="btn" href="#/problems/${d.slug}">Let's go →</a><button class="btn ghost small claim">I solved it! Claim bonus</button>`}</div></div>
    <div class="grid g4" style="margin-top:18px">${Object.entries(MODES).map(([k, [t, dsc, art]]) => `<a class="tile" href="#/challenges/${k}"><div class="art">${art(art)}</div><div class="body"><h3>${t}</h3><p>${dsc}</p></div></a>`).join('')}</div></div>`;
  el.querySelector('.claim')?.addEventListener('click', () => {
    if (!store.isSolved(d.slug)) { toast('Solve it first! (Pass all tests on the problem page.)'); return; }
    if (store.mark('daily:' + today())) { store.addXP(25, 'daily'); store.badge('Daily Doer'); }
    render(el);
  });
}

function play(el, mode, arg) {
  const [t, dsc] = MODES[mode];
  el.innerHTML = `<div class="wrap" style="padding-top:22px"><a class="crumb" href="#/challenges">← Challenges</a><h1>${t}</h1><p class="muted">${dsc}</p><div class="arena"></div></div>`;
  const arena = el.querySelector('.arena');
  if (mode === 'predict') {
    const go = () => runQuiz(arena, shuffle(PREDICT).slice(0, 8), { title: 'Predict the Output', onEnd: (s, again) => { if (again) go(); else if (s >= 7) store.badge('Fortune Teller'); } });
    return go();
  }
  if (mode === 'bigo') {
    const items = () => shuffle(BIGO).slice(0, 8).map(([c, ans, why]) => ['What is the time complexity?', c, BIGO_OPTS, BIGO_OPTS.indexOf(ans), why]);
    const go = () => runQuiz(arena, items(), { title: 'Big-O Quiz', onEnd: (s, again) => { if (again) go(); else if (s >= 7) store.badge('Big-O Brain'); } });
    return go();
  }
  if (mode === 'speed') {
    let stop;
    const go = () => { stop = runQuiz(arena, shuffle([...CONCEPTS, ...PREDICT]).slice(0, 20), { title: 'Speed Round', timeLimit: 60, xpEach: 1, onEnd: (s, again) => { if (again) go(); else if (s >= 10) store.badge('Speed Demon'); } }); };
    go(); return () => stop?.();
  }
  return bugHunt(arena, +(arg || 0));
}

async function bugHunt(el, idx) {
  const [slug, hint, code] = BUGS[idx % BUGS.length];
  const p = bySlug[slug];
  el.innerHTML = `<div class="row" style="margin-bottom:10px">${BUGS.map((b, i) => `<a class="chipbtn ${i === idx ? 'on' : ''}" href="#/challenges/bugs/${i}">${store.isDone('bug:' + b[0]) ? '✓' : '○'} ${i + 1}</a>`).join('')}<span class="grow"></span><span class="pys"></span></div>
    <div class="card code-card"><h3>${esc(p.title)}</h3><p>${esc(p.story)}</p><div class="res-banner warn">Clue: ${esc(hint)}</div><div class="ed"></div>
    <div class="row"><button class="btn green run">▶ Run tests</button><a class="btn ghost small" href="#/problems/${slug}">See the full problem</a>${idx + 1 < BUGS.length ? `<a class="btn soft small" href="#/challenges/bugs/${idx + 1}">Next bug →</a>` : ''}</div></div><div class="results"></div>`;
  const off = pyStatus(el.querySelector('.pys'));
  await waitForCM();
  const ed = createEditor(el.querySelector('.ed'), code, { minLines: 10 });
  el.querySelector('.run').onclick = async () => {
    const r = el.querySelector('.results');
    r.innerHTML = '<div class="loadbox"><span class="spinner"></span> Testing…</div>';
    try {
      const res = await py.run('test', { ...payloadOf(p), code: ed.get(), tests: p.tests }, 15000);
      const o = renderResults(r, res, { names: argNames(p) });
      if (o.total && o.pass === o.total && store.mark('bug:' + slug)) { store.addXP(15, 'bug'); toast('Squashed! +15 XP'); if (BUGS.every(b => store.isDone('bug:' + b[0]))) store.badge('Bug Squasher'); }
    } catch (e) { r.innerHTML = `<div class="res-banner bad">${e.message === 'TIMEOUT' ? 'Timed out (infinite loop?)' : esc(e.message)}</div>`; }
  };
  return off;
}
