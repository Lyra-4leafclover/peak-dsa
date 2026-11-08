# PeakDSA

A beginner-friendly website for learning data structures and algorithms, built around pictures and step-by-step Python execution.

## What's inside
- **Learn**: 19 visual lessons (arrays, hash maps, stacks, queues, linked lists, trees, heaps, graphs, tries, Big-O, two pointers, sliding window, binary search, sorting, recursion, backtracking, DP, greedy). Each has an analogy, an interactive toy, a traced Python demo and common mistakes.
- **Problems**: 349 classic interview problems with original plain-language descriptions, hints, tests and animated solutions. Write your own Python, run tests, and replay your own code.
- **Visualizer**: paste any Python (scripts, functions, LeetCode-style `class Solution`) and watch it run line by line with a live picture of every variable, list, dict, linked list, tree, graph and the call stack.
- **Speeds**: Snail, Walk, Run, Zoom, Manual, plus Predict mode (guess the next line).
- **Challenges**: daily problem, predict the output, Big-O quiz, bug hunt, 60-second speed round.
- **Mocks**: timed coding interviews with secret tests, and a concept round.
- **Labs**: sorting race, maze pathfinder (BFS/DFS/Dijkstra/A*), memoization, heap, BST, hash table, BFS vs DFS, binary search game, Big-O race.
- XP, levels, streaks and badges are saved in your browser (localStorage).

## Run it
It's a static site with no build step. Python runs in the browser via [Pyodide](https://pyodide.org) inside a Web Worker.

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

(Opening `index.html` straight from disk won't work because browsers block workers and module imports on `file://`.)

## Adding problems
Problems live in `tools/problems/p0*.py`. Each `P(...)` call has a story, trick, hints, a solution (lines can end with `#> note` to show a tip while that line runs), tests and complexity. Rebuild and validate them all with CPython:

```bash
python3 tools/build_problems.py   # writes js/data/problems.js
```

## Layout
- `js/engine/` Pyodide worker and the `sys.settrace` tracer
- `js/viz/` renderers, diffing, plain-English explanations, the step player
- `js/pages/` one module per route
- `js/learn/widgets.js` interactive data-structure toys
- `js/data/` lessons, quizzes, generated problems
- `js/ui/icons.js` flat Lucide icons (ISC) used for page art

Problem descriptions are original, written for this project. LeetCode numbers are only given as references.
