from pb import P
T = 'Arrays & Hashing'

P('roman-to-integer', 'Read the Roman Clock', 13, 'Easy', T,
  "Turn a Roman numeral like \"MCMXCIV\" into a normal number.",
  "Walk left to right. If a letter is smaller than the one after it (like I before V), subtract it; otherwise add it.",
  ["Make a dict from letter to value.", "IV = 5 - 1: the small one comes first, so it subtracts."],
  '''
class Solution:
    def romanToInt(self, s: str) -> int:
        val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        total = 0
        for i in range(len(s)):
            if i + 1 < len(s) and val[s[i]] < val[s[i + 1]]:
                total -= val[s[i]]  #> small before big: subtract
            else:
                total += val[s[i]]  #> normal: add
        return total
''', [(["III"], 3), (["LVIII"], 58), (["MCMXCIV"], 1994)], 'O(n)', 'O(1)')

P('integer-to-roman', 'Write the Roman Clock', 12, 'Medium', T,
  "Turn a normal number (1 to 3999) into a Roman numeral.",
  "Greedy: list the values from big to small (including 900, 400, 90...). Keep taking the biggest one that still fits.",
  ["Include the special pairs CM, CD, XC, XL, IX, IV in your list.", "Like making change with coins."],
  '''
class Solution:
    def intToRoman(self, num: int) -> str:
        pairs = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
                 (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
        out = []
        for v, sym in pairs:
            while num >= v:
                out.append(sym)  #> the biggest piece that fits
                num -= v
        return ''.join(out)
''', [([3749], "MMMDCCXLIX"), ([58], "LVIII"), ([1994], "MCMXCIV")], 'O(1)', 'O(1)')

P('longest-common-prefix', 'Shared Beginning', 14, 'Easy', T,
  "Find the longest start that ALL the words share. \"flower\", \"flow\", \"flight\" share \"fl\".",
  "Look at the letters column by column. Stop at the first column where the words disagree or one word runs out.",
  ["Use the first word as the ruler.", "Return the part of the first word before the mismatch."],
  '''
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        first = strs[0]
        for i in range(len(first)):
            for w in strs[1:]:
                if i >= len(w) or w[i] != first[i]:
                    return first[:i]  #> column i disagrees: stop
        return first
''', [([["flower", "flow", "flight"]], "fl"), ([["dog", "racecar", "car"]], ""), ([["a"]], "a")], 'O(total letters)', 'O(1)')

P('find-first-occurrence', 'Find the Word in the Sentence', 28, 'Easy', T,
  "Return where the small string first appears inside the big string, or -1 if it never does.",
  "Slide the small word along the big one and check each spot.",
  ["There are len(big) - len(small) + 1 starting spots.", "Slicing big[i:i+m] grabs the window."],
  '''
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        m = len(needle)
        for i in range(len(haystack) - m + 1):
            if haystack[i:i + m] == needle:
                return i  #> found it here
        return -1
''', [(["sadbutsad", "sad"], 0), (["leetcode", "leeto"], -1), (["hello", "ll"], 2)], 'O(n·m)', 'O(1)')

P('length-of-last-word', 'How Long Is the Last Word?', 58, 'Easy', T,
  "Given a sentence (maybe with extra spaces), how many letters are in the last word?",
  "Start from the end, skip spaces, then count letters until the next space.",
  ["Trailing spaces don't count.", "Or just use s.split()[-1]."],
  '''
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        i = len(s) - 1
        while s[i] == ' ':
            i -= 1  #> skip trailing spaces
        n = 0
        while i >= 0 and s[i] != ' ':
            n += 1  #> count the letters
            i -= 1
        return n
''', [(["Hello World"], 5), (["   fly me   to   the moon  "], 4), (["luffy is still joyboy"], 6)], 'O(n)', 'O(1)')

P('zigzag-conversion', 'Zigzag Writing', 6, 'Medium', T,
  "Write the letters in a zigzag down and up across some rows, then read row by row.",
  "Keep one string per row. Walk the letters, moving down a row each time until the bottom, then up until the top.",
  ["Flip direction at the top and bottom rows.", "With 1 row, nothing changes."],
  '''
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1:
            return s
        rows = [''] * numRows
        r, step = 0, 1
        for ch in s:
            rows[r] += ch  #> drop the letter in the current row
            if r == 0:
                step = 1  #> bounce down
            elif r == numRows - 1:
                step = -1  #> bounce up
            r += step
        return ''.join(rows)
''', [(["PAYPALISHIRING", 3], "PAHNAPLSIIGYIR"), (["PAYPALISHIRING", 4], "PINALSIGYAHRPI"), (["A", 1], "A")], 'O(n)', 'O(n)')

