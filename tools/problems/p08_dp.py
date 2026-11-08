from pb import P
D1, D2 = '1-D Dynamic Programming', '2-D Dynamic Programming'

P('climbing-stairs', 'Climbing Stairs', 70, 'Easy', D1,
  "You can climb 1 or 2 steps at a time. How many different ways can you reach step n?",
  "To land on step n you came from step n-1 or n-2. So ways(n) = ways(n-1) + ways(n-2). Save answers instead of recomputing.",
  ["Write down the first few: 1, 2, 3, 5, 8… look familiar?", "Only the last two numbers matter."],
  '''
class Solution:
    def climbStairs(self, n: int) -> int:
        a, b = 1, 1  #> ways to reach step 0 and step 1
        for _ in range(n - 1):
            a, b = b, a + b  #> next = sum of the two before
        return b
''', [([2], 2), ([3], 3), ([5], 8)], 'O(n)', 'O(1)')

P('fib-memo', 'Fibonacci With a Memory', 509, 'Easy', D1,
  "F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2). Compute F(n). Watch how a memory (memo) stops repeated work!",
  "Plain recursion recomputes the same values again and again. A dictionary of saved answers makes each one computed once.",
  ["Check the memo before computing.", "Store the answer before returning."],
  '''
class Solution:
    def fib(self, n: int) -> int:
        memo = {}
        def f(k):
            if k < 2:
                return k
            if k in memo:
                return memo[k]  #> already know this one!
            memo[k] = f(k - 1) + f(k - 2)
            return memo[k]
        return f(n)
''', [([4], 3), ([10], 55), ([0], 0)], 'O(n)', 'O(n)')

P('min-cost-stairs', 'Cheapest Way Up the Stairs', 746, 'Easy', D1,
  "Each step has a cost to stand on. Start at step 0 or 1, climb 1 or 2 at a time. Cheapest way past the top?",
  "cheapest(i) = cost[i] + min(cheapest(i-1), cheapest(i-2)). The top is just past the last step.",
  ["Build answers from the bottom up.", "Answer = min of the last two."],
  '''
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        a, b = cost[0], cost[1]
        for c in cost[2:]:
            a, b = b, c + min(a, b)  #> cheapest way to stand here
        return min(a, b)
''', [([[10, 15, 20]], 15), ([[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]], 6)], 'O(n)', 'O(1)')

P('house-robber', 'Sneaky Robber', 198, 'Medium', D1,
  "Houses in a row with money. You can't rob two neighbours. Most money?",
  "At each house: rob it (its money + best up to two houses back) or skip it (best up to the previous house).",
  ["Only two numbers to carry along.", "best = max(skip, rob)."],
  '''
class Solution:
    def rob(self, nums: List[int]) -> int:
        prev2, prev1 = 0, 0  #> best two houses back, best one house back
        for x in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + x)  #> skip vs rob
        return prev1
''', [([[1, 2, 3, 1]], 4), ([[2, 7, 9, 3, 1]], 12)], 'O(n)', 'O(1)', bars=True)

P('house-robber-ii', 'Sneaky Robber on a Circle', 213, 'Medium', D1,
  "Same as before, but the houses are in a circle: the first and last are neighbours.",
  "You can't take both the first and the last. So solve twice: without the first, and without the last.",
  ["Reuse the straight-line robber.", "One house? Just take it."],
  '''
class Solution:
    def rob(self, nums: List[int]) -> int:
        def line(arr):
            a, b = 0, 0
            for x in arr:
                a, b = b, max(b, a + x)
            return b
        if len(nums) == 1:
            return nums[0]
        return max(line(nums[1:]), line(nums[:-1]))  #> drop first OR drop last
''', [([[2, 3, 2]], 3), ([[1, 2, 3, 1]], 4), ([[1, 2, 3]], 3)], 'O(n)', 'O(1)')

P('longest-palindromic-substring', 'Longest Mirror Chunk', 5, 'Medium', D1,
  "Find the longest chunk of the string that reads the same backwards.",
  "Every palindrome has a centre. Try each centre (a letter, or the gap between two letters) and expand outwards while it mirrors.",
  ["2n-1 centres.", "Expand while s[l] == s[r]."],
  '''
class Solution:
    def longestPalindrome(self, s: str) -> str:
        best = ''
        for c in range(len(s)):
            for l, r in ((c, c), (c, c + 1)):  #> odd and even centres
                while l >= 0 and r < len(s) and s[l] == s[r]:
                    l -= 1
                    r += 1
                if r - l - 1 > len(best):
                    best = s[l + 1:r]
        return best
''', [(["babad"], "bab"), (["cbbd"], "bb"), (["a"], "a")], 'O(n²)', 'O(1)')

