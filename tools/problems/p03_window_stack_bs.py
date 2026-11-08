from pb import P
W, S, B = 'Sliding Window', 'Stack', 'Binary Search'

P('longest-substring-no-repeat', 'Longest Stretch With No Repeats', 3, 'Medium', W,
  "Find the length of the longest chunk of the string where no letter repeats.",
  "A stretchy window: grow the right edge. If the new letter is already inside, shrink from the left until it isn't.",
  ["A set holds the letters currently inside the window.", "Window size = r - l + 1."],
  '''
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        inside = set()
        l = 0
        best = 0
        for r in range(len(s)):
            while s[r] in inside:  #> repeat! shrink from the left
                inside.remove(s[l])
                l += 1
            inside.add(s[r])  #> grow the window
            best = max(best, r - l + 1)
        return best
''', [(["abcabcbb"], 3), (["bbbbb"], 1), (["pwwkew"], 3), ([""], 0)], 'O(n)', 'O(k)')

P('max-sum-subarray-k', 'Best Chunk of Size K', 643, 'Easy', W,
  "Find the biggest average of any k numbers in a row.",
  "Slide a fixed-size window: add the number coming in, subtract the number going out.",
  ["Don't re-add k numbers each time.", "Sum changes by (new - old)."],
  '''
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        s = sum(nums[:k])  #> first window
        best = s
        for r in range(k, len(nums)):
            s += nums[r] - nums[r - k]  #> one in, one out
            best = max(best, s)
        return best / k
''', [([[1, 12, -5, -6, 50, 3], 4], 12.75), ([[5], 1], 5.0)], 'O(n)', 'O(1)', cmp='float')

P('char-replacement', 'Make the Longest Same-Letter Run', 424, 'Medium', W,
  "You may change up to k letters. What's the longest run of one repeated letter you can make?",
  "In a window, letters to change = window size - count of its most common letter. If that's more than k, shrink.",
  ["Track counts inside the window.", "Keep the max count seen; it only needs to grow."],
  '''
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        l = 0
        top = 0
        best = 0
        for r in range(len(s)):
            count[s[r]] = count.get(s[r], 0) + 1
            top = max(top, count[s[r]])  #> most common letter in the window
            while (r - l + 1) - top > k:  #> too many letters to change
                count[s[l]] -= 1
                l += 1
            best = max(best, r - l + 1)
        return best
''', [(["ABAB", 2], 4), (["AABABBA", 1], 4)], 'O(n)', 'O(26)')

P('permutation-in-string', 'Scrambled Word Hiding Inside', 567, 'Medium', W,
  "Does s2 contain a chunk that is a rearrangement of s1?",
  "Slide a window the size of s1 over s2 and compare letter counts.",
  ["Two count dictionaries that are equal = same letters.", "Window size is fixed: len(s1)."],
  '''
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        need = Counter(s1)
        win = Counter()
        k = len(s1)
        for r, ch in enumerate(s2):
            win[ch] += 1  #> letter enters the window
            if r >= k:
                win[s2[r - k]] -= 1  #> letter leaves the window
                if win[s2[r - k]] == 0:
                    del win[s2[r - k]]
            if win == need:
                return True
        return False
''', [(["ab", "eidbaooo"], True), (["ab", "eidboaoo"], False)], 'O(n)', 'O(26)')

P('min-window-substring', 'Smallest Window With Everything', 76, 'Hard', W,
  "Find the shortest chunk of s that contains every letter of t (with repeats). Return '' if none.",
  "Grow right until the window has everything. Then shrink left as much as possible while it still has everything. Record the best.",
  ["Track how many letter types are fully satisfied.", "Shrink only while still valid."],
  '''
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)
        missing = len(t)  #> letters still needed
        l = 0
        best = (0, float('inf'))
        for r, ch in enumerate(s):
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1
            while missing == 0:  #> window has everything: try to shrink
                if r - l < best[1] - best[0]:
                    best = (l, r)
                need[s[l]] += 1
                if need[s[l]] > 0:
                    missing += 1
                l += 1
        return '' if best[1] == float('inf') else s[best[0]:best[1] + 1]
''', [(["ADOBECODEBANC", "ABC"], "BANC"), (["a", "a"], "a"), (["a", "aa"], "")], 'O(n)', 'O(k)')