P('rotate-array', 'Spin the Array', 189, 'Medium', T,
  "Shift every number k places to the right; ones that fall off the end wrap around to the front. Change the list itself.",
  "Reverse the whole list, then reverse the first k, then reverse the rest. Magic!",
  ["k might be bigger than the length: use k % n.", "Three reverses, no extra list."],
  '''
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n
        def rev(l, r):
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1
        rev(0, n - 1)  #> flip everything
        rev(0, k - 1)  #> flip the first k back
        rev(k, n - 1)  #> flip the rest back
''', [([[1, 2, 3, 4, 5, 6, 7], 3], [5, 6, 7, 1, 2, 3, 4]), ([[-1, -100, 3, 99], 2], [3, 99, -1, -100])], 'O(n)', 'O(1)', inplace=0)

P('h-index', 'Research Score', 274, 'Medium', T,
  "Each number is how many times a paper was cited. Find the biggest h such that h papers have at least h citations each.",
  "Sort from most cited to least. Walk down; while paper number i+1 still has at least i+1 citations, h grows.",
  ["Sort descending.", "Stop at the first paper that's too small."],
  '''
class Solution:
    def hIndex(self, citations: List[int]) -> int:
        citations.sort(reverse=True)
        h = 0
        for i, c in enumerate(citations):
            if c >= i + 1:
                h = i + 1  #> i+1 papers with at least i+1 cites
            else:
                break
        return h
''', [([[3, 0, 6, 1, 5]], 3), ([[1, 3, 1]], 1), ([[0]], 0)], 'O(n log n)', 'O(1)')

P('isomorphic-strings', 'Secret Code Match', 205, 'Easy', T,
  "Can you swap letters with a secret code to turn the first word into the second? Each letter must always map to the same letter, and no two letters can map to the same one.",
  "Keep two dicts: s→t and t→s. Any disagreement means no.",
  ["\"egg\" and \"add\": e→a, g→d. Works!", "Check both directions."],
  '''
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        st, ts = {}, {}
        for a, b in zip(s, t):
            if st.get(a, b) != b or ts.get(b, a) != a:
                return False  #> the code would contradict itself
            st[a] = b
            ts[b] = a
        return True
''', [(["egg", "add"], True), (["foo", "bar"], False), (["paper", "title"], True)], 'O(n)', 'O(1)')

P('word-pattern', 'Does the Sentence Follow the Pattern?', 290, 'Easy', T,
  "Pattern \"abba\" and sentence \"dog cat cat dog\": each letter stands for one word, consistently. Does it match?",
  "Same as secret code matching, but letters map to whole words. Use two dicts.",
  ["Different number of words and letters: no.", "Check both directions."],
  '''
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()
        if len(words) != len(pattern):
            return False
        pw, wp = {}, {}
        for ch, w in zip(pattern, words):
            if pw.get(ch, w) != w or wp.get(w, ch) != ch:
                return False
            pw[ch] = w  #> remember the pairing
            wp[w] = ch
        return True
''', [(["abba", "dog cat cat dog"], True), (["abba", "dog cat cat fish"], False), (["aaaa", "dog cat cat dog"], False)], 'O(n)', 'O(n)')

P('game-of-life', 'Game of Life', 289, 'Medium', T,
  "A grid of cells: 1 alive, 0 dead. Each cell looks at its 8 neighbours: alive with 2-3 live neighbours stays alive, dead with exactly 3 comes alive, everything else dies. Update the grid to the next moment.",
  "Count neighbours using a copy of the old grid, so updates don't mess up the counting.",
  ["Copy the grid first.", "Check all 8 directions and stay inside the edges."],
  '''
class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        R, C = len(board), len(board[0])
        old = [row[:] for row in board]  #> freeze the current moment
        for r in range(R):
            for c in range(C):
                n = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if (dr or dc) and 0 <= r + dr < R and 0 <= c + dc < C:
                            n += old[r + dr][c + dc]
                if old[r][c] == 1 and n not in (2, 3):
                    board[r][c] = 0  #> lonely or crowded: dies
                elif old[r][c] == 0 and n == 3:
                    board[r][c] = 1  #> exactly 3 friends: born
''', [([[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]], [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]), ([[[1, 1], [1, 0]]], [[1, 1], [1, 1]])], 'O(R·C)', 'O(R·C)', inplace=0)

