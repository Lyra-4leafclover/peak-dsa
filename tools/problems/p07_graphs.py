from pb import P
T = 'Graphs'
G1 = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]

P('number-of-islands', 'Count the Islands', 200, 'Medium', T,
  "A map of '1' (land) and '0' (water). Land touching up/down/left/right is the same island. How many islands?",
  "Scan every cell. When you find unvisited land, that's a new island: flood it (DFS) so you don't count it again.",
  ["Flooding = turn the land you visit into water.", "Count how many times you start a flood."],
  '''
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        R, C = len(grid), len(grid[0])
        def sink(r, c):
            if r < 0 or c < 0 or r >= R or c >= C or grid[r][c] != '1':
                return
            grid[r][c] = '0'  #> visited: sink it
            sink(r + 1, c); sink(r - 1, c); sink(r, c + 1); sink(r, c - 1)
        count = 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == '1':
                    count += 1  #> brand new island!
                    sink(r, c)
        return count
''', [([G1], 3), ([[["1", "1", "1"], ["0", "1", "0"], ["1", "1", "1"]]], 1)], 'O(R·C)', 'O(R·C)')

P('max-area-island', 'Biggest Island', 695, 'Medium', T,
  "Grid of 1s and 0s. Return the size of the biggest island.",
  "Same flood idea, but the flood returns how many cells it sank.",
  ["area = 1 + areas of 4 neighbours.", "Track the max."],
  '''
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        R, C = len(grid), len(grid[0])
        def area(r, c):
            if r < 0 or c < 0 or r >= R or c >= C or grid[r][c] != 1:
                return 0
            grid[r][c] = 0
            return 1 + area(r + 1, c) + area(r - 1, c) + area(r, c + 1) + area(r, c - 1)
        best = 0
        for r in range(R):
            for c in range(C):
                best = max(best, area(r, c))
        return best
''', [([[[0, 0, 1, 0, 0], [0, 1, 1, 0, 1], [0, 1, 0, 0, 1], [0, 0, 0, 1, 1]]], 4), ([[[0, 0, 0]]], 0)], 'O(R·C)', 'O(R·C)')

