import { art, icon } from '../ui/icons.js';
/* Labs: bigger interactive playgrounds. */
import { mountWidget } from '../learn/widgets.js';
import { store } from '../store.js';

const LABS = [
  ['sortrace', 'Sorting Race', 'Four sorting algorithms race on the same shuffled bars. Who wins?', 'sorting'],
  ['maze', 'Maze Pathfinder', 'Draw walls, then watch BFS, DFS, Dijkstra and A* hunt for the exit.', 'maze'],
  ['fib', 'Memo Magic', 'See how many calls recursion makes with and without a memory.', 'recursion'],
  ['heap', 'Heap Lab', 'Push and pop and watch values bubble up and sink down.', 'heap'],
  ['bst', 'BST Builder', 'Grow your own binary search tree and search it.', 'tree'],
  ['hash', 'Hash Table Lab', 'See exactly which bucket each key lands in, and what a collision looks like.', 'hashmap'],
  ['graph', 'BFS vs DFS', 'Ripples vs deep dives on a little town map.', 'graph'],
  ['guess', 'Binary Search Game', 'Beat the computer at guessing a number from 1 to 100.', 'binarysearch'],
  ['bigo', 'Big-O Race Track', 'Slide n and watch O(n²) run away from O(log n).', 'bigo'],
];
const WIDGET = { heap: 'heap', bst: 'bst', hash: 'hashmap', graph: 'graph', guess: 'guess', bigo: 'bigo' };

export function render(el, id) {
  const lab = LABS.find(l => l[0] === id);
  if (!lab) {
    el.innerHTML = `<div class="wrap"><div class="phead">${art('labs', 'ph')}<div class="txt"><h1>Labs</h1><p>Big, hands-on experiments. Break things, race things, and see the algorithms with your own eyes.</p></div></div>
      <div class="grid g3">${LABS.map(([k, t, d, a]) => `<a class="tile" href="#/labs/${k}">${store.isDone('lab:' + k) ? '<span class="done-badge">✓ tried</span>' : ''}<div class="art">${art(a)}</div><div class="body"><h3>${t}</h3><p>${d}</p></div></a>`).join('')}</div></div>`;
    return;
  }
  el.innerHTML = `<div class="wrap lab-wrap" style="padding-top:22px"><a class="crumb" href="#/labs">← All labs</a><h1>${lab[1]}</h1><p class="muted">${lab[2]}</p><div class="labbox playbox"></div></div>`;
  if (store.mark('lab:' + id)) { store.addXP(5, 'lab'); if (LABS.every(l => store.isDone('lab:' + l[0]))) store.badge('Lab Rat'); }
  const box = el.querySelector('.labbox');
  if (WIDGET[id]) { mountWidget(box, WIDGET[id]); return; }
  return ({ sortrace, maze, fib })[id](box);
}