P('kids-with-candies', 'Who Could Have the Most Candy?', 1431, 'Easy', T,
  "Each kid has some candies. If you gave ALL the extra candies to one kid, would they have the most (ties count)? Answer for every kid.",
  "Find the current max once. A kid wins if their candies + extra >= max.",
  ["One pass to find the max, one pass to answer."],
  '''
class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        top = max(candies)  #> the current record
        return [c + extraCandies >= top for c in candies]
''', [([[2, 3, 5, 1, 3], 3], [True, True, True, False, True]), ([[4, 2, 1, 1, 2], 1], [True, False, False, False, False])], 'O(n)', 'O(n)')

P('merge-alternately', 'Zip Two Words', 1768, 'Easy', T,
  "Merge two words by taking letters in turns: one from the first, one from the second... Leftover letters go at the end.",
  "Walk an index i up to the longer length; add word1[i] and word2[i] if they exist.",
  ["Check each index is inside each word."],
  '''
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        out = []
        for i in range(max(len(word1), len(word2))):
            if i < len(word1):
                out.append(word1[i])
            if i < len(word2):
                out.append(word2[i])  #> take turns
        return ''.join(out)
''', [(["abc", "pqr"], "apbqcr"), (["ab", "pqrs"], "apbqrs"), (["abcd", "pq"], "apbqcd")], 'O(n+m)', 'O(n+m)')

P('gcd-of-strings', 'Biggest Repeating Piece', 1071, 'Easy', T,
  "Find the longest string x so that both words are just x repeated some number of times.",
  "If a+b != b+a, there is no such x. Otherwise the answer is the first gcd(len a, len b) letters.",
  ["\"ABCABC\" and \"ABC\": x = \"ABC\".", "math.gcd finds the greatest common divisor."],
  '''
from math import gcd
class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 + str2 != str2 + str1:
            return ""  #> they're not made of the same brick
        return str1[:gcd(len(str1), len(str2))]
''', [(["ABCABC", "ABC"], "ABC"), (["ABABAB", "ABAB"], "AB"), (["LEET", "CODE"], "")], 'O(n+m)', 'O(n+m)')

P('can-place-flowers', 'Plant Flowers Without Neighbours', 605, 'Easy', T,
  "A flowerbed: 1 = flower, 0 = empty. Flowers can't be next to each other. Can you plant n more?",
  "Walk the bed. Plant in any empty spot whose left and right are both empty (edges count as empty).",
  ["Plant greedily as early as possible.", "Mark the spot so the next one sees it."],
  '''
class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        bed = flowerbed
        for i in range(len(bed)):
            left = i == 0 or bed[i - 1] == 0
            right = i == len(bed) - 1 or bed[i + 1] == 0
            if bed[i] == 0 and left and right:
                bed[i] = 1  #> plant here
                n -= 1
        return n <= 0
''', [([[1, 0, 0, 0, 1], 1], True), ([[1, 0, 0, 0, 1], 2], False), ([[0, 0, 1, 0, 0], 2], True)], 'O(n)', 'O(1)')

P('reverse-vowels', 'Flip Only the Vowels', 345, 'Easy', T,
  "Reverse just the vowels (a, e, i, o, u, both cases) in a word; everything else stays put.",
  "Two pointers from both ends. Each one walks until it sits on a vowel, then swap.",
  ["Turn the string into a list so you can swap.", "Skip non-vowels."],
  '''
class Solution:
    def reverseVowels(self, s: str) -> str:
        v = set('aeiouAEIOU')
        a = list(s)
        l, r = 0, len(a) - 1
        while l < r:
            if a[l] not in v:
                l += 1
            elif a[r] not in v:
                r -= 1
            else:
                a[l], a[r] = a[r], a[l]  #> both on vowels: swap
                l += 1
                r -= 1
        return ''.join(a)
''', [(["IceCreAm"], "AceCreIm"), (["leetcode"], "leotcede")], 'O(n)', 'O(n)')

