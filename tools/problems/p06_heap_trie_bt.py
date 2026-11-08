from pb import P
H, TR, BT = 'Heap', 'Tries', 'Backtracking'

P('kth-largest-stream', 'K-th Biggest, Live', 703, 'Easy', H,
  "Numbers keep arriving. After each one, report the k-th biggest so far.",
  "Keep a min-heap of only the k biggest. Its top (smallest of them) is the k-th biggest.",
  ["Heap bigger than k? Pop the smallest.", "heapq is a min-heap."],
  '''
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.h = []
        for x in nums:
            self.add(x)

    def add(self, val: int) -> int:
        heappush(self.h, val)
        if len(self.h) > self.k:
            heappop(self.h)  #> too many: drop the smallest
        return self.h[0]  #> the k-th biggest
''', [([["KthLargest", "add", "add", "add", "add", "add"], [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]], [None, 4, 5, 5, 8, 8])], 'O(log k)', 'O(k)', mode='design')

P('last-stone-weight', 'Smashing Stones', 1046, 'Easy', H,
  "Repeatedly smash the two heaviest stones. Equal? Both vanish. Different? The leftover weight goes back. What's left at the end?",
  "A max-heap gives you the two heaviest instantly. Python trick: store negatives in heapq.",
  ["-x turns a min-heap into a max-heap.", "Return 0 if nothing is left."],
  '''
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        h = [-s for s in stones]  #> negatives = max-heap
        heapify(h)
        while len(h) > 1:
            a = -heappop(h)  #> heaviest
            b = -heappop(h)  #> second heaviest
            if a != b:
                heappush(h, -(a - b))
        return -h[0] if h else 0
''', [([[2, 7, 4, 1, 8, 1]], 1), ([[1]], 1), ([[3, 3]], 0)], 'O(n log n)', 'O(n)')

P('k-closest-points', 'K Closest to Home', 973, 'Medium', H,
  "Return the k points closest to (0, 0).",
  "Distance² = x² + y². Keep a max-heap of size k so the farthest of your k is easy to kick out.",
  ["No need for square roots: compare x²+y².", "Or just heapq.nsmallest."],
  '''
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        h = []
        for x, y in points:
            d = x * x + y * y
            heappush(h, (-d, x, y))  #> max-heap by distance
            if len(h) > k:
                heappop(h)  #> kick out the farthest
        return [[x, y] for _, x, y in h]
''', [([[[1, 3], [-2, 2]], 1], [[-2, 2]]), ([[[3, 3], [5, -1], [-2, 4]], 2], [[3, 3], [-2, 4]])], 'O(n log k)', 'O(k)', cmp='deep')