/* ---------- sorting race ---------- */
function* bubble(a) { for (let e = a.length - 1; e > 0; e--) for (let j = 0; j < e; j++) { yield [j, j + 1]; if (a[j] > a[j + 1]) { [a[j], a[j + 1]] = [a[j + 1], a[j]]; yield [j, j + 1, 1]; } } }
function* insertion(a) { for (let i = 1; i < a.length; i++) { let j = i; while (j > 0) { yield [j - 1, j]; if (a[j - 1] <= a[j]) break; [a[j - 1], a[j]] = [a[j], a[j - 1]]; yield [j - 1, j, 1]; j--; } } }
function* merge(a, lo = 0, hi = a.length) { if (hi - lo < 2) return; const m = (lo + hi) >> 1; yield* merge(a, lo, m); yield* merge(a, m, hi); const L = a.slice(lo, m), R = a.slice(m, hi); let i = 0, j = 0, k = lo; while (i < L.length || j < R.length) { yield [k, lo + i]; a[k++] = j >= R.length || (i < L.length && L[i] <= R[j]) ? L[i++] : R[j++]; yield [k - 1, k - 1, 1]; } }
function* quick(a, lo = 0, hi = a.length - 1) { if (lo >= hi) return; const p = a[hi]; let i = lo; for (let j = lo; j < hi; j++) { yield [j, hi]; if (a[j] < p) { [a[i], a[j]] = [a[j], a[i]]; yield [i, j, 1]; i++; } } [a[i], a[hi]] = [a[hi], a[i]]; yield [i, hi, 1]; yield* quick(a, lo, i - 1); yield* quick(a, i + 1, hi); }
function sortrace(box) {
  const ALGS = [['Bubble sort', bubble, 'O(n²)'], ['Insertion sort', insertion, 'O(n²)'], ['Merge sort', merge, 'O(n log n)'], ['Quick sort', quick, 'O(n log n)']];
  box.innerHTML = `<div class="ctrls"><label class="tiny">Bars <input class="n" type="range" min="10" max="120" value="40"></label><select class="kind"><option value="rand">Random</option><option value="near">Nearly sorted</option><option value="rev">Reversed</option></select><button class="btn small go">Race!</button><button class="btn small ghost shuf">New bars</button></div><div class="race" style="margin-top:12px"></div><div class="say" style="margin-top:10px">Each step = one comparison or swap. Fewer steps wins.</div>`;
  const race = box.querySelector('.race'); let base = [], raf = 0;
  const make = () => { const n = +box.querySelector('.n').value, k = box.querySelector('.kind').value; base = Array.from({ length: n }, (_, i) => i + 1); if (k === 'rand') base.sort(() => Math.random() - .5); else if (k === 'rev') base.reverse(); else for (let t = 0; t < n / 10; t++) { const i = Math.floor(Math.random() * (n - 1)); [base[i], base[i + 1]] = [base[i + 1], base[i]]; } lanes(); };
  let L = [];
  const lanes = () => { cancelAnimationFrame(raf); race.innerHTML = ALGS.map(([n, , o]) => `<div class="lane"><h4>${n}<span class="tag">${o}</span></h4><canvas width="300" height="140"></canvas><div class="meta"><span class="st">0 steps</span><span class="fin"></span></div></div>`).join(''); L = ALGS.map(([, g], i) => { const a = [...base]; return { a, g: g(a), el: race.children[i], done: false, steps: 0, hl: [] }; }); L.forEach(draw); };
  function draw(l) { const c = l.el.querySelector('canvas'), x = c.getContext('2d'), n = l.a.length, w = c.width / n; x.clearRect(0, 0, c.width, c.height); l.a.forEach((v, i) => { x.fillStyle = l.done ? '#22b07a' : l.hl.includes(i) ? (l.hl[2] ? '#ff6fa3' : '#e3a400') : '#8a6cff'; x.fillRect(i * w + .5, c.height - v / n * (c.height - 6), Math.max(1, w - 1), v / n * (c.height - 6)); }); l.el.querySelector('.st').textContent = `${l.steps} steps`; }
  let place = 0;
  const go = () => { lanes(); place = 0; const tick = () => { const per = Math.max(1, Math.round(base.length / 15)); let alive = false; for (const l of L) { if (l.done) continue; alive = true; for (let s = 0; s < per; s++) { const r = l.g.next(); if (r.done) { l.done = true; l.hl = []; place++; l.el.querySelector('.fin').textContent = ['1st', '2nd', '3rd', '4th'][place - 1]; if (place === 1) l.el.classList.add('win'); break; } l.hl = r.value; l.steps++; } draw(l); } if (alive) raf = requestAnimationFrame(tick); }; raf = requestAnimationFrame(tick); };
  box.querySelector('.go').onclick = go; box.querySelector('.shuf').onclick = make; box.querySelector('.n').oninput = make; box.querySelector('.kind').onchange = make;
  make();
  return () => cancelAnimationFrame(raf);
}

