from pb import P
GR, IN, MB = 'Greedy', 'Intervals', 'Math & Bits'

P('jump-game', 'Can You Hop to the End?', 55, 'Medium', GR,
  "Each number says the max jump from that spot. Starting at spot 0, can you reach the last spot?",
  "Track the farthest spot reachable so far. If you're ever standing beyond it, you're stuck.",
  ["farthest = max(farthest, i + nums[i])", "One pass."],
  '''
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        far = 0
        for i, x in enumerate(nums):
            if i > far:
                return False  #> can't even reach this spot
            far = max(far, i + x)
        return True
''', [([[2, 3, 1, 1, 4]], True), ([[3, 2, 1, 0, 4]], False)], 'O(n)', 'O(1)')

P('jump-game-ii', 'Fewest Hops to the End', 45, 'Medium', GR,
  "Same hopping game; reaching the end is guaranteed. Fewest jumps?",
  "Think in 'rounds' like BFS: each round covers a range of spots; the next round reaches up to the farthest jump from that range.",
  ["When you reach the end of the current round's range, jump++.", "Greedy BFS."],
  '''
class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps = 0
        end = 0  #> edge of what this many jumps can reach
        far = 0
        for i in range(len(nums) - 1):
            far = max(far, i + nums[i])
            if i == end:
                jumps += 1  #> must jump again
                end = far
        return jumps
''', [([[2, 3, 1, 1, 4]], 2), ([[2, 3, 0, 1, 4]], 2)], 'O(n)', 'O(1)')