P('sliding-window-max', 'Biggest in Every Window', 239, 'Hard', W,
  "Slide a window of size k across the list. Report the biggest number in each window.",
  "Keep a line (deque) of positions whose numbers are decreasing. The front is always the biggest. Kick out smaller ones from the back.",
  ["A smaller number behind a bigger newer number can never win again.", "Pop the front when it slides out of the window."],
  '''
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        q = deque()  #> positions, their numbers go big -> small
        res = []
        for i, x in enumerate(nums):
            while q and nums[q[-1]] < x:
                q.pop()  #> smaller ones behind me can never win
            q.append(i)
            if q[0] <= i - k:
                q.popleft()  #> front fell out of the window
            if i >= k - 1:
                res.append(nums[q[0]])
        return res
''', [([[1, 3, -1, -3, 5, 3, 6, 7], 3], [3, 3, 5, 5, 6, 7]), ([[1], 1], [1])], 'O(n)', 'O(k)')

P('min-size-subarray-sum', 'Shortest Chunk Reaching a Target', 209, 'Medium', W,
  "Positive numbers. Find the shortest chunk whose sum is at least target. 0 if none.",
  "Grow the window until the sum is big enough, then shrink from the left while it still is.",
  ["All positive means shrinking always lowers the sum.", "Record length each time it's valid."],
  '''
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l = 0
        s = 0
        best = float('inf')
        for r in range(len(nums)):
            s += nums[r]
            while s >= target:  #> big enough: try shrinking
                best = min(best, r - l + 1)
                s -= nums[l]
                l += 1
        return 0 if best == float('inf') else best
''', [([7, [2, 3, 1, 2, 4, 3]], 2), ([4, [1, 4, 4]], 1), ([11, [1, 1, 1, 1]], 0)], 'O(n)', 'O(1)')

P('valid-parentheses', 'Matching Brackets', 20, 'Easy', S,
  "Is every bracket ( [ { closed by the right partner, in the right order?",
  "Push open brackets on a stack (like a pile of plates). A closing bracket must match the plate on top.",
  ["The most recent opener must close first.", "At the end the pile must be empty."],
  '''
class Solution:
    def isValid(self, s: str) -> bool:
        pair = {')': '(', ']': '[', '}': '{'}
        stack = []
        for ch in s:
            if ch in pair:
                if not stack or stack[-1] != pair[ch]:
                    return False  #> top plate isn't my partner
                stack.pop()
            else:
                stack.append(ch)  #> opener: put a plate on the pile
        return not stack
''', [(["()"], True), (["()[]{}"], True), (["(]"], False), (["([)]"], False), (["{[]}"], True)], 'O(n)', 'O(n)')

P('min-stack', 'Stack That Knows Its Minimum', 155, 'Medium', S,
  "Build a stack with push, pop, top, and getMin — all instant.",
  "Store pairs: (value, smallest value at the time it was pushed). The top pair always knows the current minimum.",
  ["Each plate remembers the min below it.", "Popping automatically restores the old min."],
  '''
class MinStack:
    def __init__(self):
        self.st = []  #> pairs of (value, min so far)

    def push(self, val: int) -> None:
        m = min(val, self.st[-1][1]) if self.st else val
        self.st.append((val, m))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        return self.st[-1][1]
''', [([["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"], [[], [-2], [0], [-3], [], [], [], []]], [None, None, None, None, -3, None, 0, -2])], 'O(1) each', 'O(n)', mode='design')

