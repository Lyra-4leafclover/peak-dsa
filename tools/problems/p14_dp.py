from pb import P
D1, D2 = '1-D Dynamic Programming', '2-D Dynamic Programming'

P('tribonacci', 'Tribonacci Numbers', 1137, 'Easy', D1,
  "Like Fibonacci but each number is the sum of the previous THREE. T0=0, T1=1, T2=1. Find Tn.",
  "Keep the last three numbers and slide them forward.",
  ["No list needed, just three variables."],
  '''
class Solution:
    def tribonacci(self, n: int) -> int:
        a, b, c = 0, 1, 1
        for _ in range(n):
            a, b, c = b, c, a + b + c  #> slide the window of three
        return a
''', [([4], 4), ([25], 1389537), ([0], 0)], 'O(n)', 'O(1)')

P('perfect-squares', 'Fewest Square Pieces', 279, 'Medium', D1,
  "What's the fewest perfect squares (1, 4, 9, 16...) that add up to n?",
  "dp[i] = 1 + the smallest dp[i - square] over all squares that fit.",
  ["dp[0] = 0."],
  '''
class Solution:
    def numSquares(self, n: int) -> int:
        dp = [0] + [float('inf')] * n
        for i in range(1, n + 1):
            j = 1
            while j * j <= i:
                dp[i] = min(dp[i], dp[i - j * j] + 1)  #> use one square of size j²
                j += 1
        return dp[n]
''', [([12], 3), ([13], 2), ([1], 1)], 'O(n√n)', 'O(n)')

P('integer-break', 'Break a Number for the Biggest Product', 343, 'Medium', D1,
  "Split n into at least two positive whole numbers. What's the biggest product you can make?",
  "dp[i] = best product for i. Try every first piece j: either keep i-j whole or break it further.",
  ["max(j * (i - j), j * dp[i - j])."],
  '''
class Solution:
    def integerBreak(self, n: int) -> int:
        dp = [0, 1] + [0] * (n - 1)
        for i in range(2, n + 1):
            for j in range(1, i):
                dp[i] = max(dp[i], j * (i - j), j * dp[i - j])  #> keep or keep breaking
        return dp[n]
''', [([2], 1), ([10], 36)], 'O(n²)', 'O(n)')

P('combination-sum-iv', 'Ordered Ways to Make a Total', 377, 'Medium', D1,
  "How many ORDERED sequences of the numbers (reuse allowed) add up to target? (1,2) and (2,1) count separately.",
  "dp[t] = sum of dp[t - x] for every number x. Loop totals on the outside.",
  ["dp[0] = 1: one way to make nothing."],
  '''
class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        dp = [1] + [0] * target
        for t in range(1, target + 1):
            for x in nums:
                if x <= t:
                    dp[t] += dp[t - x]  #> end the sequence with x
        return dp[target]
''', [([[1, 2, 3], 4], 7), ([[9], 3], 0)], 'O(target·n)', 'O(target)')

P('delete-and-earn', 'Delete and Earn', 740, 'Medium', D1,
  "Pick a number x to earn x points, but then every x-1 and x+1 is deleted. What's the most you can earn?",
  "Add up the points for each value. Then it's House Robber on the values: you can't take neighbours.",
  ["points[v] = v × count of v."],
  '''
class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        points = [0] * (max(nums) + 1)
        for x in nums:
            points[x] += x
        take, skip = 0, 0
        for p in points:
            take, skip = skip + p, max(take, skip)  #> house robber on values
        return max(take, skip)
''', [([[3, 4, 2]], 6), ([[2, 2, 3, 3, 3, 4]], 9)], 'O(n + max)', 'O(max)')

P('max-circular-subarray', 'Best Stretch on a Circle', 918, 'Medium', D1,
  "The list is a circle. Find the biggest sum of a non-empty stretch (it may wrap around the end).",
  "Answer = max(best normal stretch, total - worst stretch). If everything is negative, use the best normal one.",
  ["Kadane's trick for both max and min."],
  '''
class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        cur_max = cur_min = 0
        best, worst = nums[0], nums[0]
        for x in nums:
            cur_max = max(cur_max + x, x)
            best = max(best, cur_max)
            cur_min = min(cur_min + x, x)
            worst = min(worst, cur_min)
        if best < 0:
            return best  #> all negative
        return max(best, sum(nums) - worst)  #> wrap = everything minus the worst middle
''', [([[1, -2, 3, -2]], 3), ([[5, -3, 5]], 10), ([[-3, -2, -3]], -2)], 'O(n)', 'O(1)')