P('palindromic-substrings', 'Count Mirror Chunks', 647, 'Medium', D1,
  "Count how many chunks of the string are palindromes.",
  "Expand around every centre; every successful expansion is one more palindrome.",
  ["Same trick as the longest one.", "Count instead of keeping the best."],
  '''
class Solution:
    def countSubstrings(self, s: str) -> int:
        count = 0
        for c in range(len(s)):
            for l, r in ((c, c), (c, c + 1)):
                while l >= 0 and r < len(s) and s[l] == s[r]:
                    count += 1  #> found one more palindrome
                    l -= 1
                    r += 1
        return count
''', [(["abc"], 3), (["aaa"], 6)], 'O(n²)', 'O(1)')

P('decode-ways', 'Secret Number Messages', 91, 'Medium', D1,
  "A=1, B=2 … Z=26. How many ways can a digit string be decoded into letters?",
  "ways(i) = ways(i-1) if the single digit is valid (not 0) + ways(i-2) if the two digits make 10..26.",
  ["A '0' alone is never valid.", "Only two previous answers needed."],
  '''
class Solution:
    def numDecodings(self, s: str) -> int:
        prev2, prev1 = 1, 1 if s[0] != '0' else 0
        for i in range(1, len(s)):
            cur = 0
            if s[i] != '0':
                cur += prev1  #> read one digit
            if 10 <= int(s[i - 1:i + 1]) <= 26:
                cur += prev2  #> read two digits
            prev2, prev1 = prev1, cur
        return prev1
''', [(["12"], 2), (["226"], 3), (["06"], 0)], 'O(n)', 'O(1)')

P('coin-change', 'Fewest Coins', 322, 'Medium', D1,
  "Coins of certain sizes (unlimited). Fewest coins to make the amount exactly? -1 if impossible.",
  "best[x] = 1 + min(best[x - coin]) over all coins. Build from 0 up to the amount.",
  ["best[0] = 0.", "Start everything else at infinity."],
  '''
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        best = [0] + [inf] * amount  #> fewest coins for each total
        for x in range(1, amount + 1):
            for c in coins:
                if c <= x and best[x - c] + 1 < best[x]:
                    best[x] = best[x - c] + 1  #> use coin c last
        return best[amount] if best[amount] != inf else -1
''', [([[1, 2, 5], 11], 3), ([[2], 3], -1), ([[1], 0], 0)], 'O(amount·coins)', 'O(amount)')

P('max-product-subarray', 'Biggest Product Chunk', 152, 'Medium', D1,
  "Find the continuous chunk with the biggest product.",
  "Negatives flip big and small! Track both the biggest and the smallest product ending here.",
  ["A very negative number times a negative becomes very positive.", "Swap max/min when x < 0."],
  '''
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        hi = lo = best = nums[0]
        for x in nums[1:]:
            if x < 0:
                hi, lo = lo, hi  #> negative flips big and small
            hi = max(x, hi * x)
            lo = min(x, lo * x)
            best = max(best, hi)
        return best
''', [([[2, 3, -2, 4]], 6), ([[-2, 0, -1]], 0), ([[-2, 3, -4]], 24)], 'O(n)', 'O(1)')

P('word-break', 'Split Into Dictionary Words', 139, 'Medium', D1,
  "Can the string be split into words from the dictionary (words reusable)?",
  "ok[i] = can the first i letters be split? ok[i] is True if some ok[j] is True and s[j:i] is a word.",
  ["ok[0] = True (empty string).", "Check every split point j < i."],
  '''
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        ok = [True] + [False] * len(s)
        for i in range(1, len(s) + 1):
            for j in range(i):
                if ok[j] and s[j:i] in words:
                    ok[i] = True  #> first i letters can be split
                    break
        return ok[len(s)]
''', [(["leetcode", ["leet", "code"]], True), (["applepenapple", ["apple", "pen"]], True), (["catsandog", ["cats", "dog", "sand", "and", "cat"]], False)], 'O(n²)', 'O(n)')

