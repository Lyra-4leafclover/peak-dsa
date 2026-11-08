/* Tiny wrapper around the Python worker: py.run('trace', {...}) -> Promise */
let worker = null, readyP = null, seq = 0;
const waiting = new Map();
const listeners = new Set();
export let status = 'idle'; // idle | loading | ready | error

function setStatus(s) { status = s; listeners.forEach(f => f(s)); }
export function onStatus(f) { listeners.add(f); f(status); return () => listeners.delete(f); }

function boot() {
  if (worker) return readyP;
  setStatus('loading');
  worker = new Worker(new URL('./worker.js', import.meta.url));
  readyP = new Promise((res, rej) => {
    worker.onmessage = (e) => {
      const m = e.data;
      if (m.type === 'ready') { setStatus('ready'); res(); return; }
      if (m.type === 'fatal') { setStatus('error'); rej(new Error(m.error)); return; }
      const w = waiting.get(m.id);
      if (!w) return;
      waiting.delete(m.id); clearTimeout(w.t);
      m.ok ? w.res(m.data) : w.rej(new Error(m.error));
    };
    worker.onerror = (e) => { setStatus('error'); rej(e); };
  });
  return readyP;
}

export function warmup() { boot().catch(() => {}); }

function restart() {
  if (worker) worker.terminate();
  worker = null; readyP = null;
  for (const w of waiting.values()) { clearTimeout(w.t); w.rej(new Error('Stopped')); }
  waiting.clear();
}

export async function run(cmd, payload, timeoutMs = 12000) {
  await boot();
  const id = ++seq;
  return new Promise((res, rej) => {
    const t = setTimeout(() => {
      waiting.delete(id);
      restart();
      warmup();
      rej(new Error('TIMEOUT'));
    }, timeoutMs);
    waiting.set(id, { res, rej, t });
    worker.postMessage({ id, cmd, payload });
  });
}
