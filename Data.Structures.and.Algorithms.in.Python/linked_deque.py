from custom_exception import Empty

class _DoublyLinkedBase:
    """A base class providing a doubly linked list representation."""

    class _Node:
        """Lightweight, nonpublic class for storing a doubly linked node."""
        __slots__ = "_element", "_prev", "_next"

        def __init__(self, elem, prev, nexT):
            self._element = elem
            self._prev = prev
            self._next = nexT

    def __init__(self):
        """Create an empty list."""
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    def __len__(self):
        """Return the number of elements in the list."""
        return self._size

    def is_empty(self):
        """Return True if the list is empty."""
        return self._size == 0

    def _insert_between(self, elem, predecessor, successor):
        """Add element elem between two existing nodes and return new node."""
        newest = self._Node(elem, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        """Delete non-sentinel node from the list and return its element."""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None
        return element

class LinkedDeque(_DoublyLinkedBase):
    """Double-ended queue implementation based on a doubly linked list."""

    def first(self):
        """Return the element at the front of the deque."""
        if self.is_empty():
            raise Empty("Deque is empty.")
        return self._header._next._element

    def last(self):
        """Return the element at the end of the deque."""
        if self.is_empty():
            raise Empty("Deque is empty.")
        return self._trailer._prev._element

    def add_first(self, elem):
        """Add an element to the front of the deque."""
        self._insert_between(elem, self._header, self._header._next)

    def add_last(self, elem):
        """Add an element to the back of the deque."""
        self._insert_between(elem, self._trailer._prev, self._trailer)

    def delete_first(self):
        """Remove and return the element from the front of the deque.

        Raise Empty exception if the deque is empty.
        """
        if self.is_empty():
            raise Empty("Deque is empty.")
        return self._delete_node(self._header._next)

    def delete_last(self):
        """Remove and return the element from the back of the deque.

        Raise Empty exception if the deque is empty.
        """
        if self.is_empty():
            raise Empty("Deque is empty.")
        return self._delete_node(self._trailer._prev)

class PositionalList(_DoublyLinkedBase):
    """A sequential container of elements allowing positional access."""
    #--------------- nested position class ---------------------------------
    class Position:
        """An abstraction representing the location of a single element."""
        __slots__ = "_container", "_node"

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same
            location."""
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not self == other

    #-------------------  utility method  -----------------------------------
    def _validate(self, pos):
        """Return position's node, or raise appropriate error if invalid."""
        if not isinstance(pos, self.Position):
            raise TypeError("pos must be proper Position Type")
        if pos._container is not self:
            raise ValueError("pos does not belong to this container")
        if pos._node._next is None: # convention for deprecated node
            raise ValueError("pos is no longer valid")
        return pos._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if sentinel)."""
        if node is self._header or node is self._trailer:
            return None
        else:
            return self.Position(self, node)

    #----------------------- accessors ---------------------------------------
    def first(self):
        """Return the first Position in the list (or None if the list is
        empty."""
        return self._make_position(self._header._next)

    def last(self):
        """Return the last Position in the list (or None if the list is
        empty."""
        return self._make_position(self._trailer._prev)

    def before(self, pos):
        """Return the Postion just before Postion pos (or None if pos is
        first)."""
        node = self._validate(pos)
        return self._make_position(node._prev)

    def after(self, pos):
        """Return the Postion just after Postion pos (or None if pos is
        last)."""
        node = self._validate(pos)
        return self._make_position(node._next)

    def __iter__(self):
        """Generate a forward iteration of the elements of the list."""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)
    #--------------------------  mutators  -----------------------------------
    # override inherited version to return Postion, rather than _Node
    def _insert_between(self, elem, predecessor, successor):
        """Add element elem between existing nodes and return the new
        Postion."""
        node = super()._insert_between(elem, predecessor, successor)
        return self._make_position(node)

    def add_first(self, elem):
        """Add element elem to the front of the list and return the new
        Postion."""
        return self._insert_between(elem, self._header, self._header._next)

    def add_last(self, elem):
        """Add element elem to the back of the list and return the new
        Postion."""
        return self._insert_between(elem, self._trailer._prev, self._trailer)

    def add_before(self, pos, elem):
        """Add element elem into list before Postion pos and return new
        Postion."""
        original = self._validate(pos)
        return self._insert_between(elem, original._prev, original)

    def add_after(self, pos, elem):
        """Add element elem into list after Position pos and return new
        Position."""

        original = self._validate(pos)
        return self._insert_between(elem, original, original._next)

    def delete(self, pos):
        """Remove and return the element at Position pos."""
        original = self._validate(pos)
        return self._delete_node(original)  # inherited method returns element

    def replace(self, pos, elem):
        """Replace the element at Position pos.

        Return the element formerly at Position pos.
        """
        original = self._validate(pos)
        old_value = original._element
        original._element = elem
        return old_value