P('gas-station', 'Road Trip Gas Stations', 134, 'Medium', GR,
  "Gas stations in a circle. gas[i] is fuel you get, cost[i] is fuel to reach the next. Which start lets you go all the way round? -1 if none.",
  "If total gas < total cost, impossible. Otherwise, whenever your tank goes negative, the start must be after this point.",
  ["Reset the tank and start at i+1 when it goes negative.", "There's at most one answer."],
  '''
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if sum(gas) < sum(cost):
            return -1
        tank = 0
        start = 0
        for i in range(len(gas)):
            tank += gas[i] - cost[i]
            if tank < 0:
                start = i + 1  #> nobody before here can be the start
                tank = 0
        return start
''', [([[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], 3), ([[2, 3, 4], [3, 4, 3]], -1)], 'O(n)', 'O(1)')

P('hand-of-straights', 'Group Cards Into Runs', 846, 'Medium', GR,
  "Can the cards be split into groups of size k, each made of consecutive numbers?",
  "Always start a run at the smallest card left. Use counts to take the run k cards long.",
  ["Sorted unique values + Counter.", "Missing a card in the run → False."],
  '''
class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        count = Counter(hand)
        for x in sorted(count):
            n = count[x]
            if n:
                for y in range(x, x + groupSize):  #> build n runs starting at x
                    if count[y] < n:
                        return False
                    count[y] -= n
        return True
''', [([[1, 2, 3, 6, 2, 3, 4, 7, 8], 3], True), ([[1, 2, 3, 4, 5], 4], False)], 'O(n log n)', 'O(n)')

P('partition-labels', 'Cut Into Letter-Unique Parts', 763, 'Medium', GR,
  "Cut the string into as many parts as possible so each letter appears in only one part. Return part sizes.",
  "Record each letter's last position. Walk along stretching the part's end to the farthest last position seen.",
  ["When i reaches the end of the part, cut.", "last = {ch: i}."],
  '''
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last = {ch: i for i, ch in enumerate(s)}
        res = []
        start = end = 0
        for i, ch in enumerate(s):
            end = max(end, last[ch])  #> this part must reach here
            if i == end:
                res.append(end - start + 1)  #> safe to cut
                start = i + 1
        return res
''', [(["ababcbacadefegdehijhklij"], [9, 7, 8]), (["eccbbbbdec"], [10])], 'O(n)', 'O(26)')

P('valid-parenthesis-string', 'Brackets With Wildcards', 678, 'Medium', GR,
  "'*' can be '(', ')' or nothing. Can the string be valid?",
  "Track a range [lo, hi] of how many '(' could be open. '*' widens the range.",
  ["hi < 0 → too many ')'.", "Clamp lo at 0; valid if lo == 0 at the end."],
  '''
class Solution:
    def checkValidString(self, s: str) -> bool:
        lo = hi = 0  #> min and max open brackets possible
        for ch in s:
            if ch == '(':
                lo += 1; hi += 1
            elif ch == ')':
                lo -= 1; hi -= 1
            else:
                lo -= 1; hi += 1
            if hi < 0:
                return False
            lo = max(lo, 0)
        return lo == 0
''', [(["()"], True), (["(*)"], True), (["(*))"], True), ([")("], False)], 'O(n)', 'O(1)')

P('assign-cookies', 'Hand Out Cookies', 455, 'Easy', GR,
  "Each kid needs a cookie at least size g[i]. Each cookie s[j] can go to one kid. Max happy kids?",
  "Sort both. Give the smallest cookie that works to the least greedy kid.",
  ["Two pointers over sorted lists.", "Too small a cookie? Try the next cookie."],
  '''
class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort(); s.sort()
        kid = 0
        for c in s:
            if kid < len(g) and c >= g[kid]:
                kid += 1  #> this kid is happy
        return kid
''', [([[1, 2, 3], [1, 1]], 1), ([[1, 2], [1, 2, 3]], 2)], 'O(n log n)', 'O(1)')

P('merge-intervals', 'Merge Overlapping Time Blocks', 56, 'Medium', IN,
  "Merge all overlapping intervals.",
  "Sort by start. If a block starts before the last merged block ends, stretch the last one. Otherwise start a new one.",
  ["Sorting puts overlaps next to each other.", "Compare with res[-1]."],
  '''
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        res = []
        for s, e in intervals:
            if res and s <= res[-1][1]:
                res[-1][1] = max(res[-1][1], e)  #> overlaps: stretch it
            else:
                res.append([s, e])
        return res
''', [([[[1, 3], [2, 6], [8, 10], [15, 18]]], [[1, 6], [8, 10], [15, 18]]), ([[[1, 4], [4, 5]]], [[1, 5]])], 'O(n log n)', 'O(n)')

P('insert-interval', 'Squeeze In a New Block', 57, 'Medium', IN,
  "Sorted, non-overlapping intervals. Insert a new one and merge if needed.",
  "Three phases: copy blocks ending before it, merge every block overlapping it, copy the rest.",
  ["Overlap: block start <= new end.", "Grow the new block while merging."],
  '''
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        res = []
        s, e = newInterval
        i = 0
        while i < len(intervals) and intervals[i][1] < s:
            res.append(intervals[i]); i += 1  #> entirely before
        while i < len(intervals) and intervals[i][0] <= e:
            s = min(s, intervals[i][0])  #> overlapping: absorb it
            e = max(e, intervals[i][1]); i += 1
        res.append([s, e])
        res.extend(intervals[i:])
        return res
''', [([[[1, 3], [6, 9]], [2, 5]], [[1, 5], [6, 9]]), ([[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]], [[1, 2], [3, 10], [12, 16]])], 'O(n)', 'O(n)')

P('non-overlapping-intervals', 'Fewest Blocks to Remove', 435, 'Medium', IN,
  "Remove the fewest intervals so the rest don't overlap.",
  "Sort by END time. Keep each block that starts after the last kept one ends; the rest must go.",
  ["Ending early leaves the most room.", "Count removals."],
  '''
class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        end = -inf
        removed = 0
        for s, e in intervals:
            if s >= end:
                end = e  #> keep it
            else:
                removed += 1  #> overlaps: throw it out
        return removed
''', [([[[1, 2], [2, 3], [3, 4], [1, 3]]], 1), ([[[1, 2], [1, 2], [1, 2]]], 2)], 'O(n log n)', 'O(1)')

P('meeting-rooms', 'Can One Person Attend Every Meeting?', 252, 'Easy', IN,
  "Do any meetings overlap?",
  "Sort by start; check each meeting starts after the previous ends.",
  ["Just compare neighbours after sorting.", "Touching (end == start) is fine."],
  '''
class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals.sort()
        for (s1, e1), (s2, e2) in zip(intervals, intervals[1:]):
            if s2 < e1:
                return False  #> clash!
        return True
''', [([[[0, 30], [5, 10], [15, 20]]], False), ([[[7, 10], [2, 4]]], True)], 'O(n log n)', 'O(1)')

P('meeting-rooms-ii', 'How Many Rooms Needed?', 253, 'Medium', IN,
  "Fewest meeting rooms so every meeting has a room.",
  "Sort by start. A min-heap holds end times of rooms in use. If the earliest-ending room is free, reuse it.",
  ["Heap size = rooms in use.", "Answer = biggest heap size."],
  '''
class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort()
        ends = []  #> end times of busy rooms
        for s, e in intervals:
            if ends and ends[0] <= s:
                heappop(ends)  #> that room just freed up
            heappush(ends, e)
        return len(ends)
''', [([[[0, 30], [5, 10], [15, 20]]], 2), ([[[7, 10], [2, 4]]], 1)], 'O(n log n)', 'O(n)')

P('single-number', 'The Lonely Number', 136, 'Easy', MB,
  "Every number appears twice except one. Find it with O(1) memory.",
  "XOR magic: x ^ x = 0 and x ^ 0 = x. XOR everything; pairs cancel out.",
  ["Order doesn't matter for XOR.", "Start with 0."],
  '''
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for x in nums:
            res ^= x  #> pairs cancel to 0
        return res
''', [([[2, 2, 1]], 1), ([[4, 1, 2, 1, 2]], 4)], 'O(n)', 'O(1)')

P('number-of-1-bits', 'Count the 1s in Binary', 191, 'Easy', MB,
  "How many 1s are in the binary form of n?",
  "n & (n - 1) removes the lowest 1. Count how many times you can do it.",
  ["Or check n & 1 and shift right.", "Each loop removes exactly one 1."],
  '''
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1  #> knock out the lowest 1
            count += 1
        return count
''', [([11], 3), ([128], 1), ([0], 0)], 'O(bits)', 'O(1)')

P('counting-bits', 'Count 1s for Every Number', 338, 'Easy', MB,
  "For every number 0..n, how many 1s in its binary form?",
  "bits[i] = bits[i >> 1] + (i & 1). Shifting right drops the last bit.",
  ["Reuse earlier answers (it's DP!).", "i >> 1 is i // 2."],
  '''
class Solution:
    def countBits(self, n: int) -> List[int]:
        bits = [0] * (n + 1)
        for i in range(1, n + 1):
            bits[i] = bits[i >> 1] + (i & 1)  #> half of me, plus my last bit
        return bits
''', [([2], [0, 1, 1]), ([5], [0, 1, 1, 2, 1, 2])], 'O(n)', 'O(n)')

P('missing-number', 'The Missing Number', 268, 'Easy', MB,
  "Numbers 0..n with one missing. Find it.",
  "The full total would be n(n+1)/2. Subtract what you have.",
  ["Or XOR every index and value.", "Gauss's formula."],
  '''
class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)  #> expected total - actual total
''', [([[3, 0, 1]], 2), ([[0, 1]], 2), ([[9, 6, 4, 2, 3, 5, 7, 0, 1]], 8)], 'O(n)', 'O(1)')

P('reverse-integer', 'Flip the Digits', 7, 'Medium', MB,
  "Reverse the digits of a 32-bit integer. If it overflows, return 0.",
  "Pop the last digit (x % 10), push it onto the result (res * 10 + d). Handle the sign separately.",
  ["32-bit range: -2³¹ .. 2³¹-1.", "Work with abs(x)."],
  '''
class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        x = abs(x)
        res = 0
        while x:
            res = res * 10 + x % 10  #> move the last digit over
            x //= 10
        res *= sign
        return res if -2**31 <= res <= 2**31 - 1 else 0
''', [([123], 321), ([-123], -321), ([120], 21), ([1534236469], 0)], 'O(digits)', 'O(1)')

P('pow-x-n', 'Fast Power', 50, 'Medium', MB,
  "Compute x to the power n (n can be negative) quickly.",
  "Squaring trick: x^10 = (x^5)², x^5 = x · x^4. Halve n each step.",
  ["Negative n: 1 / x^-n.", "O(log n) multiplications."],
  '''
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x, n = 1 / x, -n
        res = 1.0
        while n:
            if n & 1:
                res *= x  #> this bit of n is on
            x *= x  #> square for the next bit
            n >>= 1
        return res
''', [([2.0, 10], 1024.0), ([2.1, 3], 9.261), ([2.0, -2], 0.25)], 'O(log n)', 'O(1)', cmp='float')

P('happy-number', 'Happy Number', 202, 'Easy', MB,
  "Replace a number by the sum of the squares of its digits, again and again. Happy if it reaches 1; unhappy if it loops forever.",
  "Remember numbers you've seen. Seeing one again means a loop.",
  ["A set catches the loop.", "Tortoise-and-hare also works!"],
  '''
class Solution:
    def isHappy(self, n: int) -> bool:
        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = sum(int(d) ** 2 for d in str(n))  #> digits squared, summed
        return n == 1
''', [([19], True), ([2], False)], 'O(log n)', 'O(log n)')

P('rotate-image', 'Turn the Picture 90°', 48, 'Medium', MB,
  "Rotate a square grid 90° clockwise in place.",
  "Two easy moves: flip across the diagonal (transpose), then reverse each row.",
  ["Transpose: swap m[r][c] with m[c][r] for c > r.", "Then row.reverse()."],
  '''
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for r in range(n):
            for c in range(r + 1, n):
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]  #> flip on the diagonal
        for row in matrix:
            row.reverse()  #> mirror left-right
''', [([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]])], 'O(n²)', 'O(1)', inplace=0)