P('domino-tromino', 'Tile the Hallway', 790, 'Medium', D1,
  "How many ways can you tile a 2×n hallway with 2×1 dominoes and L-shaped trominoes? (Answer mod 10⁹+7.)",
  "The pattern works out to dp[n] = 2·dp[n-1] + dp[n-3].",
  ["dp[0]=1, dp[1]=1, dp[2]=2."],
  '''
class Solution:
    def numTilings(self, n: int) -> int:
        M = 10 ** 9 + 7
        dp = [1, 1, 2] + [0] * n
        for i in range(3, n + 1):
            dp[i] = (2 * dp[i - 1] + dp[i - 3]) % M  #> extend the smaller hallways
        return dp[n]
''', [([3], 5), ([1], 1), ([5], 24)], 'O(n)', 'O(n)')

P('stock-with-fee', 'Stock Trading With a Fee', 714, 'Medium', D1,
  "Buy and sell as often as you like, but every sale costs a fee. Max profit?",
  "Two states each day: holding a share, or not. Update both.",
  ["hold = max(hold, free - price); free = max(free, hold + price - fee)."],
  '''
class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        free, hold = 0, -prices[0]
        for p in prices[1:]:
            free = max(free, hold + p - fee)  #> sell today (or not)
            hold = max(hold, free - p)  #> buy today (or not)
        return free
''', [([[1, 3, 2, 8, 4, 9], 2], 8), ([[1, 3, 7, 5, 10, 3], 3], 6)], 'O(n)', 'O(1)')

P('stock-cooldown', 'Stock Trading With a Rest Day', 309, 'Medium', D1,
  "Buy and sell as often as you like, but after selling you must rest one day. Max profit?",
  "Three states: holding, just sold, resting. Each day updates from yesterday's states.",
  ["You can only buy from the resting state."],
  '''
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        hold, sold, rest = float('-inf'), 0, 0
        for p in prices:
            hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)  #> three moods
        return max(sold, rest)
''', [([[1, 2, 3, 0, 2]], 3), ([[1]], 0)], 'O(n)', 'O(1)')

P('stock-iii', 'Stock Trading, Two Deals Max', 123, 'Hard', D1,
  "You may complete at most two buy-sell deals (one at a time). Max profit?",
  "Track four numbers: best after 1st buy, 1st sell, 2nd buy, 2nd sell.",
  ["Each one builds on the previous."],
  '''
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        b1 = b2 = float('-inf')
        s1 = s2 = 0
        for p in prices:
            b1 = max(b1, -p)
            s1 = max(s1, b1 + p)
            b2 = max(b2, s1 - p)  #> second buy uses first profit
            s2 = max(s2, b2 + p)
        return s2
''', [([[3, 3, 5, 0, 0, 3, 1, 4]], 6), ([[1, 2, 3, 4, 5]], 4), ([[7, 6, 4, 3, 1]], 0)], 'O(n)', 'O(1)')

P('stock-iv', 'Stock Trading, k Deals Max', 188, 'Hard', D1,
  "You may complete at most k buy-sell deals. Max profit?",
  "Same as two deals, but with lists of k buys and k sells.",
  ["buy[j] uses sell[j-1]."],
  '''
class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        buy = [float('-inf')] * (k + 1)
        sell = [0] * (k + 1)
        for p in prices:
            for j in range(1, k + 1):
                buy[j] = max(buy[j], sell[j - 1] - p)  #> j-th buy
                sell[j] = max(sell[j], buy[j] + p)
        return sell[k]
''', [([2, [2, 4, 1]], 2), ([2, [3, 2, 6, 5, 0, 3]], 7)], 'O(n·k)', 'O(k)')

P('longest-palindromic-subsequence', 'Longest Hidden Palindrome', 516, 'Medium', D2,
  "Delete some letters (keeping order) to leave the longest possible palindrome. How long is it?",
  "dp[i][j] = answer for s[i..j]. Equal ends: 2 + inside. Otherwise drop one end.",
  ["Fill from short pieces to long ones."],
  '''
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        dp = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            dp[i][i] = 1
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2  #> matching ends wrap the inside
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        return dp[0][n - 1]
''', [(["bbbab"], 4), (["cbbd"], 2)], 'O(n²)', 'O(n²)')

