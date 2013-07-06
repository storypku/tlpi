"""Implementation of the Map ADT using binary search tree(BST) """
from lliststack import Stack
class BSTMap:
    """ Implementation of the Map ADT using binary search tree. """
    def __init__(self):
        """Create an empty map instance"""
        self._root = None
        self._size = 0

    def __len__(self):
        """Returns the number of entries in the map"""
        return self._size

    def __iter__(self):
        """Returns an iterator for traversing the keys in the map."""
        return _BSTMapIterator(self._root)

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

    def __contains__(self, key):
        """Determines if the map contains the given key"""
        return self._bstSearch(self._root, key) is not None

    def valueOf(self, key):
        """Returns the value associated with the key"""
        node = self._bstSearch(self._root, key)
        assert node is not None, "Invalid map key"
        return node.value

    def __getitem__(self, key):
        return self.valueOf(key)

    def maximum(self):
        """ Returns the maximum key in the map """
        assert self._size > 0, "No maximum key for an empty map"
        return self._bstMaximum(self._root).key

    def _bstMaximum(self, subtree):
        """ Helper method for finding the node containing the maximum key. """
        if subtree is None:
            return None
        elif subtree.right is None:
            return subtree
        else:
            return self._bstMaximum(subtree.right)

    def minimum(self):
        """ Returns the minimum key in the map """
        assert self._size > 0, "No minimum key for an empty map"
        return self._bstMinimum(self._root).key

    def _bstMinimum(self, subtree):
        """ Helper method for finding the node containing the minimum key. """
        if subtree is None:
            return None
        elif subtree.left is None:
            return subtree
        else:
            return self._bstMinimum(subtree.left)

    def add(self, key, value):
        """ Add a new entry to the map or replaces the value of an existing
        key."""
        node = self._bstSearch(self._root, key)
        if node is not None:
            node.value = value
            return False
        else:
            self._root = self._bstInsert(self._root, key, value)
            self._size += 1
            return True

    def __setitem__(self, key, value):
        self.add(key, value)

    def _bstInsert(self, subtree, key, value):
        """ Helper method that inserts a new item, recursively. """
        if subtree is None:
            subtree = _BSTMapNode(key, value)
        elif key < subtree.key:
            subtree.left = self._bstInsert(subtree.left, key, value)
        elif key > subtree.key:
            subtree.right = self._bstInsert(subtree.right, key, value)
        return subtree

    def remove(self, key):
        """ Removes the map entry associated with the given key. """
        assert key in self, "Invalid map key"
        self._root = self._bstRemove(self._root, key)
        self._size -= 1

    def __delitem__(self, key):
        self.remove(key)

    def _bstRemove(self, subtree, target):
        """Helper method that removes an existing item 'recursively'."""
        if subtree is None:
            return subtree
        elif target < subtree.key:
            subtree.left = self._bstRemove(subtree.left, target)
            return subtree
        elif target > subtree.key:
            subtree.right = self._bstRemove(subtree.right, target)
            return subtree
        else:
            if subtree.left is None and subtree.right is None:
                return None
            elif subtree.left is None:
                return subtree.right
            elif subtree.right is None:
                return subtree.left
            else:
                successor = self._bstMinimum(subtree.right)
                subtree.key = successor.key
                subtree.value = successor.value
                subtree.right = self._bstRemove(subtree.right, successor.key)
                return subtree

class _BSTMapIterator:
    """ Iterator for the binary search tree using a software stack """
    def __init__(self, root):
        """Create a stack for use in traversing the tree. """
        self._theStack = Stack()
        self._traverseToMinNode(root)

    def __iter__(self):
        return self

    def next(self):
        """Returns the next item from the BST in key order"""
        # If the stack is empty, we are done.
        if self._theStack.isEmpty():
            raise StopIteration
        else:       # The top node on the stack contains the next key.
            node = self._theStack.pop()
            key = node.key
            # If this node has a subtree rooted as the right child, we must
            # find the node in that subtree that contains the smallest key.
            # Again, the nodes along the path are pushed on the stack.
            if node.right is not None:
                self._traverseToMinNode(node.right)
            return key

    def _traverseToMinNode(self, subtree):
        """ Traverses down the subtree to find the node containing the
        smallest key during which the nodes along that path are pushed onto
        the stack."""
        if subtree is not None:
            self._theStack.push(subtree)
            self._traverseToMinNode(subtree.left)


class _BSTMapNode:
    """Storage class for the binary search tree nodes of the map"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