P('spiral-matrix', 'Read the Grid in a Spiral', 54, 'Medium', MB,
  "Return all values of the grid in clockwise spiral order.",
  "Keep four walls: top, bottom, left, right. Walk along each wall, then move it inward.",
  ["Stop when walls cross.", "Check walls again before the bottom and left passes."],
  '''
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []
        top, bot, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
        while top <= bot and left <= right:
            for c in range(left, right + 1): res.append(matrix[top][c])
            top += 1  #> top row done
            for r in range(top, bot + 1): res.append(matrix[r][right])
            right -= 1
            if top <= bot:
                for c in range(right, left - 1, -1): res.append(matrix[bot][c])
                bot -= 1
            if left <= right:
                for r in range(bot, top - 1, -1): res.append(matrix[r][left])
                left += 1
        return res
''', [([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [1, 2, 3, 6, 9, 8, 7, 4, 5]), ([[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])], 'O(R·C)', 'O(1)')

P('set-matrix-zeroes', 'Zero Out Rows and Columns', 73, 'Medium', MB,
  "If a cell is 0, set its whole row and column to 0. In place.",
  "First find which rows and columns have a zero, then wipe them.",
  ["Sets of rows and columns.", "Don't wipe while scanning or zeros spread."],
  '''
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        rows, cols = set(), set()
        for r, row in enumerate(matrix):
            for c, v in enumerate(row):
                if v == 0:
                    rows.add(r); cols.add(c)  #> remember, don't wipe yet
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if r in rows or c in cols:
                    matrix[r][c] = 0
''', [([[[1, 1, 1], [1, 0, 1], [1, 1, 1]]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]])], 'O(R·C)', 'O(R+C)', inplace=0)

P('fizzbuzz', 'FizzBuzz', 412, 'Easy', MB,
  "For 1..n: 'Fizz' for multiples of 3, 'Buzz' for 5, 'FizzBuzz' for both, else the number as text.",
  "Check 15 first (both), then 3, then 5.",
  ["% gives the remainder.", "Order of checks matters."],
  '''
class Solution:
    def fizzBuzz(self, n: int) -> List[str]:
        res = []
        for i in range(1, n + 1):
            if i % 15 == 0: res.append('FizzBuzz')
            elif i % 3 == 0: res.append('Fizz')
            elif i % 5 == 0: res.append('Buzz')
            else: res.append(str(i))
        return res
''', [([5], ["1", "2", "Fizz", "4", "Buzz"]), ([15], ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"])], 'O(n)', 'O(1)')

P('plus-one', 'Add One to a Digit List', 66, 'Easy', MB,
  "A number is stored as a list of digits. Add one.",
  "Start from the last digit. 9 becomes 0 and carries; anything else just goes up by one and you're done.",
  ["All 9s? Put a 1 in front.", "Walk right to left."],
  '''
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits  #> no carry, done
            digits[i] = 0  #> 9 rolls over to 0
        return [1] + digits
''', [([[1, 2, 3]], [1, 2, 4]), ([[9, 9]], [1, 0, 0])], 'O(n)', 'O(1)')

P('sort-array-merge', 'Sort It Yourself (Merge Sort)', 912, 'Medium', 'Sorting',
  "Sort the list without using sort(). Use merge sort: split in half, sort each half, zip them together.",
  "Divide and conquer. A list of 0 or 1 items is already sorted. Merging two sorted lists is easy with two pointers.",
  ["Recursion depth is log n.", "Merge: take the smaller front each time."],
  '''
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums  #> tiny lists are already sorted
        mid = len(nums) // 2
        left = self.sortArray(nums[:mid])
        right = self.sortArray(nums[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        return merged + left[i:] + right[j:]
''', [([[5, 2, 3, 1]], [1, 2, 3, 5]), ([[5, 1, 1, 2, 0, 0]], [0, 0, 1, 1, 2, 5])], 'O(n log n)', 'O(n)')

P('bubble-sort', 'Bubble Sort', None, 'Easy', 'Sorting',
  "Sort the list by repeatedly swapping neighbours that are in the wrong order. Big numbers 'bubble' to the end.",
  "After each full pass, the biggest unsorted number is in its final place. Stop early if a pass makes no swaps.",
  ["Compare nums[j] and nums[j+1].", "Each pass can ignore the already-sorted tail."],
  '''
class Solution:
    def bubbleSort(self, nums: List[int]) -> List[int]:
        n = len(nums)
        for end in range(n - 1, 0, -1):
            swapped = False
            for j in range(end):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]  #> wrong order: swap!
                    swapped = True
            if not swapped:
                break  #> nothing moved: already sorted
        return nums
''', [([[5, 1, 4, 2, 8]], [1, 2, 4, 5, 8]), ([[1, 2, 3]], [1, 2, 3])], 'O(n²)', 'O(1)', bars=True)

P('insertion-sort', 'Insertion Sort', None, 'Easy', 'Sorting',
  "Sort like sorting cards in your hand: take the next card and slide it left until it's in the right spot.",
  "Everything left of i is sorted. Shift bigger numbers right to make a gap, drop the card in.",
  ["Great for nearly-sorted lists.", "Inner loop walks left."],
  '''
class Solution:
    def insertionSort(self, nums: List[int]) -> List[int]:
        for i in range(1, len(nums)):
            card = nums[i]  #> pick up the next card
            j = i - 1
            while j >= 0 and nums[j] > card:
                nums[j + 1] = nums[j]  #> shift bigger cards right
                j -= 1
            nums[j + 1] = card  #> drop it in the gap
        return nums
''', [([[5, 2, 4, 6, 1, 3]], [1, 2, 3, 4, 5, 6]), ([[1]], [1])], 'O(n²)', 'O(1)', bars=True)

P('quick-sort', 'Quick Sort', None, 'Medium', 'Sorting',
  "Sort by picking a 'pivot', putting smaller numbers to its left and bigger to its right, then sorting each side.",
  "Lomuto partition: walk with j, and keep i as the edge of the 'smaller than pivot' zone.",
  ["Pivot = last element here.", "Recurse on both sides of the pivot's final spot."],
  '''
class Solution:
    def quickSort(self, nums: List[int]) -> List[int]:
        def sort(lo, hi):
            if lo >= hi:
                return
            pivot = nums[hi]
            i = lo  #> next slot for a small number
            for j in range(lo, hi):
                if nums[j] < pivot:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
            nums[i], nums[hi] = nums[hi], nums[i]  #> pivot lands in its final spot
            sort(lo, i - 1)
            sort(i + 1, hi)
        sort(0, len(nums) - 1)
        return nums
''', [([[3, 6, 8, 10, 1, 2, 1]], [1, 1, 2, 3, 6, 8, 10]), ([[2, 1]], [1, 2])], 'O(n log n) avg', 'O(log n)', bars=True)

P('selection-sort', 'Selection Sort', None, 'Easy', 'Sorting',
  "Find the smallest number and swap it to the front. Then the next smallest to spot 1. And so on.",
  "For each position i, scan the rest for the minimum and swap it into i.",
  ["Always n²/2 comparisons.", "Only n swaps: handy when swaps are expensive."],
  '''
class Solution:
    def selectionSort(self, nums: List[int]) -> List[int]:
        n = len(nums)
        for i in range(n):
            m = i
            for j in range(i + 1, n):
                if nums[j] < nums[m]:
                    m = j  #> new smallest found
            nums[i], nums[m] = nums[m], nums[i]
        return nums
''', [([[64, 25, 12, 22, 11]], [11, 12, 22, 25, 64])], 'O(n²)', 'O(1)', bars=True)
