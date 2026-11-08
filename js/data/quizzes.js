/* Original quiz content for Challenges and Mocks. Each: [question, code|null, options, correctIndex, why] */
export const PREDICT = [
  ['What gets printed?', 'a = [1, 2, 3]\nb = a\nb.append(4)\nprint(len(a))', ['3', '4', 'Error', '1'], 1, 'b = a does not copy. Both names point at the SAME list.'],
  ['What gets printed?', 'st = []\nfor x in [1, 2, 3]:\n    st.append(x)\nprint(st.pop(), st.pop())', ['1 2', '3 2', '2 3', '3 1'], 1, 'A stack hands back the newest first.'],
  ['What gets printed?', 'from collections import deque\nq = deque([1, 2, 3])\nq.append(4)\nprint(q.popleft())', ['4', '1', '3', '2'], 1, 'A queue serves the oldest (front) first.'],
  ['What gets printed?', 'd = {}\nfor ch in "banana":\n    d[ch] = d.get(ch, 0) + 1\nprint(d["a"])', ['1', '2', '3', '6'], 2, '"banana" has three a\'s.'],
  ['What gets printed?', 'def f(n):\n    if n == 0:\n        return 0\n    return n + f(n - 1)\nprint(f(4))', ['4', '10', '24', 'Error'], 1, '4 + 3 + 2 + 1 + 0 = 10.'],
  ['What gets printed?', 'nums = [5, 1, 4]\nx = nums.sort()\nprint(x)', ['[1, 4, 5]', 'None', '[5, 1, 4]', 'Error'], 1, 'list.sort() sorts in place and returns None.'],
  ['What gets printed?', 'from heapq import heappush, heappop\nh = []\nfor x in [7, 2, 9, 4]:\n    heappush(h, x)\nprint(heappop(h))', ['7', '9', '2', '4'], 2, 'A min-heap always pops the smallest.'],
  ['What gets printed?', 's = set([3, 1, 3, 2, 1])\nprint(len(s))', ['5', '3', '2', '1'], 1, 'Sets drop duplicates: {1, 2, 3}.'],
  ['What gets printed?', 'lo, hi = 0, 9\nsteps = 0\nwhile lo <= hi:\n    mid = (lo + hi) // 2\n    lo = mid + 1\n    steps += 1\nprint(steps)', ['10', '4', '3', '5'], 1, 'mid = 4, 7, 8, 9 → 4 steps. Halving is fast!'],
  ['What gets printed?', 'grid = [[0] * 2] * 2\ngrid[0][0] = 1\nprint(grid[1][0])', ['0', '1', 'Error', 'None'], 1, '[[0]*2]*2 repeats the SAME inner list. Use a list comprehension instead.'],
  ['What gets printed?', 'print(7 // 2, -7 // 2)', ['3 -3', '3 -4', '3.5 -3.5', '4 -3'], 1, '// rounds DOWN (toward minus infinity), so -3.5 → -4.'],
  ['What gets printed?', 'words = ["bb", "a", "ccc"]\nprint(sorted(words, key=len)[0])', ['bb', 'a', 'ccc', 'Error'], 1, 'Sorted by length, "a" comes first.'],
];
export const BIGO = [
  ['for x in nums:\n    print(x)', 'O(n)', 'One pass over n items.'],
  ['for x in nums:\n    for y in nums:\n        print(x, y)', 'O(n²)', 'n items, each paired with n items.'],
  ['while n > 1:\n    n //= 2', 'O(log n)', 'Halving each time.'],
  ['print(nums[0])', 'O(1)', 'Jumping to an index is instant.'],
  ['nums.sort()', 'O(n log n)', 'Good sorting is n log n.'],
  ['seen = set(nums)\nprint(5 in seen)', 'O(n)', 'Building the set is O(n); the lookup itself is O(1).'],
  ['for i in range(n):\n    j = 1\n    while j < n:\n        j *= 2', 'O(n log n)', 'n outer loops, each doing log n doublings.'],
  ['def f(n):\n    if n < 2: return n\n    return f(n-1) + f(n-2)', 'O(2ⁿ)', 'Each call makes two more calls.'],
  ['for i in range(n):\n    nums.pop(0)', 'O(n²)', 'pop(0) shifts everything: O(n) each time.'],
  ['for i in range(100):\n    print(i)', 'O(1)', '100 is a fixed number, it doesn\'t grow with the input.'],
];
export const BIGO_OPTS = ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 'O(n²)', 'O(2ⁿ)'];
export const CONCEPTS = [
  ['Which structure gives the most recently added item first?', null, ['Queue', 'Stack', 'Heap', 'Set'], 1, 'Stacks are Last-In-First-Out.'],
  ['Best structure to check "have I seen this before?" quickly?', null, ['List', 'Set', 'Stack', 'Linked list'], 1, 'Set lookups are O(1) on average.'],
  ['BFS on an unweighted graph finds…', null, ['The cheapest path with weights', 'The path with fewest edges', 'A random path', 'The longest path'], 1, 'BFS explores in rings, so the first time you reach a node uses the fewest edges.'],
  ['Inorder traversal of a BST gives values in…', null, ['Random order', 'Sorted order', 'Reverse insert order', 'Level order'], 1, 'Left, me, right = small to big.'],
  ['Binary search requires the data to be…', null, ['Unique', 'Sorted (or monotonic)', 'Positive', 'In a linked list'], 1, 'You must know which half to throw away.'],
  ['Which needs O(n) to get the k-th element?', null, ['Python list', 'Linked list', 'Array', 'Tuple'], 1, 'You have to walk the train car by car.'],
  ['heapq in Python is a…', null, ['Max-heap', 'Min-heap', 'Sorted list', 'Binary search tree'], 1, 'heap[0] is always the smallest. Push negatives for a max-heap.'],
  ['Dynamic programming helps when subproblems…', null, ['Never repeat', 'Overlap / repeat', 'Are random', 'Are sorted'], 1, 'Save repeated answers instead of recomputing.'],
  ['Which pattern fits "longest substring without repeats"?', null, ['Sliding window', 'Binary search', 'Heap', 'Union-Find'], 0, 'Grow the right edge, shrink the left when a repeat appears.'],
  ['Detect a cycle in a linked list with O(1) memory using…', null, ['A hash set', 'Fast & slow pointers', 'Sorting', 'BFS'], 1, 'The hare laps the tortoise if there is a loop.'],
  ['Topological sort works on…', null, ['Any graph', 'Directed graphs with no cycles', 'Trees only', 'Undirected graphs'], 1, 'A cycle means there is no valid order.'],
  ['Backtracking pattern is…', null, ['Sort then scan', 'Choose → explore → un-choose', 'Divide in half', 'Count with a dict'], 1, 'Try, recurse, undo.'],
  ['Average lookup time in a hash map?', null, ['O(1)', 'O(log n)', 'O(n)', 'O(n²)'], 0, 'The hash jumps straight to the bucket.'],
  ['Merge sort\'s time complexity?', null, ['O(n)', 'O(n log n)', 'O(n²)', 'O(log n)'], 1, 'log n levels of splitting, O(n) merging per level.'],
  ['Union-Find is great for…', null, ['Shortest paths', 'Which group is this node in?', 'Sorting', 'Prefix search'], 1, 'It merges and finds groups almost instantly.'],
  ['Dijkstra fails with…', null, ['Big graphs', 'Negative edge weights', 'Cycles', 'Undirected edges'], 1, 'It assumes a finished node can never get cheaper.'],
];
/* Bug hunts reuse a problem's tests. Each code has exactly one small bug. */
export const BUGS = [
  ['binary-search', 'The search never finds the last element sometimes…', `class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
`],
  ['reverse-linked-list', 'This loses most of the train!', `class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        cur = head
        while cur:
            cur.next = prev
            prev = cur
            cur = cur.next
        return prev
`],
  ['two-sum', 'Sometimes it pairs a number with itself.', `class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        where = {}
        for i, x in enumerate(nums):
            where[x] = i
            if target - x in where:
                return [where[target - x], i]
        return []
`],
  ['valid-parentheses', 'Something is off with leftovers…', `class Solution:
    def isValid(self, s: str) -> bool:
        pair = {')': '(', ']': '[', '}': '{'}
        stack = []
        for ch in s:
            if ch in pair:
                if not stack or stack[-1] != pair[ch]:
                    return False
                stack.pop()
            else:
                stack.append(ch)
        return True
`],
  ['max-depth', 'The tree seems one floor too short.', `class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right))
`],
  ['climbing-stairs', 'Counts are a little wrong.', `class Solution:
    def climbStairs(self, n: int) -> int:
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a + b
        return b
`],
  ['best-time-stock', 'It thinks you can sell before buying!', `class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        return max(prices) - min(prices)
`],
  ['number-of-islands', 'It counts way too many islands.', `class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        R, C = len(grid), len(grid[0])
        def sink(r, c):
            if r < 0 or c < 0 or r >= R or c >= C or grid[r][c] != '1':
                return
            sink(r + 1, c); sink(r - 1, c); sink(r, c + 1); sink(r, c - 1)
        count = 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == '1':
                    count += 1
                    grid[r][c] = '0'
        return count
`],
];
