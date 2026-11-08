/* Run a trace in the Python worker, then mount the step player. */
import * as py from '../engine/py.js';
import { createPlayer } from '../viz/player.js';
import { esc } from '../viz/values.js';

export async function showTrace(el, { code, notes = {}, payload, opts = {}, onDone }) {
  el.innerHTML = `<div class="loadbox"><span class="spinner"></span> ${py.status === 'ready' ? 'Running your code line by line…' : 'Waking up Python (first time takes a few seconds)…'}</div>`;
  let trace;
  try {
    trace = await py.run('trace', { code, maxSteps: 2500, ...payload }, 20000);
  } catch (e) {
    el.innerHTML = `<div class="res-banner bad">${e.message === 'TIMEOUT' ? 'That took too long. Is there an infinite loop? (A loop that never stops.)' : `Couldn't run Python: ${esc(e.message)}`}</div>`;
    return null;
  }
  if (!trace.steps.length) {
    el.innerHTML = trace.error
      ? `<div class="res-banner bad">${esc(trace.error.error)}${trace.error.line ? ` (line ${trace.error.line})` : ''}</div>`
      : '<div class="res-banner">Nothing ran. Did you write a function but never call it? Here we call the function for you, so keep its name.</div>';
    return null;
  }
  el.innerHTML = '';
  if (trace.truncated) el.insertAdjacentHTML('beforeend', '<div class="res-banner warn">This run was very long, so we show the first 2,500 steps. Try a smaller input!</div>');
  const holder = document.createElement('div');
  el.appendChild(holder);
  return createPlayer(holder, { code, notes, trace, opts, onDone });
}
