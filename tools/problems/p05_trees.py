from pb import P
T = 'Trees'

P('invert-tree', 'Mirror the Tree', 226, 'Easy', T,
  "Flip a binary tree like looking at it in a mirror: every left child swaps with its right child.",
  "Swap the two children of the root, then do the same thing to each child (recursion!).",
  ["An empty tree is already mirrored.", "Swap, then recurse on both sides."],
  '''
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None  #> nothing to flip
        root.left, root.right = root.right, root.left  #> swap my kids
        self.invertTree(root.left)  #> now flip each side too
        self.invertTree(root.right)
        return root
''', [([[4, 2, 7, 1, 3, 6, 9]], [4, 7, 2, 9, 6, 3, 1]), ([[2, 1, 3]], [2, 3, 1]), ([[]], [])], 'O(n)', 'O(h)')

P('max-depth', 'How Tall Is the Tree?', 104, 'Easy', T,
  "Count the number of floors from the root down to the deepest leaf.",
  "My height = 1 + the taller of my two kids' heights. An empty spot has height 0.",
  ["Trust the recursion: ask each child for its height.", "max(left, right) + 1"],
  '''
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0  #> empty spot: 0 floors
        left = self.maxDepth(root.left)  #> ask the left kid
        right = self.maxDepth(root.right)  #> ask the right kid
        return 1 + max(left, right)  #> me + the taller side
''', [([[3, 9, 20, None, None, 15, 7]], 3), ([[1, None, 2]], 2), ([[]], 0)], 'O(n)', 'O(h)')

P('same-tree', 'Twin Trees?', 100, 'Easy', T,
  "Are two trees exactly the same shape with the same numbers?",
  "Both empty: same. One empty: different. Otherwise values must match AND both left subtrees and both right subtrees must match.",
  ["Compare root values first.", "Then recurse left with left, right with right."],
  '''
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
''', [([[1, 2, 3], [1, 2, 3]], True), ([[1, 2], [1, None, 2]], False)], 'O(n)', 'O(h)')

P('subtree-of-another', 'Tree Hiding Inside a Tree', 572, 'Easy', T,
  "Is there a node in the big tree where the small tree appears exactly?",
  "At every node of the big tree, ask 'is the tree starting here the same as the small one?'",
  ["Reuse Same Tree.", "Check root, then left subtree, then right subtree."],
  '''
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def same(a, b):
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return same(a.left, b.left) and same(a.right, b.right)
        if not root:
            return False
        if same(root, subRoot):
            return True  #> found it starting here
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
''', [([[3, 4, 5, 1, 2], [4, 1, 2]], True), ([[3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2]], False)], 'O(n·m)', 'O(h)')

P('diameter-tree', 'Longest Path in the Tree', 543, 'Easy', T,
  "Find the longest path (counted in edges) between any two nodes.",
  "At each node, the longest path through it = left height + right height. Track the best while computing heights.",
  ["Compute heights bottom-up.", "Update a 'best' variable at every node."],
  '''
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        best = 0
        def height(node):
            nonlocal best
            if not node:
                return 0
            l = height(node.left)
            r = height(node.right)
            best = max(best, l + r)  #> a path bending at this node
            return 1 + max(l, r)
        height(root)
        return best
''', [([[1, 2, 3, 4, 5]], 3), ([[1, 2]], 1)], 'O(n)', 'O(h)')

P('balanced-tree', 'Is the Tree Balanced?', 110, 'Easy', T,
  "A tree is balanced if, at every node, the two sides' heights differ by at most 1.",
  "Compute heights bottom-up, but return -1 as a 'broken!' signal as soon as any node is unbalanced.",
  ["A single pass is enough.", "If a child says -1, pass -1 up."],
  '''
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def h(node):
            if not node:
                return 0
            l, r = h(node.left), h(node.right)
            if l == -1 or r == -1 or abs(l - r) > 1:
                return -1  #> broken somewhere below
            return 1 + max(l, r)
        return h(root) != -1
''', [([[3, 9, 20, None, None, 15, 7]], True), ([[1, 2, 2, 3, 3, None, None, 4, 4]], False), ([[]], True)], 'O(n)', 'O(h)')

P('level-order', 'Read the Tree Floor by Floor', 102, 'Medium', T,
  "Return the node values one floor at a time, left to right.",
  "Breadth-first search with a queue. Process exactly one floor's worth of nodes, adding their kids for the next floor.",
  ["len(queue) at the start of a round = nodes on this floor.", "deque.popleft() is fast."],
  '''
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        res = []
        q = deque([root])
        while q:
            floor = []
            for _ in range(len(q)):  #> everyone on this floor
                node = q.popleft()
                floor.append(node.val)
                if node.left:
                    q.append(node.left)  #> kids wait for the next floor
                if node.right:
                    q.append(node.right)
            res.append(floor)
        return res
''', [([[3, 9, 20, None, None, 15, 7]], [[3], [9, 20], [15, 7]]), ([[1]], [[1]]), ([[]], [])], 'O(n)', 'O(n)')

