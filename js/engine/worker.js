/* Runs Python (Pyodide) off the main thread so the page never freezes. */
const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';
importScripts(PYODIDE + 'pyodide.js');
let api = null, pyo = null;
const ready = (async () => {
  pyo = await loadPyodide({ indexURL: PYODIDE });
  pyo.runPython(await (await fetch('meaning.py?v=1')).text());
  pyo.runPython(await (await fetch('tracer.py?v=5')).text());
  api = pyo.globals.get('api');
  postMessage({ type: 'ready' });
})().catch(err => postMessage({ type: 'fatal', error: String(err) }));

const BLOCKED = {
  tkinter: 'opens a desktop window', turtle: 'draws in a desktop window', pygame: 'opens a game window',
  pyglet: 'opens a window', kivy: 'opens an app window', PyQt5: 'opens a desktop window', PyQt6: 'opens a desktop window',
  PySide6: 'opens a desktop window', wx: 'opens a desktop window', requests: 'needs the internet', urllib3: 'needs the internet',
  socket: 'needs the internet', selenium: 'controls a real browser', pyautogui: 'controls your mouse and keyboard',
  keyboard: 'reads your real keyboard', msvcrt: 'only works on Windows', curses: 'needs a real terminal window',
};

function importsOf(code) {
  const names = new Set();
  for (const m of code.matchAll(/^\s*(?:from\s+([A-Za-z_]\w*)[\w.]*\s+import|import\s+([^#\n]+))/gm)) {
    if (m[1]) names.add(m[1]);
    else m[2].split(',').forEach(part => { const n = part.trim().split(/[\s.]/)[0]; if (n) names.add(n); });
  }
  return [...names];
}

async function libs(code) {
  const names = importsOf(code);
  const bad = names.find(n => BLOCKED[n]);
  if (bad) return { blocked: bad, why: BLOCKED[bad] };
  try { await pyo.loadPackagesFromImports(code); } catch (e) { /* fall through to micropip */ }
  const find = pyo.runPython('import importlib.util\nlambda n: importlib.util.find_spec(n) is not None');
  const missing = names.filter(n => !find(n));
  if (missing.length) {
    try {
      await pyo.loadPackage('micropip');
      const mp = pyo.pyimport('micropip');
      for (const n of missing) { try { await mp.install(n); } catch (e) { /* reported below */ } }
    } catch (e) { /* offline */ }
  }
  const still = names.filter(n => !find(n));
  return { missing: still };
}

onmessage = async (e) => {
  const { id, cmd, payload } = e.data;
  try {
    await ready;
    if (cmd === 'libs') { postMessage({ id, ok: true, data: await libs(payload.code || '') }); return; }
    const out = api(cmd, JSON.stringify(payload));
    postMessage({ id, ok: true, data: JSON.parse(out) });
  } catch (err) {
    postMessage({ id, ok: false, error: String(err && err.message || err) });
  }
};
