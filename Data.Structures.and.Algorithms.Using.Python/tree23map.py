"""Implementation of the Map ADT using the 2-3 Tree.

A 2-3 tree is a search tree that is always balanced and whose shape and
structure is defined as follows:

1) Every node has capacity for one or two keys (and their corresponding
payload), which we term key one and key two.

2) Every node has capacity for two or three children, which we term the left,
middle, and right child.

3) All leaf node are at the same level.

4) Every internal node must contain two or three children. If the node has
one key, it must contain two children; if it has two keys, it must contain
three children.

For each interior node, V:

1) All keys less than the first key of node V are stored in the left subtree
of V.

2) If the node has two children, all keys greater thant the first key of node
V are stored in the middle subtree of V.

3) If the node has three children: (a) all keys greater than the first key of
node V but less than the second key are stored in the middle subtree of V;
and (b) all keys greater than the second key are stored in the right
subtree.

"""
class Tree23Map:
    """Implementation of the Map ADT using an 2-3 tree. """

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __contains__(self, key):
        """See if the map contains the given key."""
        assert key is not None, "Invalid map key."
        return self._t23Search(self._root, key) is not None

    def __getitem__(self, key):
        assert key is not None, "Invalid map key."
        node = self._t23Search(self._root, key)
        if node is not None:
            return node.getValue(key)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        return self.add(key, value)

    def add(self, key, value):
        """Adds a kv pair into the 2-3 tree or replaces the existing one if the
        given key already exists."""
        assert key is not None, "Can't specify None as key."
        node = self._t23Search(self._root, key)
        if node is not None:
            # Key already exists, either key1 or key2 must be equal to it.
            if node.key1 == key:
                node.value1 = value
            else:
                node.value2 = value
            return False
        else:
            self._t23Insert(key, value)
            self._size += 1
            return True

    def __delitem__(self, key):
        assert key is not None, "Can't specify None as key."
        pass

    def _t23Search(self, subtree, target):
        """Helper method to search the 2-3 tree for the given target key.
        Returns the reference to the node associated with the key or None. """
        if subtree is None:
            return None
        elif subtree.hasKey(target):
            return subtree
        else:
            branch = subtree.getBranch(target)
            return self._t23Search(branch, target)

    def _t23Insert(self, key, value):
        """Helper method to insert the kv pair into the 2-3 tree."""
        if self._root is None:
            self._root = _T23Node(key, value)
        else:
            (pKey, pValue, pRef) = self._t23RecInsert(self._root, key, value)
            # If the root node was split
            if pRef is not None:
                newRoot = _T23Node(pKey, pValue)
                newRoot.left = self._root
                newRoot.middle = pRef
                self._root = newRoot

    def _t23RecInsert(self, subtree, key, value):
        """Helper method to add the kv pair to subtree recursively."""
        if subtree.isLeaf():
            return self._t23AddToNode(subtree, key, value, None)
        else:
            branch = subtree.getBranch(key)
            (pKey, pValue, pRef) = self._t23RecInsert(branch, key, value)
            # If the child indicated by <branch> handles the insertion
            # "neatly", then nothing need to be done for the "current"
            # interior node indicated by <subtree>. Otherwise, the child
            # was split, the promoted key and reference have to be added
            # to the "current" interior <subtree> node.
            if pRef is None:
                return (None, None, None)
            else:
                return self._t23AddToNode(subtree, pKey, pValue, pRef)

    def _t23AddToNode(self, subtree, key, value, pRef):
        """Handle the insertion of a kv pair to a node denoted by <subtree>.
        if pRef is None, then the insertion is into an leaf node; otherwise,
        it is performed on an interior node (pRef is a reference to the new
        node generated when one of <subtree>'s children splits."""
        if subtree.isFull():
            return self._t23SplitNode(subtree, key, value, pRef)
        else:
            if key < subtree.key1:
                subtree.key2 = subtree.key1
                subtree.value2 = subtree.value1
                subtree.key1 = key
                subtree.value1 = value
                if pRef is not None:
                    subtree.right = subtree.middle
                    subtree.middle = pRef
            else: # key > subtree.key1
                subtree.key2 = key
                subtree.value2 = value
                if pRef is not None:
                    subtree.right = pRef
            return (None, None, None)

    def _t23SplitNode(self, node, key, value, pRef):
        """Splits a full non-root node denoted by <node> and returns a tuple
        with the promoted key and reference."""
        # Create the new node, the reference to which will be promoted.
        newNode = _T23Node(None, None)
        if key < node.key1: # Left
            pKey = node.key1
            pValue = node.value1
            node.key1 = key
            node.value1 = value
            newNode.key1 = node.key2
            newNode.value1 = node.value2
            # pRef comes from split of the left child of interiror <node>
            if pRef is not None:
                newNode.middle = node.right
                newNode.left = node.middle
                node.middle = pRef
                node.right = None
        elif key < node.key2: # Middle
            pKey = key
            pValue = value
            newNode.key1 = node.key2
            newNode.value1 = node.value2
            # pRef comes from split of the middle child of interiror <node>
            if pRef is not None:
                newNode.middle = node.right
                newNode.left = pRef
                node.right = None
        else: # Right
            pKey = node.key2
            pValue = node.value2
            newNode.key1 = key
            newNode.value1 = value
            # pRef comes from split of the right child of interiror <node>
            if pRef is not None:
                newNode.left = node.right
                newNode.middle = pRef
                node.right = None
        node.key2 = None
        node.value2 = None
        return (pKey, pValue, newNode)

class _T23Node(object):
    """storage class for creating the 2-3 tree nodes."""

    def __init__(self, key, value):
        self.key1 = key
        self.key2 = None
        self.value1 = value
        self.value2 = None
        self.left = None
        self.middle = None
        self.right = None

    def isLeaf(self):
        """Determine if a leaf node. """
        return self.left is None and self.middle is None and \
               self.right is None

    def isFull(self):
        """Determine if there are two keys in the node."""
        return self.key2 is not None

    def hasKey(self, target):
        """See if the node contains the given target key."""
        if self.key1 == target or (self.key2 is not None and \
                self.key2 == target):
            return True
        else:
            return False

    def getValue(self, target):
        """Returns the data associated with the target key or None."""
        if target == self.key1:
            return self.value1
        elif self.key2 is not None and target == self.key2:
            return self.value2
        else:
            return None

    def getBranch(self, target):
        """Choose the approriate branch for the given target. """
        if target < self.key1:
            return self.left
        elif self.key2 is None:
            return self.middle
        elif target < self.key2:
            return self.middle
        else:
            return self.right

if __name__ == "__main__":
    from random import randint
    LLIST = list()
    for times in range(50):
        LLIST.append(randint(1, 100))
    print "===", len(LLIST), "==="
    TTMAP = Tree23Map()
    for num in LLIST:
        TTMAP.add(num, num * 2)
        TTMAP.add(num, num * 10)
    print "===", len(TTMAP), "===="
    for num in LLIST:
        print num, TTMAP[num]