P('right-side-view', 'What You See From the Right', 199, 'Medium', T,
  "Standing on the right side of the tree, which values can you see (top to bottom)?",
  "Floor by floor (BFS), the last node on each floor is the one you see.",
  ["Level order, but keep only the last of each floor.", "DFS visiting right first also works."],
  '''
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        q = deque([root] if root else [])
        while q:
            n = len(q)
            for i in range(n):
                node = q.popleft()
                if i == n - 1:
                    res.append(node.val)  #> rightmost on this floor
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        return res
''', [([[1, 2, 3, None, 5, None, 4]], [1, 3, 4]), ([[1, None, 3]], [1, 3]), ([[]], [])], 'O(n)', 'O(n)')

P('good-nodes', 'Count the Brave Nodes', 1448, 'Medium', T,
  "A node is 'good' if nothing on the path from the root down to it is bigger than it. Count them.",
  "Walk down carrying the biggest value seen so far on this path.",
  ["Pass max-so-far as a parameter.", "Root is always good."],
  '''
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, top):
            if not node:
                return 0
            good = 1 if node.val >= top else 0  #> nobody above me is bigger
            top = max(top, node.val)
            return good + dfs(node.left, top) + dfs(node.right, top)
        return dfs(root, root.val)
''', [([[3, 1, 4, 3, None, 1, 5]], 4), ([[3, 3, None, 4, 2]], 3), ([[1]], 1)], 'O(n)', 'O(h)')

P('validate-bst', 'Is It a Real Search Tree?', 98, 'Medium', T,
  "In a binary search tree, everything on the left is smaller and everything on the right is bigger, at EVERY node. Check it.",
  "Pass down an allowed range (low, high). Going left lowers the ceiling; going right raises the floor.",
  ["Only checking a node against its direct kids is not enough!", "Start with (-inf, +inf)."],
  '''
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def ok(node, low, high):
            if not node:
                return True
            if not (low < node.val < high):
                return False  #> broke the rule
            return ok(node.left, low, node.val) and ok(node.right, node.val, high)
        return ok(root, -inf, inf)
''', [([[2, 1, 3]], True), ([[5, 1, 4, None, None, 3, 6]], False), ([[5, 4, 6, None, None, 3, 7]], False)], 'O(n)', 'O(h)')

P('kth-smallest-bst', 'K-th Smallest in a Search Tree', 230, 'Medium', T,
  "Find the k-th smallest value in a binary search tree.",
  "In-order walk (left, me, right) visits a BST in sorted order. Stop at the k-th visit.",
  ["Use an explicit stack to walk in-order.", "Count as you pop."],
  '''
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        st = []
        cur = root
        while True:
            while cur:
                st.append(cur)  #> slide all the way left
                cur = cur.left
            cur = st.pop()
            k -= 1  #> visited one more in sorted order
            if k == 0:
                return cur.val
            cur = cur.right
''', [([[3, 1, 4, None, 2], 1], 1), ([[5, 3, 6, 2, 4, None, None, 1], 3], 3)], 'O(h+k)', 'O(h)')

