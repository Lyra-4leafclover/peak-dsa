/* Toys for the extra lessons (Python basics + intermediate patterns). Same shape as widgets.js. */
const rnd = n => Math.floor(Math.random() * n);
const wait = ms => new Promise(r => setTimeout(r, ms));
function shell(el, title, ctrls) {
  el.innerHTML = `<h3>Play with it: ${title}</h3><div class="ctrls">${ctrls}</div><div class="stage"></div><div class="say">Press a button above</div>`;
  return [el.querySelector('.stage'), m => { el.querySelector('.say').innerHTML = m; }];
}
const onAct = (el, f) => { el.querySelector('.ctrls').onclick = e => { const a = e.target.closest('[data-a]')?.dataset.a; if (a) f(a); }; };
const box = (v, cls = '', lbl = '', idx = '') => `<div class="w-cell"><div class="w-lbl">${lbl}</div><div class="w-box ${cls}">${v}</div><div class="w-idx">${idx}</div></div>`;
const row = items => `<div class="w-row" style="align-items:flex-start;flex-wrap:wrap;justify-content:center">${items.join('')}</div>`;
const vars = o => `<div class="w-vars">${Object.entries(o).map(([k, v]) => `<span><b>${k}</b> = ${v}</span>`).join('')}</div>`;
const col = (...parts) => `<div style="display:flex;flex-direction:column;gap:14px;align-items:center;width:100%">${parts.join('')}</div>`;

