/* Learn content. Each lesson: a picture, an everyday analogy, the key moves (with cost),
   an interactive widget (ds only), a traced Python demo, and common mistakes. */
export const LESSONS = [
  { id: 'bigo', kind: 'algo', title: 'Big-O: how fast is fast?', art: 'bigo', emoji: '',
    analogy: 'Big-O is like asking <b>"if the pile of homework doubles, how much longer will it take?"</b> Some jobs take the same time no matter what (O(1)), some take twice as long (O(n)), and some explode (O(n²)).',
    plain: ['We don\'t count seconds (every computer is different). We count how the number of steps grows when the input gets bigger.', 'Drop the small stuff: 3n + 5 is just O(n). Only the fastest-growing part matters for big inputs.'],
    facts: [['O(1)', 'Same time always. Looking up locker #5.', 'instant'], ['O(log n)', 'Halve the problem each step. Binary search.', 'super fast'], ['O(n)', 'Look at every item once.', 'fine'], ['O(n log n)', 'Good sorting.', 'fine'], ['O(n²)', 'Every item vs every other item.', 'slow'], ['O(2ⁿ)', 'Every possible subset.', 'very slow']],
    demo: `n = 8
steps_linear = 0
for i in range(n):
    steps_linear += 1  #> one step per item: O(n)
steps_square = 0
for i in range(n):
    for j in range(n):
        steps_square += 1  #> n steps for EACH item: O(n²)
steps_log = 0
k = n
while k > 1:
    k //= 2  #> halving: O(log n)
    steps_log += 1
print(steps_linear, steps_square, steps_log)`,
    mistakes: ['Thinking O(2n) is different from O(n). It isn\'t: constants are dropped.', 'Forgetting that `x in list` is O(n) but `x in set` is O(1).', 'Hidden loops: slicing, `sorted()`, and string `+` in a loop all cost time.'], topic: null, widget: 'bigo' },
  { id: 'array', kind: 'ds', title: 'Arrays (Python lists)', art: 'array', emoji: '',
    analogy: 'An array is a <b>row of numbered lockers</b>. If you know the locker number, you walk straight to it. But squeezing a new locker into the middle means shoving every locker after it one step to the right.',
    plain: ['Items sit side by side in memory, numbered from 0.', 'Reading or changing `nums[i]` is instant. Adding to the END is (usually) instant. Inserting or deleting in the middle is slow because things shift.'],
    facts: [['nums[i]', 'read/write locker i', 'O(1)'], ['nums.append(x)', 'add to the end', 'O(1)'], ['nums.pop()', 'remove from the end', 'O(1)'], ['nums.insert(i, x)', 'squeeze in, everything shifts', 'O(n)'], ['nums.pop(0)', 'remove the front, everything shifts', 'O(n)'], ['x in nums', 'check every locker', 'O(n)']],
    demo: `nums = [3, 1, 4, 1, 5]
first = nums[0]  #> locker 0, instant
nums[2] = 9  #> change locker 2
nums.append(2)  #> add to the end
nums.insert(1, 7)  #> squeeze in: everything after shifts right
nums.pop(0)  #> remove the front: everything shifts left
total = 0
for x in nums:
    total += x  #> visit every locker once
print(total)`,
    mistakes: ['Off-by-one: the last index is len(nums) - 1, not len(nums).', 'Changing a list while looping over it.', '`b = a` does NOT copy: both names point to the same list. Use `a[:]`.'], topic: 'Arrays & Hashing', widget: 'array' },
  { id: 'hashmap', kind: 'ds', title: 'Hash maps (dict) & sets', art: 'hashmap', emoji: '',
    analogy: 'A hash map is a <b>coat check</b>. You hand over your coat and get ticket #42. Later, ticket #42 takes you straight to your coat. No searching through every coat!',
    plain: ['A "hash function" turns a key (like "apple") into a bucket number. Looking up a key jumps straight to its bucket.', 'A set is the same thing but with only keys (no values): perfect for "have I seen this?".'],
    facts: [['d[key] = v', 'store', 'O(1)'], ['d[key] / d.get(key)', 'look up', 'O(1)'], ['key in d', 'is it there?', 'O(1)'], ['del d[key]', 'remove', 'O(1)'], ['Counter(xs)', 'count everything', 'O(n)'], ['set().add(x)', 'remember x', 'O(1)']],
    demo: `words = ["cat", "dog", "cat", "bird", "dog", "cat"]
count = {}
for w in words:
    if w in count:  #> instant lookup!
        count[w] += 1
    else:
        count[w] = 1
seen = set()
for w in words:
    seen.add(w)  #> sets ignore repeats
print(count, len(seen))`,
    mistakes: ['Reading a missing key with d[key] crashes. Use d.get(key, 0) or defaultdict.', 'Lists can\'t be keys (they can change). Use tuples.', 'Dict order is insertion order, not sorted order.'], topic: 'Arrays & Hashing', widget: 'hashmap' },
  { id: 'stack', kind: 'ds', title: 'Stacks', art: 'stack', emoji: '',
    analogy: 'A stack is a <b>pile of pancakes</b>. You put new pancakes on top and you eat from the top. The last one in is the first one out (LIFO).',
    plain: ['In Python a list is a perfect stack: append() to push, pop() to take the top, stack[-1] to peek.', 'Use a stack whenever the most RECENT thing matters most: matching brackets, undo buttons, going back in a browser.'],
    facts: [['st.append(x)', 'push on top', 'O(1)'], ['st.pop()', 'take the top off', 'O(1)'], ['st[-1]', 'peek at the top', 'O(1)'], ['not st', 'is it empty?', 'O(1)']],
    demo: `stack = []
for ch in "(()[])":
    if ch in "([":
        stack.append(ch)  #> push an opener on the pile
    else:
        top = stack.pop()  #> take the most recent opener
print("balanced!" if not stack else "oops")`,
    mistakes: ['Popping an empty stack crashes: check `if stack:` first.', 'Using pop(0): that\'s a queue move and it\'s slow.'], topic: 'Stack', widget: 'stack' },
  { id: 'queue', kind: 'ds', title: 'Queues & deques', art: 'queue', emoji: '',
    analogy: 'A queue is the <b>line at a boba shop</b>. New people join at the back, the person at the front gets served first (FIFO: first in, first out).',
    plain: ['Use collections.deque: append() joins the back, popleft() serves the front, both instant.', 'Queues power Breadth-First Search: explore things in the order you discovered them.'],
    facts: [['q.append(x)', 'join the back', 'O(1)'], ['q.popleft()', 'serve the front', 'O(1)'], ['q[0]', 'peek at the front', 'O(1)'], ['q.appendleft(x)', 'cut in at the front (deque)', 'O(1)']],
    demo: `from collections import deque
line = deque()
for name in ["Ana", "Ben", "Cat"]:
    line.append(name)  #> join the back of the line
served = []
while line:
    served.append(line.popleft())  #> front person gets boba
print(served)`,
    mistakes: ['list.pop(0) is O(n). Use deque.popleft().', 'Mixing up stacks (newest first) and queues (oldest first).'], topic: 'Sliding Window', widget: 'queue' },
  { id: 'linkedlist', kind: 'ds', title: 'Linked lists', art: 'linkedlist', emoji: '',
    analogy: 'A linked list is a <b>toy train</b>. Each car holds a value and a hook to the next car. To reach car 5 you must walk from the engine through cars 1, 2, 3, 4.',
    plain: ['Each node has `.val` and `.next`. The last node\'s next is None.', 'Adding or removing a car is instant IF you\'re already standing next to it: just move hooks. But finding a car means walking.'],
    facts: [['node.next', 'go to the next car', 'O(1)'], ['find the k-th', 'walk k steps', 'O(k)'], ['insert after a node', 'rewire 2 hooks', 'O(1)'], ['dummy = ListNode(0)', 'fake front car trick', 'handy!']],
    demo: `class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

head = ListNode(1, ListNode(2, ListNode(3)))
head = ListNode(0, head)  #> new engine at the front: instant
cur = head
while cur.next:
    cur = cur.next  #> walk to the last car
cur.next = ListNode(4)  #> hook a new car on the end
head.next = head.next.next  #> unhook car 1`,
    mistakes: ['Losing the rest of the list: save `nxt = cur.next` before changing cur.next.', 'Forgetting the empty list (head is None).', 'Checking `cur.next.val` when cur.next might be None.'], topic: 'Linked List', widget: 'linkedlist' },
  { id: 'tree', kind: 'ds', title: 'Trees & binary search trees', art: 'tree', emoji: '',
    analogy: 'A tree is an <b>upside-down family tree</b>: one root at the top, each node has kids. In a <b>binary search tree</b>, smaller kids go left and bigger kids go right, like a "higher or lower?" game.',
    plain: ['Each node has `.val`, `.left`, `.right`. Nodes with no kids are leaves.', 'Most tree problems are recursion: solve it for the left kid, solve it for the right kid, combine.', 'Walk orders: preorder (me, L, R), inorder (L, me, R: sorted for a BST!), postorder (L, R, me), level order (floor by floor).'],
    facts: [['search a BST', 'go left or right each step', 'O(h)'], ['insert into a BST', 'search, then attach', 'O(h)'], ['visit every node', 'DFS or BFS', 'O(n)'], ['height h', 'balanced ≈ log n, worst = n', '']],
    demo: `class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def insert(node, v):
    if not node:
        return TreeNode(v)  #> empty spot: the new value lives here
    if v < node.val:
        node.left = insert(node.left, v)  #> smaller: go left
    else:
        node.right = insert(node.right, v)  #> bigger: go right
    return node

root = None
for v in [5, 3, 8, 1, 4]:
    root = insert(root, v)`,
    mistakes: ['Forgetting the base case `if not node: return ...`.', 'Checking a BST only against direct children.', 'Confusing depth (from the top) with height (from the bottom).'], topic: 'Trees', widget: 'bst' },
  { id: 'heap', kind: 'ds', title: 'Heaps (priority queues)', art: 'heap', emoji: '',
    analogy: 'A heap is a <b>hospital waiting room</b>: whoever is most urgent is seen first, no matter when they arrived. The smallest number always sits on the throne at the top.',
    plain: ['Python\'s heapq keeps a list arranged so heap[0] is always the smallest.', 'Pushing or popping only fixes one path from top to bottom, so it\'s O(log n).', 'Need the biggest instead? Push negative numbers.'],
    facts: [['heappush(h, x)', 'add, bubble up', 'O(log n)'], ['heappop(h)', 'remove smallest, sink down', 'O(log n)'], ['h[0]', 'peek smallest', 'O(1)'], ['heapify(list)', 'turn a list into a heap', 'O(n)']],
    demo: `from heapq import heappush, heappop
h = []
for x in [5, 3, 8, 1]:
    heappush(h, x)  #> smallest always ends up at h[0]
smallest = heappop(h)  #> take the throne-sitter
next_one = heappop(h)
print(smallest, next_one, h)`,
    mistakes: ['Expecting the heap list to be fully sorted (it isn\'t, only h[0] is guaranteed).', 'Pushing tuples with un-comparable parts: add a counter as a tie-breaker.'], topic: 'Heap', widget: 'heap' },
  { id: 'graph', kind: 'ds', title: 'Graphs, BFS & DFS', art: 'graph', emoji: '',
    analogy: 'A graph is a <b>map of towns and roads</b>. Towns are nodes, roads are edges. BFS explores like ripples in a pond (closest towns first). DFS explores like a maze runner (go deep, then back up).',
    plain: ['Store a graph as an adjacency list: a dict from each node to its neighbours.', 'BFS uses a queue and finds the fewest-steps path. DFS uses a stack (or recursion).', 'Always keep a `seen` set or you\'ll walk in circles forever.'],
    facts: [['BFS', 'queue, ripples outward', 'O(V+E)'], ['DFS', 'stack/recursion, go deep', 'O(V+E)'], ['Dijkstra', 'heap, cheapest paths', 'O(E log V)'], ['Topological sort', 'order with prerequisites', 'O(V+E)'], ['Union-Find', 'which group am I in?', '≈O(1)']],
    demo: `from collections import deque
roads = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
seen = {'A'}
q = deque(['A'])
visit = []
while q:
    town = q.popleft()  #> closest unexplored town
    visit.append(town)
    for nb in roads[town]:
        if nb not in seen:
            seen.add(nb)  #> mark it so we never queue it twice
            q.append(nb)
print(visit)`,
    mistakes: ['Marking visited when POPPING instead of when PUSHING (in BFS) leads to duplicates.', 'Forgetting disconnected parts: loop over every node as a start.'], topic: 'Graphs', widget: 'graph' },
  { id: 'trie', kind: 'ds', title: 'Tries (prefix trees)', art: 'trie', emoji: '',
    analogy: 'A trie is like the <b>index tabs in a dictionary</b>: first tab by first letter, then by second letter... Words that start the same share the same path.',
    plain: ['Each node is a dict of letter → child. A marker says "a word ends here".', 'Looking up a word or prefix takes as many steps as the word has letters, no matter how many words are stored.'],
    facts: [['insert(word)', 'walk/create letters', 'O(len)'], ['search(word)', 'walk, check end marker', 'O(len)'], ['startsWith(prefix)', 'just walk', 'O(len)']],
    demo: `root = {}
for word in ["cat", "car", "dog"]:
    node = root
    for ch in word:
        node = node.setdefault(ch, {})  #> walk down, creating as needed
    node['$'] = True  #> a word ends here
node = root
for ch in "ca":
    node = node[ch]
print(sorted(k for k in node))`,
    mistakes: ['Forgetting the end-of-word marker ("car" vs "ca").'], topic: 'Tries', widget: 'trie' },
  { id: 'twopointers', kind: 'algo', title: 'Two pointers', art: 'twopointers', emoji: '',
    analogy: 'Imagine a <b>bunny at one end of a bench and a frog at the other</b>, hopping toward each other. Each hop rules out one seat forever, so they meet after at most n hops.',
    plain: ['Works great on SORTED lists or when comparing both ends (palindromes).', 'Another flavour: a slow "writer" pointer and a fast "reader" pointer moving the same way.'],
    facts: [['opposite ends', 'pairs that sum to a target, palindromes', 'O(n)'], ['same direction', 'remove duplicates, move zeros', 'O(n)'], ['fast & slow', 'linked list middle / loops', 'O(n)']],
    demo: `nums = [1, 3, 4, 6, 8, 11]
target = 10
l, r = 0, len(nums) - 1
while l < r:
    s = nums[l] + nums[r]
    if s == target:
        break  #> found the pair!
    if s < target:
        l += 1  #> too small: left pointer hops right
    else:
        r -= 1  #> too big: right pointer hops left
print(nums[l], nums[r])`,
    mistakes: ['Using two pointers on unsorted data when the trick needs sorted data.', '`while l <= r` vs `while l < r`: think about whether l == r is a valid answer.'], topic: 'Two Pointers' },
  { id: 'window', kind: 'algo', title: 'Sliding window', art: 'window', emoji: '',
    analogy: 'A sliding window is a <b>magnifying frame sliding over candy jars</b>. Instead of recounting every jar each time, you add the jar that slides in and subtract the jar that slides out.',
    plain: ['Fixed window: size k, move both edges together.', 'Stretchy window: grow the right edge; when the window breaks a rule, shrink from the left.'],
    facts: [['fixed size k', 'add new, remove old', 'O(n)'], ['stretchy', 'grow right, shrink left while invalid', 'O(n)']],
    demo: `s = "abcabcbb"
inside = set()
l = 0
best = 0
for r in range(len(s)):
    while s[r] in inside:
        inside.remove(s[l])  #> repeat! shrink from the left
        l += 1
    inside.add(s[r])  #> grow on the right
    best = max(best, r - l + 1)
print(best)`,
    mistakes: ['Recomputing the whole window each step (that\'s O(n·k)).', 'Using `if` instead of `while` when shrinking.'], topic: 'Sliding Window' },
  { id: 'binarysearch', kind: 'algo', title: 'Binary search', art: 'binarysearch', emoji: '',
    analogy: 'Finding a word in a <b>paper dictionary</b>: open in the middle, see if your word is before or after, and throw away half the book. 1,000,000 pages need only about 20 flips!',
    plain: ['Needs sorted data (or any yes/no question that flips once from "no" to "yes").', 'Keep lo and hi. Look at mid. Throw away the half that can\'t contain the answer.'],
    facts: [['search sorted list', 'halve each step', 'O(log n)'], ['search the answer', 'smallest speed/size that works', 'O(log range)'], ['bisect_left', 'built-in helper', 'O(log n)']],
    demo: `nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2  #> peek at the middle
    if nums[mid] == target:
        break
    if nums[mid] < target:
        lo = mid + 1  #> throw away the left half
    else:
        hi = mid - 1  #> throw away the right half
print(mid)`,
    mistakes: ['Infinite loops from `lo = mid` when it should be `lo = mid + 1`.', 'Forgetting the data must be sorted.'], topic: 'Binary Search', widget: 'guess' },
  { id: 'sorting', kind: 'algo', title: 'Sorting', art: 'sorting', emoji: '',
    analogy: 'Sorting is <b>lining penguins up by height</b>. Bubble sort swaps neighbours until it\'s right. Merge sort splits the colony in half, sorts each half, then zips them together.',
    plain: ['Simple sorts (bubble, insertion, selection) are O(n²): fine for tiny lists.', 'Merge sort and quick sort are O(n log n). Python\'s sorted() uses Timsort, also O(n log n).', 'Try the Sorting Race lab to watch them compete!'],
    facts: [['bubble / insertion', 'swap neighbours / slide cards', 'O(n²)'], ['merge sort', 'split, sort halves, merge', 'O(n log n)'], ['quick sort', 'pivot, partition', 'O(n log n) avg'], ['sorted(xs, key=...)', 'Python built-in', 'O(n log n)']],
    demo: `nums = [5, 2, 4, 6, 1, 3]
for i in range(1, len(nums)):
    card = nums[i]  #> pick up the next card
    j = i - 1
    while j >= 0 and nums[j] > card:
        nums[j + 1] = nums[j]  #> slide bigger cards right
        j -= 1
    nums[j + 1] = card  #> drop the card in its spot
print(nums)`,
    mistakes: ['`nums.sort()` returns None! Use `sorted(nums)` if you need a new list.'], topic: 'Sorting', widget: 'bars' },
  { id: 'recursion', kind: 'algo', title: 'Recursion', art: 'recursion', emoji: '',
    analogy: 'Recursion is <b>Russian nesting dolls</b>. To open the big doll you open a smaller doll inside it... until you reach the tiny one that doesn\'t open (the base case). Then you close them back up in reverse.',
    plain: ['A function that calls itself on a SMALLER problem.', 'Every recursion needs a base case that stops it.', 'Watch the call stack in the visual: each call waits for the one it started.'],
    facts: [['base case', 'the smallest doll', 'required!'], ['recursive case', 'shrink the problem, call yourself', ''], ['call stack', 'Python remembers each waiting call', 'O(depth) memory']],
    demo: `def factorial(n):
    if n <= 1:
        return 1  #> base case: the tiny doll
    smaller = factorial(n - 1)  #> open the next doll and WAIT
    return n * smaller  #> close it back up

print(factorial(4))`,
    mistakes: ['No base case → RecursionError.', 'The problem doesn\'t get smaller each call.', 'Repeating work (fib) without a memo.'], topic: 'Trees' },
  { id: 'backtracking', kind: 'algo', title: 'Backtracking', art: 'backtracking', emoji: '',
    analogy: 'Backtracking is <b>exploring a hedge maze</b>: walk down a path, hit a dead end, step back to the last fork and try the next path. Leave breadcrumbs, then pick them back up.',
    plain: ['The pattern: choose → explore (recurse) → un-choose.', 'Used for "list ALL the ways" problems: subsets, permutations, puzzles like N-Queens and Sudoku.'],
    facts: [['choose', 'path.append(x)', ''], ['explore', 'recurse', ''], ['un-choose', 'path.pop()', ''], ['prune', 'stop early on dead ends', 'saves tons of time']],
    demo: `nums = [1, 2, 3]
path = []
bags = []
def go(i):
    if i == len(nums):
        bags.append(path[:])  #> a complete choice: save a copy
        return
    path.append(nums[i])  #> choose: take it
    go(i + 1)
    path.pop()  #> un-choose
    go(i + 1)  #> explore without it
go(0)
print(bags)`,
    mistakes: ['Saving `path` instead of `path[:]` (it changes later!).', 'Forgetting to undo the choice.'], topic: 'Backtracking' },
  { id: 'dp', kind: 'algo', title: 'Dynamic programming', art: 'dp', emoji: '',
    analogy: 'DP is <b>writing answers on sticky notes</b> as you climb stairs. "How many ways to reach step 10?" is easy if you already wrote down the answers for steps 9 and 8.',
    plain: ['Spot it: the big answer is built from answers to smaller versions of the same question, and those smaller ones repeat.', 'Top-down: recursion + memo dict. Bottom-up: fill a table from the smallest case up.', 'Recipe: 1) what does dp[i] mean? 2) how is it built from earlier ones? 3) what are the starting values?'],
    facts: [['memoization', 'recursion + saved answers', ''], ['tabulation', 'loop filling a table', ''], ['1-D', 'stairs, robber, coins', 'O(n)'], ['2-D', 'grids, two strings', 'O(m·n)']],
    demo: `n = 6
ways = [0] * (n + 1)
ways[0] = 1  #> 1 way to stand at the bottom
ways[1] = 1
for i in range(2, n + 1):
    ways[i] = ways[i - 1] + ways[i - 2]  #> came from 1 step or 2 steps below
print(ways[n])`,
    mistakes: ['Not defining what dp[i] MEANS before coding.', 'Wrong starting values.', 'Looping in the wrong order (using answers not computed yet).'], topic: '1-D Dynamic Programming' },
  { id: 'greedy', kind: 'algo', title: 'Greedy', art: 'greedy', emoji: '',
    analogy: 'Greedy is <b>grabbing the biggest cookie every time</b>. Sometimes that\'s the best plan overall (making change with normal coins), sometimes it\'s not (weird coins). Greedy works when a local best choice never hurts later.',
    plain: ['Usually: sort the items in a clever order, then make the obvious choice for each one.', 'Prove it (or test it!) before trusting it.'],
    facts: [['sort by end time', 'fit the most meetings', 'O(n log n)'], ['farthest reach', 'jump games', 'O(n)'], ['always best now', 'when no future regret is possible', '']],
    demo: `meetings = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]
meetings.sort(key=lambda m: m[1])  #> earliest ending first
end = -1
chosen = []
for s, e in meetings:
    if s >= end:
        chosen.append((s, e))  #> fits after the last one: grab it!
        end = e
print(chosen)`,
    mistakes: ['Assuming greedy works without checking a counter-example.'], topic: 'Greedy' },
];
export const lessonById = Object.fromEntries(LESSONS.map(l => [l.id, l]));
