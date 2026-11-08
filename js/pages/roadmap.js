import { STAGES } from '../data/roadmap.js';
import { lessonById } from '../data/lessons.js';
import { PROBLEMS } from '../data/problems.js';
import { art } from '../ui/icons.js';
import { store } from '../store.js';
import { esc } from '../viz/values.js';

const RANK = { Easy: 0, Medium: 1, Hard: 2 };
const byLc = Object.fromEntries(PROBLEMS.map(p => [p.lc, p]));
const probsOf = s => s.lc.map(n => byLc[n]).filter(Boolean).filter((p, i, a) => a.indexOf(p) === i).sort((a, b) => RANK[a.diff] - RANK[b.diff]);
const NEED = 0.6;

function status(s) {
  const ls = s.lessons.filter(id => lessonById[id]);
  const ps = probsOf(s);
  const lessonsDone = ls.filter(id => store.isDone('lesson:' + id)).length;
  const solved = ps.filter(p => store.isSolved(p.slug)).length;
  const quiz = store.isDone('cp:' + s.id);
  const parts = ls.length + ps.length + 1, got = lessonsDone + solved + (quiz ? 1 : 0);
  const done = lessonsDone === ls.length && solved >= Math.ceil(ps.length * NEED) && quiz;
  return { ls, ps, lessonsDone, solved, quiz, done, pct: got / parts };
}

export function render(el) {
  const st = STAGES.map(status);
  const cur = st.findIndex(x => !x.done);
  const doneN = st.filter(x => x.done).length;
  el.innerHTML = `<div class="wrap">
    <div class="phead">${art('roadmap', 'ph')}<div class="txt"><h1>Roadmap</h1><p>One path from zero to interview-ready, in order. For each stage: read the lesson, solve the problems from easy to hard, then pass the checkpoint. A stage counts as done when its lessons are done, you solved at least ${Math.round(NEED * 100)}% of its problems, and you passed the checkpoint.</p></div></div>
    <div class="card rm-top"><b>${doneN} / ${STAGES.length} stages done</b><div class="bar"><i style="width:${doneN / STAGES.length * 100}%"></i></div>${cur >= 0 ? `<a class="btn small" href="#rm-${STAGES[cur].id}">Continue: ${esc(STAGES[cur].title)}</a>` : '<span class="tag bg-mint">All done! Try a mock interview.</span>'}</div>
    <div class="rm-list">${STAGES.map((s, i) => stage(s, st[i], i, cur)).join('')}
      <div class="rm-stage"><div class="rm-num">${STAGES.length + 1}</div><div class="card rm-card"><h3>Final: interview practice</h3><p class="muted">Put it all together under time pressure.</p><div class="row" style="gap:8px;flex-wrap:wrap"><a class="btn small" href="#/mock">Take a mock interview</a><a class="btn small ghost" href="#/challenges">Daily challenges</a></div></div></div>
    </div></div>`;
  el.querySelectorAll('.rm-quiz').forEach(q => wireQuiz(q, STAGES.find(s => s.id === q.dataset.id), el));
  el.querySelectorAll('a[href^="#rm-"]').forEach(a => a.onclick = e => { e.preventDefault(); el.querySelector(a.getAttribute('href'))?.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
}

function stage(s, x, i, cur) {
  const cls = x.done ? 'done' : i === cur ? 'cur' : '';
  return `<div class="rm-stage ${cls}" id="rm-${s.id}"><div class="rm-num">${x.done ? '✓' : i + 1}</div><div class="card rm-card">
    <div class="row" style="gap:10px;flex-wrap:wrap"><h3>${esc(s.title)}</h3>${i === cur ? '<span class="tag bg-lav">You are here</span>' : ''}<span class="grow"></span><span class="tiny muted">${Math.round(x.pct * 100)}%</span></div>
    <p class="muted" style="margin:0">${esc(s.goal)}</p>
    <div class="rm-cols">
      <div><h4>1. Learn</h4>${x.ls.map(id => { const L = lessonById[id], ok = store.isDone('lesson:' + id); return `<a class="rm-link ${ok ? 'ok' : ''}" href="#/learn/${L.kind}/${L.id}"><span class="chk">${ok ? '✓' : '○'}</span>${esc(L.title)}</a>`; }).join('')}</div>
      <div><h4>2. Practice (${x.solved}/${x.ps.length})</h4>${x.ps.map(p => { const ok = store.isSolved(p.slug); return `<a class="rm-link ${ok ? 'ok' : ''}" href="#/problems/${p.slug}"><span class="chk">${ok ? '✓' : '○'}</span>${esc(p.title)}<span class="tag ${p.diff}">${p.diff}</span></a>`; }).join('')}</div>
      <div><h4>3. Checkpoint</h4>${x.quiz ? '<p class="tiny"><b>✓ Passed.</b></p>' : ''}<div class="rm-quiz" data-id="${s.id}"><button class="btn small ${x.quiz ? 'ghost' : ''} start">${x.quiz ? 'Retake checkpoint' : `Take checkpoint (${s.quiz.length} questions)`}</button></div></div>
    </div></div></div>`;
}

function wireQuiz(box, s, page) {
  box.querySelector('.start').onclick = () => {
    let right = 0, answered = 0;
    box.innerHTML = s.quiz.map(([q, code, opts], qi) => `<div class="q" data-q="${qi}"><b>${esc(q)}</b>${code ? `<pre class="code">${esc(code)}</pre>` : ''}<div class="opts">${opts.map((o, oi) => `<button class="chipbtn" data-o="${oi}">${esc(o)}</button>`).join('')}</div><div class="tiny why"></div></div>`).join('') + '<div class="say res"></div>';
    box.onclick = e => {
      const b = e.target.closest('[data-o]'); if (!b) return; const qd = b.closest('[data-q]'); if (qd.dataset.done) return;
      const [, , , ok, why] = s.quiz[+qd.dataset.q]; qd.dataset.done = 1; answered++;
      const good = +b.dataset.o === ok; if (good) right++;
      b.classList.add(good ? 'right' : 'wrong'); qd.querySelector(`[data-o="${ok}"]`).classList.add('right');
      qd.querySelector('.why').textContent = (good ? 'Correct. ' : 'Not quite. ') + why;
      if (answered === s.quiz.length) {
        const pass = right >= s.quiz.length - (s.quiz.length > 3 ? 1 : 0);
        if (pass && store.mark('cp:' + s.id)) store.addXP(10, 'checkpoint');
        box.querySelector('.res').innerHTML = pass ? `${right}/${s.quiz.length}: passed! <a href="#/roadmap" class="again">Update my roadmap</a>` : `${right}/${s.quiz.length}. Review the lesson and try again. <button class="chipbtn retry">Retry</button>`;
        box.querySelector('.retry')?.addEventListener('click', ev => { ev.stopPropagation(); box.onclick = null; box.innerHTML = '<button class="btn small start">Take checkpoint</button>'; wireQuiz(box, s, page); });
        box.querySelector('.again')?.addEventListener('click', ev => { ev.preventDefault(); render(page); page.querySelector('#rm-' + s.id)?.scrollIntoView({ block: 'start' }); });
      }
    };
  };
}
