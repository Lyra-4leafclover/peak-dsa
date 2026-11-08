from pb import P
T = 'Linked List'

P('reverse-linked-list', 'Turn the Train Around', 206, 'Easy', T,
  "A linked list is a train: each car points to the next. Make every car point backwards and return the new front.",
  "Walk along with three hands: prev, cur, and the saved next. Flip cur's arrow to prev, then step forward.",
  ["Save cur.next BEFORE you flip the arrow, or you lose the rest of the train.", "At the end, prev is the new head."],
  '''
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        cur = head
        while cur:
            nxt = cur.next  #> remember the rest of the train
            cur.next = prev  #> flip this car's arrow backwards
            prev = cur  #> step forward
            cur = nxt
        return prev
''', [([[1, 2, 3, 4, 5]], [5, 4, 3, 2, 1]), ([[1, 2]], [2, 1]), ([[]], [])], 'O(n)', 'O(1)')

P('merge-two-lists', 'Zip Two Sorted Trains', 21, 'Easy', T,
  "Two sorted linked lists. Join them into one sorted list.",
  "Use a fake front car (dummy). Repeatedly attach the smaller of the two front cars.",
  ["A dummy node saves you from special-casing the first car.", "When one runs out, attach the rest of the other."],
  '''
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)  #> fake front car
        tail = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1  #> attach the smaller car
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 or list2  #> attach whatever is left
        return dummy.next
''', [([[1, 2, 4], [1, 3, 4]], [1, 1, 2, 3, 4, 4]), ([[], []], []), ([[], [0]], [0])], 'O(n+m)', 'O(1)')

P('linked-list-cycle', 'Train Going in Circles?', 141, 'Easy', T,
  "Does the train loop back on itself? (The second input says which car the last one links back to; -1 means no loop.)",
  "Tortoise and hare: one pointer moves 1 step, the other 2. If there's a loop, the fast one laps the slow one.",
  ["If fast reaches the end (None), there's no loop.", "No extra memory needed."],
  '''
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next  #> tortoise: 1 step
            fast = fast.next.next  #> hare: 2 steps
            if slow is fast:
                return True  #> the hare lapped the tortoise
        return False
''', [([[3, 2, 0, -4], 1], True), ([[1, 2], 0], True), ([[1], -1], False)], 'O(n)', 'O(1)', cycle=1)

P('middle-of-list', 'Find the Middle Car', 876, 'Easy', T,
  "Return the middle car of the train (the second middle if there are two).",
  "Slow moves 1, fast moves 2. When fast reaches the end, slow is in the middle.",
  ["Fast covers twice the distance.", "Return slow."],
  '''
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow  #> slow is halfway
''', [([[1, 2, 3, 4, 5]], [3, 4, 5]), ([[1, 2, 3, 4, 5, 6]], [4, 5, 6])], 'O(n)', 'O(1)')

P('reorder-list', 'Shuffle: First, Last, Second, Second-Last…', 143, 'Medium', T,
  "Reorder L0→L1→…→Ln into L0→Ln→L1→Ln-1→… in place.",
  "Three moves: find the middle, reverse the back half, then zip the two halves together.",
  ["Each step is its own easy problem!", "Cut the list at the middle."],
  '''
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        slow, fast = head, head.next
        while fast and fast.next:  #> 1) find the middle
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None  #> cut the train in two
        prev = None
        while second:  #> 2) reverse the back half
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt
        first, second = head, prev
        while second:  #> 3) zip them together
            n1, n2 = first.next, second.next
            first.next = second
            second.next = n1
            first, second = n1, n2
''', [([[1, 2, 3, 4]], [1, 4, 2, 3]), ([[1, 2, 3, 4, 5]], [1, 5, 2, 4, 3])], 'O(n)', 'O(1)', inplace=0)

