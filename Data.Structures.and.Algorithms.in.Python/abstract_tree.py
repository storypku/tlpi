from linked_queue import LinkedQueue

class Tree:
    """Abstract base class representing a tree structure."""

    # ------------- nested Position class  ----------------------------------
    class Position:
        """An abstraction representing the location of a single element."""

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError("must be implemented by subclass")

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError("must be implemented by subclass")

        def __ne__(self, other):
            """Return True if other Position does not represent the same
            location."""
            return not (self == other)

    # -------  abstract method that concrete subclass must support  ----------
    def root(self):
        """Return Position representing the tree's root (or None if empty.)"""
        raise NotImplementedError("must be implemented by subclass.")

    def parent(self, pos):
        """Return Position representing pos's parent (or None if pos is
        root)."""
        raise NotImplementedError("must be implemented by subclass.")

    def num_children(self, pos):
        """Return the number of children that Position pos has."""
        raise NotImplementedError("must be implemented by subclass.")

    def children(self, pos):
        """Generate an iteration of Position representing pos's children."""
        raise NotImplementedError("must be implemented by subclass.")

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError("must be implemented by subclass.")

    # --------- concrete methods implemented in this class -------------------
    def preorder(self):
        """Generate a preorder iteration of positions in the tree."""
        if not self.is_empty():
            for pos in self._subtree_preorder(self.root()):
                yield pos

    def _subtree_preorder(self, pos):
        """Generate a preorder iteration of positions in subtree rooted at
        pos."""
        yield pos
        for child in self.children(pos):
            for other in self._subtree_preorder(child):
                yield other

    def preorder_indent(self):
        """Print preorder representation of tree."""
        if not self.is_empty():
            d = self.depth(self.root())
            self._subtree_preorder_indent(self.root(), d)

    def _subtree_preorder_indent(self, pos, d):
        """Print preorder representation of subtree rooted at pos at depth
        d."""
        print (2*d*" " + str(pos.element()))
        for child in self.children(pos):
            self._subtree_preorder_indent(child, d + 1)

    def preorder_label(self):
        if not self.is_empty():
            d = self.depth(self.root())
            path = list()
            self._subtree_preorder_label(self.root(), d, path)

    def _subtree_preorder_label(self, pos, d, path):
        """Print labeled representation of subtree rooted at pos at depth
        d."""
        label = ".".join(str(j+1) for j in path)
        print (2*d*" " + label, str(pos.element()))
        path.append(0)
        for child in self.children(pos):
            self._subtree_preorder_label(child, d+1, path)
            path[-1] += 1
        path.pop()

    def parenthesize(self):
        if not self.is_empty():
            self._subtree_parenthesize(self.root())
            print()

    def _subtree_parenthesize(self, pos):
        """print parenthesized representation of subtree rooted at pos."""
        print(str(pos.element()), end="")
        if not self.is_leaf(pos):
            first_time = True
            for child in self.children(pos):
                sep = " (" if first_time else ", "
                print(sep, end="")
                first_time = False
                self._subtree_parenthesize(child)
            print (")", end="")

    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        if not self.is_empty():
            for pos in self._subtree_postorder(self.root()):
                yield pos

    def _subtree_postorder(self, pos):
        """Generate a postorder iteration of positions in subtree rooted at
        pos."""
        for child in self.children(pos):
            for other in self._subtree_postorder(child):
                yield other
        yield pos

    def breadthfirst(self):
        if not self.is_empty():
            fringe = LinkedQueue()
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                pos = fringe.dequeue()
                yield pos
                for child in self.children(pos):
                    fringe.enqueue(child)

    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.preorder()

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for pos in self.positions():
            yield pos.element()

    def is_root(self, pos):
        """Return True if Position pos represents the root of the tree."""
        return self.root() == pos

    def is_leaf(self, pos):
        """Return True if Position pos does not have any children."""
        return self.num_children(pos) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def depth(self, pos):
        """Return the number of levels separating Position pos from the
        root."""
        if self.is_root(pos):
            return 0
        else:
            return 1 + self.depth(self.parent(pos))

    def _height2(self, pos):
        """Return the height of the subtree rooted at Position pos."""
        if self.is_leaf(pos):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(pos))

    def height(self, pos = None):
        """Return the height of the subtree rooted at Position pos.

        If pos is None, return the height of the entire tree.
        """
        if pos is None:
            pos = self.root()
            if pos is None: # designate empty tree's height as -1
                return -1
        return self._height2(pos)   # O(n)

class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure."""

    # ------------  additional abstract methods  ----------------------
    def left(self, pos):
        """Return a Position representing pos's left child.

        Return None if pos does not have a left child.
        """
        raise NotImplementedError("must be implemented by subclass.")

    def right(self, pos):
        """Return a Position representing pos's right child.

        Return None if pos does not have a right child.
        """
        raise NotImplementedError("must be implemented by subclass.")

    # ------------  concrete methods implemented in this class  ---------
    def sibling(self, pos):
        """Return a Position representing pos's sibling (or None if no
        sibling)"""
        parent = self.parent(pos)
        if parent is None:  # pos must be the root
            return None
        else:
            if pos == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, pos):
        """Generate an iteration of Positions representing pos's children."""
        if self.left(pos) is not None:
            yield self.left(pos)
        if self.right(pos) is not None:
            yield self.right(pos)

    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
            for pos in self._subtree_inorder(self.root()):
                yield pos

    def _subtree_inorder(self, pos):
        """Generate an inorder iteration of positions in subtree rooted at
        pos."""
        if self.left(pos) is not None:
            for other in self._subtree_inorder(self.left(pos)):
                yield other
        yield pos
        if self.right(pos) is not None:
            for other in self._subtree_inorder(self.right(pos)):
                yield other

    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.inorder() # make inorder the default for binary tree.