/* ---------- maze ---------- */
function maze(box) {
  const R = 17, C = 31; let g, S = [8, 3], G = [8, 27], timer = 0, drawing = null;
  box.innerHTML = `<div class="ctrls"><button class="btn small" data-a="bfs">BFS</button><button class="btn small" data-a="dfs">DFS</button><button class="btn small" data-a="dij">Dijkstra</button><button class="btn small soft" data-a="astar">A* (smart)</button><button class="btn small ghost" data-a="clear">Clear</button><button class="btn small ghost" data-a="random">Random walls</button></div><div class="say" style="margin:10px 0">Click or drag on the grid to draw walls. Green is the start, red is the goal.</div><div class="maze" style="grid-template-columns:repeat(${C},1fr)"></div>`;
  const M = box.querySelector('.maze'), say = t => { box.querySelector('.say').innerHTML = t; };
  const reset = (walls = false) => { clearInterval(timer); g = Array.from({ length: R }, () => Array(C).fill(0)); if (walls) for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) if (Math.random() < .28) g[r][c] = 1; g[S[0]][S[1]] = g[G[0]][G[1]] = 0; M.innerHTML = ''; for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) { const d = document.createElement('div'); d.dataset.rc = r + ',' + c; M.appendChild(d); } paint(); };
  const cell = (r, c) => M.children[r * C + c];
  const paint = () => { for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) cell(r, c).className = g[r][c] ? 'wall' : ''; cell(...S).className = 'start'; cell(...G).className = 'goal'; };
  const toggle = e => { const d = e.target.closest('[data-rc]'); if (!d) return; const [r, c] = d.dataset.rc.split(',').map(Number); if ((r === S[0] && c === S[1]) || (r === G[0] && c === G[1])) return; if (drawing === null) drawing = g[r][c] ? 0 : 1; g[r][c] = drawing; d.className = drawing ? 'wall' : ''; };
  M.addEventListener('pointerdown', e => { drawing = null; clearInterval(timer); paint(); toggle(e); M.setPointerCapture?.(e.pointerId); });
  M.addEventListener('pointermove', e => { if (e.buttons) { const t = document.elementFromPoint(e.clientX, e.clientY); if (t && M.contains(t)) toggle({ target: t }); } });
  box.querySelector('.ctrls').onclick = e => {
    const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return;
    if (a === 'clear') return reset(); if (a === 'random') return reset(true);
    clearInterval(timer); paint();
    const key = (r, c) => r * C + c, prev = new Map([[key(...S), null]]), dist = new Map([[key(...S), 0]]);
    const h = (r, c) => Math.abs(r - G[0]) + Math.abs(c - G[1]);
    let front = [[...S]], seenN = 0;
    timer = setInterval(() => {
      for (let rep = 0; rep < 3; rep++) {
        if (!front.length) { clearInterval(timer); say(`No path! Explored ${seenN} cells.`); return; }
        let cur;
        if (a === 'bfs') cur = front.shift(); else if (a === 'dfs') cur = front.pop();
        else { let bi = 0; front.forEach((p, i) => { const f = q => dist.get(key(...q)) + (a === 'astar' ? h(...q) : 0); if (f(p) < f(front[bi])) bi = i; }); cur = front.splice(bi, 1)[0]; }
        const [r, c] = cur; seenN++;
        if (r === G[0] && c === G[1]) { clearInterval(timer); let k = prev.get(key(r, c)), len = 1; while (k !== null && k !== undefined && k !== key(...S)) { M.children[k].className = 'path'; k = prev.get(k); len++; } say(`${a.toUpperCase()} found a path of length <b>${len}</b> after exploring <b>${seenN}</b> cells. ${a === 'dfs' ? 'DFS paths are often long and twisty!' : a === 'astar' ? 'A* aims toward the goal, so it explores less.' : 'BFS/Dijkstra always find the shortest path.'}`); return; }
        if (!(r === S[0] && c === S[1])) cell(r, c).className = 'seen';
        for (const [dr, dc] of [[0, 1], [1, 0], [0, -1], [-1, 0]]) { const nr = r + dr, nc = c + dc; if (nr < 0 || nc < 0 || nr >= R || nc >= C || g[nr][nc] || prev.has(key(nr, nc))) continue; prev.set(key(nr, nc), key(r, c)); dist.set(key(nr, nc), dist.get(key(r, c)) + 1); front.push([nr, nc]); if (!(nr === G[0] && nc === G[1])) cell(nr, nc).className = 'front'; }
      }
      say(`${a.toUpperCase()} exploring… ${seenN} cells checked`);
    }, 30);
  };
  reset(true);
  return () => clearInterval(timer);
}

/* ---------- memo magic ---------- */
function fib(box) {
  box.innerHTML = `<div class="ctrls"><label class="tiny">n = <input class="n" type="range" min="1" max="25" value="10"></label><b class="nv">10</b></div><div class="stage" style="flex-direction:column;align-items:stretch;gap:14px"></div><div class="say"></div>`;
  const st = box.querySelector('.stage');
  const draw = () => {
    const n = +box.querySelector('.n').value; box.querySelector('.nv').textContent = n;
    let plain = 0; const f = k => { plain++; return k < 2 ? k : f(k - 1) + f(k - 2); }; const v = f(n);
    let memoCalls = 0; const memo = {}; const g = k => { memoCalls++; if (k in memo) return memo[k]; return (memo[k] = k < 2 ? k : g(k - 1) + g(k - 2)); }; g(n);
    const max = plain;
    st.innerHTML = [['Plain recursion', plain, 'var(--pinkD)'], ['With a memo', memoCalls, 'var(--mintD)']].map(([t, c, col]) => `<div style="display:grid;grid-template-columns:170px 1fr 90px;gap:10px;align-items:center;font-weight:800"><span>${t}</span><div class="bar"><i style="width:${Math.max(.5, c / max * 100)}%;background:${col}"></i></div><span class="mono">${c.toLocaleString()} calls</span></div>`).join('');
    box.querySelector('.say').innerHTML = `fib(${n}) = <b>${v}</b>. The memo version is <b>${Math.round(plain / memoCalls)}×</b> fewer calls. That's dynamic programming in one picture!`;
  };
  box.querySelector('.n').oninput = draw; draw();
}