P('longest-increasing-subsequence', 'Longest Rising Pick', 300, 'Medium', D1,
  "Pick numbers (in order, skipping allowed) so each is bigger than the last. Longest possible?",
  "Keep 'tails': tails[k] = smallest possible ending of a rising pick of length k+1. Binary search where each number goes.",
  ["Simpler O(n²) DP: lis[i] = 1 + max(lis[j]) for j<i with nums[j]<nums[i].", "bisect_left finds the spot."],
  '''
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []
        for x in nums:
            i = bisect_left(tails, x)  #> where x fits
            if i == len(tails):
                tails.append(x)  #> longest pick grows
            else:
                tails[i] = x  #> a better (smaller) ending
        return len(tails)
''', [([[10, 9, 2, 5, 3, 7, 101, 18]], 4), ([[0, 1, 0, 3, 2, 3]], 4), ([[7, 7, 7]], 1)], 'O(n log n)', 'O(n)')

P('partition-equal-subset', 'Split Into Two Equal Piles', 416, 'Medium', D1,
  "Can you split the numbers into two piles with equal sums?",
  "Total must be even. Then: can some numbers add up to total/2? Keep a set of reachable sums.",
  ["Each number either joins the pile or not.", "A set of sums grows as you go."],
  '''
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        goal = total // 2
        sums = {0}  #> sums we can make so far
        for x in nums:
            sums |= {s + x for s in sums if s + x <= goal}
            if goal in sums:
                return True
        return goal in sums
''', [([[1, 5, 11, 5]], True), ([[1, 2, 3, 5]], False)], 'O(n·sum)', 'O(sum)')

P('max-subarray', 'Best Chunk Sum (Kadane)', 53, 'Medium', D1,
  "Find the continuous chunk with the biggest sum.",
  "Kadane: walk along keeping the best chunk ending here. If it ever goes negative, start fresh.",
  ["cur = max(x, cur + x)", "Track the best cur."],
  '''
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        cur = best = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)  #> extend the chunk or start fresh
            best = max(best, cur)
        return best
''', [([[-2, 1, -3, 4, -1, 2, 1, -5, 4]], 6), ([[1]], 1), ([[5, 4, -1, 7, 8]], 23)], 'O(n)', 'O(1)', bars=True)

P('unique-paths', 'Robot Paths in a Grid', 62, 'Medium', D2,
  "A robot at the top-left of an m×n grid moves only right or down. How many paths to the bottom-right?",
  "Paths to a cell = paths from above + paths from the left. Fill the grid row by row.",
  ["First row and first column are all 1.", "You only need one row at a time."],
  '''
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[1] * n for _ in range(m)]
        for r in range(1, m):
            for c in range(1, n):
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]  #> from above + from the left
        return dp[m - 1][n - 1]
''', [([3, 7], 28), ([3, 2], 3)], 'O(m·n)', 'O(m·n)')

P('longest-common-subsequence', 'Longest Shared Pick', 1143, 'Medium', D2,
  "Longest sequence of letters that appears (in order, skipping allowed) in both words.",
  "Grid dp[i][j] = answer for the first i letters of a and first j of b. Same letter: diagonal + 1. Otherwise: best of up or left.",
  ["Add an extra row/column of zeros.", "Classic 2-D DP."],
  '''
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        a, b = text1, text2
        dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1  #> letters match!
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[len(a)][len(b)]
''', [(["abcde", "ace"], 3), (["abc", "abc"], 3), (["abc", "def"], 0)], 'O(m·n)', 'O(m·n)')

P('edit-distance', 'Fewest Typing Fixes', 72, 'Medium', D2,
  "Fewest single-letter inserts, deletes or replaces to turn word1 into word2.",
  "dp[i][j] = fixes for first i letters vs first j letters. Same letter: free (diagonal). Else 1 + min(insert, delete, replace).",
  ["Row 0 / column 0 = all inserts / deletes.", "Three neighbours to look at."],
  '''
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        a, b = word1, word2
        dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
        for i in range(len(a) + 1):
            dp[i][0] = i
        for j in range(len(b) + 1):
            dp[0][j] = j
        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]  #> no fix needed
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[len(a)][len(b)]
''', [(["horse", "ros"], 3), (["intention", "execution"], 5)], 'O(m·n)', 'O(m·n)')

