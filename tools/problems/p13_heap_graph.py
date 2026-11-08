from pb import P
H, TR, BT, G = 'Heap', 'Tries', 'Backtracking', 'Graphs'

P('design-twitter', 'Mini Twitter', 355, 'Medium', H,
  "Build a tiny Twitter: post tweets, follow/unfollow, and get the 10 newest tweets from you and the people you follow.",
  "Give every tweet a time number. For the feed, gather tweets from you + followees and take the 10 newest with a heap.",
  ["A counter that goes up each post works as a clock.", "heapq.nlargest grabs the newest 10."],
  '''
import heapq
from collections import defaultdict
class Twitter:
    def __init__(self):
        self.t = 0
        self.tweets = defaultdict(list)
        self.follows = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.t += 1  #> tick the clock
        self.tweets[userId].append((self.t, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        people = self.follows[userId] | {userId}
        allt = [tw for p in people for tw in self.tweets[p]]
        return [tid for _, tid in heapq.nlargest(10, allt)]  #> 10 newest

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].discard(followeeId)
''', [([["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"], [[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]], [None, None, [5], None, None, [6, 5], None, [5]])], 'O(n log 10) feed', 'O(n)', mode='design')

P('k-smallest-pairs', 'Cheapest Pairs', 373, 'Medium', H,
  "Two sorted lists. Find the k pairs (one from each) with the smallest sums.",
  "Start a heap with each nums1[i] paired with nums2[0]. Pop the smallest; push its next partner nums2[j+1].",
  ["The heap holds (sum, i, j)."],
  '''
import heapq
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        h = [(a + nums2[0], i, 0) for i, a in enumerate(nums1[:k])]
        heapq.heapify(h)
        out = []
        while h and len(out) < k:
            _, i, j = heapq.heappop(h)  #> cheapest pair left
            out.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(h, (nums1[i] + nums2[j + 1], i, j + 1))
        return out
''', [([[1, 7, 11], [2, 4, 6], 3], [[1, 2], [1, 4], [1, 6]]), ([[1, 1, 2], [1, 2, 3], 2], [[1, 1], [1, 1]])], 'O(k log k)', 'O(k)')

P('ipo', 'Grow Your Startup', 502, 'Hard', H,
  "You have w money. Each project needs some capital to start and gives some profit. You can do at most k projects. What's the most money you can end with?",
  "Sort projects by capital. Each round, push every project you can now afford into a max-heap of profits, then do the best one.",
  ["Money only grows, so affordable projects stay affordable."],
  '''
import heapq
class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        projects = sorted(zip(capital, profits))
        h, i = [], 0
        for _ in range(k):
            while i < len(projects) and projects[i][0] <= w:
                heapq.heappush(h, -projects[i][1])  #> now affordable
                i += 1
            if not h:
                break
            w -= heapq.heappop(h)  #> do the most profitable one
        return w
''', [([2, 0, [1, 2, 3], [0, 1, 1]], 4), ([3, 0, [1, 2, 3], [0, 1, 2]], 6)], 'O(n log n)', 'O(n)')

P('smallest-infinite-set', 'Endless Number Jar', 2336, 'Medium', H,
  "A jar holds every positive number. popSmallest takes out the smallest; addBack puts a number back (if it's missing).",
  "Keep a pointer 'next new number' plus a min-heap (and set) of numbers that were added back.",
  ["Added-back numbers are always smaller than the pointer."],
  '''
import heapq
class SmallestInfiniteSet:
    def __init__(self):
        self.next = 1
        self.back = []
        self.inback = set()

    def popSmallest(self) -> int:
        if self.back:
            x = heapq.heappop(self.back)  #> a returned number is smaller
            self.inback.remove(x)
            return x
        self.next += 1
        return self.next - 1

    def addBack(self, num: int) -> None:
        if num < self.next and num not in self.inback:
            heapq.heappush(self.back, num)
            self.inback.add(num)
''', [([["SmallestInfiniteSet", "addBack", "popSmallest", "popSmallest", "popSmallest", "addBack", "popSmallest", "popSmallest", "popSmallest"], [[], [2], [], [], [], [1], [], [], []]], [None, None, 1, 2, 3, None, 1, 4, 5])], 'O(log n)', 'O(n)', mode='design')

P('total-cost-hire', 'Hire the Cheapest Workers', 2462, 'Medium', H,
  "Hire k workers in k rounds. Each round, look only at the first 'candidates' and last 'candidates' workers left, and hire the cheapest (ties: lower index). Total cost?",
  "Two min-heaps: one for the front group, one for the back group. Refill a heap from the middle after hiring from it.",
  ["Don't let the two groups overlap."],
  '''
import heapq
class Solution:
    def totalCost(self, costs: List[int], k: int, candidates: int) -> int:
        front, back = [], []
        l, r = 0, len(costs) - 1
        total = 0
        for _ in range(k):
            while len(front) < candidates and l <= r:
                heapq.heappush(front, costs[l]); l += 1
            while len(back) < candidates and l <= r:
                heapq.heappush(back, costs[r]); r -= 1
            if not back or (front and front[0] <= back[0]):
                total += heapq.heappop(front)  #> front side is cheaper
            else:
                total += heapq.heappop(back)
        return total
''', [([[17, 12, 10, 2, 7, 2, 11, 20, 8], 3, 4], 11), ([[1, 2, 4, 1], 3, 3], 4)], 'O((k+c) log c)', 'O(c)')

P('max-subsequence-score', 'Best Team Score', 2542, 'Medium', H,
  "Pick k positions. Score = (sum of their nums1) × (smallest of their nums2). Find the best score.",
  "Sort by nums2 from big to small. Each one in turn is the minimum; keep the k biggest nums1 so far in a min-heap.",
  ["When the heap has more than k, drop its smallest."],
  '''
import heapq
class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        pairs = sorted(zip(nums2, nums1), reverse=True)
        h, total, best = [], 0, 0
        for m, a in pairs:
            heapq.heappush(h, a)
            total += a
            if len(h) > k:
                total -= heapq.heappop(h)  #> drop the weakest
            if len(h) == k:
                best = max(best, total * m)  #> m is the current minimum
        return best
''', [([[1, 3, 3, 2], [2, 1, 3, 4], 3], 12), ([[4, 2, 3, 1, 1], [7, 5, 10, 9, 6], 1], 30)], 'O(n log n)', 'O(k)')

P('search-suggestions', 'Search Box Suggestions', 1268, 'Medium', TR,
  "As you type each letter of searchWord, suggest up to 3 products (alphabetically smallest) that start with what you've typed.",
  "Sort the products. For each prefix, binary search to where it would start and take the next 3 that match.",
  ["A trie works too; sorting + bisect is shorter."],
  '''
from bisect import bisect_left
class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        products.sort()
        out = []
        for i in range(1, len(searchWord) + 1):
            pre = searchWord[:i]
            j = bisect_left(products, pre)  #> first product at or after the prefix
            out.append([p for p in products[j:j + 3] if p.startswith(pre)])
        return out
''', [([["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"], [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"], ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]), ([["havana"], "tatiana"], [[], [], [], [], [], [], []])], 'O(n log n + L log n)', 'O(1) extra')

P('n-queens-ii', 'Count the Queen Puzzles', 52, 'Hard', BT,
  "How many ways can you place n queens on an n×n board so none attack each other?",
  "Place one queen per row. Keep sets of used columns and diagonals (r-c and r+c). Backtrack.",
  ["Diagonals: r - c is the same along one direction, r + c along the other."],
  '''
class Solution:
    def totalNQueens(self, n: int) -> int:
        cols, d1, d2 = set(), set(), set()
        def place(r):
            if r == n:
                return 1  #> all rows filled
            count = 0
            for c in range(n):
                if c in cols or r - c in d1 or r + c in d2:
                    continue
                cols.add(c); d1.add(r - c); d2.add(r + c)
                count += place(r + 1)
                cols.remove(c); d1.remove(r - c); d2.remove(r + c)  #> take the queen back
            return count
        return place(0)
''', [([4], 2), ([1], 1), ([5], 10)], 'O(n!)', 'O(n)')

P('combination-sum-iii', 'k Digits That Add Up', 216, 'Medium', BT,
  "Find every set of k different digits from 1 to 9 that adds up to n.",
  "Backtrack: try digits in increasing order, stop when too big or too many.",
  ["Start each next digit after the last one to avoid repeats."],
  '''
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        out, path = [], []
        def go(start, left):
            if len(path) == k:
                if left == 0:
                    out.append(path[:])  #> exactly k digits, exact sum
                return
            for d in range(start, 10):
                if d > left:
                    break
                path.append(d)
                go(d + 1, left - d)
                path.pop()
        go(1, n)
        return out
''', [([3, 7], [[1, 2, 4]]), ([3, 9], [[1, 2, 6], [1, 3, 5], [2, 3, 4]]), ([4, 1], [])], 'O(C(9,k))', 'O(k)', cmp='deep')

P('permutations-ii', 'Every Order (With Repeats)', 47, 'Medium', BT,
  "List every different ordering of the numbers. The list can have repeats, so don't list the same order twice.",
  "Sort. Backtrack with a 'used' list, and skip a number if it equals the previous one that is NOT used right now.",
  ["Sorting puts twins side by side."],
  '''
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        out, path, used = [], [], [False] * len(nums)
        def go():
            if len(path) == len(nums):
                out.append(path[:])
                return
            for i in range(len(nums)):
                if used[i] or (i and nums[i] == nums[i - 1] and not used[i - 1]):
                    continue  #> this twin would repeat an order
                used[i] = True
                path.append(nums[i])
                go()
                path.pop()
                used[i] = False
        go()
        return out
''', [([[1, 1, 2]], [[1, 1, 2], [1, 2, 1], [2, 1, 1]]), ([[1, 2, 3]], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])], 'O(n·n!)', 'O(n)', cmp='deep')

P('walls-and-gates', 'Distance to the Nearest Door', 286, 'Medium', G,
  "A grid: -1 is a wall, 0 is a door, 2147483647 is an empty room. Fill each room with its distance to the nearest door.",
  "Multi-source BFS: start from ALL doors at once. The first time you reach a room is its shortest distance.",
  ["Only step into rooms still marked empty."],
  '''
from collections import deque
class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        INF = 2147483647
        R, C = len(rooms), len(rooms[0])
        q = deque((r, c) for r in range(R) for c in range(C) if rooms[r][c] == 0)
        while q:
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and rooms[nr][nc] == INF:
                    rooms[nr][nc] = rooms[r][c] + 1  #> one step further from a door
                    q.append((nr, nc))
''', [([[[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1], [2147483647, -1, 2147483647, -1], [0, -1, 2147483647, 2147483647]]], [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]])], 'O(R·C)', 'O(R·C)', inplace=0)

P('min-height-trees', 'Best Root for a Short Tree', 310, 'Medium', G,
  "A tree given as edges. Which node(s), as the root, make the tree as short as possible?",
  "Peel leaves layer by layer (like an onion). The last 1 or 2 nodes left are the centres.",
  ["A leaf has exactly one neighbour.", "Stop when 2 or fewer nodes remain."],
  '''
class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n == 1:
            return [0]
        nb = [set() for _ in range(n)]
        for a, b in edges:
            nb[a].add(b); nb[b].add(a)
        leaves = [i for i in range(n) if len(nb[i]) == 1]
        left = n
        while left > 2:
            left -= len(leaves)
            nxt = []
            for leaf in leaves:
                j = nb[leaf].pop()
                nb[j].remove(leaf)  #> peel the leaf off
                if len(nb[j]) == 1:
                    nxt.append(j)
            leaves = nxt
        return leaves
''', [([4, [[1, 0], [1, 2], [1, 3]]], [1]), ([6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]], [3, 4])], 'O(n)', 'O(n)', cmp='sorted')

P('reconstruct-itinerary', 'Rebuild the Trip', 332, 'Hard', G,
  "Plane tickets [from, to]. Use every ticket exactly once starting from \"JFK\". If several trips work, pick the alphabetically smallest.",
  "Hierholzer's trick: DFS taking the smallest destination first; add an airport to the route when you're stuck there, then reverse.",
  ["Sort destinations so the smallest is used first."],
  '''
from collections import defaultdict
class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        g = defaultdict(list)
        for a, b in sorted(tickets, reverse=True):
            g[a].append(b)  #> smallest destination ends up last (pop is fast)
        route = []
        def go(a):
            while g[a]:
                go(g[a].pop())
            route.append(a)  #> stuck here: write it down
        go('JFK')
        return route[::-1]
''', [([[["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]], ["JFK", "MUC", "LHR", "SFO", "SJC"]), ([[["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]], ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"])], 'O(E log E)', 'O(E)')

P('evaluate-division', 'Currency Exchange Puzzle', 399, 'Medium', G,
  "a / b = 2 and b / c = 3. What's a / c? Answer each query, or -1.0 if it can't be known.",
  "A graph: an edge a→b with weight 2 and b→a with 0.5. A query is a path search multiplying weights.",
  ["Unknown letters give -1.0.", "x / x = 1.0 if x is known."],
  '''
from collections import defaultdict
class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        g = defaultdict(dict)
        for (a, b), v in zip(equations, values):
            g[a][b] = v
            g[b][a] = 1 / v
        def find(a, b, seen):
            if a == b:
                return 1.0
            seen.add(a)
            for nxt, w in g[a].items():
                if nxt not in seen:
                    r = find(nxt, b, seen)
                    if r != -1.0:
                        return w * r  #> multiply along the path
            return -1.0
        return [find(a, b, set()) if a in g and b in g else -1.0 for a, b in queries]
''', [([[["a", "b"], ["b", "c"]], [2.0, 3.0], [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]], [6.0, 0.5, -1.0, 1.0, -1.0])], 'O(Q·(V+E))', 'O(V+E)')

P('min-genetic-mutation', 'DNA Steps', 433, 'Medium', G,
  "Change one letter (A, C, G, T) at a time to get from start to end. Every step must be in the bank. Fewest steps, or -1?",
  "BFS over gene strings; neighbours are bank genes one letter away.",
  ["Remove genes from the bank once visited."],
  '''
from collections import deque
class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        left = set(bank)
        q = deque([(startGene, 0)])
        while q:
            g, d = q.popleft()
            if g == endGene:
                return d
            for i in range(len(g)):
                for ch in 'ACGT':
                    nxt = g[:i] + ch + g[i + 1:]
                    if nxt in left:
                        left.remove(nxt)  #> visit each gene once
                        q.append((nxt, d + 1))
        return -1
''', [(["AACCGGTT", "AACCGGTA", ["AACCGGTA"]], 1), (["AACCGGTT", "AAACGGTA", ["AACCGGTA", "AACCGCTA", "AAACGGTA"]], 2)], 'O(n·L·4)', 'O(n)')

P('zero-one-matrix', 'Distance to the Nearest Zero', 542, 'Medium', G,
  "For every cell in a 0/1 grid, how far (in up/down/left/right steps) is the nearest 0?",
  "Multi-source BFS from every 0 at once.",
  ["Mark 1-cells as unknown (-1) first."],
  '''
from collections import deque
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        R, C = len(mat), len(mat[0])
        dist = [[0 if mat[r][c] == 0 else -1 for c in range(C)] for r in range(R)]
        q = deque((r, c) for r in range(R) for c in range(C) if mat[r][c] == 0)
        while q:
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1  #> ripple outward
                    q.append((nr, nc))
        return dist
''', [([[[0, 0, 0], [0, 1, 0], [0, 0, 0]]], [[0, 0, 0], [0, 1, 0], [0, 0, 0]]), ([[[0, 0, 0], [0, 1, 0], [1, 1, 1]]], [[0, 0, 0], [0, 1, 0], [1, 2, 1]])], 'O(R·C)', 'O(R·C)')

P('number-of-provinces', 'Friend Groups', 547, 'Medium', G,
  "isConnected[i][j] = 1 means city i and j are directly connected. How many separate groups are there?",
  "DFS from each unvisited city, marking its whole group. Count how many times you start.",
  ["Union-Find works too."],
  '''
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        seen = set()
        def visit(i):
            for j in range(n):
                if isConnected[i][j] and j not in seen:
                    seen.add(j)
                    visit(j)
        groups = 0
        for i in range(n):
            if i not in seen:
                groups += 1  #> a new group starts here
                seen.add(i)
                visit(i)
        return groups
''', [([[[1, 1, 0], [1, 1, 0], [0, 0, 1]]], 2), ([[[1, 0, 0], [0, 1, 0], [0, 0, 1]]], 3)], 'O(n²)', 'O(n)')

P('accounts-merge', 'Merge Email Accounts', 721, 'Medium', G,
  "Each account is [name, emails...]. Accounts sharing any email belong to the same person. Merge them (emails sorted).",
  "Union-Find on emails: link every email in an account to the first one. Then group emails by their root.",
  ["Remember which name each email belongs to."],
  '''
from collections import defaultdict
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        parent, owner = {}, {}
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for acc in accounts:
            for e in acc[1:]:
                parent.setdefault(e, e)
                owner[e] = acc[0]
                parent[find(e)] = find(acc[1])  #> same person as the first email
        groups = defaultdict(list)
        for e in parent:
            groups[find(e)].append(e)
        return [[owner[r]] + sorted(es) for r, es in groups.items()]
''', [([[["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]], [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]])], 'O(n log n)', 'O(n)', cmp='deep')

P('swim-in-rising-water', 'Swim When the Water Rises', 778, 'Hard', G,
  "Each cell has a height. At time t you can swim through cells with height <= t. Earliest time to get from top-left to bottom-right?",
  "Dijkstra-style: a min-heap by 'highest cell on the path so far'. Always expand the lowest one.",
  ["The answer is the max height along the best path."],
  '''
import heapq
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        h, seen = [(grid[0][0], 0, 0)], {(0, 0)}
        while h:
            t, r, c = heapq.heappop(h)  #> lowest water level path
            if (r, c) == (n - 1, n - 1):
                return t
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    heapq.heappush(h, (max(t, grid[nr][nc]), nr, nc))
''', [([[[0, 2], [1, 3]]], 3), ([[[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]]], 16)], 'O(n² log n)', 'O(n²)')

P('keys-and-rooms', 'Rooms and Keys', 841, 'Medium', G,
  "Room 0 is open. Each room has keys to other rooms. Can you visit every room?",
  "DFS/BFS from room 0 using keys as edges. Check if you saw all rooms.",
  ["A stack of keys to try."],
  '''
class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        seen, stack = {0}, [0]
        while stack:
            for key in rooms[stack.pop()]:
                if key not in seen:
                    seen.add(key)  #> unlock a new room
                    stack.append(key)
        return len(seen) == len(rooms)
''', [([[[1], [2], [3], []]], True), ([[[1, 3], [3, 0, 1], [2], [0]]], False)], 'O(V+E)', 'O(V)')

P('snakes-and-ladders', 'Snakes and Ladders', 909, 'Medium', G,
  "A board game numbered 1 to n² in a zigzag from the bottom-left. Roll 1-6 each move; snakes and ladders jump you. Fewest moves to the last square?",
  "BFS over square numbers. Convert a number to (row, col) carefully because rows alternate direction.",
  ["-1 means no snake or ladder.", "Only one jump per move."],
  '''
from collections import deque
class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        def cell(k):
            r, c = divmod(k - 1, n)
            row = n - 1 - r
            col = c if r % 2 == 0 else n - 1 - c  #> rows zigzag
            return board[row][col]
        q, seen = deque([(1, 0)]), {1}
        while q:
            k, moves = q.popleft()
            if k == n * n:
                return moves
            for d in range(1, 7):
                nxt = k + d
                if nxt > n * n:
                    break
                if cell(nxt) != -1:
                    nxt = cell(nxt)
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, moves + 1))
        return -1
''', [([[[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, 35, -1, -1, 13, -1], [-1, -1, -1, -1, -1, -1], [-1, 15, -1, -1, -1, -1]]], 4), ([[[-1, -1], [-1, 3]]], 1)], 'O(n²)', 'O(n²)')

P('reorder-routes', 'Point the Roads to the Capital', 1466, 'Medium', G,
  "n cities, one-way roads forming a tree. Flip the fewest roads so every city can reach city 0.",
  "Treat roads as two-way but remember their real direction. DFS from 0: every road pointing AWAY from 0 must be flipped.",
  ["Store (neighbour, needs_flip)."],
  '''
class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for a, b in connections:
            g[a].append((b, 1))  #> a→b points away: flip if we go this way
            g[b].append((a, 0))
        seen, stack, flips = {0}, [0], 0
        while stack:
            u = stack.pop()
            for v, cost in g[u]:
                if v not in seen:
                    seen.add(v)
                    flips += cost
                    stack.append(v)
        return flips
''', [([6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]], 3), ([5, [[1, 0], [1, 2], [3, 2], [3, 4]]], 2)], 'O(n)', 'O(n)')

P('nearest-exit-maze', 'Nearest Exit From the Maze', 1926, 'Medium', G,
  "A maze of '.' and '+' walls. From the entrance, how many steps to the closest empty cell on the border (not the entrance itself)? -1 if none.",
  "BFS from the entrance; the first border cell you reach is the answer.",
  ["Mark cells as walls once visited."],
  '''
from collections import deque
class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        R, C = len(maze), len(maze[0])
        q = deque([(entrance[0], entrance[1], 0)])
        maze[entrance[0]][entrance[1]] = '+'
        while q:
            r, c, d = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == '.':
                    if nr in (0, R - 1) or nc in (0, C - 1):
                        return d + 1  #> reached the edge!
                    maze[nr][nc] = '+'
                    q.append((nr, nc, d + 1))
        return -1
''', [([[["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]], [1, 2]], 1), ([[["+", "+", "+"], [".", ".", "."], ["+", "+", "+"]], [1, 0]], 2), ([[[".", "+"]], [0, 0]], -1)], 'O(R·C)', 'O(R·C)')

P('open-the-lock', 'Crack the Combination Lock', 752, 'Medium', G,
  "A 4-wheel lock starts at \"0000\". Each move turns one wheel one notch. Avoid the deadend combos. Fewest moves to reach target, or -1?",
  "BFS over combinations; each has 8 neighbours (4 wheels × up/down).",
  ["Put deadends in the seen set from the start."],
  '''
from collections import deque
class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        seen = set(deadends)
        if '0000' in seen:
            return -1
        seen.add('0000')
        q = deque([('0000', 0)])
        while q:
            s, d = q.popleft()
            if s == target:
                return d
            for i in range(4):
                for step in (1, -1):
                    nxt = s[:i] + str((int(s[i]) + step) % 10) + s[i + 1:]  #> turn one wheel
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, d + 1))
        return -1
''', [([["8888"], "0009"], 1), ([["0201", "0101", "0102", "1212", "2002"], "0202"], 6), ([["0000"], "8888"], -1)], 'O(10⁴)', 'O(10⁴)')
