/* Visualize ANY Python: scripts, plain functions, LeetCode-style Solution classes, design classes. */
import * as py from '../engine/py.js';
import { createEditor, waitForCM } from '../ui/editor.js';
import { showTrace } from '../ui/theater.js';
import { pyStatus } from '../ui/pystatus.js';
import { splitNotes } from '../ui/code.js';
import { esc } from '../viz/values.js';
import { store } from '../store.js';

const PRESETS = [
  ['🫧 Bubble sort (script)', `nums = [5, 2, 8, 1, 9, 3]
for end in range(len(nums) - 1, 0, -1):
    for j in range(end):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
print(nums)
`],
  ['➕ Two Sum (LeetCode style)', `class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
`],
  ['🚂 Reverse a linked list', `class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        return prev
`],
  ['🌳 Tree depth (recursion)', `class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
`],
  ['🕸 BFS on a graph', `from collections import deque
graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D', 'E'], 'D': ['F'], 'E': ['F'], 'F': []}
seen = {'A'}
queue = deque(['A'])
order = []
while queue:
    node = queue.popleft()
    order.append(node)
    for nb in graph[node]:
        if nb not in seen:
            seen.add(nb)
            queue.append(nb)
print(order)
`],
  ['🪆 Fibonacci recursion', `def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(4))
`],
  ['🥞 Stack: matching brackets', `def balanced(s):
    stack = []
    pairs = {')': '(', ']': '['}
    for ch in s:
        if ch in '([':
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack

print(balanced("([()])"))
`],
  ['👑 Heap: top 3 smallest', `import heapq
nums = [9, 4, 7, 1, 8, 2]
heap = []
for x in nums:
    heapq.heappush(heap, x)
top3 = [heapq.heappop(heap) for _ in range(3)]
print(top3)
`],
];
const HINT = { ListNode: 'a list like [1, 2, 3] → we build the linked list for you', TreeNode: 'level order like [3, 9, 20, null, null, 15, 7]', graph: 'adjacency list like [[2, 4], [1, 3], [2, 4], [1, 3]]' };

export async function render(el) {
  el.innerHTML = `<div class="wrap">
    <div class="phead"><img src="assets/art/recursion.webp" alt=""><div class="txt"><h1>Code Visualizer</h1>
      <p>Paste <b>any</b> Python here: a little script, a function, or a whole LeetCode <code>class Solution</code>. Press Visualize and watch it run line by line, in the real order, with pictures. Add <code>#&gt; a note</code> at the end of a line to leave yourself a tip that pops up when that line runs.</p></div></div>
    <div class="card pg">
      <div class="row"><b>Try an example:</b><div class="presets">${PRESETS.map((p, i) => `<button class="chipbtn" data-p="${i}">${p[0]}</button>`).join('')}</div></div>
      <div class="ed"></div>
      <div class="inputs"></div>
      <div class="row"><button class="btn green viz">🎬 Visualize</button><span class="pys"></span></div>
    </div>
    <div class="pg-out"></div></div>`;
  const $ = s => el.querySelector(s);
  const offPy = pyStatus($('.pys'));
  await waitForCM();
  const ed = createEditor($('.ed'), store.get('pgcode', PRESETS[0][1]), { onChange: v => { store.set('pgcode', v); sig = null; }, minLines: 12 });
  let sig = null, player = null;
  $('.presets').onclick = e => { const b = e.target.closest('[data-p]'); if (b) { ed.set(PRESETS[+b.dataset.p][1]); sig = null; $('.inputs').innerHTML = ''; } };

  async function inspect() {
    const code = splitNotes(ed.get()).code;
    const s = await py.run('inspect', { code });
    if (s.error) { $('.inputs').innerHTML = `<div class="res-banner bad">💥 ${esc(s.error)}</div>`; return null; }
    if (s.mode === 'function') {
      const old = sig && sig.fn === s.fn ? [...el.querySelectorAll('[data-in]')].map(i => i.value) : [];
      $('.inputs').innerHTML = `<div class="inbox"><b>Inputs for <code>${esc(s.fn)}</code>:</b>${s.params.length ? '' : ' <span class="muted">(no inputs needed)</span>'}${s.params.map((p, i) => `<label><span>${esc(p.name)}${p.hint ? ` <i class="muted">: ${esc(p.hint)}</i>` : ''}</span><input data-in="${i}" placeholder="${esc(HINT[p.type] || 'e.g. [2, 7, 11, 15] or 9 or "abc"')}" value="${esc(old[i] ?? guess(p))}"></label>`).join('')}</div>`;
    } else if (s.mode === 'design') {
      $('.inputs').innerHTML = `<div class="inbox"><b>Calls on <code>${esc(s.cls)}</code>:</b><label><span>operations</span><input data-in="0" value='["${esc(s.cls)}"]'></label><label><span>arguments</span><input data-in="1" value="[[]]"></label></div>`;
    } else $('.inputs').innerHTML = '';
    sig = s;
    return s;
  }
  function guess(p) {
    if (p.type === 'ListNode') return '[1, 2, 3, 4]';
    if (p.type === 'TreeNode') return '[3, 9, 20, null, null, 15, 7]';
    if (p.type === 'graph') return '[[2, 4], [1, 3], [2, 4], [1, 3]]';
    if (/List\[List\[str/.test(p.hint)) return '[["1","1","0"],["0","1","0"]]';
    if (/List\[List/.test(p.hint)) return '[[1, 2], [3, 4]]';
    if (/List\[str/.test(p.hint)) return '["eat", "tea", "ate"]';
    if (/List/.test(p.hint)) return '[2, 7, 11, 15]';
    if (/str/.test(p.hint)) return '"hello"';
    if (/int|float/.test(p.hint)) return '9';
    if (/bool/.test(p.hint)) return 'True';
    return '';
  }
  $('.viz').onclick = async () => {
    const out = $('.pg-out');
    out.innerHTML = '<div class="loadbox"><span class="spinner"></span> Getting ready…</div>';
    let s = sig;
    try { if (!s) { s = await inspect(); if (!s) { out.innerHTML = ''; return; } if (s.mode !== 'script' && (s.params?.length || s.mode === 'design')) { out.innerHTML = '<div class="res-banner">👆 We found your function! Check the inputs above, then press Visualize again.</div>'; return; } } }
    catch (e) { out.innerHTML = `<div class="res-banner bad">😵 ${esc(e.message)}</div>`; return; }
    const { code, notes } = splitNotes(ed.get());
    const vals = [...el.querySelectorAll('[data-in]')].map(i => i.value);
    let payload;
    if (s.mode === 'script') payload = { mode: 'script' };
    else if (s.mode === 'design') { try { payload = { mode: 'design', args: [JSON.parse(vals[0]), JSON.parse(vals[1])] }; } catch { out.innerHTML = '<div class="res-banner bad">Operations and arguments must be JSON lists.</div>'; return; } }
    else payload = { mode: 'function', fn: s.fn, params: s.params.map(p => p.name), types: Object.fromEntries(s.params.filter(p => p.type).map(p => [p.name, p.type])), rawArgs: vals };
    player?.destroy?.();
    player = await showTrace(out, { code, notes, payload });
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
  return () => { offPy(); player?.destroy?.(); };
}