P('coin-change-ii', 'Ways to Make Change', 518, 'Medium', D2,
  "How many different coin combinations make the amount? (Order doesn't matter.)",
  "Loop coins on the OUTSIDE so each combination is counted once. ways[x] += ways[x - coin].",
  ["ways[0] = 1.", "Swapping the loops would count orders."],
  '''
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        ways = [1] + [0] * amount
        for c in coins:  #> coins outside: no double counting
            for x in range(c, amount + 1):
                ways[x] += ways[x - c]
        return ways[amount]
''', [([5, [1, 2, 5]], 4), ([3, [2]], 0), ([10, [10]], 1)], 'O(amount·coins)', 'O(amount)')

P('target-sum', 'Plus or Minus to Hit Target', 494, 'Medium', D2,
  "Put + or - before every number. How many ways reach the target?",
  "Memo on (index, current total). Each number branches into + and -.",
  ["lru_cache / a dict makes it fast.", "Base case: end of list, total == target?"],
  '''
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        memo = {}
        def go(i, total):
            if i == len(nums):
                return 1 if total == target else 0
            if (i, total) in memo:
                return memo[(i, total)]
            memo[(i, total)] = go(i + 1, total + nums[i]) + go(i + 1, total - nums[i])
            return memo[(i, total)]
        return go(0, 0)
''', [([[1, 1, 1, 1, 1], 3], 5), ([[1], 1], 1)], 'O(n·sum)', 'O(n·sum)')

P('interleaving-string', 'Shuffle Two Words Together', 97, 'Medium', D2,
  "Can s3 be made by shuffling s1 and s2 together while keeping each one's letter order?",
  "dp[i][j] = can the first i of s1 and first j of s2 make the first i+j of s3?",
  ["Lengths must add up.", "Come from the top (used s1) or the left (used s2)."],
  '''
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1) + len(s2) != len(s3):
            return False
        dp = [[False] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        dp[0][0] = True
        for i in range(len(s1) + 1):
            for j in range(len(s2) + 1):
                if i and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                    dp[i][j] = True  #> last letter came from s1
                if j and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                    dp[i][j] = True  #> last letter came from s2
        return dp[len(s1)][len(s2)]
''', [(["aabcc", "dbbca", "aadbbcbcac"], True), (["aabcc", "dbbca", "aadbbbaccc"], False)], 'O(m·n)', 'O(m·n)')

P('min-path-sum', 'Cheapest Walk Through the Grid', 64, 'Medium', D2,
  "Move only right or down from top-left to bottom-right. Minimise the sum of the numbers you step on.",
  "Each cell's best = its value + the cheaper of (above, left).",
  ["Edges only have one way in.", "Can update the grid in place."],
  '''
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        R, C = len(grid), len(grid[0])
        for r in range(R):
            for c in range(C):
                if r == 0 and c == 0:
                    continue
                up = grid[r - 1][c] if r else inf
                left = grid[r][c - 1] if c else inf
                grid[r][c] += min(up, left)  #> cheapest way to get here
        return grid[R - 1][C - 1]
''', [([[[1, 3, 1], [1, 5, 1], [4, 2, 1]]], 7), ([[[1, 2, 3], [4, 5, 6]]], 12)], 'O(R·C)', 'O(1)')

P('knapsack-01', 'Pack the Backpack', None, 'Medium', D2,
  "Items with weights and values. Backpack holds capacity weight. Max total value? (Each item once.)",
  "best[w] = best value with capacity w. For each item, go through capacities from BIG to small so it's used once.",
  ["The classic 0/1 knapsack.", "Backwards loop = no reuse."],
  '''
class Solution:
    def knapsack(self, weights: List[int], values: List[int], capacity: int) -> int:
        best = [0] * (capacity + 1)
        for wt, val in zip(weights, values):
            for w in range(capacity, wt - 1, -1):  #> big to small: use item once
                best[w] = max(best[w], best[w - wt] + val)
        return best[capacity]
''', [([[1, 3, 4, 5], [1, 4, 5, 7], 7], 9), ([[2], [3], 1], 0)], 'O(n·W)', 'O(W)')
