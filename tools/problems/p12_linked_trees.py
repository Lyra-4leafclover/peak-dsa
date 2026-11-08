from pb import P
L, T = 'Linked List', 'Trees'

P('rotate-list', 'Spin the Train', 61, 'Medium', L,
  "Move the last k cars of the train to the front, one at a time.",
  "Find the length and the tail. Join the tail to the head (a ring), then cut the ring at the right spot.",
  ["k can be huge: use k % length.", "The new tail is length - k - 1 steps from the head."],
  '''
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return None
        n, tail = 1, head
        while tail.next:
            tail = tail.next
            n += 1
        k %= n
        tail.next = head  #> make a ring
        new_tail = head
        for _ in range(n - k - 1):
            new_tail = new_tail.next
        new_head = new_tail.next
        new_tail.next = None  #> cut the ring
        return new_head
''', [([[1, 2, 3, 4, 5], 2], [4, 5, 1, 2, 3]), ([[0, 1, 2], 4], [2, 0, 1]), ([[], 1], [])], 'O(n)', 'O(1)')

P('remove-duplicates-list', 'Remove Repeat Cars', 83, 'Easy', L,
  "The train is sorted. Remove repeated values so each appears once.",
  "If a car has the same value as the next car, skip the next car.",
  ["Only move forward when the next value is different."],
  '''
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next  #> unhook the twin
            else:
                cur = cur.next
        return head
''', [([[1, 1, 2]], [1, 2]), ([[1, 1, 2, 3, 3]], [1, 2, 3])], 'O(n)', 'O(1)')

P('remove-duplicates-list-ii', 'Remove Every Repeated Value', 82, 'Medium', L,
  "Sorted train. Remove ALL cars whose value appears more than once.",
  "Use a dummy front car. When you spot a run of equal values, skip the whole run.",
  ["prev stays on the last car you're keeping."],
  '''
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while head:
            if head.next and head.val == head.next.val:
                while head.next and head.val == head.next.val:
                    head = head.next  #> walk past the whole run
                prev.next = head.next  #> drop the run
            else:
                prev = prev.next
            head = head.next
        return dummy.next
''', [([[1, 2, 3, 3, 4, 4, 5]], [1, 2, 5]), ([[1, 1, 1, 2, 3]], [2, 3])], 'O(n)', 'O(1)')

P('partition-list', 'Small Cars First', 86, 'Medium', L,
  "Move all cars with value less than x before the others, keeping the original order inside each group.",
  "Build two little trains (small and big), then hook the big one after the small one.",
  ["Two dummy heads make it easy.", "End the big train with None."],
  '''
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        small, big = ListNode(0), ListNode(0)
        s, b = small, big
        while head:
            if head.val < x:
                s.next = head  #> goes on the small train
                s = s.next
            else:
                b.next = head
                b = b.next
            head = head.next
        b.next = None
        s.next = big.next  #> join the trains
        return small.next
''', [([[1, 4, 3, 2, 5, 2], 3], [1, 2, 2, 4, 3, 5]), ([[2, 1], 2], [1, 2])], 'O(n)', 'O(1)')

P('reverse-linked-list-ii', 'Turn Around Part of the Train', 92, 'Medium', L,
  "Reverse only the cars from position left to position right (counting from 1).",
  "Walk to the car before 'left'. Then repeatedly pull the next car out and put it right after that car.",
  ["A dummy front car handles left = 1."],
  '''
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        before = dummy
        for _ in range(left - 1):
            before = before.next
        cur = before.next
        for _ in range(right - left):
            move = cur.next
            cur.next = move.next
            move.next = before.next  #> pull it to the front of the section
            before.next = move
        return dummy.next
''', [([[1, 2, 3, 4, 5], 2, 4], [1, 4, 3, 2, 5]), ([[5], 1, 1], [5])], 'O(n)', 'O(1)')

