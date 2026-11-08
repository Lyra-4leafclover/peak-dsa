from pb import P
T = 'Two Pointers'

P('valid-palindrome', 'Reads the Same Both Ways', 125, 'Easy', T,
  "Ignore spaces, punctuation and capital letters. Does the text read the same forwards and backwards?",
  "One finger at the start, one at the end. Skip junk, compare letters, move both fingers inward.",
  ["str.isalnum() tells you if a character is a letter or digit.", "Compare lowercase versions."],
  '''
class Solution:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            if not s[l].isalnum():
                l += 1  #> skip junk on the left
            elif not s[r].isalnum():
                r -= 1  #> skip junk on the right
            elif s[l].lower() != s[r].lower():
                return False  #> mismatch!
            else:
                l += 1
                r -= 1
        return True
''', [(["A man, a plan, a canal: Panama"], True), (["race a car"], False), ([" "], True)], 'O(n)', 'O(1)')

P('two-sum-sorted', 'Two Sum on a Sorted Shelf', 167, 'Medium', T,
  "The list is sorted. Find two numbers that add up to target and return their positions counted from 1.",
  "Left finger at the smallest, right finger at the biggest. Too big? Move right finger left. Too small? Move left finger right.",
  ["Sorted order tells you which way to move.", "Each step throws away one number forever."],
  '''
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l, r = 0, len(numbers) - 1
        while l < r:
            s = numbers[l] + numbers[r]
            if s == target:
                return [l + 1, r + 1]
            if s < target:
                l += 1  #> need bigger: move left finger up
            else:
                r -= 1  #> need smaller: move right finger down
        return []
''', [([[2, 7, 11, 15], 9], [1, 2]), ([[2, 3, 4], 6], [1, 3]), ([[-1, 0], -1], [1, 2])], 'O(n)', 'O(1)')

P('three-sum', 'Three That Make Zero', 15, 'Medium', T,
  "Find every different group of three numbers that adds up to 0. No repeated groups.",
  "Sort. Fix one number, then do the two-finger trick on the rest to find pairs adding to -that number. Skip repeats.",
  ["Sorting makes skipping duplicates easy: equal numbers sit together.", "This is Two Sum (sorted) inside a loop."],
  '''
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue  #> same first number as last time: skip
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s < 0:
                    l += 1
                elif s > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])  #> found a trio!
                    l += 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1  #> skip repeats
        return res
''', [([[-1, 0, 1, 2, -1, -4]], [[-1, -1, 2], [-1, 0, 1]]), ([[0, 1, 1]], []), ([[0, 0, 0]], [[0, 0, 0]])], 'O(n²)', 'O(1) extra', cmp='deep')

P('container-most-water', 'Biggest Water Tank', 11, 'Medium', T,
  "Each number is a wall height. Pick two walls; water fills between them up to the SHORTER wall. What's the most water?",
  "Start with the widest tank (both ends). The shorter wall is the limit, so move IT inward hoping for a taller one.",
  ["Area = width × shorter height.", "Moving the taller wall can never help."],
  '''
class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        best = 0
        while l < r:
            area = (r - l) * min(height[l], height[r])  #> width x shorter wall
            best = max(best, area)
            if height[l] < height[r]:
                l += 1  #> left wall is the weak one
            else:
                r -= 1
        return best
''', [([[1, 8, 6, 2, 5, 4, 8, 3, 7]], 49), ([[1, 1]], 1)], 'O(n)', 'O(1)', bars=True)

