/* Progress lives in this browser (localStorage): XP, solved problems, streaks, badges. */
const KEY = 'peakdsa.v1';
let data;
try { data = JSON.parse(localStorage.getItem(KEY)) || {}; } catch { data = {}; }
data.xp ??= 0; data.solved ??= {}; data.code ??= {}; data.days ??= []; data.badges ??= []; data.prefs ??= {}; data.mocks ??= []; data.done ??= {};
const subs = new Set();
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(data)); } catch {} subs.forEach(f => f(data)); };
const today = () => new Date().toISOString().slice(0, 10);

export const LEVELS = [
  [0, 'Seedling'], [50, 'Sprout'], [150, 'Pointer Pal'], [300, 'Loop Legend'], [500, 'Hash Hero'],
  [800, 'Tree Climber'], [1200, 'Graph Guru'], [1800, 'DP Wizard'], [2600, 'Algo Royalty'], [4000, 'PEAK'],
];

export const store = {
  data: () => data,
  get: (k, d) => (k in data.prefs ? data.prefs[k] : d),
  set: (k, v) => { data.prefs[k] = v; save(); },
  sub: f => (subs.add(f), () => subs.delete(f)),
  addXP(n, why) {
    data.xp += n;
    const t = today();
    if (!data.days.includes(t)) data.days.push(t);
    save();
    window.dispatchEvent(new CustomEvent('xp', { detail: { n, why } }));
  },
  level() {
    let i = 0;
    while (i + 1 < LEVELS.length && data.xp >= LEVELS[i + 1][0]) i++;
    const next = LEVELS[i + 1];
    return { name: LEVELS[i][1], idx: i, next: next ? next[0] : null, base: LEVELS[i][0] };
  },
  streak() {
    const set = new Set(data.days);
    let n = 0;
    const d = new Date();
    if (!set.has(d.toISOString().slice(0, 10))) d.setDate(d.getDate() - 1);
    while (set.has(d.toISOString().slice(0, 10))) { n++; d.setDate(d.getDate() - 1); }
    return n;
  },
  solve(id, xp) {
    const first = !data.solved[id];
    data.solved[id] = data.solved[id] || today();
    save();
    if (first) store.addXP(xp, 'solve');
    return first;
  },
  isSolved: id => !!data.solved[id],
  saveCode(id, code) { data.code[id] = code; save(); },
  code: id => data.code[id],
  mark(key) { const first = !data.done[key]; data.done[key] = today(); save(); return first; },
  isDone: k => !!data.done[k],
  addMock(m) { data.mocks.unshift(m); data.mocks = data.mocks.slice(0, 30); save(); },
  badge(id) { if (!data.badges.includes(id)) { data.badges.push(id); save(); window.dispatchEvent(new CustomEvent('badge', { detail: id })); } },
  reset() { localStorage.removeItem(KEY); location.reload(); },
};
