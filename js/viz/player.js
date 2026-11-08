import { icon } from '../ui/icons.js';
/* The "theater": code on one side, live pictures on the other, playback controls below. */
import { renderState } from './render.js';
import { explain, stateAt } from './explain.js';
import { highlight } from '../ui/code.js';
import { esc } from './values.js';
import { store } from '../store.js';

export const SPEEDS = [
  { id: 'snail', label: 'Snail', ms: 2600, tip: 'super slow, lots of time to read' },
  { id: 'walk', label: 'Walk', ms: 1300, tip: 'comfy reading speed' },
  { id: 'run', label: 'Run', ms: 550, tip: 'quick' },
  { id: 'zoom', label: 'Zoom', ms: 140, tip: 'blink and you miss it' },
  { id: 'manual', label: 'Manual', ms: 0, tip: 'you press Next yourself' },
];

export function createPlayer(root, { code, notes = {}, trace, opts = {}, onDone }) {
  const lines = code.split('\n');
  const steps = trace.steps;
  let k = Math.max(0, Math.min(steps.length - 1, opts.startAt || 0)), timer = null, playing = false;
  let speed = store.get('speed', 'walk');
  let predict = false, score = { ok: 0, total: 0 };

  root.innerHTML = `
  <div class="theater">
    <div class="th-left">
      <div class="th-head"><span class="pill-lbl">Code</span><span class="th-step"></span></div>
      <div class="codeview" role="list">${lines.map((l, i) => `<div class="cl" data-l="${i + 1}"><span class="ln">${i + 1}</span><span class="hits"></span><span class="ct">${highlight(l)}</span>${notes[i + 1] ? '<span class="nmark" title="This line has a tip"></span>' : ''}</div>`).join('')}</div>
      <div class="explain" aria-live="polite"></div>
    </div>
    <div class="th-right"><div class="th-head"><span class="pill-lbl">What's happening</span><span class="th-legend">changed things glow <span class="glow-dot"></span></span></div><div class="vizarea"></div></div>
    <div class="th-controls">
      <div class="ctrl-row">
        <button class="ib" data-a="first" title="Back to start">${icon('skip-back')}</button>
        <button class="ib" data-a="prev" title="Previous step (←)">${icon('chevron-left')}</button>
        <button class="ib play" data-a="play" title="Play / pause (space)">${icon('play')}</button>
        <button class="ib" data-a="next" title="Next step (→)">${icon('chevron-right')}</button>
        <button class="ib" data-a="last" title="Jump to end">${icon('skip-forward')}</button>
        <input type="range" class="scrub" min="0" max="${Math.max(0, steps.length - 1)}" value="0" aria-label="Timeline">
      </div>
      <div class="ctrl-row wrap">
        <div class="seg speeds">${SPEEDS.map(s => `<button data-s="${s.id}" title="${s.tip}">${s.label}</button>`).join('')}</div>
        <button class="chipbtn predict" title="Guess which line runs next">Predict mode</button>
        <span class="pscore"></span>
      </div>
    </div>
  </div>`;
  const $ = s => root.querySelector(s);
  const viz = $('.vizarea'), ex = $('.explain'), scrub = $('.scrub'), stepLbl = $('.th-step');
  const lineEls = [...root.querySelectorAll('.cl')];
  if (trace.truncated) ex.insertAdjacentHTML('beforebegin', '');

  function paint() {
    const s = steps[k];
    if (!s) { viz.innerHTML = '<div class="viz-empty">This code finished before doing anything.</div>'; return; }
    const hits = {};
    for (let i = 0; i <= k; i++) if (steps[i].e === 'line') hits[steps[i].l] = (hits[steps[i].l] || 0) + 1;
    const prevL = k > 0 ? steps[k - 1].l : -1;
    lineEls.forEach((el, i) => {
      const n = i + 1;
      el.classList.toggle('cur', n === s.l);
      el.classList.toggle('was', n === prevL && n !== s.l);
      el.classList.toggle('ret', n === s.l && s.e === 'return');
      el.querySelector('.hits').textContent = hits[n] ? `×${hits[n]}` : '';
    });
    const curEl = lineEls[s.l - 1];
    if (curEl) {
      const box = root.querySelector('.codeview');
      const top = curEl.offsetTop - box.offsetTop;
      if (top < box.scrollTop || top > box.scrollTop + box.clientHeight - 40) box.scrollTop = top - box.clientHeight / 3;
    }
    const e = explain(trace, k, lines, notes);
    ex.innerHTML = `<div class="ex-line">Line ${s.l}</div><div class="ex-head">${e.head}</div>${e.note ? `<div class="ex-note">${esc(e.note)}</div>` : ''}${e.changes.length ? `<div class="ex-chg"><b>What changed:</b><ul>${e.changes.map(x => `<li class="t-${x.t}">${x.html}</li>`).join('')}</ul></div>` : ''}${k === steps.length - 1 ? finalBox() : ''}`;
    const state = stateAt(steps, k);
    const prevState = k > 0 ? stateAt(steps, k - 1) : null;
    renderState(viz, state, prevState, trace, { ...opts, stepIndex: k + (state === s ? 0 : 1) });
    scrub.value = k;
    stepLbl.textContent = `step ${k + 1} / ${steps.length}${trace.truncated ? ' (stopped early: too many steps)' : ''}`;
    $('.play').innerHTML = icon(playing ? 'pause' : 'play');
    root.querySelectorAll('.speeds button').forEach(b => b.classList.toggle('on', b.dataset.s === speed));
  }
  function finalBox() {
    const err = trace.error;
    if (trace.needInput != null) return '<div class="ex-final wait">Paused: your program wants you to type something in the box below.</div>';
    if (err) return `<div class="ex-final err">${esc(err.error)}${err.line ? ` (line ${err.line})` : ''}</div>`;
    if (trace.result !== null && trace.result !== undefined) return `<div class="ex-final">Done! The answer is <code>${esc(trace.result)}</code></div>`;
    return '<div class="ex-final">Done!</div>';
  }
  function go(n) { k = Math.max(0, Math.min(steps.length - 1, n)); paint(); if (k === steps.length - 1) { stop(); onDone && onDone(); } }
  function stop() { playing = false; clearTimeout(timer); paint(); }
  function tick() {
    if (!playing) return;
    if (k >= steps.length - 1) { stop(); return; }
    go(k + 1);
    const sp = SPEEDS.find(s => s.id === speed);
    if (sp.ms) timer = setTimeout(tick, sp.ms);
    else stop();
  }
  function play() {
    if (predict) { ask(); return; }
    if (speed === 'manual') { go(k + 1); return; }
    if (k >= steps.length - 1) k = 0;
    playing = !playing;
    clearTimeout(timer);
    paint();
    if (playing) timer = setTimeout(tick, 250);
  }
  function ask() {
    if (k >= steps.length - 1) return;
    ex.insertAdjacentHTML('afterbegin', '');
    ex.querySelector('.ex-ask')?.remove();
    ex.insertAdjacentHTML('afterbegin', '<div class="ex-ask">Which line runs <b>next</b>? Tap it in the code!</div>');
    root.classList.add('asking');
  }
  root.querySelector('.codeview').addEventListener('click', (e) => {
    if (!root.classList.contains('asking')) return;
    const el = e.target.closest('.cl');
    if (!el) return;
    const guess = +el.dataset.l;
    const right = steps[k + 1].l;
    root.classList.remove('asking');
    score.total++;
    const ok = guess === right;
    if (ok) { score.ok++; store.addXP(2, 'predict'); }
    go(k + 1);
    ex.insertAdjacentHTML('afterbegin', `<div class="ex-verdict ${ok ? 'ok' : 'no'}">${ok ? 'Nailed it! +2 XP' : `Not quite. You picked line ${guess}, it was line ${right}.`}</div>`);
    root.querySelector('.pscore').textContent = `${score.ok}/${score.total} right`;
    if (predict && k < steps.length - 1) setTimeout(ask, 300);
  });
  root.querySelector('.th-controls').addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.a) {
      const a = b.dataset.a;
      if (a !== 'play') stop();
      if (a === 'first') go(0);
      if (a === 'prev') go(k - 1);
      if (a === 'next') go(k + 1);
      if (a === 'last') go(steps.length - 1);
      if (a === 'play') play();
      if (predict && a !== 'play') ask();
    } else if (b.dataset.s) {
      speed = b.dataset.s;
      store.set('speed', speed);
      paint();
    } else if (b.classList.contains('predict')) {
      predict = !predict;
      b.classList.toggle('on', predict);
      stop();
      root.classList.remove('asking');
      if (predict) ask(); else ex.querySelector('.ex-ask')?.remove();
    }
  });
  scrub.addEventListener('input', () => { stop(); go(+scrub.value); });
  const onKey = (e) => {
    if (!document.body.contains(root)) { document.removeEventListener('keydown', onKey); return; }
    if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName) || document.activeElement?.closest?.('.CodeMirror')) return;
    if (e.key === 'ArrowRight') { stop(); go(k + 1); e.preventDefault(); }
    else if (e.key === 'ArrowLeft') { stop(); go(k - 1); e.preventDefault(); }
    else if (e.key === ' ') { play(); e.preventDefault(); }
  };
  document.addEventListener('keydown', onKey);
  paint();
  return {
    play() { if (!playing) play(); },
    stop,
    destroy() { stop(); document.removeEventListener('keydown', onKey); },
  };
}
