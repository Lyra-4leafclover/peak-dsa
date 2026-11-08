import { store, LEVELS } from '../store.js';
import { PROBLEMS } from '../data/problems.js';
import { TOPICS } from '../data/topics.js';
import { esc } from '../viz/values.js';

const ALL_BADGES = ['First Solve 🐣', 'Ten Down 🔟', 'Half-Century 🏏', 'Hard Hitter 💪', 'Daily Doer 📅', 'Fortune Teller 🔮', 'Bug Squasher 🐛', 'Speed Demon ⚡', 'Big-O Brain 🧠', 'Mock Survivor 🎤', 'Lab Rat 🧪', 'Scholar 🎓'];
export function render(el) {
  const d = store.data(), lv = store.level();
  const pct = lv.next ? ((d.xp - lv.base) / (lv.next - lv.base) * 100) : 100;
  el.innerHTML = `<div class="wrap">
    <div class="phead"><img src="assets/art/mascot.webp" alt="" style="object-fit:contain;background:#fff"><div class="txt"><h1>Your progress</h1>
      <p>Level <b>${lv.name}</b> · ${d.xp} XP · 🔥 ${store.streak()} day streak</p>
      <div class="progress-strip"><div class="bar"><i style="width:${pct}%"></i></div><b>${lv.next ? `${lv.next - d.xp} XP to next level` : 'Max level!'}</b></div></div></div>
    <div class="grid g2">
      <div class="card"><h3>📊 Solved by topic</h3>${TOPICS.map(t => { const all = PROBLEMS.filter(p => p.topic === t[0]); const s = all.filter(p => store.isSolved(p.slug)).length; return `<div class="trow"><span>${t[2]} ${t[0]}</span><div class="bar"><i style="width:${s / all.length * 100}%"></i></div><b>${s}/${all.length}</b></div>`; }).join('')}</div>
      <div class="card"><h3>🏅 Badges</h3><div class="badges">${ALL_BADGES.map(b => `<div class="badge ${d.badges.includes(b) ? 'got' : ''}">${b}</div>`).join('')}</div>
        <h3 style="margin-top:20px">🪜 Levels</h3><div class="levels">${LEVELS.map(([x, n], i) => `<div class="${i <= lv.idx ? 'got' : ''}"><b>${n}</b><span>${x} XP</span></div>`).join('')}</div></div>
      <div class="card"><h3>🎤 Mock interview history</h3>${d.mocks.length ? `<table class="mt">${d.mocks.map(m => `<tr><td>${esc(m.date)}</td><td>${esc(m.kind)}</td><td><b>${esc(m.score)}</b></td></tr>`).join('')}</table>` : '<p class="muted">No mocks yet. <a href="#/mock">Try one!</a></p>'}</div>
      <div class="card"><h3>⚙️ Data</h3><p class="muted">Everything is saved only in this browser. Nothing is uploaded.</p><button class="btn ghost small reset">🗑 Reset all progress</button></div>
    </div></div>`;
  el.querySelector('.reset').onclick = () => { if (confirm('Really delete all XP, solves and saved code?')) store.reset(); };
}
