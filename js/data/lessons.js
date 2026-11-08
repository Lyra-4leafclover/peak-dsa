/* Learn content. Each lesson: a picture, an everyday analogy, the key moves (with cost),
   an interactive widget (ds only), a traced Python demo, and common mistakes. */
export const LESSONS = [
  {"id": "pybasics", "kind": "basics", "title": "Python basics for DSA", "art": "pybasics", "emoji": "", "analogy": "Python is like giving <b>step-by-step instructions to a very literal robot</b>. It reads one line at a time, top to bottom, and only does exactly what each line says.", "plain": ["A variable is a labelled box: `total = 0` puts 0 in a box called total. A list `[4, 8, 15]` holds many values in order.", "A `for` loop repeats its indented lines once per item. An `if` only runs its lines when the test is True. A function (`def`) is a reusable recipe: give it inputs, it hands back a result with `return`.", "On problem pages your code lives inside `class Solution:` with a method like `def twoSum(self, nums, target)`. `self` is just a required first word; ignore it for now."], "facts": [["x = 5", "make or change a variable", ""], ["nums = [1, 2, 3]", "a list (array)", ""], ["for x in nums:", "repeat once per item", ""], ["for i in range(n):", "repeat with i = 0, 1, ..., n-1", ""], ["if / elif / else", "choose what runs", ""], ["def f(a, b): return a + b", "a function", ""], ["len(nums)", "how many items", "O(1)"]], "demo": "name = \"Ada\"  #> a variable is a labelled box\nnums = [4, 8, 15]  #> a list holds many values in order\ntotal = 0\nfor x in nums:\n    total += x  #> the loop body runs once per item\ndef double(n):\n    return n * 2  #> a function: give it n, get back n * 2\nbig = double(total)\nif big > 50:\n    msg = \"big\"  #> if: only runs when the test is True\nelse:\n    msg = \"small\"\nprint(name, total, big, msg)", "mistakes": ["Indentation matters: the lines inside a loop or `if` must be pushed in by 4 spaces.", "`=` stores a value, `==` compares two values.", "`range(5)` gives 0 to 4, not 1 to 5.", "Forgetting `return`: the function then hands back None."], "topic": null, "widget": "pyloop", "practice": [1480, 1929, 58, 344, 9, 1672, 412]},
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
  {"id": "strings", "kind": "ds", "title": "Strings", "art": "strings", "emoji": "", "analogy": "A string is a <b>row of letter tiles</b>, like in Scrabble. Each tile has a position number, just like an array. But the tiles are glued down: to change one you make a new row.", "plain": ["`s[i]` reads one character, `s[a:b]` copies a slice, `len(s)` counts characters.", "Strings can not be changed in place (they are immutable). Build a list of pieces and `\"\".join(pieces)` at the end; adding with `+` in a loop is slow.", "Most string problems are really array problems: two pointers, sliding window, or counting letters with a dict."], "facts": [["s[i]", "read a character", "O(1)"], ["s[a:b]", "copy a slice", "O(b-a)"], ["\"\".join(parts)", "glue pieces together", "O(n)"], ["s + t", "makes a brand-new string", "O(n)"], ["ch in s", "search every character", "O(n)"], ["s.split()", "cut into words", "O(n)"]], "demo": "s = \"racecar\"\nchars = list(s)  #> a string is a row of characters, like a list\nl, r = 0, len(s) - 1\nok = True\nwhile l < r:\n    if s[l] != s[r]:  #> compare the two ends\n        ok = False\n        break\n    l += 1\n    r -= 1\ncounts = {}\nfor ch in s:\n    counts[ch] = counts.get(ch, 0) + 1\nword = \"\".join(reversed(chars))  #> build new strings with join\nprint(ok, counts, word)", "mistakes": ["Trying `s[0] = \"x\"`: strings can not be changed. Make a new one.", "Building a string with `+=` inside a loop (that is O(n²)).", "Forgetting upper vs lower case: use `.lower()` when the problem ignores case."], "topic": null, "widget": "strings", "practice": [344, 125, 14, 58, 242, 151, 5, 647]},
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
  {"id": "grid", "kind": "ds", "title": "Grids (2-D arrays)", "art": "grid", "emoji": "", "analogy": "A grid is a <b>chessboard or a spreadsheet</b>. Every square has a row number and a column number, and its neighbours are the squares directly up, down, left and right.", "plain": ["In Python a grid is a list of lists: `grid[r][c]` is row r, column c.", "Many grid problems are graph problems in disguise: each cell is a dot, and it is connected to its 4 neighbours. BFS or DFS then explores it.", "Always check the edges before stepping: `0 <= r < rows and 0 <= c < cols`."], "facts": [["grid[r][c]", "read a cell", "O(1)"], ["len(grid), len(grid[0])", "rows, columns", "O(1)"], ["[(1,0),(-1,0),(0,1),(0,-1)]", "the 4 directions", ""], ["flood fill / BFS", "visit a whole region", "O(rows·cols)"]], "demo": "grid = [\n    [1, 1, 0],\n    [0, 1, 0],\n    [1, 0, 1],\n]\nrows, cols = len(grid), len(grid[0])\nseen = set()\ndef fill(r, c):\n    if r < 0 or c < 0 or r >= rows or c >= cols:\n        return  #> fell off the edge\n    if grid[r][c] == 0 or (r, c) in seen:\n        return\n    seen.add((r, c))  #> mark this land cell\n    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:\n        fill(r + dr, c + dc)  #> visit up, down, left, right\nislands = 0\nfor r in range(rows):\n    for c in range(cols):\n        if grid[r][c] == 1 and (r, c) not in seen:\n            islands += 1  #> a new island\n            fill(r, c)\nprint(islands)", "mistakes": ["`[[0] * cols] * rows` copies the SAME row many times. Use `[[0] * cols for _ in range(rows)]`.", "Mixing up rows and columns (r goes down, c goes across).", "Forgetting to mark cells as seen, so the search loops forever."], "topic": null, "widget": "grid", "practice": [733, 200, 695, 463, 994, 54, 48, 73]},
  {"id": "unionfind", "kind": "ds", "title": "Union-Find (disjoint sets)", "art": "unionfind", "emoji": "", "analogy": "Union-Find is like <b>friend groups at a party</b>. Every group has one leader. To check if two people are in the same group, ask each \"who is your leader?\". To join two groups, one leader starts following the other.", "plain": ["`parent[x]` points to someone closer to the leader of x. `find(x)` follows the pointers up to the leader.", "`union(a, b)` finds both leaders; if they differ, one becomes the boss of the other.", "Use it when a problem keeps joining things and asking \"are these connected?\": friend circles, redundant edges, counting groups."], "facts": [["find(x)", "who is the leader?", "≈ O(1)"], ["union(a, b)", "merge two groups", "≈ O(1)"], ["find(a) == find(b)", "same group?", "≈ O(1)"]], "demo": "parent = list(range(6))  #> everyone starts as their own leader\ndef find(x):\n    while parent[x] != x:\n        parent[x] = parent[parent[x]]  #> shortcut: point closer to the leader\n        x = parent[x]\n    return x\ndef union(a, b):\n    ra, rb = find(a), find(b)\n    if ra == rb:\n        return False  #> already in the same group\n    parent[rb] = ra  #> merge the two groups\n    return True\nfor a, b in [(0, 1), (1, 2), (3, 4), (2, 0)]:\n    union(a, b)\ngroups = len({find(x) for x in range(6)})\nprint(groups, parent)", "mistakes": ["Setting `parent[a] = b` instead of joining the two LEADERS.", "Forgetting path compression, so long chains make find slow."], "topic": null, "widget": "unionfind", "practice": [547, 684, 323, 261, 128, 721]},
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
  {"id": "prefix", "kind": "algo", "title": "Prefix sums", "art": "prefix", "emoji": "", "analogy": "A prefix sum is like the <b>running total on a shopping receipt</b>. If you know the total after item 2 and after item 5, the cost of items 3 to 5 is just one subtraction.", "plain": ["Build `prefix` where `prefix[i]` is the sum of the first i numbers (`prefix[0] = 0`).", "Then the sum of `nums[l..r]` is `prefix[r + 1] - prefix[l]`, instantly, for any range.", "With a dict of earlier prefix sums you can count subarrays that add up to k in one pass."], "facts": [["build prefix", "one pass", "O(n)"], ["range sum", "prefix[r+1] - prefix[l]", "O(1)"], ["count sums with a dict", "seen[prefix - k]", "O(n)"]], "demo": "nums = [3, 1, 4, 1, 5, 9]\nprefix = [0]\nfor x in nums:\n    prefix.append(prefix[-1] + x)  #> running total so far\ndef range_sum(l, r):\n    return prefix[r + 1] - prefix[l]  #> any range in one subtraction\na = range_sum(1, 3)\nb = range_sum(0, 5)\nprint(prefix, a, b)", "mistakes": ["Off-by-one: prefix has n + 1 entries, and the range uses r + 1.", "Forgetting `seen[0] = 1` when counting subarrays that sum to k."], "topic": null, "widget": "prefix", "practice": [1480, 303, 724, 238, 560, 525, 304]},
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
  {"id": "intervals", "kind": "algo", "title": "Intervals", "art": "intervals", "emoji": "", "analogy": "Intervals are <b>meetings on a calendar</b>. Each has a start and an end. The big questions: which ones overlap, how to merge them, and how many rooms you need.", "plain": ["Step one is almost always: sort by start time.", "Two intervals [a, b] and [c, d] (sorted, so a <= c) overlap when c <= b. Then the merged block is [a, max(b, d)].", "For \"how many rooms\", sort starts and ends separately, or keep a min-heap of end times."], "facts": [["intervals.sort()", "sort by start", "O(n log n)"], ["c <= b", "do they overlap?", "O(1)"], ["[a, max(b, d)]", "merge two", "O(1)"], ["heap of end times", "rooms needed", "O(n log n)"]], "demo": "meetings = [[1, 3], [8, 10], [2, 6], [15, 18]]\nmeetings.sort()  #> sort by start time first\nmerged = [meetings[0]]\nfor start, end in meetings[1:]:\n    last = merged[-1]\n    if start <= last[1]:\n        last[1] = max(last[1], end)  #> overlaps: stretch the last block\n    else:\n        merged.append([start, end])  #> gap: start a new block\nprint(merged)", "mistakes": ["Forgetting to sort first.", "Using `last[1] = end` instead of `max(last[1], end)` (a short meeting inside a long one).", "Deciding whether touching ends ([1,2] and [2,3]) count as overlapping: read the problem."], "topic": "Intervals", "widget": "intervals", "practice": [252, 56, 57, 435, 253, 986]},
  {"id": "monostack", "kind": "algo", "title": "Monotonic stack", "art": "monostack", "emoji": "", "analogy": "Picture <b>people in a queue waiting to see over taller heads</b>. When a tall person arrives, everyone shorter in front of them gets their answer (\"someone taller came!\") and leaves. The ones left waiting are always in order.", "plain": ["A monotonic stack keeps its items in sorted order (always going down, or always going up).", "Before pushing a new item, pop everything it \"beats\". Each popped item just found its next greater (or smaller) element.", "Every item is pushed once and popped once, so the whole thing is O(n)."], "facts": [["while stack and top < x: pop", "resolve waiting items", "O(1) avg"], ["stack.append(i)", "store the index, not the value", "O(1)"], ["whole pass", "each item in and out once", "O(n)"]], "demo": "temps = [73, 74, 75, 71, 69, 72, 76]\nanswer = [0] * len(temps)\nstack = []  #> indexes of days still waiting for a warmer day\nfor i, t in enumerate(temps):\n    while stack and temps[stack[-1]] < t:\n        j = stack.pop()  #> day j just found a warmer day\n        answer[j] = i - j\n    stack.append(i)\nprint(answer)", "mistakes": ["Storing values when you need distances (store indexes).", "Using `if` instead of `while` when popping.", "Mixing up < and <= when equal values appear."], "topic": null, "widget": "monostack", "practice": [496, 739, 503, 901, 853, 84]},
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
  {"id": "topo", "kind": "algo", "title": "Topological sort", "art": "topo", "emoji": "", "analogy": "Topological sort is <b>planning your school classes</b>: you must take Maths 1 before Maths 2. It finds an order where every class comes after everything it depends on.", "plain": ["Count how many prerequisites each task still needs (\"in-degree\").", "Put every task that needs nothing into a queue. Take one, add it to the order, and lower the count of everything that depended on it. When a count hits 0, it joins the queue.", "If some tasks never reach 0, there is a cycle and no valid order exists."], "facts": [["in-degree count", "how many must come first", "O(V + E)"], ["queue of 0-need tasks", "ready to take", ""], ["len(order) < n", "there is a cycle", "O(1)"]], "demo": "from collections import deque\ncourses = 4\nprereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]\ngraph = {c: [] for c in range(courses)}\nneed = [0] * courses\nfor after, before in prereqs:\n    graph[before].append(after)\n    need[after] += 1  #> how many classes must come first\nq = deque([c for c in range(courses) if need[c] == 0])\norder = []\nwhile q:\n    c = q.popleft()  #> nothing blocks this class: take it\n    order.append(c)\n    for nxt in graph[c]:\n        need[nxt] -= 1\n        if need[nxt] == 0:\n            q.append(nxt)  #> all its prerequisites are done\nprint(order)", "mistakes": ["Drawing the edge the wrong way round (before → after).", "Forgetting to check for a cycle at the end."], "topic": null, "widget": "topo", "practice": [207, 210, 269, 310, 1462]},
  {"id": "dijkstra", "kind": "algo", "title": "Shortest paths (Dijkstra)", "art": "dijkstra", "emoji": "", "analogy": "Dijkstra is like <b>water spreading out from a town along roads of different lengths</b>. The water always reaches the nearest town next, so the first time it reaches a town, that is the shortest way there.", "plain": ["BFS finds shortest paths when every road has the same length. When roads have different lengths, use a min-heap instead of a queue.", "Pop the closest town, then try every road out of it: if it gives a shorter distance to a neighbour, save it and push it.", "Dijkstra needs roads with no negative lengths."], "facts": [["heapq.heappop(heap)", "closest unfinished town", "O(log n)"], ["if nd < dist[nxt]", "found a shorter road", "O(1)"], ["whole run", "with a heap", "O(E log V)"]], "demo": "import heapq\ngraph = {\n    \"A\": [(\"B\", 4), (\"C\", 1)],\n    \"B\": [(\"D\", 1)],\n    \"C\": [(\"B\", 2), (\"D\", 5)],\n    \"D\": [],\n}\ndist = {\"A\": 0}\nheap = [(0, \"A\")]\nwhile heap:\n    d, node = heapq.heappop(heap)  #> closest unfinished town\n    if d > dist[node]:\n        continue  #> an old, longer entry: skip it\n    for nxt, w in graph[node]:\n        nd = d + w\n        if nd < dist.get(nxt, float(\"inf\")):\n            dist[nxt] = nd  #> found a shorter road\n            heapq.heappush(heap, (nd, nxt))\nprint(dist)", "mistakes": ["Using a normal queue when roads have different lengths.", "Not skipping old heap entries (`if d > dist[node]: continue`).", "Using Dijkstra with negative road lengths."], "topic": null, "widget": "dijkstra", "practice": [743, 1631, 787, 1584, 778]},
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
  {"id": "dp2", "kind": "algo", "title": "2-D dynamic programming", "art": "dp2", "emoji": "", "analogy": "2-D DP is filling in a <b>times table</b>: each square is worked out from squares you already filled in, usually the one above and the one to the left.", "plain": ["Decide what `dp[i][j]` MEANS, for example \"number of ways to reach row i, column j\" or \"answer for the first i letters of a and first j letters of b\".", "Fill the first row and column (the easy edges), then fill the rest in order so every square you need is already done.", "Comparing two strings (LCS, edit distance) is the classic 2-D DP."], "facts": [["dp = [[0] * m for _ in range(n)]", "make the table", "O(n·m)"], ["dp[i][j] from dp[i-1][j], dp[i][j-1]", "fill from neighbours", "O(1) each"], ["answer", "usually dp[-1][-1]", ""]], "demo": "rows, cols = 3, 4\ndp = [[0] * cols for _ in range(rows)]\nfor r in range(rows):\n    for c in range(cols):\n        if r == 0 or c == 0:\n            dp[r][c] = 1  #> edges: only one straight way in\n        else:\n            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]  #> from above + from the left\nprint(dp[rows - 1][cols - 1])", "mistakes": ["Not writing down what dp[i][j] means before coding.", "Wrong table size (strings usually need len + 1).", "Filling in an order that uses squares not computed yet."], "topic": "2-D Dynamic Programming", "widget": "dp2", "practice": [62, 64, 1143, 72, 518, 97]},
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
  {"id": "bits", "kind": "algo", "title": "Bit tricks", "art": "bits", "emoji": "", "analogy": "Inside the computer every number is a <b>row of light switches</b>, each on (1) or off (0). Bit tricks flip and test those switches directly, which is super fast.", "plain": ["13 in binary is 1101: 8 + 4 + 0 + 1.", "`a & b` keeps switches on in BOTH, `a | b` in EITHER, `a ^ b` in exactly ONE. `x ^ x` is 0, so pairs cancel out.", "`x << 1` doubles, `x >> 1` halves, `x & 1` tells you odd or even, and `x & (x - 1)` turns off the lowest 1."], "facts": [["a & b", "AND", "O(1)"], ["a | b", "OR", "O(1)"], ["a ^ b", "XOR: different = 1", "O(1)"], ["x << k / x >> k", "times / divide by 2ᵏ", "O(1)"], ["x & (x - 1)", "drop the lowest 1", "O(1)"], ["bin(x)", "see the bits", ""]], "demo": "n = 13\nbinary = bin(n)  #> 13 is 1101 in binary\nones = 0\nx = n\nwhile x:\n    x &= x - 1  #> this trick deletes the lowest 1 bit\n    ones += 1\nis_odd = n & 1 == 1  #> the last bit tells odd or even\ndoubled = n << 1  #> shift left = times 2\nhalved = n >> 1  #> shift right = halve (rounding down)\na = 5 ^ 3 ^ 5  #> x ^ x cancels out\nprint(binary, ones, is_odd, doubled, halved, a)", "mistakes": ["Mixing up `^` (XOR) with \"to the power\" (that is `**`).", "Python ints never overflow, so problems about 32-bit numbers need a mask like `& 0xFFFFFFFF`."], "topic": "Math & Bits", "widget": "bits", "practice": [191, 338, 136, 268, 190, 371]},
];
export const lessonById = Object.fromEntries(LESSONS.map(l => [l.id, l]));