P('eval-rpn', 'Calculator With No Brackets', 150, 'Medium', S,
  "Evaluate math written in 'postfix' form: numbers first, then the operator. Like ['2','1','+','3','*'] = (2+1)*3.",
  "Numbers go on the stack. An operator pops two numbers, combines them, and pushes the result.",
  ["Order matters for - and /: second pop is the left side.", "Division rounds toward zero: int(a / b)."],
  '''
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        st = []
        for t in tokens:
            if t in '+-*/':
                b = st.pop()  #> right side
                a = st.pop()  #> left side
                if t == '+': st.append(a + b)
                elif t == '-': st.append(a - b)
                elif t == '*': st.append(a * b)
                else: st.append(int(a / b))
            else:
                st.append(int(t))
        return st[0]
''', [([["2", "1", "+", "3", "*"]], 9), ([["4", "13", "5", "/", "+"]], 6)], 'O(n)', 'O(n)')

P('daily-temperatures', 'Wait for a Warmer Day', 739, 'Medium', S,
  "For each day, how many days until a warmer one? 0 if it never gets warmer.",
  "Keep a stack of days still waiting. When a warmer day comes, it answers everyone on the stack who is colder.",
  ["The stack holds temperatures going down.", "This pattern is called a 'monotonic stack'."],
  '''
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        res = [0] * len(temperatures)
        st = []  #> days still waiting for warmth
        for i, t in enumerate(temperatures):
            while st and temperatures[st[-1]] < t:
                j = st.pop()  #> day j finally got a warmer day
                res[j] = i - j
            st.append(i)
        return res
''', [([[73, 74, 75, 71, 69, 72, 76, 73]], [1, 1, 4, 2, 1, 1, 0, 0]), ([[30, 60, 90]], [1, 1, 0])], 'O(n)', 'O(n)', bars=True)

P('generate-parentheses', 'All Valid Bracket Strings', 22, 'Medium', S,
  "List every valid way to arrange n pairs of brackets.",
  "Build the string one char at a time. Add '(' if you have some left; add ')' only if it would close something.",
  ["Track how many opens and closes you've used.", "closes can never exceed opens."],
  '''
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res = []
        def build(cur, opens, closes):
            if len(cur) == 2 * n:
                res.append(cur)  #> complete string!
                return
            if opens < n:
                build(cur + '(', opens + 1, closes)
            if closes < opens:
                build(cur + ')', opens, closes + 1)
        build('', 0, 0)
        return res
''', [([3], ["((()))", "(()())", "(())()", "()(())", "()()()"]), ([1], ["()"])], 'O(4^n/√n)', 'O(n)', cmp='sorted')

P('car-fleet', 'Car Convoys', 853, 'Medium', S,
  "Cars drive toward a target. A faster car that catches a slower one gets stuck behind it (a fleet). How many fleets arrive?",
  "Sort cars from closest to the target. Compute each car's arrival time. If a car would arrive sooner than the fleet in front, it joins it.",
  ["time = (target - position) / speed", "Keep a stack of fleet arrival times."],
  '''
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)  #> closest to target first
        st = []
        for p, s in cars:
            t = (target - p) / s
            if not st or t > st[-1]:
                st.append(t)  #> slower than the fleet ahead: new fleet
        return len(st)
''', [([12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]], 3), ([10, [3], [3]], 1)], 'O(n log n)', 'O(n)')

P('largest-rectangle-histogram', 'Biggest Rectangle in the Bars', 84, 'Hard', S,
  "Bars of different heights stand side by side. What's the biggest rectangle you can draw inside them?",
  "Keep a stack of bars with rising heights. When a shorter bar arrives, pop taller bars: each popped bar's rectangle can't stretch further right.",
  ["Each bar is the 'shortest' of some rectangle.", "A popped bar can extend left to where its stack entry started."],
  '''
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        st = []  #> (start index, height)
        best = 0
        for i, h in enumerate(heights + [0]):
            start = i
            while st and st[-1][1] > h:
                j, hh = st.pop()  #> this bar can't go further right
                best = max(best, hh * (i - j))
                start = j  #> I can stretch back to where it started
            st.append((start, h))
        return best
''', [([[2, 1, 5, 6, 2, 3]], 10), ([[2, 4]], 4)], 'O(n)', 'O(n)', bars=True)

