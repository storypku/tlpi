class Empty(Exception):
    """Error attempting to access an element from an empty container."""
    pass

class ArrayQueue:
    """FIFO queue implementation using a Python list as underlying storage."""
    DEFAULT_CAPACITY = 10

    def __init__(self):
        """Create an empty queue."""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return the element at the front of the queue.

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty.")
        return self._data[self._front]

    def dequeue(self):
        """Remove and return the first element of the queue (i.e., FIFO).

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty.")
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        if self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return answer

    def _resize(self, cap):
        """Resize to a new list of capacity >= len(self)."""
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (walk + 1) % len(old)
        self._front = 0

    def enqueue(self, elem):
        """Add an element to the back of the queue."""
        if self._size == len(self._data):
            self._resize(2 * self._size)
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = elem
        self._size += 1

class Deque:
    """Double-ended queue implementation using a Python list as underlying storage."""
    DEFAULT_CAPACITY = 10

    def __init__(self):
        """Create an empty deque."""
        self._data = [None] * Deque.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        """Return the number of elements in the deque."""
        return self._size

    def is_empty(self):
        """Return True if the deque is empty."""
        return self._size == 0

    def first(self):
        """Return the first element of the deque.

        Raise Empty exception if the deque is empty.
        """
        if self.is_empty():
            raise Empty("Deque is empty.")
        return self._data[self._front]

    def last(self):
        """Return the last element of the deque.

        Raise Empty exception if the deque is empty.
        """
        if self.is_empty():
            raise Empty("Deque is empty.")
        last = (self._front + self._size - 1) % len(self._data)
        return self._data[last]

    def _resize(self, cap):
        """Resize to a new list of capacity >= len(self)."""
        pass

    def add_first(elem):
        """Add element elem to the front of the deque."""
        pass

    def add_last(elem):
        """Add element elem to the back of the deque."""
        pass

    def delete_first():
        """Remove and return the first element from the deque."""
        pass

    def delete_last():
        """Remove and return the last element from the deque."""
        pass