P('trapping-rain-water', 'Rain Between the Towers', 42, 'Hard', T,
  "Towers of different heights. After it rains, how much water gets stuck between them?",
  "Water above a spot = min(tallest on left, tallest on right) - its height. Two fingers: always move the side with the smaller max.",
  ["Water level is decided by the shorter of the two tallest walls.", "The side with the smaller max is safe to settle."],
  '''
class Solution:
    def trap(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        lmax, rmax = 0, 0
        water = 0
        while l < r:
            if height[l] < height[r]:
                lmax = max(lmax, height[l])
                water += lmax - height[l]  #> water sitting on top of l
                l += 1
            else:
                rmax = max(rmax, height[r])
                water += rmax - height[r]  #> water sitting on top of r
                r -= 1
        return water
''', [([[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], 6), ([[4, 2, 0, 3, 2, 5]], 9)], 'O(n)', 'O(1)', bars=True)

P('reverse-string', 'Flip the Letters', 344, 'Easy', T,
  "Reverse a list of characters in place.",
  "Swap the first and last, then the second and second-last... meet in the middle.",
  ["Two fingers walking toward each other.", "Stop when they meet."],
  '''
class Solution:
    def reverseString(self, s: List[str]) -> None:
        l, r = 0, len(s) - 1
        while l < r:
            s[l], s[r] = s[r], s[l]  #> swap the outside pair
            l += 1
            r -= 1
''', [([list("hello")], list("olleh")), ([list("Hannah")], list("hannaH"))], 'O(n)', 'O(1)', inplace=0)

P('squares-sorted', 'Square Them, Keep Sorted', 977, 'Easy', T,
  "A sorted list (may have negatives). Square every number and return the squares sorted.",
  "The biggest square is at one of the two ends. Fill the answer from the back using two fingers.",
  ["-7 squared is bigger than 3 squared!", "Compare abs values at both ends."],
  '''
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [0] * n
        l, r = 0, n - 1
        for k in range(n - 1, -1, -1):  #> fill from the back
            if abs(nums[l]) > abs(nums[r]):
                res[k] = nums[l] * nums[l]
                l += 1
            else:
                res[k] = nums[r] * nums[r]
                r -= 1
        return res
''', [([[-4, -1, 0, 3, 10]], [0, 1, 9, 16, 100]), ([[-7, -3, 2, 3, 11]], [4, 9, 9, 49, 121])], 'O(n)', 'O(n)')

P('merge-sorted-array', 'Merge Two Sorted Shelves', 88, 'Easy', T,
  "nums1 has m real numbers then empty slots (0s). Merge the n numbers of nums2 into nums1 so it stays sorted.",
  "Fill from the BACK. Compare the biggest remaining of each list and drop the bigger one into the last empty slot.",
  ["Filling from the front would overwrite numbers you still need.", "Three pointers: end of nums1's real part, end of nums2, write spot."],
  '''
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        i, j, k = m - 1, n - 1, m + n - 1
        while j >= 0:
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]  #> nums1's is bigger, put it at the back
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
''', [([[1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3], [1, 2, 2, 3, 5, 6]), ([[1], 1, [], 0], [1]), ([[0], 0, [1], 1], [1])], 'O(m+n)', 'O(1)', inplace=0)

P('is-subsequence', 'Hidden Inside', 392, 'Easy', T,
  "Can you get word s by deleting some letters from t (without changing the order)?",
  "Walk through t with one finger. Every time it matches the next letter of s, move s's finger too.",
  ["Greedy matching always works here.", "Done when s's finger reaches the end."],
  '''
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0  #> how much of s we've matched
        for ch in t:
            if i < len(s) and ch == s[i]:
                i += 1  #> matched one more letter of s
        return i == len(s)
''', [(["abc", "ahbgdc"], True), (["axc", "ahbgdc"], False), (["", "x"], True)], 'O(n)', 'O(1)')

P('remove-element', 'Throw Out a Value', 27, 'Easy', T,
  "Remove every copy of val from the list (in place) and return how many numbers are left.",
  "A writer pointer copies over every number that isn't val.",
  ["Same idea as squashing duplicates.", "Order of what's left can stay the same."],
  '''
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        w = 0
        for x in nums:
            if x != val:
                nums[w] = x  #> keep it
                w += 1
        return w
''', [([[3, 2, 2, 3], 3], 2), ([[0, 1, 2, 2, 3, 0, 4, 2], 2], 5)], 'O(n)', 'O(1)')
