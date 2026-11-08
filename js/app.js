/* Router + shell. Each page lives in js/pages/*.js and exports render(el, ...params). */
import { store } from './store.js';
import { hydrateIcons } from './ui/icons.js';
hydrateIcons();

const routes = {
  '': () => import('./pages/home.js'),
  roadmap: () => import('./pages/roadmap.js'),
  learn: () => import('./pages/learn.js'),
  problems: () => import('./pages/problems.js'),
  playground: () => import('./pages/playground.js'),
  challenges: () => import('./pages/challenges.js'),
  mock: () => import('./pages/mock.js'),
  labs: () => import('./pages/labs.js'),
  me: () => import('./pages/me.js'),
};
const app = document.getElementById('app');
let cleanup = null;

async function route() {
  const parts = location.hash.replace(/^#\/?/, '').split('?')[0].split('/').map(decodeURIComponent);
  const key = parts[0] in routes ? parts[0] : '';
  document.querySelectorAll('.navlinks a').forEach(a => a.classList.toggle('on', a.dataset.r === key));
  document.getElementById('navlinks').classList.remove('open');
  if (cleanup) { try { cleanup(); } catch {} cleanup = null; }
  try {
    const mod = await routes[key]();
    app.innerHTML = '';
    const r = await mod.render(app, ...parts.slice(1));
    if (typeof r === 'function') cleanup = r;
  } catch (e) {
    console.error(e);
    app.innerHTML = `<div class="wrap" style="padding:60px 20px"><h2>Oops, this page tripped over</h2><p class="muted">${String(e.message || e)}</p><a class="btn" href="#/">Go home</a></div>`;
  }
  window.scrollTo(0, 0);
}

export function toast(msg, ms = 2600) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = msg;
  document.getElementById('toasts').appendChild(t);
  setTimeout(() => t.remove(), ms);
}

function paintXP() {
  const lv = store.level();
  const pill = document.getElementById('xp-pill');
  pill.querySelector('.lv').textContent = `Lv ${lv.idx + 1}`;
  pill.querySelector('.xpn').textContent = `${store.data().xp} XP`;
  pill.title = `${lv.name} · streak ${store.streak()} day(s)`;
}
store.sub(paintXP);
paintXP();
window.addEventListener('xp', e => { if (e.detail.n >= 5) toast(`+${e.detail.n} XP`); });
window.addEventListener('badge', e => toast(`New badge: ${e.detail}`, 3500));
document.getElementById('burger').onclick = () => document.getElementById('navlinks').classList.toggle('open');
window.addEventListener('hashchange', route);
route();
