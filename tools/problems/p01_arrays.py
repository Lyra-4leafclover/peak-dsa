from pb import P
T = 'Arrays & Hashing'

P('contains-duplicate', 'Spot the Twin', 217, 'Easy', T,
  "You get a list of numbers. Is any number in there more than once? Answer True or False.",
  "Keep a 'seen it' bag (a set). Before adding a number, check if it's already in the bag.",
  ["A set can tell you 'is x in here?' super fast.", "Walk through once. Seen it before? You're done: True."],
  '''
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()  #> an empty bag for numbers we've met
        for x in nums:
            if x in seen:  #> met this one before? twin found!
                return True
            seen.add(x)  #> remember it for later
        return False  #> checked everything, no twins
''', [([[1, 2, 3, 1]], True), ([[1, 2, 3, 4]], False), ([[]], False), ([[5, 5]], True)], 'O(n)', 'O(n)')

P('valid-anagram', 'Same Letters, Different Order', 242, 'Easy', T,
  "Two words. Can you rearrange the letters of the first to make the second? (Like 'listen' and 'silent'.)",
  "Count how many of each letter both words have. If the counts match, they're anagrams.",
  ["Different lengths can never be anagrams.", "A dictionary of letter -> count works great."],
  '''
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):  #> different sizes? impossible
            return False
        count = {}
        for ch in s:
            count[ch] = count.get(ch, 0) + 1  #> +1 for letters in the first word
        for ch in t:
            count[ch] = count.get(ch, 0) - 1  #> -1 for letters in the second word
            if count[ch] < 0:  #> second word has an extra one of these
                return False
        return True
''', [(["anagram", "nagaram"], True), (["rat", "car"], False), (["a", "ab"], False)], 'O(n)', 'O(1) (26 letters)')

P('two-sum', 'Two Numbers That Add Up', 1, 'Easy', T,
  "Find the positions of two numbers in the list that add up to the target. There's always exactly one answer.",
  "For each number, the partner you need is target - number. Keep a phone book: number -> where you saw it.",
  ["Checking every pair is slow (n²). Can you remember what you've seen?", "Look up the partner BEFORE storing the current number."],
  '''
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        where = {}  #> phone book: number -> its index
        for i, x in enumerate(nums):
            need = target - x  #> the partner that would complete the sum
            if need in where:  #> have we met the partner already?
                return [where[need], i]
            where[x] = i  #> write this number in the phone book
        return []
''', [([[2, 7, 11, 15], 9], [0, 1]), ([[3, 2, 4], 6], [1, 2]), ([[3, 3], 6], [0, 1])], 'O(n)', 'O(n)')

P('group-anagrams', 'Anagram Families', 49, 'Medium', T,
  "Put words into groups where every word in a group uses exactly the same letters.",
  "Sort each word's letters to make its 'family name' (eat -> aet). Words with the same family name go together.",
  ["What do 'eat', 'tea' and 'ate' all become after sorting their letters?", "Use a dictionary from family name -> list of words."],
  '''
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for w in strs:
            key = ''.join(sorted(w))  #> family name: letters in abc order
            if key not in groups:
                groups[key] = []
            groups[key].append(w)  #> join your family
        return list(groups.values())
''', [([["eat", "tea", "tan", "ate", "nat", "bat"]], [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]), ([[""]], [[""]]), ([["a"]], [["a"]])], 'O(n·k log k)', 'O(n·k)', cmp='deep')

P('top-k-frequent', 'Most Popular K', 347, 'Medium', T,
  "Return the k numbers that appear the most often.",
  "Count everything, then put numbers into buckets by how often they appear. Read buckets from the most popular down.",
  ["First step: count with a dictionary.", "A number can appear at most n times, so make n+1 buckets."],
  '''
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        for x in nums:
            count[x] = count.get(x, 0) + 1  #> tally votes
        buckets = [[] for _ in range(len(nums) + 1)]  #> bucket i = numbers seen i times
        for x, c in count.items():
            buckets[c].append(x)
        res = []
        for c in range(len(buckets) - 1, 0, -1):  #> most popular bucket first
            for x in buckets[c]:
                res.append(x)
                if len(res) == k:
                    return res
        return res
''', [([[1, 1, 1, 2, 2, 3], 2], [1, 2]), ([[1], 1], [1]), ([[4, 4, 5, 5, 5, 6], 2], [5, 4])], 'O(n)', 'O(n)', cmp='sorted')

P('product-except-self', 'Everyone Else Multiplied', 238, 'Medium', T,
  "For each spot, multiply together every OTHER number in the list. No division allowed!",
  "Answer at i = (product of everything on the left) × (product of everything on the right). Do one pass left→right, one pass right→left.",
  ["Make a 'left products' pass first.", "Then walk backwards with a running 'right product'."],
  '''
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [1] * n
        left = 1
        for i in range(n):
            res[i] = left  #> everything to my left, multiplied
            left *= nums[i]
        right = 1
        for i in range(n - 1, -1, -1):
            res[i] *= right  #> now also times everything to my right
            right *= nums[i]
        return res
''', [([[1, 2, 3, 4]], [24, 12, 8, 6]), ([[-1, 1, 0, -3, 3]], [0, 0, 9, 0, 0])], 'O(n)', 'O(1) extra')