P('unique-paths-ii', 'Robot Paths Around Rocks', 63, 'Medium', D2,
  "A robot goes only right or down from top-left to bottom-right. 1 = rock. How many paths?",
  "ways[c] = ways from above + ways from the left; a rock cell has 0 ways.",
  ["One row of memory is enough."],
  '''
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        C = len(obstacleGrid[0])
        ways = [1] + [0] * (C - 1)
        for row in obstacleGrid:
            for c in range(C):
                if row[c] == 1:
                    ways[c] = 0  #> rock: no way through
                elif c:
                    ways[c] += ways[c - 1]
        return ways[-1]
''', [([[[0, 0, 0], [0, 1, 0], [0, 0, 0]]], 2), ([[[0, 1], [0, 0]]], 1)], 'O(R·C)', 'O(C)')

P('triangle-min-path', 'Cheapest Path Down the Triangle', 120, 'Medium', D2,
  "Walk from the top of a number triangle to the bottom, moving to one of the two numbers below each step. Smallest total?",
  "Work from the bottom up: each number adds the smaller of its two children.",
  ["The top ends up holding the answer."],
  '''
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        best = triangle[-1][:]
        for row in reversed(triangle[:-1]):
            best = [x + min(best[i], best[i + 1]) for i, x in enumerate(row)]  #> pick the cheaper child
        return best[0]
''', [([[[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]], 11), ([[[-10]]], -10)], 'O(n²)', 'O(n)')

P('maximal-square', 'Biggest Square of Ones', 221, 'Medium', D2,
  "In a grid of '0' and '1', find the area of the biggest square made only of '1's.",
  "dp[r][c] = side of the biggest square ending here = 1 + min(up, left, up-left).",
  ["Area = side²."],
  '''
class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        R, C = len(matrix), len(matrix[0])
        dp = [[0] * (C + 1) for _ in range(R + 1)]
        side = 0
        for r in range(R):
            for c in range(C):
                if matrix[r][c] == '1':
                    dp[r + 1][c + 1] = 1 + min(dp[r][c + 1], dp[r + 1][c], dp[r][c])  #> grow from 3 neighbours
                    side = max(side, dp[r + 1][c + 1])
        return side * side
''', [([[["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]], 4), ([[["0", "1"], ["1", "0"]]], 1), ([[["0"]]], 0)], 'O(R·C)', 'O(R·C)')

P('distinct-subsequences', 'Count Hidden Copies', 115, 'Hard', D2,
  "How many ways can you delete letters from s to leave exactly t?",
  "dp[j] = ways to build t[:j]. Walk s; for each letter, update j from right to left: if it matches t[j-1], add dp[j-1].",
  ["dp[0] = 1 (empty t)."],
  '''
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        dp = [1] + [0] * len(t)
        for ch in s:
            for j in range(len(t), 0, -1):
                if t[j - 1] == ch:
                    dp[j] += dp[j - 1]  #> use this letter as t's j-th letter
        return dp[-1]
''', [(["rabbbit", "rabbit"], 3), (["babgbag", "bag"], 5)], 'O(n·m)', 'O(m)')

P('regex-matching', 'Pattern Matching With . and *', 10, 'Hard', D2,
  "Does the pattern match the WHOLE string? '.' matches any letter, 'x*' means zero or more x's.",
  "dp[i][j] = does s[i:] match p[j:]? With a '*' next, either skip 'x*' or use it once and stay.",
  ["Fill from the end backwards."],
  '''
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
        dp[len(s)][len(p)] = True
        for i in range(len(s), -1, -1):
            for j in range(len(p) - 1, -1, -1):
                first = i < len(s) and p[j] in (s[i], '.')
                if j + 1 < len(p) and p[j + 1] == '*':
                    dp[i][j] = dp[i][j + 2] or (first and dp[i + 1][j])  #> skip x* or eat one letter
                else:
                    dp[i][j] = first and dp[i + 1][j + 1]
        return dp[0][0]
''', [(["aa", "a"], False), (["aa", "a*"], True), (["ab", ".*"], True), (["mississippi", "mis*is*p*."], False)], 'O(n·m)', 'O(n·m)')

P('burst-balloons', 'Pop the Balloons', 312, 'Hard', D2,
  "Popping balloon i earns left × i × right (its current neighbours; outside counts as 1). Pop all of them. Max coins?",
  "Think about which balloon is popped LAST in a range. dp[l][r] = best for the open range (l, r).",
  ["Add a 1 at both ends.", "The last balloon k in (l, r) earns v[l]·v[k]·v[r]."],
  '''
class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        v = [1] + nums + [1]
        n = len(v)
        dp = [[0] * n for _ in range(n)]
        for gap in range(2, n):
            for l in range(n - gap):
                r = l + gap
                for k in range(l + 1, r):
                    dp[l][r] = max(dp[l][r], dp[l][k] + v[l] * v[k] * v[r] + dp[k][r])  #> k pops last
        return dp[0][n - 1]
''', [([[3, 1, 5, 8]], 167), ([[1, 5]], 10)], 'O(n³)', 'O(n²)')

P('longest-increasing-path', 'Longest Uphill Walk in a Grid', 329, 'Hard', D2,
  "Moving up/down/left/right, always to a bigger number, what's the longest walk?",
  "DFS with a memo: best(r, c) = 1 + the best of bigger neighbours.",
  ["No need for a visited set: you can't go in circles when always climbing."],
  '''
from functools import lru_cache
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        R, C = len(matrix), len(matrix[0])
        @lru_cache(None)
        def best(r, c):
            out = 1
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] > matrix[r][c]:
                    out = max(out, 1 + best(nr, nc))  #> climb to a bigger neighbour
            return out
        return max(best(r, c) for r in range(R) for c in range(C))
''', [([[[9, 9, 4], [6, 6, 8], [2, 1, 1]]], 4), ([[[3, 4, 5], [3, 2, 6], [2, 2, 1]]], 4), ([[[1]]], 1)], 'O(R·C)', 'O(R·C)')

P('job-scheduling', 'Best Set of Gigs', 1235, 'Hard', D1,
  "Each job has a start, an end and a profit. Pick jobs that don't overlap (one may start exactly when another ends). Max profit?",
  "Sort by end time. dp[i] = best using the first i jobs: skip job i, or take it plus the best that ends by its start (binary search).",
  ["bisect_right on end times finds the compatible jobs."],
  '''
from bisect import bisect_right
class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))
        ends = [e for e, _, _ in jobs]
        dp = [0] * (len(jobs) + 1)
        for i, (e, s, p) in enumerate(jobs):
            k = bisect_right(ends, s, 0, i)  #> jobs finished before this one starts
            dp[i + 1] = max(dp[i], dp[k] + p)
        return dp[-1]
''', [([[1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]], 120), ([[1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]], 150)], 'O(n log n)', 'O(n)')

P('ones-and-zeroes', 'Packing Bits in a Bag', 474, 'Medium', D2,
  "Each string uses some 0s and 1s. With at most m zeros and n ones, how many strings can you pick?",
  "Knapsack with two limits: dp[z][o] = most strings using z zeros and o ones. Loop limits downward.",
  ["Going downward stops a string from being used twice."],
  '''
class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for s in strs:
            z, o = s.count('0'), s.count('1')
            for i in range(m, z - 1, -1):
                for j in range(n, o - 1, -1):
                    dp[i][j] = max(dp[i][j], dp[i - z][j - o] + 1)  #> take this string
        return dp[m][n]
''', [([["10", "0001", "111001", "1", "0"], 5, 3], 4), ([["10", "0", "1"], 1, 1], 2)], 'O(k·m·n)', 'O(m·n)')

P('min-path-falling', 'Cheapest Fall Through the Grid', 931, 'Medium', D2,
  "Start anywhere in the top row and fall to the bottom, each step going down, down-left or down-right. Smallest total?",
  "Each cell adds the cheapest of the three cells above it.",
  ["Answer = min of the last row."],
  '''
class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        n = len(matrix)
        prev = matrix[0][:]
        for r in range(1, n):
            prev = [matrix[r][c] + min(prev[max(c - 1, 0):c + 2]) for c in range(n)]  #> cheapest of the 3 above
        return min(prev)
''', [([[[2, 1, 3], [6, 5, 4], [7, 8, 9]]], 13), ([[[-19, 57], [-40, -5]]], -59)], 'O(n²)', 'O(n)')

P('wiggle-subsequence', 'Longest Zigzag Sequence', 376, 'Medium', D1,
  "Pick numbers (keeping order) so the differences alternate between going up and going down. Longest such pick?",
  "Track the longest pick ending on an up-step and on a down-step.",
  ["An up-step extends a down-ending pick."],
  '''
class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        up = down = 1
        for a, b in zip(nums, nums[1:]):
            if b > a:
                up = down + 1  #> going up after a down
            elif b < a:
                down = up + 1
        return max(up, down)
''', [([[1, 7, 4, 9, 2, 5]], 6), ([[1, 17, 5, 10, 13, 15, 10, 5, 16, 8]], 7), ([[1, 2, 3, 4, 5, 6, 7, 8, 9]], 2)], 'O(n)', 'O(1)')
