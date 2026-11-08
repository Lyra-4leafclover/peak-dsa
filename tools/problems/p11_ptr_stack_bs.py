from pb import P
TP, SW, ST, BS = 'Two Pointers', 'Sliding Window', 'Stack', 'Binary Search'

P('three-sum-closest', 'Three Numbers Near the Target', 16, 'Medium', TP,
  "Pick three numbers whose sum is as close as possible to the target. Return that sum.",
  "Sort. Fix one number, then squeeze two pointers from both ends of the rest, keeping the closest sum.",
  ["Too small? Move the left pointer right. Too big? Move the right pointer left."],
  '''
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        best = nums[0] + nums[1] + nums[2]
        for i in range(len(nums) - 2):
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if abs(s - target) < abs(best - target):
                    best = s  #> closer than before
                if s < target:
                    l += 1
                elif s > target:
                    r -= 1
                else:
                    return s
        return best
''', [([[-1, 2, 1, -4], 1], 2), ([[0, 0, 0], 1], 0)], 'O(n²)', 'O(1)')

P('four-sum', 'Four Numbers That Add Up', 18, 'Medium', TP,
  "Find every different group of four numbers that adds up to the target.",
  "Sort. Two loops fix the first two numbers; two pointers find the last two. Skip repeats.",
  ["Same as 3-sum with one more loop.", "Skip equal neighbours to avoid duplicate groups."],
  '''
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n, out = len(nums), []
        for a in range(n):
            if a and nums[a] == nums[a - 1]:
                continue
            for b in range(a + 1, n):
                if b > a + 1 and nums[b] == nums[b - 1]:
                    continue
                l, r = b + 1, n - 1
                while l < r:
                    s = nums[a] + nums[b] + nums[l] + nums[r]
                    if s == target:
                        out.append([nums[a], nums[b], nums[l], nums[r]])  #> a match!
                        l += 1
                        while l < r and nums[l] == nums[l - 1]:
                            l += 1
                    elif s < target:
                        l += 1
                    else:
                        r -= 1
        return out
''', [([[1, 0, -1, 0, -2, 2], 0], [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]), ([[2, 2, 2, 2, 2], 8], [[2, 2, 2, 2]])], 'O(n³)', 'O(1) extra', cmp='deep')

P('valid-palindrome-ii', 'Palindrome With One Eraser', 680, 'Easy', TP,
  "Can the word read the same forwards and backwards if you're allowed to delete at most one letter?",
  "Squeeze from both ends. At the first mismatch, try skipping the left letter OR the right letter.",
  ["You only get one skip.", "Check the leftover middle with slicing."],
  '''
class Solution:
    def validPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            if s[l] != s[r]:
                a, b = s[l + 1:r + 1], s[l:r]  #> erase the left OR the right letter
                return a == a[::-1] or b == b[::-1]
            l += 1
            r -= 1
        return True
''', [(["aba"], True), (["abca"], True), (["abc"], False)], 'O(n)', 'O(n)')

P('max-k-sum-pairs', 'Pairs That Make k', 1679, 'Medium', TP,
  "Each move removes two numbers that add up to k. How many moves can you make?",
  "Sort and squeeze two pointers: equal to k means a pair (move both), too small move left, too big move right.",
  ["Each number can be used once."],
  '''
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        nums.sort()
        l, r, ops = 0, len(nums) - 1, 0
        while l < r:
            s = nums[l] + nums[r]
            if s == k:
                ops += 1  #> pair removed
                l += 1
                r -= 1
            elif s < k:
                l += 1
            else:
                r -= 1
        return ops
''', [([[1, 2, 3, 4], 5], 2), ([[3, 1, 3, 4, 3], 6], 1)], 'O(n log n)', 'O(1)')

