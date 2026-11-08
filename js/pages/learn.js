import { LESSONS, lessonById } from '../data/lessons.js';
import { art, icon } from '../ui/icons.js';
import { PROBLEMS } from '../data/problems.js';
import { mountWidget } from '../learn/widgets.js';
import { showTrace } from '../ui/theater.js';
import { splitNotes } from '../ui/code.js';
import { pyStatus } from '../ui/pystatus.js';
import { store } from '../store.js';
import { esc } from '../viz/values.js';

export function render(el, kind, id) {
  if (id && lessonById[id]) return lesson(el, lessonById[id]);
  const card = l => `<a class="tile" href="#/learn/${l.kind}/${l.id}">${store.isDone('lesson:' + l.id) ? '<span class="done-badge">✓ done</span>' : ''}<div class="art">${art(l.art)}</div><div class="body"><h3>${l.emoji} ${l.title}</h3><p>${l.analogy.replace(/<[^>]+>/g, '').split('. ')[0]}.</p></div></a>`;
  el.innerHTML = `<div class="wrap">
    <div class="phead">${art('learn', 'ph')}<div class="txt"><h1>Learn</h1><p>Every lesson = a cute everyday picture, a toy you can poke, and real Python you can watch run line by line. Go in order if you're new, or jump to whatever confuses you.</p></div></div>
    <h2>Data structures</h2><p class="muted">Ways to store stuff.</p><div class="grid g4">${LESSONS.filter(l => l.kind === 'ds').map(card).join('')}</div>
    <h2 style="margin-top:34px">Algorithm patterns</h2><p class="muted">Ways to solve stuff.</p><div class="grid g4">${LESSONS.filter(l => l.kind === 'algo').map(card).join('')}</div></div>`;
}

function lesson(el, L) {
  const i = LESSONS.indexOf(L), prev = LESSONS[i - 1], next = LESSONS[i + 1];
  const practice = L.topic ? PROBLEMS.filter(p => p.topic === L.topic).slice(0, 6) : [];
  el.innerHTML = `<div class="wrap lesson" style="padding-top:22px">
    <a class="crumb" href="#/learn">← All lessons</a>
    <div class="lhero">${art(L.art, 'lh')}<div><h1>${L.emoji} ${L.title}</h1><div class="analogy">${L.analogy}</div></div></div>
    <div class="card"><h3>In plain words</h3>${L.plain.map(p => `<p>${esc(p).replace(/`([^`]+)`/g, '<code>$1</code>')}</p>`).join('')}
      <h3>The moves (and how long they take)</h3><div class="facts">${L.facts.map(([a, b, c]) => `<div class="fact">${c ? `<em>${esc(c)}</em>` : ''}<b>${esc(a)}</b><span>${esc(b)}</span></div>`).join('')}</div></div>
    ${L.widget ? '<div class="playbox"></div>' : ''}
    <div class="card"><div class="row"><h3 style="margin:0">Watch real Python do it</h3><span class="grow"></span><span class="pys"></span></div><p class="muted tiny">Press ▶ or use your arrow keys. Try Snail speed and Predict mode!</p><div class="demo"><button class="btn green rundemo">▶ Load the demo</button></div></div>
    <div class="card"><h3>Common mistakes</h3><ul class="mistakes">${L.mistakes.map(m => `<li>${esc(m).replace(/`([^`]+)`/g, '<code>$1</code>')}</li>`).join('')}</ul></div>
    ${practice.length ? `<div class="card"><h3>Practice this</h3><div class="pcards">${practice.map(p => `<a class="prow ${store.isSolved(p.slug) ? 'solved' : ''}" href="#/problems/${p.slug}"><span class="chk">${store.isSolved(p.slug) ? '✓' : '○'}</span><span class="pt">${esc(p.title)}</span><span class="tag ${p.diff}">${p.diff}</span></a>`).join('')}</div></div>` : ''}
    <div class="lnav">${prev ? `<a class="btn ghost" href="#/learn/${prev.kind}/${prev.id}">← ${prev.title}</a>` : ''}<span class="grow"></span><button class="btn green markdone">${store.isDone('lesson:' + L.id) ? '✓ Done' : 'I get it! ✓ (+5 XP)'}</button>${next ? `<a class="btn" href="#/learn/${next.kind}/${next.id}">${next.title} →</a>` : ''}</div>
  </div>`;
  const $ = s => el.querySelector(s);
  const off = pyStatus($('.pys'));
  if (L.widget) mountWidget($('.playbox'), L.widget);
  let player = null;
  const run = async () => { const { code, notes } = splitNotes(L.demo); player = await showTrace($('.demo'), { code, notes, payload: { mode: 'script' }, opts: { bars: L.id === 'sorting' } }); };
  $('.rundemo').onclick = run;
  run();
  $('.markdone').onclick = e => {
    if (store.mark('lesson:' + L.id)) { store.addXP(5, 'lesson'); }
    e.target.textContent = '✓ Done';
    if (LESSONS.every(l => store.isDone('lesson:' + l.id))) store.badge('Scholar');
  };
  return () => { off(); player?.destroy?.(); };
}