P('sort-list', 'Sort the Train', 148, 'Medium', L,
  "Sort the train's values from small to big.",
  "Merge sort: cut the train in half with slow/fast pointers, sort each half, zip them back together.",
  ["Base case: 0 or 1 car is sorted.", "Merging is the zip-two-sorted-trains trick."],
  '''
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        slow, fast = head, head.next
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
        right = slow.next
        slow.next = None  #> cut in half
        a, b = self.sortList(head), self.sortList(right)
        dummy = tail = ListNode(0)
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b  #> zip the halves
        return dummy.next
''', [([[4, 2, 1, 3]], [1, 2, 3, 4]), ([[-1, 5, 3, 4, 0]], [-1, 0, 3, 4, 5]), ([[]], [])], 'O(n log n)', 'O(log n)')

P('odd-even-list', 'Odd Cars, Then Even Cars', 328, 'Medium', L,
  "Group the 1st, 3rd, 5th... cars first, then the 2nd, 4th, 6th..., keeping order inside each group.",
  "Keep two chains (odd and even) and weave through, then attach the even chain after the odd one.",
  ["Remember the first even car so you can attach it at the end."],
  '''
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        odd, even = head, head.next
        even_head = even
        while even and even.next:
            odd.next = even.next  #> odd skips over even
            odd = odd.next
            even.next = odd.next
            even = even.next
        odd.next = even_head
        return head
''', [([[1, 2, 3, 4, 5]], [1, 3, 5, 2, 4]), ([[2, 1, 3, 5, 6, 4, 7]], [2, 3, 6, 7, 1, 5, 4])], 'O(n)', 'O(1)')

P('delete-middle-node', 'Remove the Middle Car', 2095, 'Medium', L,
  "Remove the middle car (for n cars, the one at position n // 2, counting from 0).",
  "Fast moves 2, slow moves 1, but start fast one step ahead so slow stops just BEFORE the middle.",
  ["A single car becomes an empty train."],
  '''
class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head.next:
            return None
        slow, fast = head, head.next.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        slow.next = slow.next.next  #> unhook the middle car
        return head
''', [([[1, 3, 4, 7, 1, 2, 6]], [1, 3, 4, 1, 2, 6]), ([[1, 2, 3, 4]], [1, 2, 4]), ([[2, 1]], [2])], 'O(n)', 'O(1)')

P('max-twin-sum', 'Best Twin Pair', 2130, 'Medium', L,
  "Even-length train. Car i's twin is car n-1-i. Find the biggest twin sum.",
  "Copy the values into a list, then add pairs from both ends.",
  ["Or reverse the second half in place for O(1) memory."],
  '''
class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        n = len(vals)
        return max(vals[i] + vals[n - 1 - i] for i in range(n // 2))  #> add each twin pair
''', [([[5, 4, 2, 1]], 6), ([[4, 2, 2, 3]], 7), ([[1, 100000]], 100001)], 'O(n)', 'O(n)')

P('swap-pairs', 'Swap Neighbour Cars', 24, 'Medium', L,
  "Swap every two neighbouring cars (1-2, 3-4, ...). Move the cars, not just the values.",
  "Dummy front car. For each pair a, b: point prev to b, b to a, a to whatever came after.",
  ["Three hooks change per swap."],
  '''
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a, b = prev.next, prev.next.next
            a.next = b.next
            b.next = a  #> b jumps in front of a
            prev.next = b
            prev = a
        return dummy.next
''', [([[1, 2, 3, 4]], [2, 1, 4, 3]), ([[]], []), ([[1, 2, 3]], [2, 1, 3])], 'O(n)', 'O(1)')

P('inorder-traversal', 'Visit Left, Me, Right', 94, 'Easy', T,
  "List the tree's values in inorder: left side first, then the node, then the right side.",
  "Recursion: walk(left), add me, walk(right).",
  ["For a BST this gives sorted order."],
  '''
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        out = []
        def walk(node):
            if not node:
                return
            walk(node.left)
            out.append(node.val)  #> left is done, now me
            walk(node.right)
        walk(root)
        return out
''', [([[1, None, 2, 3]], [1, 3, 2]), ([[1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9]], [4, 2, 6, 5, 7, 1, 3, 9, 8]), ([[]], [])], 'O(n)', 'O(h)')

