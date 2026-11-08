/* Run a trace in the Python worker, then mount the step player.
   If the code calls input(), we show a box; each answer re-runs the program with all answers so far. */
import * as py from '../engine/py.js';
import { createPlayer } from '../viz/player.js';
import { esc } from '../viz/values.js';

const LIMIT = 5000;
const bad = msg => `<div class="res-banner bad">${msg}</div>`;

export async function showTrace(el, { code, notes = {}, payload, opts = {}, onDone }) {
  const answers = [...(payload.stdin || [])];
  const seed = payload.seed ?? Math.floor(Math.random() * 1e9);
  let player = null;
  const busy = msg => { el.innerHTML = `<div class="loadbox"><span class="spinner"></span> ${msg}</div>`; };
  busy(py.status === 'ready' ? 'Running your code line by line…' : 'Waking up Python (first time takes a few seconds)…');

  if (/^\s*(import|from)\s/m.test(code)) {
    let L;
    try {
      if (py.status === 'ready') busy('Getting the libraries your code uses…');
      L = await py.run('libs', { code }, 180000);
    } catch (e) { el.innerHTML = bad(`Couldn't load the libraries: ${esc(e.message)}`); return null; }
    if (L.blocked) {
      el.innerHTML = bad(`Your code uses <code>${esc(L.blocked)}</code>, which ${esc(L.why)}. That can't run inside a web page, so it can't be visualized here. Programs that print text, ask for input and work with data are fine.`);
      return null;
    }
    if (L.missing.length) {
      el.innerHTML = bad(`Couldn't find the library <code>${esc(L.missing.join(', '))}</code>. Python's built-in libraries and most popular ones (like numpy and pandas) work here, but this one isn't available in the browser.`);
      return null;
    }
  }

  async function run(startAt) {
    let trace;
    try {
      trace = await py.run('trace', { code, maxSteps: LIMIT, ...payload, stdin: answers, seed }, 30000);
    } catch (e) {
      el.innerHTML = bad(e.message === 'TIMEOUT' ? 'That took too long. Is there an infinite loop? (A loop that never stops.)' : `Couldn't run Python: ${esc(e.message)}`);
      return null;
    }
    if (!trace.steps.length) {
      el.innerHTML = trace.error
        ? bad(`${esc(trace.error.error)}${trace.error.line ? ` (line ${trace.error.line})` : ''}`)
        : trace.needInput != null
          ? bad('Your program asks for input before any of your lines run.')
          : '<div class="res-banner">Nothing ran. Did you write a function but never call it? Here we call the function for you, so keep its name.</div>';
      return null;
    }
    const waiting = trace.needInput != null;
    let box = null;
    player?.destroy?.();
    el.innerHTML = '';
    if (trace.truncated) el.insertAdjacentHTML('beforeend', `<div class="res-banner warn">This run was very long, so we show the first ${LIMIT.toLocaleString()} steps. Try a smaller input!</div>`);
    const holder = document.createElement('div');
    el.appendChild(holder);
    player = createPlayer(holder, {
      code, notes, trace, opts: { ...opts, startAt },
      onDone: waiting ? () => box?.querySelector('input')?.focus({ preventScroll: true }) : onDone,
    });
    if (waiting) {
      const asked = trace.needInput.trim();
      box = document.createElement('form');
      box.className = 'stdin-box';
      box.innerHTML = `<label for="stdin-in">Your program is waiting for you to type something.${asked ? ` It asked: <b>${esc(asked)}</b>` : ''}</label>
        <div class="stdin-row"><input id="stdin-in" autocomplete="off" spellcheck="false" placeholder="Type your answer, then press Enter"><button class="btn green" type="submit">Send</button></div>
        ${answers.length ? `<div class="stdin-past"><span class="muted">Your answers so far:</span> ${answers.map(a => `<code>${esc(a) || '(empty)'}</code>`).join(' ')} <button type="button" class="chipbtn restart">Start over</button></div>` : ''}`;
      const ex = holder.querySelector('.explain');
      ex ? ex.after(box) : holder.appendChild(box);
      box.onsubmit = async e => {
        e.preventDefault();
        const btn = box.querySelector('button[type=submit]');
        btn.disabled = true; btn.textContent = 'Running…';
        answers.push(box.querySelector('input').value);
        if (await run(Math.max(0, trace.steps.length - 2))) player.play();
      };
      box.querySelector('.restart')?.addEventListener('click', () => { answers.length = 0; run(0); });
    }
    return player;
  }

  if (!(await run(0))) return null;
  return { play() { player?.play(); }, stop() { player?.stop(); }, destroy() { player?.destroy?.(); } };
}
