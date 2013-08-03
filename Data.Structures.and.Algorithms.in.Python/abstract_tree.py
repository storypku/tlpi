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