P('reverse-words', 'Say the Sentence Backwards', 151, 'Medium', T,
  "Reverse the order of the words in a sentence. Remove extra spaces.",
  "split() breaks it into words (and drops extra spaces). Reverse the list, join with single spaces.",
  ["\"  hello world  \" becomes \"world hello\"."],
  '''
class Solution:
    def reverseWords(self, s: str) -> str:
        words = s.split()  #> chop into words
        words.reverse()
        return ' '.join(words)
''', [(["the sky is blue"], "blue is sky the"), (["  hello world  "], "world hello"), (["a good   example"], "example good a")], 'O(n)', 'O(n)')

P('increasing-triplet', 'Three Climbing Steps', 334, 'Medium', T,
  "Is there any i < j < k with nums[i] < nums[j] < nums[k]?",
  "Keep the smallest number seen (first) and the smallest number that has something smaller before it (second). Anything bigger than second wins.",
  ["Two variables, one pass.", "Update first, else second, else found!"],
  '''
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        first = second = float('inf')
        for x in nums:
            if x <= first:
                first = x  #> new smallest step
            elif x <= second:
                second = x  #> a good middle step
            else:
                return True  #> third step found!
        return False
''', [([[1, 2, 3, 4, 5]], True), ([[5, 4, 3, 2, 1]], False), ([[2, 1, 5, 0, 4, 6]], True)], 'O(n)', 'O(1)')

