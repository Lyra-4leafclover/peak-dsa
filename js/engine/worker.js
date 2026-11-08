/* Runs Python (Pyodide) off the main thread so the page never freezes. */
const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';
importScripts(PYODIDE + 'pyodide.js');
let api = null;
const ready = (async () => {
  const py = await loadPyodide({ indexURL: PYODIDE });
  const src = await (await fetch('tracer.py?v=3')).text();
  py.runPython(src);
  api = py.globals.get('api');
  postMessage({ type: 'ready' });
})().catch(err => postMessage({ type: 'fatal', error: String(err) }));

onmessage = async (e) => {
  const { id, cmd, payload } = e.data;
  try {
    await ready;
    const out = api(cmd, JSON.stringify(payload));
    postMessage({ id, ok: true, data: JSON.parse(out) });
  } catch (err) {
    postMessage({ id, ok: false, error: String(err && err.message || err) });
  }
};
