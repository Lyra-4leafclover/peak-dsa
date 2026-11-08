/* Poke-able mini toys for each data structure. Each takes a .playbox element. */
import { esc } from '../viz/values.js';
const rnd = n => Math.floor(Math.random() * n);
const wait = ms => new Promise(r => setTimeout(r, ms));
function shell(el, title, ctrls) {
  el.innerHTML = `<h3>🕹 Play with it: ${title}</h3><div class="ctrls">${ctrls}</div><div class="stage"></div><div class="say">Press a button above 👆</div>`;
  return [el.querySelector('.stage'), m => { el.querySelector('.say').innerHTML = m; }, s => el.querySelector(s)];
}
const num = (el, s, d) => { const v = parseInt(el.querySelector(s)?.value, 10); return Number.isNaN(v) ? d : v; };

const W = {
  array(el) {
    let a = [3, 1, 4, 1, 5], hi = -1, cls = {};
    const [stage, say] = shell(el, 'lockers', `<input class="v" value="7" aria-label="value"><input class="i" value="2" aria-label="index"><button class="btn small" data-a="read">Read [i]</button><button class="btn small soft" data-a="append">append(v)</button><button class="btn small soft" data-a="insert">insert(i, v)</button><button class="btn small ghost" data-a="pop">pop()</button><button class="btn small ghost" data-a="del">pop(i)</button>`);
    const draw = () => { stage.innerHTML = `<div class="w-row">${a.map((x, i) => `<div class="w-cell"><div class="w-lbl">${i === hi ? '👀' : ''}</div><div class="w-box ${cls[i] || ''}">${x}</div><div class="w-idx">${i}</div></div>`).join('') || '<i class="muted">empty list []</i>'}</div>`; };
    el.querySelector('.ctrls').onclick = async e => {
      const b = e.target.closest('[data-a]'); if (!b) return;
      const v = num(el, '.v', rnd(9)), i = num(el, '.i', 0); cls = {}; hi = -1;
      if (b.dataset.a === 'read') { if (i < 0 || i >= a.length) { say(`💥 IndexError: there is no locker ${i}. Valid lockers are 0 to ${a.length - 1}.`); return; } hi = i; cls[i] = 'hi'; say(`nums[${i}] is <b>${a[i]}</b>. We jumped straight there: <b>1 step</b>, O(1).`); }
      if (b.dataset.a === 'append') { a.push(v); cls[a.length - 1] = 'ok new'; say(`Added ${v} at the end. Nobody had to move: <b>O(1)</b>.`); }
      if (b.dataset.a === 'pop') { if (!a.length) return say('Empty! Nothing to pop.'); const x = a.pop(); say(`Removed ${x} from the end. <b>O(1)</b>.`); }
      if (b.dataset.a === 'insert' || b.dataset.a === 'del') {
        const ins = b.dataset.a === 'insert';
        const k = Math.max(0, Math.min(i, ins ? a.length : a.length - 1));
        if (!ins && !a.length) return say('Empty!');
        const moved = a.length - k - (ins ? 0 : 1);
        for (let j = k; j < a.length; j++) cls[j] = 'hi';
        draw(); say(`${moved} locker(s) must shift ${ins ? 'right' : 'left'} first… 🏃`); await wait(700);
        if (ins) a.splice(k, 0, v); else a.splice(k, 1);
        cls = {}; if (ins) cls[k] = 'ok new';
        say(`${ins ? `Inserted ${v} at ${k}` : `Removed locker ${k}`}. ${moved} item(s) shifted: that's <b>O(n)</b>.`);
      }
      draw();
    };
    draw();
  },
  stack(el) {
    let s = [2, 7];
    const [stage, say] = shell(el, 'pancake stack', `<input class="v" value="5"><button class="btn small" data-a="push">push(v)</button><button class="btn small soft" data-a="pop">pop()</button><button class="btn small ghost" data-a="peek">peek</button>`);
    const draw = () => { stage.innerHTML = `<div class="w-vstack">${s.map((x, i) => `<div class="w-plate ${i === s.length - 1 ? 'top' : ''}">${x}</div>`).join('')}</div>`; };
    el.querySelector('.ctrls').onclick = e => {
      const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return;
      if (a === 'push') { const v = num(el, '.v', rnd(9)); s.push(v); say(`Put pancake <b>${v}</b> on top.`); }
      if (a === 'pop') say(s.length ? `Ate pancake <b>${s.pop()}</b> from the top. Yum.` : '💥 Empty plate! Popping an empty stack crashes.');
      if (a === 'peek') say(s.length ? `The top pancake is <b>${s[s.length - 1]}</b> (we just looked).` : 'Nothing on the plate.');
      draw();
    };
    draw();
  },
  queue(el) {
    let q = ['🐱1', '🐶2'], n = 3;
    const [stage, say] = shell(el, 'boba line', `<button class="btn small" data-a="add">append (join back)</button><button class="btn small soft" data-a="serve">popleft (serve front)</button>`);
    const draw = () => { stage.innerHTML = `<div class="w-queue"><span class="qend">front →</span>${q.map((x, i) => `<div class="w-person ${i === 0 ? 'front' : ''}">${x}</div>`).join('') || '<i class="muted">nobody</i>'}<span class="qend">← back</span></div>`; };
    el.querySelector('.ctrls').onclick = e => {
      const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return;
      if (a === 'add') { const x = ['🐰', '🐸', '🐼', '🦊', '🐨'][rnd(5)] + n++; q.push(x); say(`${x} joined the BACK of the line.`); }
      if (a === 'serve') say(q.length ? `${q.shift()} was at the front and got their boba 🧋` : 'The line is empty!');
      draw();
    };
    draw();
  },
  linkedlist(el) {
    let L = [1, 2, 3], hi = -1;
    const [stage, say] = shell(el, 'train cars', `<input class="v" value="9"><button class="btn small" data-a="front">add at front</button><button class="btn small soft" data-a="back">add at back</button><button class="btn small soft" data-a="del">remove 2nd car</button><button class="btn small ghost" data-a="rev">reverse</button><button class="btn small ghost" data-a="walk">walk to the end</button>`);
    const draw = () => { stage.innerHTML = `<div class="w-row" style="align-items:center">${L.map((x, i) => `<div class="w-cell"><div class="w-lbl">${i === 0 ? 'head' : ''}</div><div class="w-box ${i === hi ? 'hi' : ''}">${x}</div></div><span style="font-weight:900">→</span>`).join('')}<span class="muted mono">None</span></div>`; };
    el.querySelector('.ctrls').onclick = async e => {
      const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return; const v = num(el, '.v', rnd(9)); hi = -1;
      if (a === 'front') { L.unshift(v); hi = 0; say('New car hooked on at the front. Just 1 hook changed: <b>O(1)</b>.'); }
      if (a === 'back' || a === 'walk') {
        for (let i = 0; i < L.length; i++) { hi = i; draw(); say(`walking… car ${i + 1}`); await wait(350); }
        if (a === 'back') { L.push(v); hi = L.length - 1; say(`We had to walk ${L.length - 1} cars to find the end: <b>O(n)</b>. Then hooked on ${v}.`); } else say(`Walked ${L.length} cars. No shortcuts in a train!`);
      }
      if (a === 'del') { if (L.length < 2) return say('Need at least 2 cars.'); const x = L.splice(1, 1)[0]; say(`Car ${x} removed: car 1's hook now points to car 3. <b>O(1)</b> once you're standing there.`); }
      if (a === 'rev') { L.reverse(); say('Every hook flipped direction. The old last car is the new head!'); }
      draw();
    };
    draw();
  },
  hashmap(el) {
    const N = 6; let B = Array.from({ length: N }, () => []), hi = -1;
    const h = k => [...k].reduce((s, c) => s + c.charCodeAt(0), 0) % N;
    const [stage, say] = shell(el, 'coat check', `<input class="k" value="apple" style="width:110px"><input class="v" value="3"><button class="btn small" data-a="put">d[key] = v</button><button class="btn small soft" data-a="get">d[key]</button><button class="btn small ghost" data-a="del">del d[key]</button>`);
    [['cat', 1], ['dog', 4]].forEach(([k, v]) => B[h(k)].push([k, v]));
    const draw = () => { stage.innerHTML = `<div class="bucket-grid">${B.map((b, i) => `<div class="bucket ${i === hi ? 'hi' : ''}"><div class="bn">bucket ${i}</div>${b.map(([k, v]) => `<span class="kvp">${esc(k)}: ${v}</span>`).join('')}</div>`).join('')}</div>`; };
    el.querySelector('.ctrls').onclick = e => {
      const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return;
      const k = el.querySelector('.k').value.trim() || 'x', v = num(el, '.v', 0), i = h(k); hi = i;
      const sum = [...k].reduce((s, c) => s + c.charCodeAt(0), 0);
      const pre = `hash("${esc(k)}") = letter codes add up to ${sum}, ${sum} % ${N} = <b>bucket ${i}</b>. `;
      const at = B[i].findIndex(p => p[0] === k);
      if (a === 'put') { if (at >= 0) B[i][at][1] = v; else B[i].push([k, v]); say(pre + (at >= 0 ? 'Key was already there, so we updated it.' : `Stored it there.${B[i].length > 1 ? ' (Two keys share a bucket: a "collision". They just sit together.)' : ''}`)); }
      if (a === 'get') say(pre + (at >= 0 ? `Found it: <b>${B[i][at][1]}</b>. No searching other buckets!` : '💥 KeyError: not in that bucket, so it\'s not stored anywhere.'));
      if (a === 'del') { if (at >= 0) B[i].splice(at, 1); say(pre + (at >= 0 ? 'Removed.' : 'Nothing to remove.')); }
      draw();
    };
    draw();
  },
  bst(el) {
    let root = null; let path = [], found = null;
    const ins = (n, v) => { if (!n) return { v, l: null, r: null }; if (v < n.v) n.l = ins(n.l, v); else if (v > n.v) n.r = ins(n.r, v); return n; };
    [50, 30, 70, 20, 40, 60, 80].forEach(v => { root = ins(root, v); });
    const [stage, say] = shell(el, 'higher or lower tree', `<input class="v" value="45"><button class="btn small" data-a="ins">insert</button><button class="btn small soft" data-a="find">search</button><button class="btn small ghost" data-a="in">inorder walk</button><button class="btn small ghost" data-a="clear">new tree</button>`);
    function draw(mark = {}) {
      const pos = []; let x = 0;
      const lay = (n, d) => { if (!n) return; lay(n.l, d + 1); pos.push([n, x++, d]); lay(n.r, d + 1); };
      lay(root, 0);
      const P = new Map(pos.map(([n, i, d]) => [n, [30 + i * 52, 30 + d * 62]]));
      const W2 = Math.max(200, x * 52 + 10), H = Math.max(...pos.map(p => p[2]), 0) * 62 + 60;
      let edges = '', nodes = '';
      for (const [n] of pos) for (const c of [n.l, n.r]) if (c) { const [a, b] = P.get(n), [cx, cy] = P.get(c); edges += `<line class="wedge ${mark[c.v] ? 'hi' : ''}" x1="${a}" y1="${b}" x2="${cx}" y2="${cy}"/>`; }
      for (const [n] of pos) { const [a, b] = P.get(n); nodes += `<g class="wnode ${mark[n.v] || ''}"><circle cx="${a}" cy="${b}" r="20"/><text x="${a}" y="${b + 5}">${n.v}</text></g>`; }
      stage.innerHTML = root ? `<svg class="wsvg" viewBox="0 0 ${W2} ${H}" width="${W2}">${edges}${nodes}</svg>` : '<i class="muted">empty tree</i>';
    }
    el.querySelector('.ctrls').onclick = async e => {
      const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return; const v = num(el, '.v', rnd(99));
      if (a === 'clear') { root = null; draw(); say('Fresh empty tree. Insert some numbers!'); return; }
      if (a === 'in') { const out = []; const go = n => { if (n) { go(n.l); out.push(n.v); go(n.r); } }; go(root); const mk = {}; for (const x of out) { mk[x] = 'ok'; draw(mk); say(`inorder: ${out.slice(0, out.indexOf(x) + 1).join(', ')}`); await wait(350); } say(`Inorder (left, me, right) gives <b>sorted order</b>: ${out.join(', ')} 🎉`); return; }
      let n = root, steps = 0; const mk = {};
      while (n) { mk[n.v] = 'cur'; draw(mk); steps++; if (v === n.v) break; say(`${v} ${v < n.v ? '<' : '>'} ${n.v}, so go ${v < n.v ? 'LEFT' : 'RIGHT'}`); await wait(550); mk[n.v] = 'hi'; n = v < n.v ? n.l : n.r; }
      if (a === 'find') { if (n) { mk[n.v] = 'ok'; say(`Found ${v} in ${steps} step(s)! We skipped most of the tree.`); } else say(`Fell off the tree after ${steps} step(s): ${v} isn't here.`); draw(mk); }
      else { if (n) say(`${v} is already in the tree.`); else { root = ins(root, v); mk[v] = 'ok'; say(`Found an empty spot after ${steps} step(s). ${v} lives there now 🌱`); } draw(mk); }
    };
    draw();
  },
  heap(el) {
    let h = [1, 3, 5, 4, 8];
    const [stage, say] = shell(el, 'throne heap (min-heap)', `<input class="v" value="2"><button class="btn small" data-a="push">heappush</button><button class="btn small soft" data-a="pop">heappop</button>`);
    function draw(mark = {}) {
      const n = h.length, depth = Math.floor(Math.log2(Math.max(1, n))), Wd = Math.max(240, 2 ** depth * 56);
      const pos = h.map((_, i) => { const d = Math.floor(Math.log2(i + 1)), k = i + 1 - 2 ** d; return [(k + .5) * Wd / 2 ** d, 30 + d * 60]; });
      let s = '';
      h.forEach((_, i) => { if (i) { const p = (i - 1) >> 1; s += `<line class="wedge" x1="${pos[p][0]}" y1="${pos[p][1]}" x2="${pos[i][0]}" y2="${pos[i][1]}"/>`; } });
      h.forEach((v, i) => { s += `<g class="wnode ${mark[i] || (i === 0 ? 'ok' : '')}"><circle cx="${pos[i][0]}" cy="${pos[i][1]}" r="20"/><text x="${pos[i][0]}" y="${pos[i][1] + 5}">${v}</text></g>`; });
      stage.innerHTML = `<div style="display:flex;flex-direction:column;align-items:center;gap:10px;width:100%">${n ? `<svg class="wsvg" viewBox="0 0 ${Wd} ${depth * 60 + 60}" width="${Wd}">${s}</svg>` : '<i class="muted">empty heap</i>'}<div class="w-row">${h.map((v, i) => `<div class="w-cell"><div class="w-box ${mark[i] || ''}">${v}</div><div class="w-idx">${i}</div></div>`).join('')}</div><div class="tiny muted">same heap stored as a list: kids of i live at 2i+1 and 2i+2</div></div>`;
    }
    const sw = (i, j) => { [h[i], h[j]] = [h[j], h[i]]; };
    el.querySelector('.ctrls').onclick = async e => {
      const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return;
      if (a === 'push') {
        h.push(num(el, '.v', rnd(20))); let i = h.length - 1; draw({ [i]: 'hi' }); say('Added at the bottom. Now it bubbles UP while smaller than its parent…'); await wait(600);
        while (i && h[i] < h[(i - 1) >> 1]) { const p = (i - 1) >> 1; sw(i, p); i = p; draw({ [i]: 'hi' }); await wait(600); }
        say('Settled! The smallest is still on the throne 👑'); draw({ [i]: 'ok' });
      } else {
        if (!h.length) return say('Empty heap!');
        const top = h[0]; const last = h.pop(); if (h.length) { h[0] = last; let i = 0; draw({ 0: 'hi' }); say(`Took ${top} off the throne. Moved the last item to the top; now it sinks DOWN…`); await wait(700);
          for (;;) { const l = 2 * i + 1, r = l + 1; let m = i; if (l < h.length && h[l] < h[m]) m = l; if (r < h.length && h[r] < h[m]) m = r; if (m === i) break; sw(i, m); i = m; draw({ [i]: 'hi' }); await wait(600); } }
        say(`Popped <b>${top}</b>. Only one path was fixed: O(log n).`); draw();
      }
    };
    draw();
  },
  graph(el) {
    const N = { A: [60, 40], B: [180, 30], C: [80, 150], D: [220, 130], E: [320, 60], F: [330, 170], G: [180, 220] };
    const E = [['A', 'B'], ['A', 'C'], ['B', 'D'], ['C', 'D'], ['B', 'E'], ['D', 'F'], ['E', 'F'], ['C', 'G'], ['G', 'F']];
    const adj = {}; for (const k in N) adj[k] = []; for (const [a, b] of E) { adj[a].push(b); adj[b].push(a); }
    const [stage, say] = shell(el, 'town map', `<button class="btn small" data-a="bfs">BFS from A (ripples)</button><button class="btn small soft" data-a="dfs">DFS from A (deep dive)</button>`);
    function draw(st = {}, he = {}) {
      stage.innerHTML = `<svg class="wsvg" viewBox="0 0 380 250" width="380">${E.map(([a, b]) => `<line class="wedge ${he[a + b] || he[b + a] ? 'hi' : ''}" x1="${N[a][0]}" y1="${N[a][1]}" x2="${N[b][0]}" y2="${N[b][1]}"/>`).join('')}${Object.entries(N).map(([k, [x, y]]) => `<g class="wnode ${st[k] || ''}"><circle cx="${x}" cy="${y}" r="20"/><text x="${x}" y="${y + 5}">${k}</text></g>`).join('')}</svg>`;
    }
    el.querySelector('.ctrls').onclick = async e => {
      const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return;
      const st = { A: 'hi' }, he = {}, seen = new Set(['A']), box = ['A'], order = [];
      while (box.length) {
        const u = a === 'bfs' ? box.shift() : box.pop();
        st[u] = 'cur'; order.push(u); draw(st, he);
        say(`${a === 'bfs' ? 'Queue' : 'Stack'}: [${box.join(', ')}] · visiting <b>${u}</b> · order so far: ${order.join(' → ')}`);
        await wait(800);
        for (const v of adj[u]) if (!seen.has(v)) { seen.add(v); box.push(v); st[v] = 'hi'; he[u + v] = 1; }
        st[u] = 'ok'; draw(st, he);
      }
      say(`Done! ${a === 'bfs' ? 'BFS' : 'DFS'} order: <b>${order.join(' → ')}</b>. ${a === 'bfs' ? 'Closest towns came first.' : 'It dove deep before coming back.'}`);
    };
    draw();
  },
  trie(el) {
    const root = {}; const add = w => { let n = root; for (const c of w) n = n[c] ??= {}; n.$ = 1; };
    ['cat', 'car', 'cart', 'dog', 'do'].forEach(add);
    const [stage, say] = shell(el, 'letter tree', `<input class="k" value="care" style="width:120px"><button class="btn small" data-a="add">insert</button><button class="btn small soft" data-a="find">search</button><button class="btn small ghost" data-a="pre">starts with?</button>`);
    function draw(hl = '') {
      const rows = []; const go = (n, pre, d) => { for (const c of Object.keys(n).filter(k => k !== '$').sort()) { rows.push([pre + c, d, !!n[c].$]); go(n[c], pre + c, d + 1); } };
      go(root, '', 0);
      stage.innerHTML = `<div style="font-family:var(--mono);font-weight:800;line-height:1.9;width:100%">${rows.map(([p, d, end]) => `<div style="padding-left:${d * 26}px">${'└ '}<span class="kvp" style="background:${hl && hl.startsWith(p) ? 'var(--butter)' : end ? 'var(--mint)' : 'var(--lav)'};border-radius:8px;padding:1px 8px">${p.at(-1)}</span>${end ? ' <span class="tiny muted">✔ "' + p + '"</span>' : ''}</div>`).join('')}</div>`;
    }
    el.querySelector('.ctrls').onclick = e => {
      const a = e.target.closest('[data-a]')?.dataset.a; if (!a) return; const w = el.querySelector('.k').value.trim().toLowerCase().replace(/[^a-z]/g, ''); if (!w) return;
      let n = root; let i = 0; for (; i < w.length && n; i++) n = n[w[i]];
      if (a === 'add') { add(w); say(`Inserted "${w}". Shared letters were reused, new ones were added. Green = a word ends here.`); }
      else if (a === 'find') say(n && n.$ ? `"${w}" is a word here ✅ (${w.length} steps)` : n ? `The path exists but no word ends at "${w}" ❌` : `Path breaks at letter ${i}: "${w}" is not here ❌`);
      else say(n ? `Yes! Some word starts with "${w}" ✅` : `No word starts with "${w}" ❌`);
      draw(w);
    };
    draw();
  },
  guess(el) {
    let secret, lo, hi, tries;
    const [stage, say] = shell(el, 'number guessing (1-100)', `<button class="btn small" data-a="new">New secret number</button><button class="btn small soft" data-a="bot">Let the computer binary-search</button>`);
    const draw = (mid) => { stage.innerHTML = `<div style="width:100%"><div style="display:flex;gap:2px;flex-wrap:wrap">${Array.from({ length: 100 }, (_, i) => i + 1).map(x => `<button class="w-box ${x === mid ? 'hi' : x < lo || x > hi ? 'dim' : ''}" data-g="${x}" style="min-width:30px;height:30px;font-size:.75rem;padding:0;cursor:pointer">${x}</button>`).join('')}</div></div>`; };
    const reset = () => { secret = 1 + rnd(100); lo = 1; hi = 100; tries = 0; draw(); say('I picked a number from 1 to 100. Click a number to guess! Smart move: always guess the middle.'); };
    stage.onclick = e => { const b = e.target.closest('[data-g]'); if (!b) return; const g = +b.dataset.g; tries++;
      if (g === secret) { say(`🎉 Got it in ${tries} tries! Binary search never needs more than 7 for 100 numbers.`); lo = hi = g; draw(g); return; }
      if (g < secret) lo = Math.max(lo, g + 1); else hi = Math.min(hi, g - 1); draw(g); say(`${g} is too ${g < secret ? 'LOW ⬆' : 'HIGH ⬇'}. The answer is between ${lo} and ${hi}. (try #${tries})`); };
    el.querySelector('.ctrls').onclick = async e => { const a = e.target.closest('[data-a]')?.dataset.a; if (a === 'new') reset(); if (a === 'bot') { lo = 1; hi = 100; tries = 0; while (lo <= hi) { const m = (lo + hi) >> 1; tries++; draw(m); if (m === secret) { say(`🤖 Found ${m} in ${tries} guesses by always picking the middle!`); return; } say(`🤖 guess ${m}: too ${m < secret ? 'low' : 'high'}`); if (m < secret) lo = m + 1; else hi = m - 1; await wait(700); } } };
    reset();
  },
  bars(el) {
    let a;
    const [stage, say] = shell(el, 'bubble sort penguins', `<button class="btn small" data-a="shuffle">Shuffle</button><button class="btn small soft" data-a="sort">Bubble sort it!</button>`);
    const draw = (m = {}) => { stage.innerHTML = `<div class="w-row" style="align-items:flex-end;height:150px">${a.map((x, i) => `<div class="w-cell"><div style="width:30px;height:${x * 12}px;border-radius:10px 10px 4px 4px;background:${m[i] === 'hi' ? 'var(--pinkD)' : m[i] === 'ok' ? 'var(--mintD)' : 'var(--lavD)'};transition:height .2s"></div><div class="w-idx">${x}</div></div>`).join('')}</div>`; };
    const shuffle = () => { a = Array.from({ length: 10 }, () => 1 + rnd(10)); draw(); say('Ten penguins of random heights.'); };
    el.querySelector('.ctrls').onclick = async e => { const k = e.target.closest('[data-a]')?.dataset.a; if (k === 'shuffle') shuffle(); if (k === 'sort') { let sw = 0; const done = {}; for (let end = a.length - 1; end > 0; end--) { for (let j = 0; j < end; j++) { draw({ ...done, [j]: 'hi', [j + 1]: 'hi' }); await wait(160); if (a[j] > a[j + 1]) { [a[j], a[j + 1]] = [a[j + 1], a[j]]; sw++; say(`swap! (${sw} swaps so far)`); } } done[end] = 'ok'; } done[0] = 'ok'; draw(done); say(`Sorted with ${sw} swaps. The tallest penguin "bubbled" to the end each pass.`); } };
    shuffle();
  },
  bigo(el) {
    const [stage, say] = shell(el, 'growth race', `<label class="tiny">n = <input class="v" type="range" min="1" max="64" value="16" style="width:180px"></label>`);
    const F = [['O(1)', () => 1, 'var(--mintD)'], ['O(log n)', n => Math.max(1, Math.log2(n)), 'var(--skyD)'], ['O(n)', n => n, 'var(--lavD)'], ['O(n log n)', n => n * Math.max(1, Math.log2(n)), 'var(--butterD)'], ['O(n²)', n => n * n, 'var(--pinkD)']];
    const draw = () => { const n = +el.querySelector('.v').value; const max = n * n; stage.innerHTML = `<div style="width:100%;display:flex;flex-direction:column;gap:8px">${F.map(([k, f, c]) => { const v = f(n); return `<div style="display:grid;grid-template-columns:90px 1fr 70px;gap:8px;align-items:center;font-weight:800"><span class="mono">${k}</span><div class="bar"><i style="width:${Math.max(1, v / max * 100)}%;background:${c}"></i></div><span class="mono">${Math.round(v)}</span></div>`; }).join('')}</div>`; say(`With n = ${n} items: O(n²) does <b>${n * n}</b> steps while O(log n) does about <b>${Math.max(1, Math.round(Math.log2(n)))}</b>. Slide n bigger!`); };
    el.querySelector('.v').oninput = draw; draw();
  },
};
export function mountWidget(el, id) { if (W[id]) { W[id](el); return true; } return false; }