P('string-compression', 'Squish Repeated Letters', 443, 'Medium', T,
  "Compress a list of letters: runs like a,a,a become a,3. Write the result into the same list and return its new length.",
  "Read pointer finds each run; write pointer writes the letter and its count digits.",
  ["Runs of length 1 get no number.", "Counts like 12 take two slots: '1','2'."],
  '''
class Solution:
    def compress(self, chars: List[str]) -> int:
        w = 0
        i = 0
        while i < len(chars):
            j = i
            while j < len(chars) and chars[j] == chars[i]:
                j += 1  #> find the end of this run
            chars[w] = chars[i]
            w += 1
            if j - i > 1:
                for d in str(j - i):
                    chars[w] = d  #> write the count
                    w += 1
            i = j
        return w
''', [([["a", "a", "b", "b", "c", "c", "c"]], 6), ([["a"]], 1), ([["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]], 4)], 'O(n)', 'O(1)')

P('unique-occurrences', 'Every Count Different?', 1207, 'Easy', T,
  "Count how many times each number appears. Are all those counts different from each other?",
  "Count with a dict, then check if the set of counts is as big as the list of counts.",
  ["Counter does the counting.", "A set drops duplicate counts."],
  '''
from collections import Counter
class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        counts = Counter(arr).values()
        return len(set(counts)) == len(counts)  #> any repeated count shrinks the set
''', [([[1, 2, 2, 1, 1, 3]], True), ([[1, 2]], False), ([[-3, 0, 1, -3, 1, 1, 1, -3, 10, 0]], True)], 'O(n)', 'O(n)')

P('close-strings', 'Shuffle-and-Swap Twins', 1657, 'Medium', T,
  "You may swap any two letters' positions, or swap ALL of one letter with ALL of another letter. Can you turn word1 into word2?",
  "They must use the same set of letters, and the sorted list of letter counts must match.",
  ["Order doesn't matter at all (swaps fix it).", "Compare letter sets and sorted counts."],
  '''
from collections import Counter
class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        a, b = Counter(word1), Counter(word2)
        same_letters = set(a) == set(b)
        same_counts = sorted(a.values()) == sorted(b.values())
        return same_letters and same_counts
''', [(["abc", "bca"], True), (["a", "aa"], False), (["cabbba", "abbccc"], True)], 'O(n)', 'O(1)')

P('equal-row-column-pairs', 'Rows That Match Columns', 2352, 'Medium', T,
  "In a square grid, count pairs (row, column) where the row and the column contain exactly the same numbers in the same order.",
  "Count every row as a tuple in a dict. Then for each column (as a tuple), add how many rows match it.",
  ["zip(*grid) gives you the columns.", "Tuples can be dict keys; lists can't."],
  '''
from collections import Counter
class Solution:
    def equalPairs(self, grid: List[List[int]]) -> int:
        rows = Counter(tuple(r) for r in grid)
        total = 0
        for col in zip(*grid):
            total += rows[col]  #> how many rows look exactly like this column
        return total
''', [([[[3, 2, 1], [1, 7, 6], [2, 7, 7]]], 1), ([[[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]], 3)], 'O(n²)', 'O(n²)')

P('find-difference-arrays', 'What Does Only One Have?', 2215, 'Easy', T,
  "Two lists. Return [numbers only in the first, numbers only in the second], with no repeats.",
  "Make sets, then use set subtraction both ways.",
  ["set(a) - set(b) keeps what's only in a."],
  '''
class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        a, b = set(nums1), set(nums2)
        return [sorted(a - b), sorted(b - a)]  #> only-in-a, only-in-b
''', [([[1, 2, 3], [2, 4, 6]], [[1, 3], [4, 6]]), ([[1, 2, 3, 3], [1, 1, 2, 2]], [[3], []])], 'O(n+m)', 'O(n+m)', cmp='deep')

P('contains-duplicate-ii', 'Twins Close Together', 219, 'Easy', T,
  "Are there two equal numbers whose positions are at most k apart?",
  "Remember the last position of every number. When you see it again, check the distance.",
  ["A dict from number to its latest index."],
  '''
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        last = {}
        for i, x in enumerate(nums):
            if x in last and i - last[x] <= k:
                return True  #> twins close enough
            last[x] = i
        return False
''', [([[1, 2, 3, 1], 3], True), ([[1, 0, 1, 1], 1], True), ([[1, 2, 3, 1, 2, 3], 2], False)], 'O(n)', 'O(n)')

P('summary-ranges', 'Squish Number Runs', 228, 'Easy', T,
  "Sorted unique numbers. Describe them as ranges: [0,1,2,4,5,7] becomes [\"0->2\",\"4->5\",\"7\"].",
  "Start a run, extend it while the next number is exactly +1, then write it out.",
  ["Single-number runs are written alone."],
  '''
class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        out = []
        i = 0
        while i < len(nums):
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1  #> the run continues
            out.append(str(nums[i]) if i == j else f"{nums[i]}->{nums[j]}")
            i = j + 1
        return out
''', [([[0, 1, 2, 4, 5, 7]], ["0->2", "4->5", "7"]), ([[0, 2, 3, 4, 6, 8, 9]], ["0", "2->4", "6", "8->9"]), ([[]], [])], 'O(n)', 'O(1)')

P('contiguous-array', 'Equal Zeros and Ones', 525, 'Medium', T,
  "Find the longest stretch with the same number of 0s and 1s.",
  "Count 1 as +1 and 0 as -1. A stretch is balanced when the running total repeats. Remember where each total first appeared.",
  ["Start with total 0 at index -1.", "Same total twice = balanced in between."],
  '''
class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        first = {0: -1}
        total = best = 0
        for i, x in enumerate(nums):
            total += 1 if x == 1 else -1
            if total in first:
                best = max(best, i - first[total])  #> balanced since then
            else:
                first[total] = i
        return best
''', [([[0, 1]], 2), ([[0, 1, 0]], 2), ([[0, 1, 1, 1, 1, 1, 0, 0, 0]], 6)], 'O(n)', 'O(n)')

P('disappeared-numbers', 'Missing From the Roll Call', 448, 'Easy', T,
  "A list of n numbers, each from 1 to n, with some repeats. Which numbers from 1 to n are missing?",
  "Put everything in a set, then check 1 to n.",
  ["A set makes \"is it here?\" instant."],
  '''
class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        have = set(nums)
        return [x for x in range(1, len(nums) + 1) if x not in have]  #> who didn't answer?
''', [([[4, 3, 2, 7, 8, 2, 3, 1]], [5, 6]), ([[1, 1]], [2])], 'O(n)', 'O(n)')

P('first-unique-char', 'First Letter With No Twin', 387, 'Easy', T,
  "Find the position of the first letter that appears only once. -1 if there is none.",
  "Count every letter first, then walk again and return the first with count 1.",
  ["Two passes."],
  '''
from collections import Counter
class Solution:
    def firstUniqChar(self, s: str) -> int:
        count = Counter(s)
        for i, ch in enumerate(s):
            if count[ch] == 1:
                return i  #> lonely letter found
        return -1
''', [(["leetcode"], 0), (["loveleetcode"], 2), (["aabb"], -1)], 'O(n)', 'O(1)')

P('intersection-of-arrays', 'Numbers in Both', 349, 'Easy', T,
  "Which numbers appear in both lists? No repeats in the answer.",
  "Turn both into sets and take the overlap with &.",
  ["set & set = what they share."],
  '''
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return list(set(nums1) & set(nums2))  #> the overlap
''', [([[1, 2, 2, 1], [2, 2]], [2]), ([[4, 9, 5], [9, 4, 9, 8, 4]], [9, 4])], 'O(n+m)', 'O(n+m)', cmp='sorted')

P('intersection-of-arrays-ii', 'Numbers in Both (With Repeats)', 350, 'Easy', T,
  "Like the overlap, but if a number shows up twice in both lists, include it twice.",
  "Count the first list. Walk the second; whenever a count is still above 0, take it and decrease the count.",
  ["Counter is perfect here."],
  '''
from collections import Counter
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        count = Counter(nums1)
        out = []
        for x in nums2:
            if count[x] > 0:
                out.append(x)  #> still have one to match
                count[x] -= 1
        return out
''', [([[1, 2, 2, 1], [2, 2]], [2, 2]), ([[4, 9, 5], [9, 4, 9, 8, 4]], [4, 9])], 'O(n+m)', 'O(n)', cmp='sorted')

P('max-consecutive-ones', 'Longest Run of Ones', 485, 'Easy', T,
  "How many 1s in a row is the longest streak?",
  "Count the current streak; reset to 0 on a 0. Remember the best.",
  ["One pass."],
  '''
class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        cur = best = 0
        for x in nums:
            cur = cur + 1 if x == 1 else 0  #> streak grows or breaks
            best = max(best, cur)
        return best
''', [([[1, 1, 0, 1, 1, 1]], 3), ([[1, 0, 1, 1, 0, 1]], 2)], 'O(n)', 'O(1)')

P('pascals-triangle', "Pascal's Triangle", 118, 'Easy', T,
  "Build the first n rows of Pascal's triangle. Each number is the sum of the two above it; edges are 1.",
  "Each new row starts and ends with 1; the middle is pairs of the previous row added up.",
  ["Row 3 is [1, 2, 1], row 4 is [1, 3, 3, 1]."],
  '''
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        rows = [[1]]
        for _ in range(numRows - 1):
            prev = rows[-1]
            mid = [prev[i] + prev[i + 1] for i in range(len(prev) - 1)]  #> add the two above
            rows.append([1] + mid + [1])
        return rows
''', [([5], [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]), ([1], [[1]])], 'O(n²)', 'O(n²)')

P('largest-number', 'Biggest Number From Pieces', 179, 'Medium', T,
  "Arrange the numbers side by side to make the biggest possible number. Return it as a string.",
  "Sort with a special rule: a goes before b if a+b (as strings) is bigger than b+a.",
  ["\"9\" + \"34\" = \"934\" beats \"349\".", "If the answer starts with 0, it's just \"0\"."],
  '''
from functools import cmp_to_key
class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        s = [str(x) for x in nums]
        s.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else 1))  #> which order glues bigger?
        out = ''.join(s)
        return '0' if out[0] == '0' else out
''', [([[10, 2]], "210"), ([[3, 30, 34, 5, 9]], "9534330"), ([[0, 0]], "0")], 'O(n log n)', 'O(n)')

P('majority-element-ii', 'Who Shows Up a Lot?', 229, 'Medium', T,
  "Find every number that appears more than n/3 times.",
  "Count everything and keep the numbers whose count beats n // 3.",
  ["There can be at most 2 such numbers."],
  '''
from collections import Counter
class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        need = len(nums) // 3
        return [x for x, c in Counter(nums).items() if c > need]  #> more than a third
''', [([[3, 2, 3]], [3]), ([[1]], [1]), ([[1, 2]], [1, 2])], 'O(n)', 'O(n)', cmp='sorted')

P('sort-chars-by-frequency', 'Most Common Letters First', 451, 'Medium', T,
  "Rearrange the letters so the most common ones come first (equal counts: biggest letter first here, to keep one answer).",
  "Count letters, sort by (count, letter) from biggest down, and write each letter count times.",
  ["Counter + sorted with a key."],
  '''
from collections import Counter
class Solution:
    def frequencySort(self, s: str) -> str:
        count = Counter(s)
        order = sorted(count, key=lambda ch: (count[ch], ch), reverse=True)  #> most common first
        return ''.join(ch * count[ch] for ch in order)
''', [(["tree"], "eetr"), (["cccaaa"], "cccaaa"), (["Aabb"], "bbaA")], 'O(n log n)', 'O(n)')