P('valid-sudoku', 'Sudoku Rule Checker', 36, 'Medium', T,
  "Look at a partly-filled 9×9 Sudoku. Does it break any rule? (No repeats in a row, column, or 3×3 box.) Empty cells are '.'.",
  "Keep a 'seen' set for every row, every column and every box. Box number = (row//3, col//3).",
  ["27 sets total: 9 rows, 9 columns, 9 boxes.", "r//3 and c//3 tell you which box a cell is in."],
  '''
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                v = board[r][c]
                if v == '.':
                    continue  #> empty cell, nothing to check
                b = (r // 3) * 3 + c // 3  #> which 3x3 box (0..8)
                if v in rows[r] or v in cols[c] or v in boxes[b]:
                    return False  #> repeat found: rule broken
                rows[r].add(v)
                cols[c].add(v)
                boxes[b].add(v)
        return True
''', [([[list("53..7...."), list("6..195..."), list(".98....6."), list("8...6...3"), list("4..8.3..1"), list("7...2...6"), list(".6....28."), list("...419..5"), list("....8..79")]], True),
      ([[list("83..7...."), list("6..195..."), list(".98....6."), list("8...6...3"), list("4..8.3..1"), list("7...2...6"), list(".6....28."), list("...419..5"), list("....8..79")]], False)], 'O(81)', 'O(81)')

P('encode-decode', 'Pack and Unpack Words', 271, 'Medium', T,
  "Turn a list of words into ONE string, then turn it back into the exact same list. Words can contain any character, even '#'.",
  "Write each word as length + '#' + word. When unpacking, read the number, skip the '#', then grab exactly that many characters.",
  ["A plain separator breaks if the word contains it.", "Lengths tell you exactly where each word ends."],
  '''
class Solution:
    def roundTrip(self, words: List[str]) -> List[str]:
        packed = ''
        for w in words:
            packed += str(len(w)) + '#' + w  #> e.g. 'hi' -> '2#hi'
        res, i = [], 0
        while i < len(packed):
            j = i
            while packed[j] != '#':  #> read the length digits
                j += 1
            n = int(packed[i:j])
            res.append(packed[j + 1:j + 1 + n])  #> grab exactly n chars
            i = j + 1 + n
        return res
''', [([["neet", "code", "love", "you"]], ["neet", "code", "love", "you"]), ([["we", "say", ":", "yes", "#4#"]], ["we", "say", ":", "yes", "#4#"]), ([[]], [])], 'O(n)', 'O(n)')

