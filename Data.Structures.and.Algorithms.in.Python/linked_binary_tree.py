from abstract_tree import BinaryTree

class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    class _Node:    # Lightweight, non-public class for storing a node
        __slots__ = "_element", "_parent", "_left", "_right"

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor, should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same
            location."""
            return type(other) is type(self) and other._node is self._node

    def _validate(self, pos):
        if not isinstance(pos, self.Position):
            raise TypeError("pos must be proper Position type.")
        elif pos._container is not self:
            raise ValueError("pos does not belong to this container.")
        elif pos._node is None:
            raise ValueError("pos is not valid.")
        if pos._node._parent is pos._node:  # convention for deprecated nodes
            raise ValueError("pos is no longer valid.")
        return pos._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    # ------------- public accessors -----------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None for empty tree."""
        return self._make_position(self._root)

    def parent(self, pos):
        """Return the Position of pos's parent (or None if pos is root)."""
        node = self._validate(pos)
        return self._make_position(node._parent)

    def left(self, pos):
        """Return the Position of pos's left child (or None if no left
        child)."""
        node = self._validate(pos)
        return self._make_position(node._left)

    def right(self, pos):
        """Return the Position of pos's right child (or None if no right
        child)."""
        node = self._validate(pos)
        return self._make_position(node._right)

    def num_children(self, pos):
        """Return the number of children of Position pos."""
        node = self._validate(pos)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    def _add_root(self, elem):
        """Place element elem at the root of an empty tree and return new
        Position.

        Raise ValueError if tree nonempty.
        """
        if self.root() is not None:
            raise ValueError("Root exists")
        self._size = 1
        self._root = self._Node(elem)
        return self._make_position(self._root)

    def _add_left(self, pos, elem):
        """Create a new left child for Position pos, stroring element elem.

        Return the Position of the new node.
        Raise ValueError if Position pos is invalid or pos already has a left
        child.
        """
        node = self._validate(pos)
        if node._left is not None:
            raise ValueError("Left child exists")
        self._size += 1
        node._left = self._Node(elem, node)
        return self._make_position(node._left)

    def _add_right(self, pos, elem):
        """Create a new right child for Position pos, stroring element elem.

        Return the Position of the new node.
        Raise ValueError if Position pos is invalid or pos already has a right
        child.
        """
        node = self._validate(pos)
        if node._right is not None:
            raise ValueError("Right child exists")
        self._size += 1
        node._right = self._Node(elem, node)
        return self._make_position(node._right)

    def _replace(self, pos, elem):
        """Replace element at the Position pos with elem, and return the old
        element."""
        node = self._validate(pos)
        old = node._element
        node._element = elem
        return old

    def _delete(self, pos):
        """Delete the node at Position pos, and replace it with its child, if
        any.

        Return the element that had been stored at Position pos.
        Raise ValueError if Position pos is invalid or pos has two children.
        """
        node = self._validate(pos)
        if self.num_children(pos) == 2:
            raise ValueError("pos has two children")
        child = node._left if node._left is not None else node._right
        if child is not None:
            child._parent = node._parent # child's grandparent becomes parent.
        if node is self._root:
            self._root = child # child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node # convention for deprecated node
        return node._element

    def _attach(self, pos, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external
        pos."""
        node = self._validate(pos)
        if not self.is_leaf(pos):
            raise ValueError("position must be leaf")
        if not type(self) is type(t1) is type(t2):
            raise TypeError("Tree types must match")
        self._size += len(t1) + len(t2)
        if not t1.is_empty():   # attach t1 as left subtree of node
            t1._root._parent = node
            node._left = t1._root
            t1._root = None # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0

class MutableLinkedBinaryTree(LinkedBinaryTree):
    """Linked representation of a binary tree structure (with public update
    methods)."""
    def add_root(self, elem):
        """Place element elem at the root of an empty tree and return new
        Position.

        Raise ValueError if tree nonempty.
        """
        return self._add_root(elem)

    def add_left(self, pos, elem):
        """Create a new left child for Position pos, stroring element elem.

        Return the Position of the new node.
        Raise ValueError if Position pos is invalid or pos already has a left
        child.
        """
        return self._add_left(pos, elem)

    def add_right(self, pos, elem):
        """Create a new right child for Position pos, stroring element elem.

        Return the Position of the new node.
        Raise ValueError if Position pos is invalid or pos already has a right
        child.
        """
        return self._add_right(pos, elem)

    def replace(self, pos, elem):
        """Replace element at the Position pos with elem, and return the old
        element."""
        return self._replace(pos, elem)

    def delete(self, pos):
        """Delete the node at Position pos, and replace it with its child, if
        any.

        Return the element that had been stored at Position pos.
        Raise ValueError if Position pos is invalid or pos has two children.
        """
        return self._delete(pos)

    def attach(self, pos, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external
        pos."""
        self._attach(pos, t1, t2)

