class Empty(Exception):
    """Error attempting to access an element from an empty container."""
    pass

class ArrayStack:
    """LIFO Stack implementation using a Python list as underlying storage."""

    def __init__(self):
        """Create an empty stack."""
        self._data = []

    def __len__(self):
        """Return the number of elements in the stack."""
        return len(self._data)

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self._data) == 0

    def push(self, elem):
        """Add element elem to the top of the stack."""
        self._data.append(elem)

    def peek(self):
        """Return the element at the top of the stack."""
        if self.is_empty():
            raise Empty("Can't peek at an empty stack.")
        return self._data[-1]

    def pop(self):
        """Remove and return the element from teh top of the stack.

        Raise Empty exception if the stack is empty."""
        if self.is_empty():
            raise Empty("Can't pop from an empty stack.")
        return self._data.pop()
