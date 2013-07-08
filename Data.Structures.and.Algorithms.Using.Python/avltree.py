"""Implementation of the Map ADT using AVL tree. """

LEFT_HIGH  = 1
EQUAL_HIGH = 0
RIGHT_HIGH = -1

from bst import _BSTMapIterator

class AVLMap:
    """Implementation of the Map ADT using AVL tree. """

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self._bstSearch(self._root, key) is not None

    def __setitem__(self, key, value):
        return self.add(key, value)

    def __getitem__(self, key):
        return self.valueOf(key)

    def __delitem__(self, key):
        self.remove(key)

    def __iter__(self):
        return _BSTMapIterator(self._root)

    def add(self, key, value):
        """ Add a new entry to the map or replaces the value of an existing
        key."""
        node = self._bstSearch(self._root, key)
        if node is not None:
            node.value = value
            return False
        else:
            (self._root, _) = self._avlInsert(self._root, key, value)
            self._size += 1
            return True

    def valueOf(self, key):
        """ Returns the value associated with the given key. """

        node = self._bstSearch(self._root, key)
        assert node is not None, "Invalid map key."
        return node.value

    def _bstSearch(self, subtree, target):
        """Helper method recursively searching the tree for a target key."""

        if subtree is None:
            return None
        elif target < subtree.key:
            return self._bstSearch(subtree.left, target)
        elif target > subtree.key:
            return self._bstSearch(subtree.right, target)
        else:
            return subtree

    def remove(self, key):
        """Remove the map entry associated with the given key."""

        assert key in self, "Invalid map key."
        (self._root, _) = self._avlRemove(self._root, key)
        self._size -= 1

    def _avlInsert(self, subtree, key, value):
        """Recursive method to handle the insertion into an AVL tree. The
        function returns a tuple containing a reference to the root of the
        subtree and a boolean to indicate if the subtree grew taller."""
        if subtree is None:
            subtree = _AVLMapNode(key, value)
            taller = True
        elif key == subtree.key:
            subtree.value = value
            taller = False
        elif key < subtree.key:
            (subtree.left, taller) = self._avlInsert(subtree.left, key, value)
            # If the subtree grew taller, see if it needs rebalancing
            if taller:
                if subtree.bfactor == LEFT_HIGH:
                    subtree = self._avlLeftBalance(subtree)
                    taller = False
                elif subtree.bfactor == EQUAL_HIGH:
                    subtree.bfactor = LEFT_HIGH
                    taller = True
                else: # RIGHT_HIGH
                    subtree.bfactor = EQUAL_HIGH
                    taller = False
        else:   # key > subtree.key
            (subtree.right, taller) = self._avlInsert(subtree.right, key,
                    value)
            # If the subtree grew taller, see if it needs rebalancing
            if taller:
                if subtree.bfactor == LEFT_HIGH:
                    subtree.bfactor = EQUAL_HIGH
                    taller = False
                elif subtree.bfactor == EQUAL_HIGH:
                    subtree.bfactor = RIGHT_HIGH
                    taller = True
                else: # RIGHT_HIGH
                    subtree = self._avlRightBalance(subtree)
                    taller = False
        # Returns the results
        return (subtree, taller)

    def _avlLeftBalance(self, pivot):
        """Rebalance a node when its left subtree is higher. """
        ccc = pivot.left
        # See if rebalancing is due to case 1: LL
        if ccc.bfactor == LEFT_HIGH:
            pivot.bfactor = EQUAL_HIGH
            ccc.bfactor = EQUAL_HIGH
            pivot = self._avlRotateRight(pivot)
            return pivot
        # Otherwise, a balance from the left is due to case 2: LR
        else:
            ggg = ccc.right
            if ggg.bfactor == LEFT_HIGH:
                pivot.bfactor = RIGHT_HIGH
                ccc.bfactor = EQUAL_HIGH
            # ggg.bfactor == RIGHT_HIGH since != EQUAL_HIGH in this case
            else:
                pivot.bfactor = EQUAL_HIGH
                ccc.bfactor = LEFT_HIGH
            # Both cases above set ggg's balance factor to equal high
            ggg.bfactor = EQUAL_HIGH

            pivot.left = self._avlRotateLeft(ccc)
            pivot = self._avlRotateRight(pivot)
            return pivot

    def _avlRightBalance(self, pivot):
        """Rebalance a node when its right subtree is higher."""
        ccc = pivot.right
        # See if rebalancing is due to case 3: RR
        if ccc.bfactor == RIGHT_HIGH:
            pivot.bfactor = EQUAL_HIGH
            ccc.bfactor = EQUAL_HIGH
            pivot = self._avlRotateLeft(pivot)
            return pivot
        # Otherwise, a balance from the left is due to case 4: RL
        else:
            ggg = ccc.left
            if ggg.bfactor == LEFT_HIGH:
                pivot.bfactor = EQUAL_HIGH
                ccc.bfactor = RIGHT_HIGH
            # ggg.bfactor == RIGHT_HIGH since != EQUAL_HIGH in this case
            else:
                pivot.bfactor = LEFT_HIGH
                ccc.bfactor = EQUAL_HIGH
            # Both cases above set ggg's balance factor to equal high
            ggg.bfactor = EQUAL_HIGH

            pivot.right = self._avlRotateRight(ccc)
            pivot = self._avlRotateLeft(pivot)
            return pivot

    def _avlRemove(self, subtree, target):
        """Recursive method to handle the deletion from an AVL tree. The
        function returns a tuple containing a reference to the root of the
        subtree and a boolean to indicate if the subtree grew shorter."""
        if target == subtree.key:
            if subtree.left is None and subtree.right is None: # Leaf node
                subtree = None
                shorter = True
            elif subtree.left is None:
                subtree = subtree.right
                shorter = True
            elif subtree.right is None:
                subtree = subtree.left
                shorter = True
            else:  # Interior node with two children both present
                successor = self._bstMinimum(subtree.right)
                subtree.key = successor.key
                subtree.value = successor.value
                (subtree.right, shorter) = self._avlRemove(subtree.right, \
                        successor.key)
                if shorter:
                    if subtree.bfactor == LEFT_HIGH:
                        if subtree.left.bfactor == EQUAL_HIGH:
                            shorter = False
                        else:
                            shorter = True
                        # TODO: Be careful!
                        subtree = self._avlLeftBalance(subtree)
                    elif subtree.bfactor == EQUAL_HIGH:
                        subtree.bfactor = LEFT_HIGH
                        shorter = False
                    else:
                        subtree.bfactor = EQUAL_HIGH
                        shorter = True
        elif target < subtree.key:
            (subtree.left, shorter) = self._avlRemove(subtree.left, target)
            if shorter:
                if subtree.bfactor == LEFT_HIGH:
                    subtree.bfactor = EQUAL_HIGH
                    shorter = True
                elif subtree.bfactor == EQUAL_HIGH:
                    subtree.bfactor = RIGHT_HIGH
                    shorter = False
                else:  # RIGHT_HIGH, rebalance needed
                    if subtree.right.bfactor == EQUAL_HIGH:
                        shorter = False
                    else:
                        shorter = True
                    # TODO: Be careful!
                    subtree = self._avlRightBalance(subtree)
        else: # target > subtree.key
            (subtree.right, shorter) = self._avlRemove(subtree.right, target)
            if shorter:
                if subtree.bfactor == LEFT_HIGH:
                    if subtree.left.bfactor == EQUAL_HIGH:
                        shorter = False
                    else:
                        shorter = True
                    # TODO: Be careful!
                    subtree = self._avlLeftBalance(subtree)

                elif subtree.bfactor == EQUAL_HIGH:
                    subtree.bfactor = LEFT_HIGH
                    shorter = False
                else:   # RIGHT_HIGH
                    subtree.bfactor = EQUAL_HIGH
                    shorter = True
        return (subtree, shorter)

    def _avlRotateRight(self, pivot):
        """Rotate the pivot to the right around its left child."""
        ccc = pivot.left
        pivot.left = ccc.right
        ccc.right = pivot
        return ccc

    def _avlRotateLeft(self, pivot):
        """Rotates the pivot to the left around its right child."""
        ccc = pivot.right
        pivot.right = ccc.left
        ccc.left = pivot
        return ccc

    def _bstMinimum(self, subtree):
        """ Helper method for finding the node containing the minimum key. """
        if subtree is None:
            return None
        elif subtree.left is None:
            return subtree
        else:
            return self._bstMinimum(subtree.left)

    def breathFirstTrav(self):
        """Breath-first traversal of an AVL tree."""
        from llistqueue import Queue
        trQ = Queue()
        trQ.enqueue(self._root)
        while not trQ.isEmpty():
            node = trQ.dequeue()
            print "%4s %-4s" % (node.key, node.bfactor)
            if node.left is not None:
                trQ.enqueue(node.left)
            if node.right is not None:
                trQ.enqueue(node.right)

class _AVLMapNode:
    """ Storage class for creating the AVL tree node. """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.bfactor = EQUAL_HIGH
        self.left = None
        self.right = None


if __name__ == "__main__":
    mmap = AVLMap()
    for num in [60, 51, 7, 39, 46, 72, 83, 91, 100, 73]:
        mmap.add(num, num * 2)
    mmap.breathFirstTrav()
