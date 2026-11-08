import { PROBLEMS } from '../data/problems.js';
import { TOPICS } from '../data/topics.js';
import { store } from '../store.js';
import { warmup } from '../engine/py.js';

export function render(el) {
  warmup();
  const solved = Object.keys(store.data().solved).length;
  el.innerHTML = `
  <section class="hero"><div class="wrap">
    <div>
      <span class="tag bg-lav">🦉 Hi! I'm Hoot, your DSA buddy</span>
      <h1>Data structures & algorithms, <span>finally make sense.</span></h1>
      <p class="lead">No scary math. Every idea is a picture you can poke. Then watch real Python run <b>one line at a time</b>, in the exact order the computer reads it, with the picture changing right next to it.</p>
      <div class="cta"><a class="btn" href="#/learn">📚 Start learning</a><a class="btn ghost" href="#/problems">🧩 Solve problems</a><a class="btn soft" href="#/playground">🎬 Visualize any code</a></div>
      <div class="stats"><div><b>${PROBLEMS.length}</b>problems with animated solutions</div><div><b>${TOPICS.length}</b>topics</div><div><b>5</b>playback speeds</div>${solved ? `<div><b>${solved}</b>solved by you 🎉</div>` : ''}</div>
    </div>
    <div class="art"><img src="assets/art/hero.webp" alt="Hoot the owl standing on number blocks, with a tree, a linked list and a stack of pancakes around"></div>
  </div></section>

  <section class="section"><div class="wrap">
    <h2>How it works</h2><p class="muted">Three steps. That's it.</p>
    <div class="grid g3 steps3">
      <div class="feature bg-sky"><h3>See it 👀</h3><p>Every structure is a friendly picture: arrays are lockers, stacks are pancakes, queues are a boba line. Push buttons and watch them change.</p></div>
      <div class="feature bg-pink"><h3>Watch it run 🎬</h3><p>Code plays like a video. The current line glows, a sentence explains it in plain English, and the picture updates. Slow it down to 🐢 or step by hand.</p></div>
      <div class="feature bg-mint"><h3>Do it yourself ✏️</h3><p>Write Python right in your browser. Run tests, get hints, earn XP, and replay YOUR code to see exactly where it went wrong.</p></div>
    </div>
  </div></section>

  <section class="section"><div class="wrap">
    <h2>Pick your adventure</h2><p class="muted">Everything is free, and your progress saves in this browser.</p>
    <div class="grid g3">
      ${[['#/learn', 'tree', 'Learn', 'Visual lessons for every data structure and algorithm pattern, explained like you\'re five.'],
        ['#/problems', 'challenges', 'Problem Bank', `${PROBLEMS.length} classic interview problems with plain-word stories, hints and step-by-step animations.`],
        ['#/playground', 'recursion', 'Code Visualizer', 'Paste ANY Python (even a LeetCode solution) and watch it run line by line with pictures.'],
        ['#/labs', 'labs', 'Labs', 'Sorting races, maze path-finders, a BST builder, a hash table, Big-O race track and more.'],
        ['#/challenges', 'binarysearch', 'Challenges', 'Daily puzzles, predict-the-output, bug hunts, speed rounds and badges to collect.'],
        ['#/mock', 'mock', 'Mock Interviews', 'Timed interview simulations with secret tests, a quiz round, and a score card at the end.'],
      ].map(([h, a, t, d]) => `<a class="tile" href="${h}"><div class="art"><img src="assets/art/${a}.webp" alt="" loading="lazy"></div><div class="body"><h3>${t}</h3><p>${d}</p></div></a>`).join('')}
    </div>
  </div></section>

  <section class="section"><div class="wrap">
    <div class="card cta-card"><img src="assets/art/mascot.webp" alt=""><div><h2>Never coded before?</h2><p class="muted">Start with <b>Arrays</b> in Learn, then try <b>Spot the Twin</b>. Use 🐢 Snail speed and turn on 🔮 Predict mode to guess the next line. You'll be surprised how fast it clicks.</p>
    <div class="row"><a class="btn" href="#/learn/ds/array">Start with Arrays →</a><a class="btn ghost" href="#/problems/contains-duplicate">Try Spot the Twin</a></div></div></div>
  </div></section>`;
}
