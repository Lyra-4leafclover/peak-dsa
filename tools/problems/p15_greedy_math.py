from pb import P
G, I, M = 'Greedy', 'Intervals', 'Math & Bits'

P('merge-triplets', 'Build the Target Triplet', 1899, 'Medium', G,
  "You can merge triplets by taking the max of each position. Can you end up with exactly the target triplet?",
  "Ignore any triplet with a number bigger than the target's. From the rest, check every target position is reached by someone.",
  ["A too-big number can never be undone."],
  '''
class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        got = set()
        for t in triplets:
            if all(t[i] <= target[i] for i in range(3)):  #> safe to use
                for i in range(3):
                    if t[i] == target[i]:
                        got.add(i)
        return len(got) == 3
''', [([[[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]], True), ([[[3, 4, 5], [4, 5, 6]], [3, 2, 5]], False)], 'O(n)', 'O(1)')

P('min-arrows-balloons', 'Fewest Arrows to Pop Balloons', 452, 'Medium', G,
  "Balloons are ranges on a line. An arrow at x pops every balloon covering x. Fewest arrows?",
  "Sort by end. Shoot at the end of the first balloon; skip every balloon that covers that spot.",
  ["A new arrow is needed only when a balloon starts after the last shot."],
  '''
class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort(key=lambda p: p[1])
        arrows, shot = 0, float('-inf')
        for s, e in points:
            if s > shot:
                arrows += 1
                shot = e  #> shoot at this balloon's end
        return arrows
''', [([[[10, 16], [2, 8], [1, 6], [7, 12]]], 2), ([[[1, 2], [3, 4], [5, 6], [7, 8]]], 4)], 'O(n log n)', 'O(1)')

P('dota2-senate', 'Senate Voting Battle', 649, 'Medium', G,
  "Senators from two parties (R and D) take turns banning one opponent. Who wins?",
  "Two queues of positions. The earlier senator bans the other and goes to the back (position + n).",
  ["Compare the fronts of both queues each round."],
  '''
from collections import deque
class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        n = len(senate)
        r = deque(i for i, c in enumerate(senate) if c == 'R')
        d = deque(i for i, c in enumerate(senate) if c == 'D')
        while r and d:
            a, b = r.popleft(), d.popleft()
            if a < b:
                r.append(a + n)  #> R acts first, bans D, waits for next round
            else:
                d.append(b + n)
        return 'Radiant' if r else 'Dire'
''', [(["RD"], "Radiant"), (["RDD"], "Dire")], 'O(n)', 'O(n)')

P('lemonade-change', 'Lemonade Stand Change', 860, 'Easy', G,
  "Lemonade costs $5. Customers pay with $5, $10 or $20 in order. Can you always give correct change?",
  "Count your $5 and $10 bills. For $20, prefer giving $10+$5 (save the fives).",
  ["Fives are the most useful bill."],
  '''
class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        five = ten = 0
        for b in bills:
            if b == 5:
                five += 1
            elif b == 10:
                five, ten = five - 1, ten + 1
            elif ten:
                five, ten = five - 1, ten - 1  #> keep fives when possible
            else:
                five -= 3
            if five < 0:
                return False
        return True
''', [([[5, 5, 5, 10, 20]], True), ([[5, 5, 10, 10, 20]], False)], 'O(n)', 'O(1)')

P('queue-by-height', 'Line Up by Height', 406, 'Medium', G,
  "Each person is [height, k] where k = how many people in front are at least as tall. Rebuild the line.",
  "Sort tallest first (ties: smaller k first). Insert each person at position k: shorter people later can't disturb them.",
  ["Tall people don't notice short ones."],
  '''
class Solution:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        people.sort(key=lambda p: (-p[0], p[1]))
        line = []
        for p in people:
            line.insert(p[1], p)  #> exactly k taller people ahead
        return line
''', [([[[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]], [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]])], 'O(n²)', 'O(n)')

P('candy', 'Fair Candy Handout', 135, 'Hard', G,
  "Kids in a row have ratings. Everyone gets at least 1 candy, and a kid with a higher rating than a neighbour gets more than that neighbour. Fewest candies?",
  "Two passes: left-to-right fixes the left neighbour rule, right-to-left fixes the right one (keep the max).",
  ["Start everyone at 1."],
  '''
class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        c = [1] * n
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                c[i] = c[i - 1] + 1  #> beat the left neighbour
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                c[i] = max(c[i], c[i + 1] + 1)
        return sum(c)
''', [([[1, 0, 2]], 5), ([[1, 2, 2]], 4)], 'O(n)', 'O(n)')

P('stock-ii', 'Stock Trading, Many Deals', 122, 'Medium', G,
  "Buy and sell as often as you like (hold one share at most). Max profit?",
  "Grab every rise: add each positive day-to-day difference.",
  ["Many small wins = one big win."],
  '''
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))  #> take every up-day
''', [([[7, 1, 5, 3, 6, 4]], 7), ([[1, 2, 3, 4, 5]], 4), ([[7, 6, 4, 3, 1]], 0)], 'O(n)', 'O(1)')

P('min-interval-queries', 'Smallest Interval for Each Query', 1851, 'Hard', I,
  "For each query point, find the size of the smallest interval containing it (size = right - left + 1), or -1.",
  "Sort intervals and queries. Sweep queries in order, pushing intervals that started into a heap by size; pop ones that already ended.",
  ["Answer in the original query order."],
  '''
import heapq
class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort()
        h, i, ans = [], 0, {}
        for q in sorted(queries):
            while i < len(intervals) and intervals[i][0] <= q:
                l, r = intervals[i]
                heapq.heappush(h, (r - l + 1, r))  #> started: candidate
                i += 1
            while h and h[0][1] < q:
                heapq.heappop(h)  #> already ended
            ans[q] = h[0][0] if h else -1
        return [ans[q] for q in queries]
''', [([[[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]], [3, 3, 1, 4]), ([[[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]], [2, -1, 4, 6])], 'O((n+q) log n)', 'O(n+q)')

P('palindrome-number', 'Same Number Backwards?', 9, 'Easy', M,
  "Does the number read the same forwards and backwards?",
  "Negative numbers never do. Otherwise rebuild the number backwards digit by digit and compare.",
  ["x % 10 is the last digit, x // 10 drops it."],
  '''
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        rev, n = 0, x
        while n:
            rev = rev * 10 + n % 10  #> move the last digit over
            n //= 10
        return rev == x
''', [([121], True), ([-121], False), ([10], False)], 'O(digits)', 'O(1)')

P('multiply-strings', 'Multiply Big Numbers by Hand', 43, 'Medium', M,
  "Multiply two numbers given as strings, without turning them into ints directly.",
  "School multiplication: digit i times digit j lands in slot i + j + 1. Carry at the end.",
  ["The answer has at most len(a) + len(b) digits."],
  '''
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        res = [0] * (len(num1) + len(num2))
        for i in range(len(num1) - 1, -1, -1):
            for j in range(len(num2) - 1, -1, -1):
                total = res[i + j + 1] + int(num1[i]) * int(num2[j])
                res[i + j + 1] = total % 10  #> keep the ones digit
                res[i + j] += total // 10  #> carry the rest
        s = ''.join(map(str, res)).lstrip('0')
        return s or '0'
''', [(["2", "3"], "6"), (["123", "456"], "56088"), (["0", "52"], "0")], 'O(n·m)', 'O(n+m)')

P('add-binary', 'Add Two Binary Numbers', 67, 'Easy', M,
  "Add two binary strings like \"11\" + \"1\" = \"100\".",
  "Add from the right with a carry, just like normal addition but in base 2.",
  ["digit = total % 2, carry = total // 2."],
  '''
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i, j, carry, out = len(a) - 1, len(b) - 1, 0, []
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += int(a[i]); i -= 1
            if j >= 0:
                total += int(b[j]); j -= 1
            out.append(str(total % 2))  #> write the bit
            carry = total // 2
        return ''.join(reversed(out))
''', [(["11", "1"], "100"), (["1010", "1011"], "10101")], 'O(n)', 'O(n)')

P('add-strings', 'Add Two Big Numbers', 415, 'Easy', M,
  "Add two numbers given as strings without turning them into ints directly.",
  "Column addition from the right with a carry.",
  ["Same as adding binary, but base 10."],
  '''
class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        i, j, carry, out = len(num1) - 1, len(num2) - 1, 0, []
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += int(num1[i]); i -= 1
            if j >= 0:
                total += int(num2[j]); j -= 1
            out.append(str(total % 10))  #> write the digit
            carry = total // 10
        return ''.join(reversed(out))
''', [(["11", "123"], "134"), (["456", "77"], "533"), (["0", "0"], "0")], 'O(n)', 'O(n)')

P('single-number-ii', 'The One That Appears Once (Others Thrice)', 137, 'Medium', M,
  "Every number appears three times except one. Find it.",
  "For each of the 32 bits, count how many numbers have it. Counts not divisible by 3 belong to the loner.",
  ["Handle negatives by fixing the sign bit at the end."],
  '''
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for b in range(32):
            if sum((x >> b) & 1 for x in nums) % 3:
                res |= 1 << b  #> the loner has this bit
        return res - (1 << 32) if res >= 1 << 31 else res
''', [([[2, 2, 3, 2]], 3), ([[0, 1, 0, 1, 0, 1, 99]], 99), ([[-2, -2, 1, 1, 4, 1, 4, 4, -4, -2]], -4)], 'O(32n)', 'O(1)')

P('max-points-on-line', 'Most Points on One Line', 149, 'Hard', M,
  "Given points on a grid, what's the most points that lie on one straight line?",
  "For each point, count the slopes to every other point (as a reduced fraction). The most common slope wins.",
  ["Reduce dy/dx with gcd and fix the sign so equal slopes match."],
  '''
from math import gcd
from collections import Counter
class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        best = 1
        for i, (x1, y1) in enumerate(points):
            slopes = Counter()
            for x2, y2 in points[i + 1:]:
                dx, dy = x2 - x1, y2 - y1
                g = gcd(dx, dy)
                dx, dy = dx // g, dy // g
                if dx < 0 or (dx == 0 and dy < 0):
                    dx, dy = -dx, -dy
                slopes[(dx, dy)] += 1  #> same slope = same line through this point
            if slopes:
                best = max(best, max(slopes.values()) + 1)
        return best
''', [([[[1, 1], [2, 2], [3, 3]]], 3), ([[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]], 4)], 'O(n²)', 'O(n)')

P('factorial-trailing-zeroes', 'Zeros at the End of n!', 172, 'Medium', M,
  "How many zeros are at the end of n! (n factorial)?",
  "Each zero needs a 5 (2s are plentiful). Count multiples of 5, 25, 125, ...",
  ["n // 5 + n // 25 + ..."],
  '''
class Solution:
    def trailingZeroes(self, n: int) -> int:
        count = 0
        while n:
            n //= 5
            count += n  #> how many more fives
        return count
''', [([3], 0), ([5], 1), ([100], 24)], 'O(log n)', 'O(1)')

P('reverse-bits', 'Mirror the Bits', 190, 'Easy', M,
  "Reverse the 32 bits of a number.",
  "Take the last bit of n 32 times and push it onto the result from the right.",
  ["res = (res << 1) | (n & 1)."],
  '''
class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)  #> move the lowest bit over
            n >>= 1
        return res
''', [([43261596], 964176192), ([4294967293], 3221225471)], 'O(32)', 'O(1)')

P('bitwise-and-range', 'AND of a Whole Range', 201, 'Medium', M,
  "AND together every number from left to right. What's the result?",
  "Only the shared leading bits survive. Shift both right until they're equal, then shift back.",
  ["Any bit that changes inside the range becomes 0."],
  '''
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        shift = 0
        while left != right:
            left >>= 1  #> drop bits that differ
            right >>= 1
            shift += 1
        return left << shift
''', [([5, 7], 4), ([0, 0], 0), ([1, 2147483647], 0)], 'O(log n)', 'O(1)')

P('sum-two-integers', 'Add Without +', 371, 'Medium', M,
  "Add two integers without using + or -.",
  "XOR adds without carrying; AND then shift left gives the carry. Repeat until no carry (masking to 32 bits).",
  ["Python ints are endless, so mask with 0xFFFFFFFF."],
  '''
class Solution:
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        while b & mask:
            a, b = a ^ b, (a & b) << 1  #> sum without carry, and the carry
        a &= mask
        return a if a <= 0x7FFFFFFF else ~(a ^ mask)
''', [([1, 2], 3), ([2, 3], 5), ([-1, 1], 0)], 'O(32)', 'O(1)')

P('count-primes', 'Count the Primes', 204, 'Medium', M,
  "How many prime numbers are smaller than n?",
  "Sieve of Eratosthenes: cross out multiples of each prime starting from its square.",
  ["Only go up to √n for the outer loop."],
  '''
class Solution:
    def countPrimes(self, n: int) -> int:
        if n < 3:
            return 0
        prime = [True] * n
        prime[0] = prime[1] = False
        i = 2
        while i * i < n:
            if prime[i]:
                for j in range(i * i, n, i):
                    prime[j] = False  #> a multiple can't be prime
            i += 1
        return sum(prime)
''', [([10], 4), ([0], 0), ([1], 0)], 'O(n log log n)', 'O(n)')

P('detect-squares', 'Spot the Squares', 2013, 'Medium', M,
  "Add points one by one. count(p) asks: how many axis-aligned squares can be made with p and three added points?",
  "Count points in a dict. For a query, try every added point diagonal to it, and multiply the counts of the other two corners.",
  ["A diagonal partner must have |dx| == |dy| > 0."],
  '''
from collections import Counter
class DetectSquares:
    def __init__(self):
        self.pts = Counter()

    def add(self, point: List[int]) -> None:
        self.pts[tuple(point)] += 1

    def count(self, point: List[int]) -> int:
        x, y = point
        total = 0
        for (a, b), c in self.pts.items():
            if abs(a - x) == abs(b - y) and a != x:
                total += c * self.pts[(a, y)] * self.pts[(x, b)]  #> the other two corners
        return total
''', [([["DetectSquares", "add", "add", "add", "count", "count", "add", "count"], [[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]], [None, None, None, None, 1, 0, None, 2])], 'O(n) count', 'O(n)', mode='design')

P('excel-column-number', 'Spreadsheet Column Number', 171, 'Easy', M,
  "A=1, B=2, ..., Z=26, AA=27... Turn a column title into its number.",
  "It's base 26: number = number × 26 + letter value.",
  ["ord(ch) - ord('A') + 1."],
  '''
class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        n = 0
        for ch in columnTitle:
            n = n * 26 + ord(ch) - ord('A') + 1  #> shift left one 'digit'
        return n
''', [(["A"], 1), (["AB"], 28), (["ZY"], 701)], 'O(n)', 'O(1)')

P('happy-power-of-two', 'Is It a Power of Two?', 231, 'Easy', M,
  "Is n equal to 2 to some power?",
  "A power of two has exactly one 1-bit, so n & (n - 1) == 0.",
  ["n must be positive."],
  '''
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and n & (n - 1) == 0  #> removing the only 1-bit leaves zero
''', [([1], True), ([16], True), ([3], False)], 'O(1)', 'O(1)')