export const W2 = {
  pyloop(el) {
    const nums = [4, 8, 15, 16]; let i = -1, total = 0;
    const [stage, say] = shell(el, 'a for loop, one step at a time', `<button class="btn small" data-a="step">Run the next loop step</button><button class="btn small ghost" data-a="reset">Start over</button>`);
    const draw = () => { stage.innerHTML = col(row(nums.map((x, k) => box(x, k === i ? 'hi' : k < i ? 'ok' : '', k === i ? 'x' : '', k))), vars({ x: i >= 0 && i < nums.length ? nums[i] : '-', total })); };
    onAct(el, a => {
      if (a === 'reset') { i = -1; total = 0; say('total = 0. Ready to loop over the list.'); }
      if (a === 'step') { if (i + 1 >= nums.length) { say(`The loop is finished: no items left. total = <b>${total}</b>`); i = nums.length; } else { i++; total += nums[i]; say(`<code>for x in nums</code> gives x = <b>${nums[i]}</b>, then <code>total += x</code> makes total <b>${total}</b>.`); } }
      draw();
    });
    draw();
  },
  strings(el) {
    const [stage, say] = shell(el, 'letter tiles', `<input class="v" value="level" style="width:130px"><button class="btn small" data-a="pal">Palindrome? (two pointers)</button><button class="btn small soft" data-a="rev">Reverse</button><button class="btn small ghost" data-a="count">Count letters</button>`);
    const get = () => (el.querySelector('.v').value || 'level').slice(0, 14);
    const draw = (s, m = {}) => { stage.innerHTML = row([...s].map((ch, k) => box(ch === ' ' ? '·' : ch, m[k] || '', m['l' + k] || '', k))); };
    let busy = false;
    onAct(el, async a => {
      if (busy) return; const s = get();
      if (a === 'rev') { draw([...s].reverse().join('')); say(`Reversed: <b>${[...s].reverse().join('')}</b>. Strings can not change, so this is a NEW string.`); }
      if (a === 'count') { const c = {}; for (const ch of s) c[ch] = (c[ch] || 0) + 1; draw(s); say('Counts: ' + Object.entries(c).map(([k, v]) => `<b>${k}</b>:${v}`).join(', ')); }
      if (a === 'pal') { busy = true; let l = 0, r = s.length - 1, ok = true; while (l < r) { const same = s[l] === s[r]; draw(s, { [l]: same ? 'ok' : 'bad', [r]: same ? 'ok' : 'bad', ['l' + l]: 'l', ['l' + r]: 'r' }); say(`s[${l}] = "${s[l]}" vs s[${r}] = "${s[r]}": ${same ? 'same, move both inward' : 'different!'}`); await wait(700); if (!same) { ok = false; break; } l++; r--; } say(ok ? `<b>${s}</b> is a palindrome: it reads the same both ways.` : `<b>${s}</b> is not a palindrome.`); busy = false; }
    });
    draw(get());
  },
  grid(el) {
    const R = 5, C = 7; let g = Array.from({ length: R }, () => Array.from({ length: C }, () => +(Math.random() < .45))), color = {};
    const COLS = ['var(--mint)', 'var(--sky)', 'var(--peach)', 'var(--lav)', 'var(--pink)', 'var(--butter)'];
    const [stage, say] = shell(el, 'islands on a map', `<button class="btn small" data-a="count">Count islands (flood fill)</button><button class="btn small ghost" data-a="new">New map</button>`);
    const draw = () => { stage.innerHTML = `<div class="w-grid" style="grid-template-columns:repeat(${C},38px)">${g.map((rw, r) => rw.map((v, c) => `<button class="w-gcell" data-rc="${r},${c}" style="background:${color[r + ',' + c] || (v ? '#d9cfc0' : '#fff')}">${v}</button>`).join('')).join('')}</div>`; };
    stage.onclick = e => { const b = e.target.closest('[data-rc]'); if (!b) return; const [r, c] = b.dataset.rc.split(',').map(Number); g[r][c] ^= 1; color = {}; draw(); say(`Cell (${r}, ${c}) is now ${g[r][c] ? 'land' : 'water'}. Click cells to draw your own map.`); };
    let busy = false;
    onAct(el, async a => {
      if (busy) return;
      if (a === 'new') { g = g.map(rw => rw.map(() => +(Math.random() < .45))); color = {}; draw(); say('A new random map. 1 = land, 0 = water.'); }
      if (a === 'count') { busy = true; color = {}; let n = 0;
        for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) if (g[r][c] && !color[r + ',' + c]) { const col = COLS[n++ % COLS.length]; const st = [[r, c]];
          while (st.length) { const [y, x] = st.pop(); if (y < 0 || x < 0 || y >= R || x >= C || !g[y][x] || color[y + ',' + x]) continue; color[y + ',' + x] = col; draw(); say(`Island ${n}: painting (${y}, ${x}) and checking its 4 neighbours`); await wait(160); st.push([y + 1, x], [y - 1, x], [y, x + 1], [y, x - 1]); } }
        say(`Found <b>${n}</b> island${n === 1 ? '' : 's'}. Each colour was found by one flood fill.`); busy = false; }
    });
    draw();
  },
  unionfind(el) {
    const N = 8; let parent = [...Array(N).keys()];
    const find = x => { while (parent[x] !== x) x = parent[x]; return x; };
    const [stage, say] = shell(el, 'friend groups', `union(<input class="a" value="0">, <input class="b" value="1">)<button class="btn small" data-a="union">Join groups</button><button class="btn small soft" data-a="find">Same group?</button><button class="btn small ghost" data-a="reset">Reset</button>`);
    const COLS = ['var(--mint)', 'var(--sky)', 'var(--peach)', 'var(--lav)', 'var(--pink)', 'var(--butter)', '#e8f5c8', '#f3e0ff'];
    const draw = (hi = []) => { const groups = {}; for (let i = 0; i < N; i++) (groups[find(i)] ||= []).push(i);
      stage.innerHTML = col(`<div class="w-row" style="flex-wrap:wrap;justify-content:center;gap:12px">${Object.entries(groups).map(([root, m], gi) => `<div class="w-group" style="background:${COLS[gi % COLS.length]}"><div class="w-idx">leader ${root}</div><div class="w-row">${m.map(x => `<div class="w-box ${hi.includes(x) ? 'hi' : ''}" style="min-width:38px;height:38px">${x}</div>`).join('')}</div></div>`).join('')}</div>`, vars({ parent: '[' + parent.join(', ') + ']' })); };
    const ab = () => [Math.min(N - 1, Math.max(0, +el.querySelector('.a').value || 0)), Math.min(N - 1, Math.max(0, +el.querySelector('.b').value || 0))];
    onAct(el, a => { const [x, y] = ab();
      if (a === 'reset') { parent = [...Array(N).keys()]; draw(); say('Everyone is their own leader again.'); return; }
      const rx = find(x), ry = find(y);
      if (a === 'union') { if (rx === ry) say(`${x} and ${y} already share leader ${rx}. Nothing to do.`); else { parent[ry] = rx; say(`Leader ${ry} now follows leader ${rx}, so the two groups merged.`); } }
      if (a === 'find') say(`find(${x}) = ${rx}, find(${y}) = ${ry}: ${rx === ry ? '<b>same group</b>' : '<b>different groups</b>'}.`);
      draw([x, y]); });
    draw();
  },
  prefix(el) {
    const nums = Array.from({ length: 8 }, () => 1 + rnd(9)); const pre = [0]; nums.forEach(x => pre.push(pre[pre.length - 1] + x));
    const [stage, say] = shell(el, 'range sums in one subtraction', `sum of nums[<input class="l" value="2">..<input class="r" value="5">]<button class="btn small" data-a="sum">Work it out</button>`);
    const draw = (l = -1, r = -1) => { stage.innerHTML = col(`<div class="w-idx">nums</div>` + row(nums.map((x, k) => box(x, k >= l && k <= r ? 'hi' : '', '', k))), `<div class="w-idx">prefix (running total)</div>` + row(pre.map((x, k) => box(x, k === l || k === r + 1 ? 'ok' : '', k === l ? 'minus' : k === r + 1 ? 'take' : '', k)))); };
    onAct(el, () => { let l = +el.querySelector('.l').value || 0, r = +el.querySelector('.r').value || 0; l = Math.max(0, Math.min(7, l)); r = Math.max(l, Math.min(7, r)); draw(l, r); say(`prefix[${r + 1}] - prefix[${l}] = ${pre[r + 1]} - ${pre[l]} = <b>${pre[r + 1] - pre[l]}</b>. No adding up needed!`); });
    draw(); say('Pick a range and press the button.');
  },
  intervals(el) {
    let iv; const MAX = 24;
    const [stage, say] = shell(el, 'merge the meetings', `<button class="btn small" data-a="merge">Sort and merge</button><button class="btn small ghost" data-a="new">New meetings</button>`);
    const bar = ([s, e], c, lbl) => `<div class="w-track"><div class="w-iv" style="left:${s / MAX * 100}%;width:${Math.max(2, (e - s) / MAX * 100)}%;background:${c}">${lbl || `${s}-${e}`}</div></div>`;
    const draw = (list, merged = []) => { stage.innerHTML = `<div style="width:100%;display:flex;flex-direction:column;gap:6px">${list.map(x => bar(x, 'var(--sky)')).join('')}${merged.length ? '<div class="w-idx" style="margin-top:6px">merged</div>' + merged.map(x => bar(x, 'var(--mint)')).join('') : ''}</div>`; };
    const make = () => { iv = Array.from({ length: 6 }, () => { const s = rnd(20); return [s, Math.min(MAX, s + 1 + rnd(5))]; }); draw(iv); say('Six meetings. Some overlap. Press merge.'); };
    let busy = false;
    onAct(el, async a => { if (busy) return; if (a === 'new') return make(); busy = true;
      const s = iv.map(x => [...x]).sort((x, y) => x[0] - y[0]); draw(s); say('Step 1: sort by start time.'); await wait(900); const m = [];
      for (const x of s) { if (m.length && x[0] <= m[m.length - 1][1]) { m[m.length - 1][1] = Math.max(m[m.length - 1][1], x[1]); say(`${x[0]}-${x[1]} overlaps the last block, so stretch it.`); } else { m.push([...x]); say(`${x[0]}-${x[1]} starts after the last block ends: new block.`); } draw(s, m); await wait(800); }
      say(`Done: ${s.length} meetings became <b>${m.length}</b> blocks.`); busy = false; });
    make();
  },
  monostack(el) {
    let t, i, st, ans;
    const [stage, say] = shell(el, 'waiting for a warmer day', `<button class="btn small" data-a="step">Next day</button><button class="btn small ghost" data-a="new">New temperatures</button>`);
    const draw = () => { stage.innerHTML = col(`<div class="w-idx">temperatures</div>` + row(t.map((x, k) => box(x, k === i ? 'hi' : st.includes(k) ? '' : k < i ? 'ok' : 'dim', k === i ? 'today' : '', k))), `<div class="w-idx">answer (days to wait)</div>` + row(ans.map((x, k) => box(x, '', '', k))), `<div class="w-idx">stack (days still waiting)</div>` + row(st.length ? st.map(k => box(t[k], '', '', 'day ' + k)) : ['<i class="muted">empty</i>'])); };
    const make = () => { t = Array.from({ length: 8 }, () => 60 + rnd(20)); i = -1; st = []; ans = t.map(() => 0); draw(); say('Press Next day to walk through the list.'); };
    onAct(el, a => { if (a === 'new') return make(); if (i + 1 >= t.length) { say('All days done. Anyone left on the stack never got a warmer day (answer 0).'); return; }
      i++; const popped = []; while (st.length && t[st[st.length - 1]] < t[i]) { const j = st.pop(); ans[j] = i - j; popped.push(j); } st.push(i); draw();
      say(popped.length ? `${t[i]} is warmer than day${popped.length > 1 ? 's' : ''} ${popped.join(', ')}: they get popped with their answer. Then today waits on the stack.` : `${t[i]} is not warmer than the top of the stack, so today just waits on the stack.`); });
    make();
  },
  topo(el) {
    const names = ['Intro', 'Loops', 'Lists', 'Funcs', 'DSA', 'Mock']; const pre = [[1, 0], [2, 0], [3, 1], [4, 2], [4, 3], [5, 4]];
    let need, q, order;
    const [stage, say] = shell(el, 'planning your classes', `<button class="btn small" data-a="step">Take the next class</button><button class="btn small ghost" data-a="reset">Reset</button>`);
    const draw = () => { stage.innerHTML = col(row(names.map((n, k) => box(n, order.includes(k) ? 'ok' : q.includes(k) ? 'hi' : '', order.includes(k) ? 'done' : `needs ${need[k]}`, pre.filter(p => p[0] === k).map(p => 'after ' + names[p[1]]).join(', ') || 'no prereqs'))), vars({ ready: '[' + q.map(k => names[k]).join(', ') + ']', order: '[' + order.map(k => names[k]).join(', ') + ']' })); };
    const reset = () => { need = names.map((_, k) => pre.filter(p => p[0] === k).length); q = names.map((_, k) => k).filter(k => !need[k]); order = []; draw(); say('Classes that need nothing go into the "ready" queue.'); };
    onAct(el, a => { if (a === 'reset') return reset(); if (!q.length) { say(order.length === names.length ? 'Every class is planned in a valid order!' : 'Stuck: there must be a cycle.'); return; }
      const c = q.shift(); order.push(c); const freed = []; for (const [after, before] of pre) if (before === c) { need[after]--; if (!need[after]) { q.push(after); freed.push(names[after]); } }
      draw(); say(`Took <b>${names[c]}</b>.${freed.length ? ` Now ${freed.join(' and ')} ${freed.length > 1 ? 'are' : 'is'} ready.` : ''}`); });
    reset();
  },
  dijkstra(el) {
    const P = { A: [40, 90], B: [170, 30], C: [170, 150], D: [300, 90], E: [420, 90] };
    const E = [['A', 'B', 4], ['A', 'C', 1], ['C', 'B', 2], ['B', 'D', 1], ['C', 'D', 5], ['D', 'E', 3], ['B', 'E', 7]];
    let dist, done, heap;
    const [stage, say] = shell(el, 'shortest roads from A', `<button class="btn small" data-a="step">Visit the closest town</button><button class="btn small ghost" data-a="reset">Reset</button>`);
    const draw = (cur) => { stage.innerHTML = `<svg viewBox="0 0 460 200" style="width:100%;max-width:520px">${E.map(([a, b, w]) => { const [x1, y1] = P[a], [x2, y2] = P[b]; return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#d9cfc0" stroke-width="3"/><rect x="${(x1 + x2) / 2 - 11}" y="${(y1 + y2) / 2 - 11}" width="22" height="22" rx="6" fill="#fff" stroke="#efe3d1"/><text x="${(x1 + x2) / 2}" y="${(y1 + y2) / 2 + 5}" text-anchor="middle" font-size="13" font-weight="800">${w}</text>`; }).join('')}${Object.entries(P).map(([n, [x, y]]) => `<circle cx="${x}" cy="${y}" r="22" fill="${n === cur ? 'var(--lav)' : done.has(n) ? 'var(--mint)' : '#fff'}" stroke="${n === cur ? 'var(--lavD)' : '#d9cfc0'}" stroke-width="3"/><text x="${x}" y="${y + 5}" text-anchor="middle" font-weight="900">${n}</text><text x="${x}" y="${y + 40}" text-anchor="middle" font-size="12" fill="#5b5b72">${n in dist ? 'dist ' + dist[n] : 'dist ?'}</text>`).join('')}</svg>`; };
    const reset = () => { dist = { A: 0 }; done = new Set(); heap = [[0, 'A']]; draw(); say('Start at A with distance 0. Every other town is unknown.'); };
    onAct(el, a => { if (a === 'reset') return reset();
      heap.sort((x, y) => x[0] - y[0]); let top; while (heap.length && done.has((top = heap.shift())[1])) top = null;
      if (!top) { say('Every town is finished. These are the shortest distances from A.'); draw(); return; }
      const [d, n] = top; done.add(n); const better = [];
      for (const [a2, b2, w] of E) for (const [u, v] of [[a2, b2], [b2, a2]]) if (u === n && !done.has(v) && d + w < (dist[v] ?? Infinity)) { dist[v] = d + w; heap.push([d + w, v]); better.push(`${v} = ${d + w}`); }
      draw(n); say(`Closest unfinished town: <b>${n}</b> (distance ${d}). ${better.length ? 'Shorter roads found: ' + better.join(', ') + '.' : 'No shorter roads from here.'}`); });
    reset();
  },
  dp2(el) {
    const [stage, say] = shell(el, 'paths through a grid', `rows <input class="r" value="4"> cols <input class="c" value="5"><button class="btn small" data-a="fill">Fill the table</button>`);
    let busy = false;
    const draw = (R, C, dp, cur) => { stage.innerHTML = `<div class="w-grid" style="grid-template-columns:repeat(${C},44px)">${dp.map((rw, r) => rw.map((v, c) => `<div class="w-gcell" style="background:${r === cur?.[0] && c === cur?.[1] ? 'var(--lav)' : cur && ((r === cur[0] - 1 && c === cur[1]) || (r === cur[0] && c === cur[1] - 1)) ? 'var(--butter)' : v ? 'var(--mint)' : '#fff'}">${v || ''}</div>`).join('')).join('')}</div>`; };
    onAct(el, async () => { if (busy) return; busy = true; const R = Math.max(2, Math.min(6, +el.querySelector('.r').value || 4)), C = Math.max(2, Math.min(7, +el.querySelector('.c').value || 5)); const dp = Array.from({ length: R }, () => Array(C).fill(0));
      for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) { dp[r][c] = r === 0 || c === 0 ? 1 : dp[r - 1][c] + dp[r][c - 1]; draw(R, C, dp, [r, c]); say(r === 0 || c === 0 ? `dp[${r}][${c}] = 1: on the edge there is only one straight way.` : `dp[${r}][${c}] = above ${dp[r - 1][c]} + left ${dp[r][c - 1]} = <b>${dp[r][c]}</b>`); await wait(260); }
      draw(R, C, dp); say(`There are <b>${dp[R - 1][C - 1]}</b> ways to walk from the top-left to the bottom-right moving only right or down.`); busy = false; });
    draw(4, 5, Array.from({ length: 4 }, () => Array(5).fill(0))); say('Press Fill to build the table one square at a time.');
  },
  bits(el) {
    let a = 13, b = 6;
    const [stage, say] = shell(el, 'light switches', `B = <input class="b" value="6"><button class="btn small" data-a="and">A & B</button><button class="btn small" data-a="or">A | B</button><button class="btn small" data-a="xor">A ^ B</button><button class="btn small soft" data-a="shl">A << 1</button><button class="btn small soft" data-a="shr">A >> 1</button>`);
    const bitsOf = x => Array.from({ length: 8 }, (_, k) => (x >> (7 - k)) & 1);
    const line = (name, x, click) => `<div class="w-bitrow"><b class="mono">${name}</b>${bitsOf(x).map((v, k) => `<button class="w-bit ${v ? 'on' : ''}" ${click ? `data-bit="${7 - k}"` : 'disabled'}>${v}</button>`).join('')}<span class="mono">= ${x}</span></div>`;
    const draw = (res, op) => { stage.innerHTML = `<div style="display:flex;flex-direction:column;gap:8px;align-items:center"><div class="w-bitrow"><span></span>${[128, 64, 32, 16, 8, 4, 2, 1].map(v => `<span class="w-idx" style="width:34px;text-align:center">${v}</span>`).join('')}<span></span></div>${line('A', a, true)}${line('B', b)}${res !== undefined ? line(op, res) : ''}</div>`; };
    stage.onclick = e => { const t = e.target.closest('[data-bit]'); if (!t) return; a ^= 1 << +t.dataset.bit; draw(); say(`Flipped a switch. A is now <b>${a}</b> (${a.toString(2)} in binary).`); };
    onAct(el, op => { b = Math.max(0, Math.min(255, +el.querySelector('.b').value || 0)); const R = { and: [a & b, 'A&B', 'kept switches on in BOTH'], or: [a | b, 'A|B', 'kept switches on in EITHER'], xor: [a ^ b, 'A^B', 'kept switches on in exactly ONE'], shl: [(a << 1) & 255, 'A<<1', 'slid every switch left: times 2'], shr: [a >> 1, 'A>>1', 'slid every switch right: halve, rounding down'] }[op];
      draw(R[0], R[1]); say(`${R[1]} = <b>${R[0]}</b>: it ${R[2]}.`); });
    draw(); say('Click the switches of A to change it.');
  },
};
