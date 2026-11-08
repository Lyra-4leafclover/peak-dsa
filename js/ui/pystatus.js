/* A little "Python engine" status light. */
import { onStatus, warmup } from '../engine/py.js';
const TXT = { idle: 'Python sleeping', loading: 'Waking up Python… (first time ~5-10s)', ready: 'Python ready', error: 'Python failed to load (check internet)' };
export function pyStatus(el) {
  el.classList.add('pyload');
  el.innerHTML = '<i></i><span></span>';
  const off = onStatus(s => { el.className = `pyload ${s}`; el.querySelector('span').textContent = TXT[s]; });
  warmup();
  return off;
}