P('backspace-compare', 'Typing With Backspaces', 844, 'Easy', S,
  "'#' means backspace. Do two typed strings end up the same?",
  "Type each string onto a stack. '#' pops the last letter.",
  ["Backspace on an empty screen does nothing.", "Compare the final stacks."],
  '''
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def typed(x):
            st = []
            for ch in x:
                if ch == '#':
                    if st:
                        st.pop()  #> erase the last letter
                else:
                    st.append(ch)
            return st
        return typed(s) == typed(t)
''', [(["ab#c", "ad#c"], True), (["ab##", "c#d#"], True), (["a#c", "b"], False)], 'O(n)', 'O(n)')

P('binary-search', 'Guess the Spot', 704, 'Easy', B,
  "Find target in a sorted list and return its position, or -1.",
  "Look at the middle. Too small? Throw away the left half. Too big? Throw away the right half. Repeat.",
  ["Each guess halves the search space.", "Stop when lo > hi."],
  '''
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2  #> peek at the middle
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1  #> answer is on the right
            else:
                hi = mid - 1  #> answer is on the left
        return -1
''', [([[-1, 0, 3, 5, 9, 12], 9], 4), ([[-1, 0, 3, 5, 9, 12], 2], -1)], 'O(log n)', 'O(1)')

P('search-2d-matrix', 'Search a Sorted Grid', 74, 'Medium', B,
  "Each row is sorted, and each row starts bigger than the previous row ends. Is target in the grid?",
  "Pretend the grid is one long sorted list. Position k lives at row k // cols, column k % cols.",
  ["One binary search over rows*cols spots.", "Convert index -> (row, col)."],
  '''
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        R, C = len(matrix), len(matrix[0])
        lo, hi = 0, R * C - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            v = matrix[mid // C][mid % C]  #> unfold the grid
            if v == target:
                return True
            if v < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return False
''', [([[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3], True), ([[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13], False)], 'O(log(mn))', 'O(1)')

P('koko-bananas', 'Slowest Speed to Finish Snacks', 875, 'Medium', B,
  "Piles of bananas, h hours. Eating speed k means k bananas per hour (one pile at a time). What's the slowest k that finishes in time?",
  "Binary search on the ANSWER (the speed). For a guessed speed, count hours needed. Too slow? Go faster.",
  ["Hours for a pile = ceil(pile / k).", "Speeds range from 1 to max(piles)."],
  '''
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        lo, hi = 1, max(piles)
        while lo < hi:
            k = (lo + hi) // 2  #> try this speed
            hours = sum((p + k - 1) // k for p in piles)
            if hours <= h:
                hi = k  #> fast enough, try slower
            else:
                lo = k + 1  #> too slow, go faster
        return lo
''', [([[3, 6, 7, 11], 8], 4), ([[30, 11, 23, 4, 20], 5], 30), ([[30, 11, 23, 4, 20], 6], 23)], 'O(n log m)', 'O(1)')

P('find-min-rotated', 'Lowest Point in a Rotated List', 153, 'Medium', B,
  "A sorted list got rotated (like [3,4,5,1,2]). Find the smallest number in O(log n).",
  "Compare the middle with the right end. If middle is bigger, the drop is to the right. Otherwise it's at mid or left.",
  ["The minimum is where the 'drop' happens.", "Compare with nums[hi]."],
  '''
class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1  #> the drop is to the right of mid
            else:
                hi = mid  #> mid could be the minimum
        return nums[lo]
''', [([[3, 4, 5, 1, 2]], 1), ([[4, 5, 6, 7, 0, 1, 2]], 0), ([[11, 13, 15, 17]], 11)], 'O(log n)', 'O(1)')

P('search-rotated', 'Search a Rotated List', 33, 'Medium', B,
  "Find target in a rotated sorted list. Return its index or -1.",
  "One half is always properly sorted. Check if target fits in the sorted half; if so go there, else go to the other half.",
  ["Compare nums[lo] with nums[mid] to see which half is sorted.", "Then check if target lies inside that half's range."],
  '''
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:  #> left half is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:  #> right half is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1
''', [([[4, 5, 6, 7, 0, 1, 2], 0], 4), ([[4, 5, 6, 7, 0, 1, 2], 3], -1), ([[1], 0], -1)], 'O(log n)', 'O(1)')

P('first-bad-version', 'First Broken Version', 278, 'Easy', B,
  "Versions 1..n. Once a version is bad, all later ones are bad too. Find the first bad one. (Here: bad is given as a number so we can test.)",
  "Binary search for the first spot where isBad becomes True.",
  ["When mid is bad, the answer is mid or earlier.", "When mid is good, the answer is after mid."],
  '''
class Solution:
    def firstBadVersion(self, n: int, bad: int) -> int:
        isBad = lambda v: v >= bad  #> pretend API
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if isBad(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
''', [([5, 4], 4), ([1, 1], 1), ([100, 37], 37)], 'O(log n)', 'O(1)')

P('time-based-kv', 'Time-Travel Notebook', 981, 'Medium', B,
  "Store values with timestamps. get(key, t) returns the value set at the latest time ≤ t.",
  "For each key keep a list of (time, value) in time order. Binary search for the last time ≤ t.",
  ["Timestamps arrive increasing, so lists stay sorted.", "bisect_right helps find 'last ≤ t'."],
  '''
class TimeMap:
    def __init__(self):
        self.store = {}  #> key -> list of (time, value)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        arr = self.store.get(key, [])
        lo, hi = 0, len(arr) - 1
        res = ''
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid][0] <= timestamp:
                res = arr[mid][1]  #> good candidate, look for later
                lo = mid + 1
            else:
                hi = mid - 1
        return res
''', [([["TimeMap", "set", "get", "get", "set", "get", "get"], [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]], [None, None, "bar", "bar", None, "bar2", "bar2"])], 'O(log n) get', 'O(n)', mode='design')

P('median-two-sorted', 'Middle of Two Sorted Lists', 4, 'Hard', B,
  "Find the median of two sorted lists together, in O(log(m+n)).",
  "Binary search a 'cut' in the smaller list. The cut in the other list is forced. A good cut has everything on the left ≤ everything on the right.",
  ["Always search the shorter list.", "Use -inf / +inf at the edges."],
  '''
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        if len(A) > len(B):
            A, B = B, A
        total = len(A) + len(B)
        half = total // 2
        lo, hi = 0, len(A)
        while True:
            i = (lo + hi) // 2  #> take i from A
            j = half - i  #> and the rest from B
            Al = A[i - 1] if i > 0 else -inf
            Ar = A[i] if i < len(A) else inf
            Bl = B[j - 1] if j > 0 else -inf
            Br = B[j] if j < len(B) else inf
            if Al <= Br and Bl <= Ar:  #> perfect cut
                if total % 2:
                    return float(min(Ar, Br))
                return (max(Al, Bl) + min(Ar, Br)) / 2
            if Al > Br:
                hi = i - 1
            else:
                lo = i + 1
''', [([[1, 3], [2]], 2.0), ([[1, 2], [3, 4]], 2.5)], 'O(log(min(m,n)))', 'O(1)', cmp='float')

P('sqrt-x', 'Square Root (Rounded Down)', 69, 'Easy', B,
  "Return the square root of x rounded down, without using ** or sqrt.",
  "Binary search for the biggest number whose square is ≤ x.",
  ["Answer is between 0 and x.", "mid*mid vs x decides the direction."],
  '''
class Solution:
    def mySqrt(self, x: int) -> int:
        lo, hi = 0, x
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if mid * mid <= x:
                ans = mid  #> fits, try bigger
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
''', [([4], 2), ([8], 2), ([0], 0)], 'O(log x)', 'O(1)')