P('remove-nth-from-end', 'Remove the N-th Car From the Back', 19, 'Medium', T,
  "Remove the n-th car counting from the end, and return the head.",
  "Send a scout n steps ahead. Then move both together; when the scout hits the end, the other is right before the car to remove.",
  ["A dummy front car handles removing the very first car.", "The gap between the two pointers stays n."],
  '''
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        scout = head
        for _ in range(n):
            scout = scout.next  #> scout gets an n-car head start
        behind = dummy
        while scout:
            scout = scout.next
            behind = behind.next
        behind.next = behind.next.next  #> skip over the unlucky car
        return dummy.next
''', [([[1, 2, 3, 4, 5], 2], [1, 2, 3, 5]), ([[1], 1], []), ([[1, 2], 1], [1])], 'O(n)', 'O(1)')

P('copy-random-list', 'Copy a Train With Wild Arrows', 138, 'Medium', T,
  "Each car has a next arrow AND a random arrow (to any car, or None). Make a deep copy. Input pairs are [value, random_index].",
  "First pass: make a copy of every car and store old→new in a dictionary. Second pass: wire up next and random using the dictionary.",
  ["The dictionary is the map from originals to clones.", "map[None] = None makes things easy."],
  '''
class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        clone = {None: None}
        cur = head
        while cur:
            clone[cur] = Node(cur.val)  #> 1) make a twin of each car
            cur = cur.next
        cur = head
        while cur:
            clone[cur].next = clone[cur.next]  #> 2) wire the twins
            clone[cur].random = clone[cur.random]
            cur = cur.next
        return clone[head]
''', [([[[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]], [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]), ([[[1, 1], [2, 1]]], [[1, 1], [2, 1]])], 'O(n)', 'O(n)', types={'head': 'random'}, nodeMode='random')

P('add-two-numbers', 'Add Numbers Written Backwards', 2, 'Medium', T,
  "Two numbers stored digit-by-digit in reverse (342 is 2→4→3). Add them and return the sum the same way.",
  "Add digit by digit like you did in school, carrying the 1.",
  ["Keep going while either list or the carry is left.", "digit = total % 10, carry = total // 10."],
  '''
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            carry = total // 10  #> the 1 you carry
            tail.next = ListNode(total % 10)
            tail = tail.next
        return dummy.next
''', [([[2, 4, 3], [5, 6, 4]], [7, 0, 8]), ([[0], [0]], [0]), ([[9, 9, 9], [9]], [8, 0, 0, 1])], 'O(n)', 'O(n)')

P('find-duplicate-number', 'The Repeated Number (Loop Trick)', 287, 'Medium', T,
  "n+1 numbers, each from 1 to n, one repeats. Find it without changing the list and with O(1) memory.",
  "Treat each value as an arrow to an index. The repeat is where two arrows point to the same spot: the start of a loop. Use tortoise & hare.",
  ["Phase 1: find where slow and fast meet.", "Phase 2: restart one at 0, move both by 1; they meet at the loop start."],
  '''
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break  #> they met inside the loop
        slow2 = 0
        while slow2 != slow:
            slow = nums[slow]
            slow2 = nums[slow2]
        return slow  #> the loop's entrance = the duplicate
''', [([[1, 3, 4, 2, 2]], 2), ([[3, 1, 3, 4, 2]], 3)], 'O(n)', 'O(1)')

P('lru-cache', 'Forgetful Cache (LRU)', 146, 'Medium', T,
  "A cache with limited space. When full, throw out the item used least recently. get and put must be instant.",
  "OrderedDict keeps items in usage order. Move an item to the end when used; pop from the front when full.",
  ["Classic version: hash map + doubly linked list.", "OrderedDict.move_to_end and popitem(last=False)."],
  '''
class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.d = OrderedDict()  #> oldest at the front, newest at the back

    def get(self, key: int) -> int:
        if key not in self.d:
            return -1
        self.d.move_to_end(key)  #> just used: now the newest
        return self.d[key]

    def put(self, key: int, value: int) -> None:
        self.d[key] = value
        self.d.move_to_end(key)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)  #> evict the oldest
''', [([["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"], [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]], [None, None, None, 1, None, -1, None, -1, 3, 4])], 'O(1)', 'O(capacity)', mode='design')

P('merge-k-lists', 'Zip K Sorted Trains', 23, 'Hard', T,
  "Merge k sorted linked lists into one sorted list.",
  "Put the front car of each train into a min-heap. Repeatedly take the smallest, attach it, and push its next car.",
  ["The heap always holds at most k cars.", "Store (value, index, node) so ties don't compare nodes."],
  '''
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        for i, node in enumerate(lists):
            if node:
                heappush(heap, (node.val, i, node))  #> each train's front car
        dummy = ListNode(0)
        tail = dummy
        while heap:
            val, i, node = heappop(heap)  #> smallest front car
            tail.next = node
            tail = node
            if node.next:
                heappush(heap, (node.next.val, i, node.next))
        return dummy.next
''', [([[[1, 4, 5], [1, 3, 4], [2, 6]]], [1, 1, 2, 3, 4, 4, 5, 6]), ([[]], [])], 'O(N log k)', 'O(k)', types={'lists': 'lists'})

P('reverse-k-group', 'Flip Every K Cars', 25, 'Hard', T,
  "Reverse the train in groups of k cars. A leftover group shorter than k stays as is.",
  "For each group: check there are k cars, reverse just those, then reconnect to the part before and after.",
  ["Keep a pointer to the car just before the group.", "After reversing, the group's old first car is its new last."],
  '''
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        before = dummy
        while True:
            kth = before
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next  #> fewer than k left
            after = kth.next
            prev, cur = after, before.next
            while cur is not after:  #> reverse this group
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt
            first = before.next
            before.next = kth  #> reconnect
            before = first
''', [([[1, 2, 3, 4, 5], 2], [2, 1, 4, 3, 5]), ([[1, 2, 3, 4, 5], 3], [3, 2, 1, 4, 5])], 'O(n)', 'O(1)')

P('palindrome-linked-list', 'Train Reads the Same Both Ways?', 234, 'Easy', T,
  "Do the car numbers read the same forwards and backwards?",
  "Find the middle, reverse the second half, and compare it with the first half.",
  ["Fast/slow pointers find the middle.", "Or copy values into a list (uses more memory)."],
  '''
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        prev = None
        while slow:  #> reverse the back half
            nxt = slow.next
            slow.next = prev
            prev = slow
            slow = nxt
        a, b = head, prev
        while b:
            if a.val != b.val:
                return False
            a, b = a.next, b.next
        return True
''', [([[1, 2, 2, 1]], True), ([[1, 2]], False), ([[1, 2, 3, 2, 1]], True)], 'O(n)', 'O(1)')

P('remove-list-elements', 'Kick Out Cars With a Value', 203, 'Easy', T,
  "Remove every car whose value equals val.",
  "Dummy front car, then skip over any next car that matches.",
  ["Don't move forward after a removal: the new next might match too.", "Return dummy.next."],
  '''
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        cur = dummy
        while cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next  #> skip it
            else:
                cur = cur.next
        return dummy.next
''', [([[1, 2, 6, 3, 4, 5, 6], 6], [1, 2, 3, 4, 5]), ([[7, 7, 7], 7], [])], 'O(n)', 'O(1)')

P('intersection-two-lists', 'Where Two Trains Join', 160, 'Easy', T,
  "Two trains merge into the same tail. Return the value where they first share a car (inputs: listA, listB, skipA, skipB of the shared part), or None.",
  "Walk A then B, and B then A. Both walkers travel the same total distance, so they arrive at the meeting car together.",
  ["Switch tracks when you hit the end.", "If there's no meeting car, both reach None together."],
  '''
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        a, b = headA, headB
        while a is not b:
            a = a.next if a else headB  #> finished A? hop onto B
            b = b.next if b else headA
        return a.val if a else None
''', [([[4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], 2, 3], 8), ([[2, 6, 4], [1, 5], 3, 2], None)], 'O(n+m)', 'O(1)', types={'headA': 'joined'})