P('preorder-traversal', 'Visit Me, Left, Right', 144, 'Easy', T,
  "List the values in preorder: the node first, then its left side, then its right side.",
  "Recursion: add me, walk(left), walk(right).",
  ["Like reading a family tree from the top."],
  '''
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        out = []
        def walk(node):
            if node:
                out.append(node.val)  #> me first
                walk(node.left)
                walk(node.right)
        walk(root)
        return out
''', [([[1, None, 2, 3]], [1, 2, 3]), ([[1, 2, 3, 4, 5]], [1, 2, 4, 5, 3])], 'O(n)', 'O(h)')

P('postorder-traversal', 'Visit Left, Right, Me', 145, 'Easy', T,
  "List the values in postorder: left side, right side, then the node.",
  "Recursion: walk(left), walk(right), add me.",
  ["Kids before parents, like cleaning up from the bottom."],
  '''
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        out = []
        def walk(node):
            if node:
                walk(node.left)
                walk(node.right)
                out.append(node.val)  #> both kids done, now me
        walk(root)
        return out
''', [([[1, None, 2, 3]], [3, 2, 1]), ([[1, 2, 3, 4, 5]], [4, 5, 2, 3, 1])], 'O(n)', 'O(h)')

P('zigzag-level-order', 'Zigzag Floor by Floor', 103, 'Medium', T,
  "List each floor of the tree, but alternate direction: left-to-right, then right-to-left, and so on.",
  "Normal BFS floor by floor; reverse every other floor.",
  ["A flag flips each floor."],
  '''
from collections import deque
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        out, q, flip = [], deque([root]), False
        while q:
            floor = []
            for _ in range(len(q)):
                node = q.popleft()
                floor.append(node.val)
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
            out.append(floor[::-1] if flip else floor)  #> every other floor backwards
            flip = not flip
        return out
''', [([[3, 9, 20, None, None, 15, 7]], [[3], [20, 9], [15, 7]]), ([[1]], [[1]]), ([[]], [])], 'O(n)', 'O(n)')

P('build-tree-in-post', 'Rebuild From Inorder and Postorder', 106, 'Medium', T,
  "Given the inorder and postorder lists of a tree (no repeated values), rebuild the tree.",
  "The LAST postorder value is the root. Find it in inorder: everything left of it is the left subtree, right is the right subtree.",
  ["Build the right subtree first when popping from the end of postorder.", "A dict of positions makes finding fast."],
  '''
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        where = {v: i for i, v in enumerate(inorder)}
        def build(lo, hi):
            if lo > hi:
                return None
            val = postorder.pop()  #> last one is this subtree's root
            node = TreeNode(val)
            node.right = build(where[val] + 1, hi)
            node.left = build(lo, where[val] - 1)
            return node
        return build(0, len(inorder) - 1)
''', [([[9, 3, 15, 20, 7], [9, 15, 7, 20, 3]], [3, 9, 20, None, None, 15, 7]), ([[-1], [-1]], [-1])], 'O(n)', 'O(n)')

P('flatten-tree', 'Squash the Tree Into a Line', 114, 'Medium', T,
  "Flatten the tree into a 'linked list' using right pointers, in preorder order. Left pointers become None. Change the tree itself.",
  "For each node: if it has a left side, find the rightmost node of that left side, hook the right side after it, move the left side to the right.",
  ["Work down the right spine one node at a time."],
  '''
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        cur = root
        while cur:
            if cur.left:
                tail = cur.left
                while tail.right:
                    tail = tail.right  #> end of the left side
                tail.right = cur.right
                cur.right = cur.left  #> left side moves to the right
                cur.left = None
            cur = cur.right
''', [([[1, 2, 5, 3, 4, None, 6]], [1, None, 2, None, 3, None, 4, None, 5, None, 6]), ([[0]], [0])], 'O(n)', 'O(1)', inplace=0)

P('sum-root-to-leaf', 'Path Numbers', 129, 'Medium', T,
  "Every root-to-leaf path spells a number (1→2→3 is 123). Add all those numbers.",
  "Carry the number so far down: new = old × 10 + digit. At a leaf, return it.",
  ["Empty side gives 0."],
  '''
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def go(node, num):
            if not node:
                return 0
            num = num * 10 + node.val  #> add this digit
            if not node.left and not node.right:
                return num  #> a leaf: the number is complete
            return go(node.left, num) + go(node.right, num)
        return go(root, 0)
''', [([[1, 2, 3]], 25), ([[4, 9, 0, 5, 1]], 1026)], 'O(n)', 'O(h)')