P('longest-consecutive', 'Longest Number Run', 128, 'Medium', T,
  "How long is the longest run of numbers that go up by 1 (like 4,5,6,7)? They can be in any order in the list.",
  "Put everything in a set. Only start counting from a number whose 'x-1' is NOT in the set: that's the start of a run.",
  ["Sorting works but is O(n log n). Can a set do better?", "A run starts at x if x-1 is missing."],
  '''
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        s = set(nums)
        best = 0
        for x in s:
            if x - 1 not in s:  #> x is the START of a run
                length = 1
                while x + length in s:  #> keep stepping up
                    length += 1
                best = max(best, length)
        return best
''', [([[100, 4, 200, 1, 3, 2]], 4), ([[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], 9), ([[]], 0)], 'O(n)', 'O(n)')

P('majority-element', 'The Crowd Favourite', 169, 'Easy', T,
  "One number appears in MORE than half the spots. Find it.",
  "Boyer-Moore voting: keep a candidate and a score. Same number: +1. Different: -1. Score hits 0? Pick a new candidate.",
  ["The majority survives all the cancelling out.", "You only need two variables."],
  '''
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        cand, score = None, 0
        for x in nums:
            if score == 0:
                cand = x  #> new candidate takes the stage
            score += 1 if x == cand else -1  #> vote for or against
        return cand
''', [([[3, 2, 3]], 3), ([[2, 2, 1, 1, 1, 2, 2]], 2)], 'O(n)', 'O(1)')

P('remove-duplicates-sorted', 'Squash Repeats (Sorted)', 26, 'Easy', T,
  "A sorted list has repeats. Move the unique numbers to the front and return how many unique numbers there are.",
  "A 'writer' pointer marks where the next unique number goes. A 'reader' pointer scans everything.",
  ["Because it's sorted, repeats sit next to each other.", "Only write when the reader sees something new."],
  '''
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        w = 1  #> next free slot for a new unique number
        for r in range(1, len(nums)):
            if nums[r] != nums[w - 1]:  #> something new!
                nums[w] = nums[r]
                w += 1
        return w
''', [([[1, 1, 2]], 2), ([[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]], 5)], 'O(n)', 'O(1)')

P('best-time-stock', 'Buy Low, Sell High', 121, 'Easy', T,
  "Prices for each day. Buy on one day, sell on a LATER day. What's the most money you can make? (0 if you can't make any.)",
  "Walk through the days remembering the cheapest price so far. Each day ask: if I sold today, how much would I make?",
  ["You only need the lowest price before today.", "Profit today = price - cheapest so far."],
  '''
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        cheapest = prices[0]
        best = 0
        for p in prices:
            cheapest = min(cheapest, p)  #> best day to have bought so far
            best = max(best, p - cheapest)  #> what if I sell today?
        return best
''', [([[7, 1, 5, 3, 6, 4]], 5), ([[7, 6, 4, 3, 1]], 0)], 'O(n)', 'O(1)')

P('move-zeroes', 'Zeros to the Back', 283, 'Easy', T,
  "Push all the 0s to the end of the list, keeping the other numbers in the same order. Change the list itself.",
  "A pointer 'w' marks where the next non-zero goes. Swap each non-zero into spot w.",
  ["Think of it like a queue of non-zero numbers stepping forward.", "Swapping keeps zeros drifting right."],
  '''
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        w = 0  #> where the next non-zero belongs
        for r in range(len(nums)):
            if nums[r] != 0:
                nums[w], nums[r] = nums[r], nums[w]  #> swap it forward
                w += 1
''', [([[0, 1, 0, 3, 12]], [1, 3, 12, 0, 0]), ([[0]], [0])], 'O(n)', 'O(1)', inplace=0)

P('find-pivot-index', 'Balance Point', 724, 'Easy', T,
  "Find the spot where the sum of everything on its left equals the sum of everything on its right. Return -1 if there's none.",
  "Total sum first. Then walk along keeping a 'left sum'. Right sum = total - left - current.",
  ["You don't need to re-add the right side each time.", "right = total - left - nums[i]"],
  '''
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        left = 0
        for i, x in enumerate(nums):
            if left == total - left - x:  #> left side == right side?
                return i
            left += x
        return -1
''', [([[1, 7, 3, 6, 5, 6]], 3), ([[1, 2, 3]], -1), ([[2, 1, -1]], 0)], 'O(n)', 'O(1)')

P('subarray-sum-k', 'Chunks That Sum to K', 560, 'Medium', T,
  "Count how many continuous chunks of the list add up to exactly k.",
  "Running sum trick: if running_sum - k appeared before, the numbers between then and now add up to k. Count running sums in a dictionary.",
  ["sum(i..j) = prefix[j] - prefix[i-1].", "Start the dictionary with {0: 1}."],
  '''
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        seen = {0: 1}  #> running sum 0 has happened once (before we start)
        run = 0
        count = 0
        for x in nums:
            run += x
            count += seen.get(run - k, 0)  #> chunks ending here that sum to k
            seen[run] = seen.get(run, 0) + 1
        return count
''', [([[1, 1, 1], 2], 2), ([[1, 2, 3], 3], 2), ([[1, -1, 0], 0], 3)], 'O(n)', 'O(n)')

P('sort-colors', 'Sort the Flags (0,1,2)', 75, 'Medium', T,
  "A list only has 0s, 1s and 2s. Sort it in place in ONE pass, without using sort().",
  "Dutch flag: three pointers. low = where the next 0 goes, high = where the next 2 goes, mid = the scanner.",
  ["0 → swap to low. 2 → swap to high. 1 → leave it.", "Don't move mid forward after swapping with high: check the new number first."],
  '''
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]  #> 0 goes to the front zone
                low += 1
                mid += 1
            elif nums[mid] == 2:
                nums[mid], nums[high] = nums[high], nums[mid]  #> 2 goes to the back zone
                high -= 1
            else:
                mid += 1  #> 1 stays in the middle
''', [([[2, 0, 2, 1, 1, 0]], [0, 0, 1, 1, 2, 2]), ([[2, 0, 1]], [0, 1, 2])], 'O(n)', 'O(1)', inplace=0)

P('first-missing-positive', 'Smallest Missing Positive', 41, 'Hard', T,
  "Find the smallest positive whole number (1, 2, 3...) that is NOT in the list. Use O(n) time and no extra list.",
  "Put each number x into seat x-1 (swap it there). Then the first seat i that doesn't hold i+1 gives the answer.",
  ["The answer is always between 1 and n+1.", "Keep swapping until the current seat holds the right number or a useless one."],
  '''
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1  #> the seat this number belongs in
                nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            if nums[i] != i + 1:  #> seat i is missing its number
                return i + 1
        return n + 1
''', [([[1, 2, 0]], 3), ([[3, 4, -1, 1]], 2), ([[7, 8, 9, 11, 12]], 1)], 'O(n)', 'O(1)')

P('ransom-note', 'Cut-Out Letter Note', 383, 'Easy', T,
  "Can you build the note using letters cut out of the magazine? Each magazine letter can be used once.",
  "Count the magazine's letters, then spend them on the note. Run out of a letter? Can't do it.",
  ["Counter(magazine) gives you letter counts.", "Subtract as you go."],
  '''
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        have = Counter(magazine)  #> letters we can cut out
        for ch in ransomNote:
            if have[ch] == 0:
                return False  #> ran out of this letter
            have[ch] -= 1
        return True
''', [(["a", "b"], False), (["aa", "aab"], True), (["aa", "ab"], False)], 'O(n)', 'O(1)')