P('flood-fill', 'Paint Bucket', 733, 'Easy', T,
  "Like the paint bucket in a drawing app: recolour the starting pixel and every same-coloured pixel connected to it.",
  "DFS from the start, painting cells that have the original colour.",
  ["If the new colour equals the old one, do nothing (or you loop forever).", "4 directions."],
  '''
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        old = image[sr][sc]
        if old == color:
            return image
        R, C = len(image), len(image[0])
        def paint(r, c):
            if 0 <= r < R and 0 <= c < C and image[r][c] == old:
                image[r][c] = color  #> splash!
                paint(r + 1, c); paint(r - 1, c); paint(r, c + 1); paint(r, c - 1)
        paint(sr, sc)
        return image
''', [([[[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2], [[2, 2, 2], [2, 2, 0], [2, 0, 1]]), ([[[0, 0, 0], [0, 0, 0]], 0, 0, 0], [[0, 0, 0], [0, 0, 0]])], 'O(R·C)', 'O(R·C)')

P('clone-graph', 'Photocopy a Graph', 133, 'Medium', T,
  "Make a deep copy of a connected graph. Input is an adjacency list: position i lists the neighbours of node i+1.",
  "DFS. Keep a dictionary original → copy. If a node was already copied, reuse its copy (stops infinite loops).",
  ["Create the copy BEFORE visiting neighbours.", "The dictionary doubles as the 'visited' set."],
  '''
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        copies = {}
        def clone(n):
            if n in copies:
                return copies[n]  #> already photocopied
            c = Node(n.val)
            copies[n] = c
            for nb in n.neighbors:
                c.neighbors.append(clone(nb))
            return c
        return clone(node) if node else None
''', [([[[2, 4], [1, 3], [2, 4], [1, 3]]], [[2, 4], [1, 3], [2, 4], [1, 3]]), ([[[]]], [[]])], 'O(V+E)', 'O(V)')

P('rotting-oranges', 'Rotten Orange Spread', 994, 'Medium', T,
  "0 = empty, 1 = fresh orange, 2 = rotten. Each minute, rotten oranges rot their fresh neighbours. Minutes until all rot? -1 if some never do.",
  "Multi-source BFS: start with ALL rotten oranges in the queue. Each BFS round is one minute.",
  ["Count fresh oranges at the start.", "If fresh > 0 at the end, return -1."],
  '''
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        R, C = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 2:
                    q.append((r, c))  #> every rotten one starts spreading
                elif grid[r][c] == 1:
                    fresh += 1
        minutes = 0
        while q and fresh:
            minutes += 1
            for _ in range(len(q)):
                r, c = q.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        q.append((nr, nc))
        return minutes if fresh == 0 else -1
''', [([[[2, 1, 1], [1, 1, 0], [0, 1, 1]]], 4), ([[[2, 1, 1], [0, 1, 1], [1, 0, 1]]], -1), ([[[0, 2]]], 0)], 'O(R·C)', 'O(R·C)')

P('pacific-atlantic', 'Rain Flowing to Both Oceans', 417, 'Medium', T,
  "Heights on an island. Pacific touches the top/left edges, Atlantic the bottom/right. Water flows to equal or lower neighbours. Which cells can reach both oceans?",
  "Think backwards: start from each ocean's edge and climb UP (to equal or higher). Cells reached from both are the answer.",
  ["Two DFS runs, two visited sets.", "Answer = intersection."],
  '''
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        R, C = len(heights), len(heights[0])
        def climb(starts):
            seen = set(starts)
            st = list(starts)
            while st:
                r, c = st.pop()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                        seen.add((nr, nc))  #> water could flow from here to the ocean
                        st.append((nr, nc))
            return seen
        pac = climb([(0, c) for c in range(C)] + [(r, 0) for r in range(R)])
        atl = climb([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R)])
        return [list(x) for x in pac & atl]
''', [([[[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]], [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]), ([[[1]]], [[0, 0]])], 'O(R·C)', 'O(R·C)', cmp='deep')

P('surrounded-regions', 'Capture Surrounded Zones', 130, 'Medium', T,
  "Flip every 'O' region that is completely surrounded by 'X' into 'X'. Regions touching the border survive.",
  "Mark survivors first: flood from every border 'O'. Then flip everything else.",
  ["Temporary marker like 'S' for safe.", "Final pass: O→X, S→O."],
  '''
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        R, C = len(board), len(board[0])
        def save(r, c):
            if 0 <= r < R and 0 <= c < C and board[r][c] == 'O':
                board[r][c] = 'S'  #> touches the border: safe
                save(r + 1, c); save(r - 1, c); save(r, c + 1); save(r, c - 1)
        for r in range(R):
            save(r, 0); save(r, C - 1)
        for c in range(C):
            save(0, c); save(R - 1, c)
        for r in range(R):
            for c in range(C):
                board[r][c] = 'O' if board[r][c] == 'S' else 'X'
''', [([[["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]], [["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]])], 'O(R·C)', 'O(R·C)', inplace=0)

P('course-schedule', 'Can You Finish All Classes?', 207, 'Medium', T,
  "Some classes need others first ([a, b] means take b before a). Can you finish them all? (No circular requirements.)",
  "Kahn's algorithm: start with classes that need nothing. Taking one removes it as a requirement from others. If you take all n, yes.",
  ["Count 'how many requirements left' per class.", "A cycle means some classes never reach 0."],
  '''
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        need = [0] * numCourses  #> requirements left per class
        unlocks = defaultdict(list)
        for a, b in prerequisites:
            unlocks[b].append(a)
            need[a] += 1
        q = deque(i for i in range(numCourses) if need[i] == 0)
        taken = 0
        while q:
            c = q.popleft()
            taken += 1  #> take this class
            for nxt in unlocks[c]:
                need[nxt] -= 1
                if need[nxt] == 0:
                    q.append(nxt)  #> now unlocked
        return taken == numCourses
''', [([2, [[1, 0]]], True), ([2, [[1, 0], [0, 1]]], False)], 'O(V+E)', 'O(V+E)')

P('course-schedule-ii', 'Class Order Planner', 210, 'Medium', T,
  "Same as before, but return an order to take the classes. Empty list if impossible.",
  "Same Kahn's algorithm, but write down each class as you take it.",
  ["This order is called a 'topological sort'.", "If not all classes were taken, return []."],
  '''
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        need = [0] * numCourses
        unlocks = defaultdict(list)
        for a, b in prerequisites:
            unlocks[b].append(a)
            need[a] += 1
        q = deque(i for i in range(numCourses) if need[i] == 0)
        order = []
        while q:
            c = q.popleft()
            order.append(c)
            for nxt in unlocks[c]:
                need[nxt] -= 1
                if need[nxt] == 0:
                    q.append(nxt)
        return order if len(order) == numCourses else []
''', [([2, [[1, 0]]], [0, 1]), ([4, [[1, 0], [2, 0], [3, 1], [3, 2]]], [0, 1, 2, 3]), ([1, []], [0])], 'O(V+E)', 'O(V+E)')

P('connected-components', 'Count Friend Groups', 323, 'Medium', T,
  "n people, and pairs who are friends. Friends of friends are in the same group. How many groups?",
  "Union-Find: everyone starts as their own group leader. Each friendship merges two groups. Count merges.",
  ["groups = n - successful merges.", "find() follows parents up to the leader."],
  '''
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))  #> everyone leads themselves
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]  #> shortcut the path
                x = parent[x]
            return x
        groups = n
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb  #> merge two groups
                groups -= 1
        return groups
''', [([5, [[0, 1], [1, 2], [3, 4]]], 2), ([5, [[0, 1], [1, 2], [2, 3], [3, 4]]], 1)], 'O(E·α(n))', 'O(n)')

P('graph-valid-tree', 'Is This Graph a Tree?', 261, 'Medium', T,
  "n nodes and some edges. Is it a tree? (Connected, and no loops.)",
  "A tree has exactly n-1 edges. Then use Union-Find: if an edge joins two nodes already in the same group, there's a loop.",
  ["Wrong edge count → not a tree.", "Union-Find detects cycles."],
  '''
class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False  #> already connected: this edge makes a loop
            parent[ra] = rb
        return True
''', [([5, [[0, 1], [0, 2], [0, 3], [1, 4]]], True), ([5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]], False)], 'O(E·α(n))', 'O(n)')

P('redundant-connection', 'The Extra Road', 684, 'Medium', T,
  "A tree got one extra edge added, creating a loop. Return the edge that can be removed (the last such one in the list).",
  "Union-Find, edge by edge. The first edge connecting two already-connected nodes is the extra one.",
  ["Same trick as Graph Valid Tree.", "Nodes are numbered from 1."],
  '''
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        parent = list(range(len(edges) + 1))
        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                return [a, b]  #> this road closes a loop
            parent[ra] = rb
        return []
''', [([[[1, 2], [1, 3], [2, 3]]], [2, 3]), ([[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]], [1, 4])], 'O(n·α(n))', 'O(n)')

P('word-ladder', 'Word Ladder', 127, 'Hard', T,
  "Change one letter at a time, every step must be a word in the list. Fewest words from begin to end (counting both)? 0 if impossible.",
  "BFS where each word is a node and neighbours differ by one letter. BFS finds the shortest path.",
  ["Try replacing each letter with a..z.", "Remove words from the set when visited."],
  '''
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0
        q = deque([(beginWord, 1)])
        while q:
            w, d = q.popleft()
            if w == endWord:
                return d
            for i in range(len(w)):
                for ch in 'abcdefghijklmnopqrstuvwxyz':
                    nw = w[:i] + ch + w[i + 1:]
                    if nw in words:
                        words.remove(nw)  #> visited
                        q.append((nw, d + 1))
        return 0
''', [(["hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]], 5), (["hit", "cog", ["hot", "dot", "dog", "lot", "log"]], 0)], 'O(n·L·26)', 'O(n)')

P('network-delay', 'Message Spread Time (Dijkstra)', 743, 'Medium', T,
  "A signal starts at node k. Edges [u, v, w] take w time. How long until every node hears it? -1 if some never do.",
  "Dijkstra: always expand the closest not-yet-finished node, using a min-heap of (time, node).",
  ["First time a node pops from the heap = its fastest time.", "Answer = the biggest of those times."],
  '''
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        g = defaultdict(list)
        for u, v, w in times:
            g[u].append((v, w))
        best = {}
        h = [(0, k)]
        while h:
            t, u = heappop(h)  #> closest unfinished node
            if u in best:
                continue
            best[u] = t
            for v, w in g[u]:
                if v not in best:
                    heappush(h, (t + w, v))
        return max(best.values()) if len(best) == n else -1
''', [([[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], 2), ([[[1, 2, 1]], 2, 1], 1), ([[[1, 2, 1]], 2, 2], -1)], 'O(E log V)', 'O(V+E)')

P('cheapest-flights-k-stops', 'Cheapest Trip With Few Stops', 787, 'Medium', T,
  "Flights [from, to, price]. Cheapest price from src to dst using at most k stops? -1 if none.",
  "Bellman-Ford, k+1 rounds: each round, relax every flight using LAST round's prices (so each round = one more flight).",
  ["Copy the price list each round.", "k stops = k+1 flights."],
  '''
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        price = [inf] * n
        price[src] = 0
        for _ in range(k + 1):
            new = price[:]  #> prices using one more flight
            for a, b, c in flights:
                if price[a] + c < new[b]:
                    new[b] = price[a] + c
            price = new
        return -1 if price[dst] == inf else price[dst]
''', [([4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1], 700), ([3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0], 500)], 'O(k·E)', 'O(n)')

P('min-cost-connect-points', 'Cheapest Way to Wire Every House', 1584, 'Medium', T,
  "Connect all points with wires. Wire cost = |x1-x2| + |y1-y2|. Minimum total cost? (Minimum spanning tree.)",
  "Prim's algorithm: grow a connected blob. Always add the cheapest wire from the blob to a new point.",
  ["Min-heap of (cost, point).", "Skip points already in the blob."],
  '''
class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        inside = set()
        h = [(0, 0)]
        total = 0
        while len(inside) < n:
            c, i = heappop(h)  #> cheapest wire out of the blob
            if i in inside:
                continue
            inside.add(i)
            total += c
            for j in range(n):
                if j not in inside:
                    d = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                    heappush(h, (d, j))
        return total
''', [([[[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]], 20), ([[[3, 12], [-2, 5], [-4, 1]]], 18)], 'O(n² log n)', 'O(n²)')

P('find-town-judge', 'Find the Town Judge', 997, 'Easy', T,
  "The judge trusts nobody, and everybody else trusts the judge. trust[i] = [a, b] means a trusts b. Find the judge or -1.",
  "Score each person: +1 when trusted, -1 when they trust someone. The judge scores exactly n-1.",
  ["One list of scores is enough.", "People are numbered 1..n."],
  '''
class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        score = [0] * (n + 1)
        for a, b in trust:
            score[a] -= 1  #> trusting someone: can't be the judge
            score[b] += 1
        for i in range(1, n + 1):
            if score[i] == n - 1:
                return i
        return -1
''', [([2, [[1, 2]]], 2), ([3, [[1, 3], [2, 3]]], 3), ([3, [[1, 3], [2, 3], [3, 1]]], -1)], 'O(n+E)', 'O(n)')

P('shortest-path-binary-matrix', 'Shortest Path Through a Maze', 1091, 'Medium', T,
  "Grid of 0 (open) and 1 (wall). Move in 8 directions. Shortest path length from top-left to bottom-right? -1 if blocked.",
  "BFS from the start; the first time you reach the end is the shortest.",
  ["Count cells, not moves: start has length 1.", "Mark cells visited when you push them."],
  '''
class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] or grid[n - 1][n - 1]:
            return -1
        q = deque([(0, 0, 1)])
        grid[0][0] = 1  #> visited
        while q:
            r, c, d = q.popleft()
            if r == n - 1 and c == n - 1:
                return d
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                        grid[nr][nc] = 1
                        q.append((nr, nc, d + 1))
        return -1
''', [([[[0, 1], [1, 0]]], 2), ([[[0, 0, 0], [1, 1, 0], [1, 1, 0]]], 4), ([[[1, 0, 0], [1, 1, 0], [1, 1, 0]]], -1)], 'O(n²)', 'O(n²)')

P('alien-dictionary', 'Alien Alphabet', 269, 'Hard', T,
  "Words are sorted in an alien alphabet. Figure out a valid letter order. Return '' if the order is impossible.",
  "Compare neighbouring words: the first different letter gives a rule 'x before y'. Then topological sort the letters.",
  ["A longer word before its own prefix is impossible.", "Kahn's algorithm on letters."],
  '''
class Solution:
    def alienOrder(self, words: List[str]) -> str:
        after = {c: set() for w in words for c in w}
        need = {c: 0 for c in after}
        for a, b in zip(words, words[1:]):
            for x, y in zip(a, b):
                if x != y:
                    if y not in after[x]:
                        after[x].add(y)  #> rule: x comes before y
                        need[y] += 1
                    break
            else:
                if len(a) > len(b):
                    return ''
        q = deque(c for c in need if need[c] == 0)
        out = []
        while q:
            c = q.popleft()
            out.append(c)
            for d in after[c]:
                need[d] -= 1
                if need[d] == 0:
                    q.append(d)
        return ''.join(out) if len(out) == len(need) else ''
''', [([["wrt", "wrf", "er", "ett", "rftt"]], "wertf"), ([["z", "x"]], "zx"), ([["z", "x", "z"]], "")], 'O(total letters)', 'O(26)')