P('count-complete-tree-nodes', 'Count a Full-ish Tree Fast', 222, 'Easy', T,
  "A complete tree (every floor full except maybe the last, filled from the left). Count its nodes.",
  "If the leftmost and rightmost depths match, the tree is perfect: 2^h - 1 nodes. Otherwise count each side the same way.",
  ["This skips most of the tree."],
  '''
class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        l, r = root, root
        hl = hr = 0
        while l:
            l, hl = l.left, hl + 1
        while r:
            r, hr = r.right, hr + 1
        if hl == hr:
            return 2 ** hl - 1  #> perfect tree: use the formula
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)
''', [([[1, 2, 3, 4, 5, 6]], 6), ([[]], 0), ([[1]], 1)], 'O(log² n)', 'O(log n)')

P('path-sum-iii', 'Paths That Add Up (Anywhere)', 437, 'Medium', T,
  "Count downward paths (they can start and end anywhere, but must go down) whose values add up to target.",
  "Running sums along the current root-to-node path. If (current sum - target) was seen before on this path, those are valid paths.",
  ["A dict of prefix sums; undo it when you go back up.", "Same trick as 'subarray sum equals k'."],
  '''
from collections import Counter
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        seen = Counter({0: 1})
        def go(node, total):
            if not node:
                return 0
            total += node.val
            count = seen[total - targetSum]  #> paths ending here
            seen[total] += 1
            count += go(node.left, total) + go(node.right, total)
            seen[total] -= 1  #> leaving this path
            return count
        return go(root, 0)
''', [([[10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], 8], 3), ([[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22], 3)], 'O(n)', 'O(n)')

P('delete-node-bst', 'Remove a Value From a BST', 450, 'Medium', T,
  "Delete the node with value key from a binary search tree and keep it a valid BST.",
  "Find it. No kids or one kid: replace it with its kid. Two kids: copy in the smallest value from its right side, then delete that one instead.",
  ["The smallest on the right is the leftmost node there."],
  '''
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.left:
                return root.right  #> one kid (or none): it takes my place
            if not root.right:
                return root.left
            nxt = root.right
            while nxt.left:
                nxt = nxt.left
            root.val = nxt.val  #> borrow the next-bigger value
            root.right = self.deleteNode(root.right, nxt.val)
        return root
''', [([[5, 3, 6, 2, 4, None, 7], 3], [5, 4, 6, 2, None, None, 7]), ([[5, 3, 6, 2, 4, None, 7], 0], [5, 3, 6, 2, 4, None, 7]), ([[], 0], [])], 'O(h)', 'O(h)')

P('min-diff-bst', 'Closest Two Values in a BST', 530, 'Easy', T,
  "Find the smallest difference between any two values in a BST.",
  "Inorder gives sorted values. The closest pair must be neighbours in that order.",
  ["Remember the previous value while walking."],
  '''
class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        vals = []
        def walk(n):
            if n:
                walk(n.left)
                vals.append(n.val)
                walk(n.right)
        walk(root)
        return min(b - a for a, b in zip(vals, vals[1:]))  #> neighbours in sorted order
''', [([[4, 2, 6, 1, 3]], 1), ([[1, 0, 48, None, None, 12, 49]], 1)], 'O(n)', 'O(n)')

P('average-of-levels', 'Average of Each Floor', 637, 'Easy', T,
  "Return the average value on each floor of the tree.",
  "BFS floor by floor; average = sum / count.",
  ["len(q) at the start of a floor tells how many nodes it has."],
  '''
from collections import deque
class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        out, q = [], deque([root])
        while q:
            total, n = 0, len(q)
            for _ in range(n):
                node = q.popleft()
                total += node.val
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
            out.append(total / n)  #> this floor's average
        return out
''', [([[3, 9, 20, None, None, 15, 7]], [3.0, 14.5, 11.0]), ([[3, 9, 20, 15, 7]], [3.0, 14.5, 11.0])], 'O(n)', 'O(n)')

P('max-width-tree', 'Widest Floor', 662, 'Medium', T,
  "How wide is the widest floor, counting the gaps between the leftmost and rightmost nodes?",
  "Number the nodes like a heap: kids of i are 2i and 2i+1. Width of a floor = last number - first number + 1.",
  ["BFS with (node, number) pairs."],
  '''
class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        best, floor = 0, [(root, 0)]
        while floor:
            best = max(best, floor[-1][1] - floor[0][1] + 1)  #> right number - left number
            nxt = []
            for node, i in floor:
                if node.left: nxt.append((node.left, 2 * i))
                if node.right: nxt.append((node.right, 2 * i + 1))
            floor = nxt
        return best
''', [([[1, 3, 2, 5, 3, None, 9]], 4), ([[1, 3, 2, 5, None, None, 9, 6, None, 7]], 7), ([[1, 3, 2, 5]], 2)], 'O(n)', 'O(n)')

P('leaf-similar', 'Same Leaves?', 872, 'Easy', T,
  "Read the leaves of each tree from left to right. Do the two trees have the same leaf sequence?",
  "Collect leaves with DFS for both trees and compare the lists.",
  ["A leaf has no kids."],
  '''
class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        def leaves(n, out):
            if n:
                if not n.left and not n.right:
                    out.append(n.val)  #> found a leaf
                leaves(n.left, out)
                leaves(n.right, out)
            return out
        return leaves(root1, []) == leaves(root2, [])
''', [([[3, 5, 1, 6, 2, 9, 8, None, None, 7, 4], [3, 5, 1, 6, 7, 4, 2, None, None, None, None, None, None, 9, 8]], True), ([[1, 2, 3], [1, 3, 2]], False)], 'O(n+m)', 'O(n+m)')

P('max-level-sum', 'The Richest Floor', 1161, 'Medium', T,
  "Floors are numbered from 1 at the root. Which floor has the biggest sum? (Ties: the smallest floor.)",
  "BFS floor by floor, tracking the best sum and its floor number.",
  ["Only replace the best on a strictly bigger sum."],
  '''
class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        best, best_lvl, lvl, floor = float('-inf'), 1, 1, [root]
        while floor:
            s = sum(n.val for n in floor)
            if s > best:
                best, best_lvl = s, lvl  #> new richest floor
            floor = [k for n in floor for k in (n.left, n.right) if k]
            lvl += 1
        return best_lvl
''', [([[1, 7, 0, 7, -8, None, None]], 2), ([[989, None, 10250, 98693, -89388, None, None, None, -32127]], 2)], 'O(n)', 'O(n)')

P('longest-zigzag-path', 'Longest Zigzag Walk', 1372, 'Medium', T,
  "Walk down the tree changing direction every step (left, right, left...). How many steps is the longest such walk?",
  "DFS carrying two numbers: the zigzag length if I arrived going left, and if I arrived going right.",
  ["Going left from a node continues a walk that arrived going right."],
  '''
class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        best = 0
        def go(node, left_len, right_len):
            nonlocal best
            if not node:
                return
            best = max(best, left_len, right_len)
            go(node.left, right_len + 1, 0)  #> turn left: continues a right-arrival
            go(node.right, 0, left_len + 1)
        go(root, 0, 0)
        return best
''', [([[1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1]], 3), ([[1, 1, 1, None, 1, None, None, 1, 1, None, 1]], 4), ([[1]], 0)], 'O(n)', 'O(h)')

P('path-sum-ii', 'Every Path That Adds Up', 113, 'Medium', T,
  "List every root-to-leaf path whose values add up to target.",
  "Backtracking down the tree: add me to the path, recurse, then remove me.",
  ["Save a COPY of the path at a good leaf."],
  '''
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        out, path = [], []
        def go(node, left):
            if not node:
                return
            path.append(node.val)
            left -= node.val
            if not node.left and not node.right and left == 0:
                out.append(path[:])  #> a full path that works
            go(node.left, left)
            go(node.right, left)
            path.pop()  #> step back up
        go(root, targetSum)
        return out
''', [([[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22], [[5, 4, 11, 2], [5, 8, 4, 5]]), ([[1, 2, 3], 5], [])], 'O(n²)', 'O(h)', cmp='deep')

P('binary-tree-paths', 'Write Down Every Path', 257, 'Easy', T,
  "List every root-to-leaf path as a string like \"1->2->5\".",
  "DFS carrying the path string so far.",
  ["Add '->' between values."],
  '''
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        out = []
        def go(node, s):
            s = s + '->' + str(node.val) if s else str(node.val)
            if not node.left and not node.right:
                out.append(s)  #> a leaf: path complete
            if node.left: go(node.left, s)
            if node.right: go(node.right, s)
        go(root, '')
        return out
''', [([[1, 2, 3, None, 5]], ["1->2->5", "1->3"]), ([[1]], ["1"])], 'O(n²)', 'O(h)', cmp='sorted')

P('sum-left-leaves', 'Add Up the Left Leaves', 404, 'Easy', T,
  "Add the values of every leaf that is someone's LEFT child.",
  "DFS. When a node's left child is a leaf, count it.",
  ["Pass down whether you're a left child."],
  '''
class Solution:
    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
        def go(node, is_left):
            if not node:
                return 0
            if not node.left and not node.right:
                return node.val if is_left else 0  #> only left leaves count
            return go(node.left, True) + go(node.right, False)
        return go(root, False)
''', [([[3, 9, 20, None, None, 15, 7]], 24), ([[1]], 0)], 'O(n)', 'O(h)')

P('merge-two-trees', 'Stack Two Trees', 617, 'Easy', T,
  "Lay one tree on top of the other. Where both have a node, add the values; otherwise take whichever exists.",
  "Recursion: if one side is empty return the other; else add values and merge both kids.",
  ["Reuse tree 1's nodes."],
  '''
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root1:
            return root2
        if not root2:
            return root1
        root1.val += root2.val  #> both here: add them
        root1.left = self.mergeTrees(root1.left, root2.left)
        root1.right = self.mergeTrees(root1.right, root2.right)
        return root1
''', [([[1, 3, 2, 5], [2, 1, 3, None, 4, None, 7]], [3, 4, 5, 5, 4, None, 7]), ([[1], [1, 2]], [2, 2])], 'O(n)', 'O(h)')

P('two-sum-bst', 'Two Sum in a Tree', 653, 'Easy', T,
  "Are there two different nodes in the BST whose values add up to k?",
  "Walk the tree with a set of values seen. For each value x, check if k - x was seen.",
  ["Same idea as the classic Two Sum."],
  '''
class Solution:
    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        seen = set()
        def go(n):
            if not n:
                return False
            if k - n.val in seen:
                return True  #> partner found
            seen.add(n.val)
            return go(n.left) or go(n.right)
        return go(root)
''', [([[5, 3, 6, 2, 4, None, 7], 9], True), ([[5, 3, 6, 2, 4, None, 7], 28], False)], 'O(n)', 'O(n)')

P('search-bst', 'Find a Value in a BST', 700, 'Easy', T,
  "Find the node with value val in a BST and return its whole subtree (or nothing).",
  "Smaller? go left. Bigger? go right. Equal? found.",
  ["Like the higher-or-lower game."],
  '''
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        while root and root.val != val:
            root = root.left if val < root.val else root.right  #> higher or lower?
        return root
''', [([[4, 2, 7, 1, 3], 2], [2, 1, 3]), ([[4, 2, 7, 1, 3], 5], [])], 'O(h)', 'O(1)')

P('unique-bsts', 'How Many Different BSTs?', 96, 'Medium', T,
  "How many differently shaped BSTs can hold the values 1 to n?",
  "Pick each value as the root. Left side has i-1 values, right side n-i. Multiply the counts and add up (dynamic programming).",
  ["count[0] = count[1] = 1.", "These are the Catalan numbers."],
  '''
class Solution:
    def numTrees(self, n: int) -> int:
        count = [1, 1] + [0] * (n - 1)
        for total in range(2, n + 1):
            for root in range(1, total + 1):
                count[total] += count[root - 1] * count[total - root]  #> left shapes × right shapes
        return count[n]
''', [([3], 5), ([1], 1), ([4], 14)], 'O(n²)', 'O(n)')