P('lca-bst', 'Closest Shared Ancestor (Search Tree)', 235, 'Medium', T,
  "In a BST, find the lowest node that has both p and q below it (or is one of them). Values p and q are given.",
  "Both smaller than me? Go left. Both bigger? Go right. Otherwise they split here: I'm the answer.",
  ["Use the BST ordering, no searching needed.", "A node can be its own ancestor."],
  '''
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: int, q: int) -> int:
        cur = root
        while cur:
            if p < cur.val and q < cur.val:
                cur = cur.left  #> both live on the left
            elif p > cur.val and q > cur.val:
                cur = cur.right  #> both live on the right
            else:
                return cur.val  #> they split here
''', [([[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8], 6), ([[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4], 2)], 'O(h)', 'O(1)')

P('lca-binary-tree', 'Closest Shared Ancestor (Any Tree)', 236, 'Medium', T,
  "Same idea, but the tree is not sorted. Values p and q are given.",
  "Ask each side: 'did you find p or q?'. If both sides say yes, I'm the meeting point.",
  ["Return the node if it matches p or q.", "If only one side found something, pass it up."],
  '''
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: int, q: int) -> int:
        def find(node):
            if not node or node.val in (p, q):
                return node
            l = find(node.left)
            r = find(node.right)
            if l and r:
                return node  #> one on each side: I'm the meeting point
            return l or r
        return find(root).val
''', [([[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1], 3), ([[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 4], 5)], 'O(n)', 'O(h)')

P('build-tree-pre-in', 'Rebuild the Tree From Two Walks', 105, 'Medium', T,
  "Given the preorder (me, left, right) and inorder (left, me, right) walks, rebuild the tree.",
  "Preorder's first value is the root. Find it in inorder: everything left of it is the left subtree, right is the right subtree.",
  ["A dictionary value -> inorder index makes lookups instant.", "Consume preorder from the front."],
  '''
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        pos = {v: i for i, v in enumerate(inorder)}
        it = iter(preorder)
        def build(lo, hi):
            if lo > hi:
                return None
            val = next(it)  #> next root in preorder
            node = TreeNode(val)
            m = pos[val]
            node.left = build(lo, m - 1)  #> left of it in inorder
            node.right = build(m + 1, hi)
            return node
        return build(0, len(inorder) - 1)
''', [([[3, 9, 20, 15, 7], [9, 3, 15, 20, 7]], [3, 9, 20, None, None, 15, 7]), ([[-1], [-1]], [-1])], 'O(n)', 'O(n)')

P('max-path-sum', 'Best Path Sum', 124, 'Hard', T,
  "A path can start and end anywhere. Find the biggest sum of values along any path.",
  "Each node returns the best 'one-armed' path going down. At each node, try bending: left arm + me + right arm.",
  ["Negative arms? Drop them (use 0).", "Track the global best separately."],
  '''
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        best = -inf
        def arm(node):
            nonlocal best
            if not node:
                return 0
            l = max(arm(node.left), 0)  #> skip negative arms
            r = max(arm(node.right), 0)
            best = max(best, node.val + l + r)  #> bend here
            return node.val + max(l, r)
        arm(root)
        return best
''', [([[1, 2, 3]], 6), ([[-10, 9, 20, None, None, 15, 7]], 42), ([[-3]], -3)], 'O(n)', 'O(h)')

P('serialize-tree', 'Save and Load a Tree', 297, 'Hard', T,
  "Turn a tree into a string and back again. (We test the round trip.)",
  "Preorder walk writing '#' for empty spots. Reading back, follow the same order.",
  ["Empty markers make the shape unambiguous.", "Use an iterator over the tokens."],
  '''
class Solution:
    def roundTrip(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        out = []
        def ser(n):
            if not n:
                out.append('#')
                return
            out.append(str(n.val))
            ser(n.left)
            ser(n.right)
        ser(root)
        text = ','.join(out)  #> the saved string
        it = iter(text.split(','))
        def de():
            v = next(it)
            if v == '#':
                return None
            n = TreeNode(int(v))
            n.left = de()
            n.right = de()
            return n
        return de()
''', [([[1, 2, 3, None, None, 4, 5]], [1, 2, 3, None, None, 4, 5]), ([[]], [])], 'O(n)', 'O(n)')

P('symmetric-tree', 'Mirror-Image Tree?', 101, 'Easy', T,
  "Is the tree a mirror of itself (left side looks like the flipped right side)?",
  "Compare two nodes at a time: outer pair (left.left vs right.right) and inner pair (left.right vs right.left).",
  ["Write a helper mirror(a, b).", "Values must match and both pairs must mirror."],
  '''
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def mirror(a, b):
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return mirror(a.left, b.right) and mirror(a.right, b.left)
        return mirror(root.left, root.right)
''', [([[1, 2, 2, 3, 4, 4, 3]], True), ([[1, 2, 2, None, 3, None, 3]], False)], 'O(n)', 'O(h)')

P('path-sum', 'Root-to-Leaf Sum', 112, 'Easy', T,
  "Is there a path from the root down to a leaf whose values add up to target?",
  "Subtract each node's value as you go down. At a leaf, check if what's left is 0.",
  ["A leaf has no kids.", "Pass the remaining amount down."],
  '''
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        left = targetSum - root.val  #> amount still needed
        if not root.left and not root.right:
            return left == 0  #> leaf: did we hit it exactly?
        return self.hasPathSum(root.left, left) or self.hasPathSum(root.right, left)
''', [([[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22], True), ([[1, 2, 3], 5], False)], 'O(n)', 'O(h)')

P('insert-bst', 'Add a Value to a Search Tree', 701, 'Medium', T,
  "Insert a new value into a BST and return the root.",
  "Walk left or right like a search until you find an empty spot, then put the new node there.",
  ["Smaller goes left, bigger goes right.", "Recursion: root.left = insert(root.left, val)."],
  '''
class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return TreeNode(val)  #> empty spot: put it here
        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        else:
            root.right = self.insertIntoBST(root.right, val)
        return root
''', [([[4, 2, 7, 1, 3], 5], [4, 2, 7, 1, 3, 5]), ([[], 1], [1])], 'O(h)', 'O(h)')

P('sorted-array-to-bst', 'Sorted List to Balanced Tree', 108, 'Easy', T,
  "Turn a sorted list into a balanced binary search tree.",
  "The middle value becomes the root. The left half builds the left subtree, the right half the right.",
  ["Middle = (lo + hi) // 2.", "Recursion on halves."],
  '''
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2  #> middle becomes the root
            node = TreeNode(nums[mid])
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node
        return build(0, len(nums) - 1)
''', [([[-10, -3, 0, 5, 9]], [0, -10, 5, None, -3, None, 9]), ([[1, 3]], [1, None, 3])], 'O(n)', 'O(log n)')
