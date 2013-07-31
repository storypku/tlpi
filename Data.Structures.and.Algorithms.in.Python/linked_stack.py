from custom_exception import Empty

class LinkedStack:
    """LIFO Stack implementation using a singly linked list for storage."""

    class _Node:
        """Light-weight, non-public class for storing a singly linked node."""
        __slots__ = "_element", "_next"
        def __init__(self, elem, link):
            self._element = elem
            self._next = link

    def __init__(self):
        """Create an empty stack."""
        self._top = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in the stack."""
        return self._size

    def is_empty(self):
        return self._size == 0

    def push(self, elem):
        """Add element elem to the top of the stack."""
        self._top = self._Node(elem, self._top)
        self._size += 1

    def peek(self):
        """Return the element at the top of the stack."""
        if self.is_empty():
            raise Empty("Stack is empty.")
        return self._top._element

    def pop(self):
        """Remove and return the element from the top of the stack."""
        if self.is_empty():
            raise Empty("Stack is empty.")
        value = self._top._element
        self._top = self._top._next
        self._size -= 1
        return value