P('kth-largest-array', 'K-th Biggest in a List', 215, 'Medium', H,
  "Find the k-th largest number in a list (not k-th different).",
  "Min-heap of size k: after scanning everything, the top is the answer.",
  ["Sorting works too, but the heap is O(n log k).", "Quickselect is another fun way."],
  '''
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        h = []
        for x in nums:
            heappush(h, x)
            if len(h) > k:
                heappop(h)  #> keep only the k biggest
        return h[0]
''', [([[3, 2, 1, 5, 6, 4], 2], 5), ([[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], 4)], 'O(n log k)', 'O(k)')

P('task-scheduler', 'Task Scheduler With Cool-Down', 621, 'Medium', H,
  "Tasks are letters. The same task needs n idle slots between repeats. Fewest time slots to finish everything?",
  "Always run the task with the most copies left. Tasks cooling down wait in a queue with the time they're ready again.",
  ["Max-heap of counts + queue of (count, ready_time).", "Time ticks by 1 each loop."],
  '''
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        h = [-c for c in Counter(tasks).values()]
        heapify(h)
        q = deque()  #> (remaining, time it's ready again)
        time = 0
        while h or q:
            time += 1
            if h:
                c = heappop(h) + 1  #> run the most common task
                if c:
                    q.append((c, time + n))
            if q and q[0][1] == time:
                heappush(h, q.popleft()[0])  #> done cooling down
        return time
''', [([["A", "A", "A", "B", "B", "B"], 2], 8), ([["A", "C", "A", "B", "D", "B"], 1], 6)], 'O(n)', 'O(26)')

P('find-median-stream', 'Live Median', 295, 'Hard', H,
  "Numbers stream in. At any time, report the median.",
  "Two heaps: a max-heap for the smaller half, a min-heap for the bigger half. Keep them balanced; the median sits at their tops.",
  ["small can have one extra.", "Move tops between heaps to rebalance."],
  '''
class MedianFinder:
    def __init__(self):
        self.small = []  #> max-heap (negatives): lower half
        self.big = []  #> min-heap: upper half

    def addNum(self, num: int) -> None:
        heappush(self.small, -num)
        heappush(self.big, -heappop(self.small))  #> biggest of small moves up
        if len(self.big) > len(self.small):
            heappush(self.small, -heappop(self.big))

    def findMedian(self) -> float:
        if len(self.small) > len(self.big):
            return float(-self.small[0])
        return (-self.small[0] + self.big[0]) / 2
''', [([["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"], [[], [1], [2], [], [3], []]], [None, None, None, 1.5, None, 2.0])], 'O(log n)', 'O(n)', mode='design')

P('top-k-words', 'Most Common Words', 692, 'Medium', H,
  "Return the k most frequent words. Ties: alphabetical order.",
  "Count, then sort by (-count, word) and take the first k. A heap of size k also works.",
  ["Sort keys can be tuples.", "-count makes bigger counts come first."],
  '''
class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        count = Counter(words)
        ranked = sorted(count, key=lambda w: (-count[w], w))  #> most common, then a-z
        return ranked[:k]
''', [([["i", "love", "leetcode", "i", "love", "coding"], 2], ["i", "love"]), ([["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4], ["the", "is", "sunny", "day"])], 'O(n log n)', 'O(n)')

P('implement-trie', 'Build a Word Tree (Trie)', 208, 'Medium', TR,
  "Build a trie: insert words, check if a word exists, check if any word starts with a prefix.",
  "Each node is a dictionary of letter -> child node. Mark the node where a word ends.",
  ["Walk letter by letter, creating nodes as needed.", "A special key like '$' marks word-ends."],
  '''
class Trie:
    def __init__(self):
        self.root = {}  #> letter -> next node

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})  #> walk or create
        node['$'] = True  #> a word ends here

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and '$' in node

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node
''', [([["Trie", "insert", "search", "search", "startsWith", "insert", "search"], [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]], [None, None, True, False, True, None, True])], 'O(len) each', 'O(total letters)', mode='design')

P('word-dictionary', 'Word Finder With Wildcards', 211, 'Medium', TR,
  "Add words, then search where '.' can match any letter.",
  "A trie. When you meet '.', try every child (a little DFS).",
  ["Normal letters: one path. Dots: all paths.", "Recursion with the index into the word."],
  '''
class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = True

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return '$' in node
            ch = word[i]
            if ch == '.':
                return any(dfs(nxt, i + 1) for k, nxt in node.items() if k != '$')  #> try every letter
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
''', [([["WordDictionary", "addWord", "addWord", "addWord", "search", "search", "search", "search"], [[], ["bad"], ["dad"], ["mad"], ["pad"], ["bad"], [".ad"], ["b.."]]], [None, None, None, None, False, True, True, True])], 'O(26^dots · len)', 'O(total letters)', mode='design')

P('word-search-ii', 'Find Many Words in a Letter Grid', 212, 'Hard', TR,
  "Find every word from the list that can be traced in the grid by moving up/down/left/right without reusing a cell.",
  "Put all words in a trie, then DFS from each cell, walking the trie at the same time. Dead end in the trie = stop early.",
  ["The trie lets you search all words at once.", "Mark cells as used while exploring, then un-mark."],
  '''
class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = {}
        for w in words:
            node = root
            for ch in w:
                node = node.setdefault(ch, {})
            node['$'] = w
        R, C = len(board), len(board[0])
        found = set()
        def dfs(r, c, node):
            ch = board[r][c]
            if ch not in node:
                return  #> no word goes this way
            nxt = node[ch]
            if '$' in nxt:
                found.add(nxt['$'])
            board[r][c] = '#'  #> mark as used
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    dfs(nr, nc, nxt)
            board[r][c] = ch  #> un-mark
        for r in range(R):
            for c in range(C):
                dfs(r, c, root)
        return list(found)
''', [([[["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]], ["oath", "pea", "eat", "rain"]], ["eat", "oath"]), ([[["a", "b"], ["c", "d"]], ["abcb"]], [])], 'O(R·C·4^L)', 'O(total letters)', cmp='sorted')

P('subsets', 'Every Possible Bag', 78, 'Medium', BT,
  "List every subset (every possible bag you could pack) of a list of different numbers.",
  "For each number, make two choices: take it or leave it. That's a decision tree; backtracking walks all of it.",
  ["n numbers → 2ⁿ subsets.", "Add to the path, recurse, then remove (undo)."],
  '''
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        path = []
        def go(i):
            if i == len(nums):
                res.append(path[:])  #> a finished bag (copy it!)
                return
            path.append(nums[i])  #> choice 1: take nums[i]
            go(i + 1)
            path.pop()  #> undo
            go(i + 1)  #> choice 2: leave it
        go(0)
        return res
''', [([[1, 2, 3]], [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]), ([[0]], [[], [0]])], 'O(n·2ⁿ)', 'O(n)', cmp='deep')

P('combination-sum', 'Coins That Make the Total', 39, 'Medium', BT,
  "Find all combinations of the numbers (each can be reused) that add up to target.",
  "Try each number starting from the current one (so no duplicates in different orders). Stop when the sum goes over.",
  ["Pass 'start' so you don't go back to earlier numbers.", "remaining < 0 → dead end."],
  '''
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        path = []
        def go(start, left):
            if left == 0:
                res.append(path[:])  #> exact total!
                return
            for i in range(start, len(candidates)):
                c = candidates[i]
                if c <= left:
                    path.append(c)
                    go(i, left - c)  #> i again: can reuse
                    path.pop()
        go(0, target)
        return res
''', [([[2, 3, 6, 7], 7], [[2, 2, 3], [7]]), ([[2, 3, 5], 8], [[2, 2, 2, 2], [2, 3, 3], [3, 5]]), ([[2], 1], [])], 'O(2^t)', 'O(t)', cmp='deep')

P('permutations', 'Every Possible Order', 46, 'Medium', BT,
  "List every ordering of a list of different numbers.",
  "Pick any unused number for the next spot, recurse, then put it back.",
  ["n numbers → n! orders.", "A 'used' set tracks what's in the path."],
  '''
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        path = []
        used = set()
        def go():
            if len(path) == len(nums):
                res.append(path[:])
                return
            for x in nums:
                if x not in used:
                    used.add(x)
                    path.append(x)  #> place x in the next spot
                    go()
                    path.pop()  #> take it back out
                    used.remove(x)
        go()
        return res
''', [([[1, 2, 3]], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), ([[0, 1]], [[0, 1], [1, 0]])], 'O(n·n!)', 'O(n)', cmp='deep')

P('subsets-ii', 'Every Bag (With Repeats in the List)', 90, 'Medium', BT,
  "Like 'Every Possible Bag', but the list can have repeats. No duplicate bags allowed.",
  "Sort first. When you decide to skip a number, skip all its copies too.",
  ["Equal numbers sit together after sorting.", "Take it, or jump past every copy."],
  '''
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res, path = [], []
        def go(i):
            if i == len(nums):
                res.append(path[:])
                return
            path.append(nums[i])
            go(i + 1)  #> take it
            path.pop()
            j = i
            while j < len(nums) and nums[j] == nums[i]:
                j += 1  #> skip all copies
            go(j)
        go(0)
        return res
''', [([[1, 2, 2]], [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]), ([[0]], [[], [0]])], 'O(n·2ⁿ)', 'O(n)', cmp='deep')

P('combination-sum-ii', 'Coins Used Once Each', 40, 'Medium', BT,
  "Each number can be used only once, and the list may have repeats. Find unique combos that hit target.",
  "Sort. In each loop level, skip a number equal to the one just tried at the same level.",
  ["i > start and c[i] == c[i-1] → skip.", "Recurse with i+1 (no reuse)."],
  '''
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        res, path = [], []
        def go(start, left):
            if left == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue  #> same choice again: skip
                if candidates[i] > left:
                    break
                path.append(candidates[i])
                go(i + 1, left - candidates[i])
                path.pop()
        go(0, target)
        return res
''', [([[10, 1, 2, 7, 6, 1, 5], 8], [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]), ([[2, 5, 2, 1, 2], 5], [[1, 2, 2], [5]])], 'O(2ⁿ)', 'O(n)', cmp='deep')

P('word-search', 'Trace a Word in the Grid', 79, 'Medium', BT,
  "Can you trace the word in the grid moving up/down/left/right, never reusing a cell?",
  "Start from every cell. DFS letter by letter; mark the cell used, explore, then un-mark.",
  ["Wrong letter or out of bounds → backtrack.", "Un-marking lets other paths use the cell."],
  '''
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        R, C = len(board), len(board[0])
        def dfs(r, c, i):
            if i == len(word):
                return True  #> matched every letter
            if r < 0 or c < 0 or r >= R or c >= C or board[r][c] != word[i]:
                return False
            tmp = board[r][c]
            board[r][c] = '#'  #> mark as used
            ok = dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1)
            board[r][c] = tmp  #> un-mark
            return ok
        for r in range(R):
            for c in range(C):
                if dfs(r, c, 0):
                    return True
        return False
''', [([[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"], True), ([[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"], True), ([[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"], False)], 'O(R·C·4^L)', 'O(L)')

P('palindrome-partitioning', 'Cut Into Palindromes', 131, 'Medium', BT,
  "Cut the string into pieces where every piece reads the same backwards. List every way.",
  "Try every first piece that's a palindrome, then solve the rest the same way.",
  ["piece == piece[::-1] checks a palindrome.", "When you reach the end, save the path."],
  '''
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        res, path = [], []
        def go(i):
            if i == len(s):
                res.append(path[:])
                return
            for j in range(i + 1, len(s) + 1):
                piece = s[i:j]
                if piece == piece[::-1]:  #> palindrome piece
                    path.append(piece)
                    go(j)
                    path.pop()
        go(0)
        return res
''', [(["aab"], [["a", "a", "b"], ["aa", "b"]]), (["a"], [["a"]])], 'O(n·2ⁿ)', 'O(n)', cmp='deep')

P('letter-combinations', 'Phone Keypad Words', 17, 'Medium', BT,
  "Old phones map digits to letters (2=abc, 3=def…). List every letter combo a digit string could spell.",
  "For each digit, branch into each of its letters.",
  ["Empty input → empty list.", "Depth of recursion = number of digits."],
  '''
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        keys = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
        res = []
        def go(i, cur):
            if i == len(digits):
                res.append(cur)
                return
            for ch in keys[digits[i]]:
                go(i + 1, cur + ch)  #> branch for each letter
        go(0, '')
        return res
''', [(["23"], ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]), ([""], []), (["2"], ["a", "b", "c"])], 'O(4ⁿ)', 'O(n)', cmp='sorted')

P('n-queens', 'Peaceful Queens', 51, 'Hard', BT,
  "Place n queens on an n×n chessboard so none can attack another. Return every board.",
  "Go row by row. In each row try each column that isn't attacked by column, or either diagonal (r-c and r+c).",
  ["Sets for cols, r-c diagonals, r+c diagonals.", "Undo after each try."],
  '''
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        res = []
        cols, d1, d2 = set(), set(), set()
        board = [['.'] * n for _ in range(n)]
        def go(r):
            if r == n:
                res.append([''.join(row) for row in board])
                return
            for c in range(n):
                if c in cols or r - c in d1 or r + c in d2:
                    continue  #> this square is attacked
                cols.add(c); d1.add(r - c); d2.add(r + c)
                board[r][c] = 'Q'
                go(r + 1)
                board[r][c] = '.'  #> pick the queen back up
                cols.remove(c); d1.remove(r - c); d2.remove(r + c)
        go(0)
        return res
''', [([4], [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]), ([1], [["Q"]])], 'O(n!)', 'O(n)', cmp='deep')

P('combinations', 'Choose K From N', 77, 'Medium', BT,
  "List every way to choose k numbers from 1..n.",
  "Pick numbers in increasing order so each group appears once.",
  ["Start the next pick after the last one.", "Stop when the path has k numbers."],
  '''
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res, path = [], []
        def go(start):
            if len(path) == k:
                res.append(path[:])
                return
            for x in range(start, n + 1):
                path.append(x)
                go(x + 1)
                path.pop()
        go(1)
        return res
''', [([4, 2], [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]), ([1, 1], [[1]])], 'O(k·C(n,k))', 'O(k)', cmp='deep')