P('next-permutation', 'The Next Arrangement', 31, 'Medium', TP,
  "Rearrange the numbers into the next bigger order (like the next number on an odometer). If it's already the biggest, wrap to the smallest. Change the list itself.",
  "From the right, find the first number smaller than its right neighbour. Swap it with the smallest bigger number to its right, then reverse everything after it.",
  ["[1,2,3] → [1,3,2].", "If no such number, just reverse the whole list."],
  '''
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        i = len(nums) - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1  #> find the first dip from the right
        if i >= 0:
            j = len(nums) - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]  #> bump it up a little
        nums[i + 1:] = reversed(nums[i + 1:])  #> make the tail as small as possible
''', [([[1, 2, 3]], [1, 3, 2]), ([[3, 2, 1]], [1, 2, 3]), ([[1, 1, 5]], [1, 5, 1])], 'O(n)', 'O(1)', inplace=0)

P('max-consecutive-ones-iii', 'Longest Ones With k Flips', 1004, 'Medium', SW,
  "You can flip up to k zeros into ones. What's the longest run of ones you can make?",
  "Stretchy window: grow right; if it holds more than k zeros, shrink from the left.",
  ["Count zeros inside the window."],
  '''
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        l = zeros = best = 0
        for r, x in enumerate(nums):
            zeros += x == 0
            while zeros > k:
                zeros -= nums[l] == 0  #> too many flips: shrink
                l += 1
            best = max(best, r - l + 1)
        return best
''', [([[1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2], 6), ([[0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3], 10)], 'O(n)', 'O(1)')

P('max-vowels-substring', 'Most Vowels in a Window', 1456, 'Medium', SW,
  "Which stretch of exactly k letters has the most vowels? Return that count.",
  "Fixed window: add the letter coming in, subtract the letter going out.",
  ["Start by counting the first k letters."],
  '''
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        v = set('aeiou')
        cur = sum(ch in v for ch in s[:k])
        best = cur
        for i in range(k, len(s)):
            cur += (s[i] in v) - (s[i - k] in v)  #> one in, one out
            best = max(best, cur)
        return best
''', [(["abciiidef", 3], 3), (["aeiou", 2], 2), (["leetcode", 3], 2)], 'O(n)', 'O(1)')

P('longest-ones-after-delete', 'Delete One, Join the Ones', 1493, 'Medium', SW,
  "You MUST delete exactly one number. What's the longest run of only ones left?",
  "Window with at most one zero inside. The answer is window length minus 1 (the deleted one).",
  ["All ones? You still have to delete one."],
  '''
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        l = zeros = best = 0
        for r, x in enumerate(nums):
            zeros += x == 0
            while zeros > 1:
                zeros -= nums[l] == 0
                l += 1
            best = max(best, r - l)  #> length minus the deleted one
        return best
''', [([[1, 1, 0, 1]], 3), ([[0, 1, 1, 1, 0, 1, 1, 0, 1]], 5), ([[1, 1, 1]], 2)], 'O(n)', 'O(1)')

P('find-all-anagrams', 'Find Every Scrambled Copy', 438, 'Medium', SW,
  "Find every starting position in s where a scrambled version of p begins.",
  "Slide a window the size of p over s, keeping letter counts. When the counts match p's, record the start.",
  ["Compare two Counters, or two arrays of 26 counts."],
  '''
from collections import Counter
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        need, have = Counter(p), Counter()
        out, k = [], len(p)
        for i, ch in enumerate(s):
            have[ch] += 1
            if i >= k:
                have[s[i - k]] -= 1  #> letter leaving the window
                if have[s[i - k]] == 0:
                    del have[s[i - k]]
            if have == need:
                out.append(i - k + 1)  #> same letters: scrambled copy!
        return out
''', [(["cbaebabacd", "abc"], [0, 6]), (["abab", "ab"], [0, 1, 2])], 'O(n)', 'O(1)')

P('subarray-product-less-than-k', 'Small Products', 713, 'Medium', SW,
  "Count the stretches of positive numbers whose product is less than k.",
  "Stretchy window keeps the product below k. Every time the right edge moves, it adds r - l + 1 new stretches.",
  ["Shrink from the left while the product is too big.", "If k <= 1, the answer is 0."],
  '''
class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0
        prod, l, count = 1, 0, 0
        for r, x in enumerate(nums):
            prod *= x
            while prod >= k:
                prod //= nums[l]  #> too big: drop the left number
                l += 1
            count += r - l + 1  #> all stretches ending at r
        return count
''', [([[10, 5, 2, 6], 100], 8), ([[1, 2, 3], 0], 0)], 'O(n)', 'O(1)')

P('concat-all-words', 'Find the Word Chain', 30, 'Hard', SW,
  "All the words have the same length. Find every spot in s where all of them appear glued together in any order.",
  "Try each start; chop the next len(words)*w letters into words and compare counts with the word list.",
  ["Counter of the words is the target.", "Stop early when a chunk isn't needed."],
  '''
from collections import Counter
class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        w, n = len(words[0]), len(words)
        need = Counter(words)
        out = []
        for i in range(len(s) - w * n + 1):
            seen = Counter()
            for j in range(n):
                piece = s[i + j * w:i + (j + 1) * w]
                if piece not in need:
                    break
                seen[piece] += 1
                if seen[piece] > need[piece]:
                    break  #> used a word too often
            else:
                out.append(i)  #> every word used exactly right
        return out
''', [(["barfoothefoobarman", ["foo", "bar"]], [0, 9]), (["wordgoodgoodgoodbestword", ["word", "good", "best", "word"]], []), (["barfoofoobarthefoobarman", ["bar", "foo", "the"]], [6, 9, 12])], 'O(n·k)', 'O(k)')

P('longest-valid-parentheses', 'Longest Neat Brackets', 32, 'Hard', ST,
  "In a string of ( and ), find the longest stretch where the brackets are perfectly matched.",
  "Stack of positions, starting with -1 as a floor. Push '(' positions; on ')' pop, and if the stack is empty push this spot as the new floor, otherwise measure from the top.",
  ["The stack top is where the current neat stretch started."],
  '''
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]
        best = 0
        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)  #> unmatched ): new floor
                else:
                    best = max(best, i - stack[-1])  #> neat since the top
        return best
''', [(["(()"], 2), ([")()())"], 4), ([""], 0)], 'O(n)', 'O(n)')

P('simplify-path', 'Tidy the Folder Path', 71, 'Medium', ST,
  "Clean up a Unix folder path: '.' means stay, '..' means go up one folder, extra slashes don't matter.",
  "Split by '/'. Use a stack of folder names: push names, pop on '..', ignore '.' and empty pieces.",
  ["Can't go above the root.", "Join with '/' and add a leading '/'."],
  '''
class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        for part in path.split('/'):
            if part == '..':
                if stack:
                    stack.pop()  #> go up a folder
            elif part and part != '.':
                stack.append(part)  #> go into a folder
        return '/' + '/'.join(stack)
''', [(["/home/"], "/home"), (["/home//foo/"], "/home/foo"), (["/home/user/Documents/../Pictures"], "/home/user/Pictures"), (["/../"], "/")], 'O(n)', 'O(n)')

P('basic-calculator', 'Calculator With Brackets', 224, 'Hard', ST,
  "Work out an expression with +, -, brackets and spaces, like \"(1+(4+5+2)-3)+(6+8)\".",
  "Keep a running result and sign. On '(' push the result and sign onto a stack and start fresh; on ')' finish and combine with what you pushed.",
  ["Numbers can have several digits.", "A '-' before a bracket flips the whole bracket."],
  '''
class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        res, num, sign = 0, 0, 1
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch in '+-':
                res += sign * num
                num, sign = 0, 1 if ch == '+' else -1
            elif ch == '(':
                stack.append(res)  #> save the outside work
                stack.append(sign)
                res, sign = 0, 1
            elif ch == ')':
                res += sign * num
                num = 0
                res = stack.pop() * res + stack.pop()  #> combine with the outside
        return res + sign * num
''', [(["1 + 1"], 2), ([" 2-1 + 2 "], 3), (["(1+(4+5+2)-3)+(6+8)"], 23)], 'O(n)', 'O(n)')

P('basic-calculator-ii', 'Calculator With Times and Divide', 227, 'Medium', ST,
  "Work out an expression with + - * / (whole-number division toward zero), no brackets.",
  "Push numbers onto a stack: + pushes it, - pushes its negative, * and / combine with the top right away. Sum the stack at the end.",
  ["Times and divide happen first, so do them immediately.", "int(a / b) rounds toward zero."],
  '''
class Solution:
    def calculate(self, s: str) -> int:
        stack, num, op = [], 0, '+'
        for i, ch in enumerate(s + '+'):
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch in '+-*/':
                if op == '+':
                    stack.append(num)
                elif op == '-':
                    stack.append(-num)
                elif op == '*':
                    stack.append(stack.pop() * num)  #> multiply right now
                else:
                    stack.append(int(stack.pop() / num))
                op, num = ch, 0
        return sum(stack)
''', [(["3+2*2"], 7), ([" 3/2 "], 1), ([" 3+5 / 2 "], 5)], 'O(n)', 'O(n)')

P('queue-using-stacks', 'Queue Made of Two Stacks', 232, 'Easy', ST,
  "Build a queue (first in, first out) using only two stacks.",
  "Push into an 'in' stack. When you need the front, pour 'in' into an 'out' stack (which reverses the order) only if 'out' is empty.",
  ["Pouring flips the order: the oldest ends on top.", "Each item is poured at most once."],
  '''
class MyQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _pour(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())  #> flip the order

    def pop(self) -> int:
        self._pour()
        return self.outbox.pop()

    def peek(self) -> int:
        self._pour()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
''', [([["MyQueue", "push", "push", "peek", "pop", "empty"], [[], [1], [2], [], [], []]], [None, None, None, 1, 1, False])], 'O(1) average', 'O(n)', mode='design')

P('stack-using-queues', 'Stack Made of a Queue', 225, 'Easy', ST,
  "Build a stack (last in, first out) using only a queue.",
  "After pushing a new item to the back, rotate all older items behind it, so the newest is at the front.",
  ["deque: append, popleft.", "Rotating costs O(n) per push."],
  '''
from collections import deque
class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())  #> move older items behind the new one

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return not self.q
''', [([["MyStack", "push", "push", "top", "pop", "empty"], [[], [1], [2], [], [], []]], [None, None, None, 2, 2, False])], 'O(n) push', 'O(n)', mode='design')

P('decode-string', 'Unpack the Repeats', 394, 'Medium', ST,
  "\"3[a2[c]]\" means 'acc' three times: \"accaccacc\". Decode it.",
  "Stack of (text so far, repeat count). On '[' push and start fresh; on ']' pop and glue: old + count × current.",
  ["Numbers can have many digits.", "Nested brackets work naturally with a stack."],
  '''
class Solution:
    def decodeString(self, s: str) -> str:
        stack, cur, num = [], '', 0
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == '[':
                stack.append((cur, num))  #> save the outside and the count
                cur, num = '', 0
            elif ch == ']':
                prev, k = stack.pop()
                cur = prev + cur * k  #> repeat and glue back
            else:
                cur += ch
        return cur
''', [(["3[a]2[bc]"], "aaabcbc"), (["3[a2[c]]"], "accaccacc"), (["2[abc]3[cd]ef"], "abcabccdcdcdef")], 'O(output)', 'O(n)')

P('asteroid-collision', 'Space Rock Crash', 735, 'Medium', ST,
  "Rocks fly in a row: positive goes right, negative goes left, size = absolute value. When two meet, the smaller explodes (equal: both). What's left?",
  "Stack of survivors. A left-moving rock keeps smashing right-moving rocks on top of the stack while it's bigger.",
  ["Only a + on the stack and a - arriving can crash."],
  '''
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        st = []
        for a in asteroids:
            alive = True
            while alive and a < 0 and st and st[-1] > 0:
                if st[-1] < -a:
                    st.pop()  #> the right-mover explodes
                    continue
                if st[-1] == -a:
                    st.pop()  #> both explode
                alive = False
            if alive:
                st.append(a)
        return st
''', [([[5, 10, -5]], [5, 10]), ([[8, -8]], []), ([[10, 2, -5]], [10])], 'O(n)', 'O(n)')

P('online-stock-span', 'Stock Price Streak', 901, 'Medium', ST,
  "Each day you get a price. Say how many days in a row (including today) the price was at most today's price.",
  "Keep a stack of (price, span). Today swallows every smaller-or-equal price on top and adds their spans.",
  ["Each day is pushed and popped once: fast overall."],
  '''
class StockSpanner:
    def __init__(self):
        self.st = []

    def next(self, price: int) -> int:
        span = 1
        while self.st and self.st[-1][0] <= price:
            span += self.st.pop()[1]  #> swallow the smaller days
        self.st.append((price, span))
        return span
''', [([["StockSpanner", "next", "next", "next", "next", "next", "next", "next"], [[], [100], [80], [60], [70], [60], [75], [85]]], [None, 1, 1, 1, 2, 1, 4, 6])], 'O(1) average', 'O(n)', mode='design')

P('removing-stars', 'Stars Eat Letters', 2390, 'Medium', ST,
  "Each * deletes itself and the closest letter to its left. What's left?",
  "Stack: push letters, pop on *.",
  ["Join the stack at the end."],
  '''
class Solution:
    def removeStars(self, s: str) -> str:
        st = []
        for ch in s:
            if ch == '*':
                st.pop()  #> star eats the last letter
            else:
                st.append(ch)
        return ''.join(st)
''', [(["leet**cod*e"], "lecoe"), (["erase*****"], "")], 'O(n)', 'O(n)')

P('remove-adjacent-duplicates', 'Pop Matching Neighbours', 1047, 'Easy', ST,
  "Keep removing two equal letters standing side by side until you can't. What's left?",
  "Stack: if the new letter equals the top, pop (they cancel). Otherwise push.",
  ["\"abbaca\" → \"ca\"."],
  '''
class Solution:
    def removeDuplicates(self, s: str) -> str:
        st = []
        for ch in s:
            if st and st[-1] == ch:
                st.pop()  #> twins cancel out
            else:
                st.append(ch)
        return ''.join(st)
''', [(["abbaca"], "ca"), (["azxxzy"], "ay")], 'O(n)', 'O(n)')

P('next-greater-element-i', 'Who Is Taller to My Right?', 496, 'Easy', ST,
  "For each number in nums1 (which is also somewhere in nums2), find the first bigger number to its right in nums2, or -1.",
  "Walk nums2 with a stack of numbers waiting for a bigger one. When a bigger number arrives, it answers everyone smaller on the stack.",
  ["Save answers in a dict, then look them up for nums1."],
  '''
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nxt, st = {}, []
        for x in nums2:
            while st and st[-1] < x:
                nxt[st.pop()] = x  #> x is the answer for the smaller ones
            st.append(x)
        return [nxt.get(x, -1) for x in nums1]
''', [([[4, 1, 2], [1, 3, 4, 2]], [-1, 3, -1]), ([[2, 4], [1, 2, 3, 4]], [3, -1])], 'O(n+m)', 'O(n)')

P('next-greater-element-ii', 'Taller to My Right (Circle)', 503, 'Medium', ST,
  "The list is a circle. For each number, find the next bigger one going around, or -1.",
  "Go around twice with a stack of waiting positions.",
  ["Index i % n handles the wrap-around."],
  '''
class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans, st = [-1] * n, []
        for i in range(2 * n):
            x = nums[i % n]
            while st and nums[st[-1]] < x:
                ans[st.pop()] = x  #> answered!
            if i < n:
                st.append(i)
        return ans
''', [([[1, 2, 1]], [2, -1, 2]), ([[1, 2, 3, 4, 3]], [2, 3, 4, -1, 4])], 'O(n)', 'O(n)')

P('remove-k-digits', 'Make the Smallest Number', 402, 'Medium', ST,
  "Remove k digits from a number (given as a string) to make it as small as possible.",
  "Stack of digits. While the top is bigger than the new digit and you still have removals, pop it.",
  ["Big digits early are the worst.", "Strip leading zeros; empty means \"0\"."],
  '''
class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        st = []
        for d in num:
            while k and st and st[-1] > d:
                st.pop()  #> a smaller digit should go first
                k -= 1
            st.append(d)
        st = st[:len(st) - k]
        return ''.join(st).lstrip('0') or '0'
''', [(["1432219", 3], "1219"), (["10200", 1], "200"), (["10", 2], "0")], 'O(n)', 'O(n)')

P('recent-counter', 'Calls in the Last 3 Seconds', 933, 'Easy', SW,
  "ping(t) records a call at time t (in ms, always increasing) and returns how many calls happened in [t-3000, t].",
  "Keep a queue of times. Drop old ones from the front.",
  ["deque.popleft is instant."],
  '''
from collections import deque
class RecentCounter:
    def __init__(self):
        self.q = deque()

    def ping(self, t: int) -> int:
        self.q.append(t)
        while self.q[0] < t - 3000:
            self.q.popleft()  #> too old, forget it
        return len(self.q)
''', [([["RecentCounter", "ping", "ping", "ping", "ping"], [[], [1], [100], [3001], [3002]]], [None, 1, 2, 3, 3])], 'O(1) average', 'O(n)', mode='design')

P('first-last-position', 'Where Does It Start and End?', 34, 'Medium', BS,
  "Sorted list. Find the first and last position of target, or [-1, -1].",
  "Two binary searches: one for the leftmost spot where target could go, one for the spot after the last target.",
  ["bisect_left and bisect_right do exactly this."],
  '''
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def first_at_least(x):
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = (lo + hi) // 2
                if nums[mid] < x:
                    lo = mid + 1  #> too small: go right
                else:
                    hi = mid
            return lo
        a = first_at_least(target)
        if a == len(nums) or nums[a] != target:
            return [-1, -1]
        return [a, first_at_least(target + 1) - 1]
''', [([[5, 7, 7, 8, 8, 10], 8], [3, 4]), ([[5, 7, 7, 8, 8, 10], 6], [-1, -1]), ([[], 0], [-1, -1])], 'O(log n)', 'O(1)')

P('search-insert-position', 'Where Would It Go?', 35, 'Easy', BS,
  "Sorted list. Return where target is, or where it would be inserted to keep it sorted.",
  "Binary search for the first spot whose value is at least target.",
  ["When the loop ends, lo is the answer."],
  '''
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1  #> it goes to the right of mid
            else:
                hi = mid
        return lo
''', [([[1, 3, 5, 6], 5], 2), ([[1, 3, 5, 6], 2], 1), ([[1, 3, 5, 6], 7], 4)], 'O(log n)', 'O(1)')

P('find-peak-element', 'Find a Mountain Top', 162, 'Medium', BS,
  "Find any position whose number is bigger than both neighbours (the edges count as -infinity). Do it fast.",
  "Look at mid. If the right neighbour is bigger, a peak must be to the right (you're walking uphill). Otherwise it's at mid or to the left.",
  ["Always walk uphill.", "lo == hi at the end is a peak."],
  '''
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < nums[mid + 1]:
                lo = mid + 1  #> uphill to the right
            else:
                hi = mid  #> downhill: peak is here or left
        return lo
''', [([[1, 2, 3, 1]], 2), ([[1, 2, 1, 3, 5, 6, 4]], 5)], 'O(log n)', 'O(1)')

P('peak-of-mountain', 'Top of the Mountain', 852, 'Medium', BS,
  "The numbers go strictly up and then strictly down. Find the top's position.",
  "Binary search: if the next number is bigger you're on the way up.",
  ["Same as finding a peak."],
  '''
class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        lo, hi = 0, len(arr) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < arr[mid + 1]:
                lo = mid + 1  #> still climbing
            else:
                hi = mid
        return lo
''', [([[0, 1, 0]], 1), ([[0, 2, 1, 0]], 1), ([[0, 10, 5, 2]], 1)], 'O(log n)', 'O(1)')

P('single-in-sorted', 'The Lonely One in a Sorted List', 540, 'Medium', BS,
  "Sorted list where every number appears twice except one. Find it fast.",
  "Before the lonely one, pairs start at even positions. Check mid (made even): if it matches its right neighbour, the lonely one is further right.",
  ["Force mid to be even.", "Pairs break after the lonely number."],
  '''
class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if mid % 2:
                mid -= 1  #> stand on the start of a pair
            if nums[mid] == nums[mid + 1]:
                lo = mid + 2  #> pairs are fine so far: go right
            else:
                hi = mid
        return nums[lo]
''', [([[1, 1, 2, 3, 3, 4, 4, 8, 8]], 2), ([[3, 3, 7, 7, 10, 11, 11]], 10)], 'O(log n)', 'O(1)')

P('k-closest-elements', 'The k Nearest Numbers', 658, 'Medium', BS,
  "Sorted list. Return the k numbers closest to x, in sorted order (ties prefer the smaller number).",
  "Binary search for the left edge of the k-wide window: compare how far the window's two ends are from x.",
  ["The window starts somewhere in [0, n-k]."],
  '''
class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        lo, hi = 0, len(arr) - k
        while lo < hi:
            mid = (lo + hi) // 2
            if x - arr[mid] > arr[mid + k] - x:
                lo = mid + 1  #> the right end is closer: slide right
            else:
                hi = mid
        return arr[lo:lo + k]
''', [([[1, 2, 3, 4, 5], 4, 3], [1, 2, 3, 4]), ([[1, 1, 2, 3, 4, 5], 4, -1], [1, 1, 2, 3])], 'O(log n + k)', 'O(1)')

P('search-2d-matrix-ii', 'Staircase Search', 240, 'Medium', BS,
  "Every row and every column is sorted. Is target in the grid?",
  "Start at the top-right corner. Too big? Go left. Too small? Go down. Each step throws away a row or column.",
  ["The top-right corner is the magic starting spot."],
  '''
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        r, c = 0, len(matrix[0]) - 1
        while r < len(matrix) and c >= 0:
            v = matrix[r][c]
            if v == target:
                return True
            if v > target:
                c -= 1  #> too big: this column is out
            else:
                r += 1  #> too small: this row is out
        return False
''', [([[[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]], 5], True), ([[[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]], 20], False)], 'O(R+C)', 'O(1)')

P('successful-pairs', 'Strong Enough Spells', 2300, 'Medium', BS,
  "For each spell, count potions where spell × potion >= success.",
  "Sort potions. For each spell, binary search the weakest potion that works; everything after it works too.",
  ["Needed potion = ceil(success / spell)."],
  '''
from bisect import bisect_left
class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort()
        n = len(potions)
        out = []
        for s in spells:
            need = (success + s - 1) // s
            out.append(n - bisect_left(potions, need))  #> everyone from here on works
        return out
''', [([[5, 1, 3], [1, 2, 3, 4, 5], 7], [4, 0, 3]), ([[3, 1, 2], [8, 5, 8], 16], [2, 0, 2])], 'O((n+m) log m)', 'O(1)')

P('kth-smallest-in-matrix', 'k-th Smallest in a Sorted Grid', 378, 'Medium', BS,
  "Rows and columns are sorted. Find the k-th smallest number overall.",
  "Binary search on the VALUE. For a guess, count how many numbers are <= it (staircase walk). Find the smallest guess with count >= k.",
  ["Search between the smallest and the biggest number."],
  '''
class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)
        def count_le(x):
            r, c, cnt = n - 1, 0, 0
            while r >= 0 and c < n:
                if matrix[r][c] <= x:
                    cnt += r + 1  #> this whole column part is small enough
                    c += 1
                else:
                    r -= 1
            return cnt
        lo, hi = matrix[0][0], matrix[-1][-1]
        while lo < hi:
            mid = (lo + hi) // 2
            if count_le(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
''', [([[[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8], 13), ([[[-5]], 1], -5)], 'O(n log range)', 'O(1)')
