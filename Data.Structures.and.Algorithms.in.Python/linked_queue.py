from custom_exception import Empty

class LinkedQueue:
    """FIFO queue implementation using a singly linked list for storage."""

    class _Node:
        """Light-weight, nonpublic class for storing a singly linked node."""
        def __init__(self, elem, link):
            self._element = elem
            self._next = link

    def __init__(self):
        """Create an empty queue."""
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return the element at the front of the queue"""
        if self.is_empty():
            raise Empty("Queue is empty.")
        return self._head._element

    def last(self):
        """Return the element at the back of the queue"""
        if self.is_empty():
            raise Empty("Queue is empty.")
        return self._tail._element

    def dequeue(self):
        """Remove and return the first element of the queue. (i.e., FIFO.)

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty.")
        value = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return value

    def enqueue(self, elem):
        """Add an element to the back of the queue."""
        newest = self._Node(elem, None)
        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest
        self._size += 1

class CircularQueue:
    """Queue implementation using circularly linked list for storage."""

    class _Node:
        """Light-weight, nonpublic class for storing a singly linked node."""
        def __init__(self, elem, link):
            self._element = elem
            self._next = link

    def __init__(self):
        """Create an empty queue."""
        self._tail = None
        self._size = 0

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
        head = self._tail._next
        return head._element

    def last(self):
        """Return the element at the back of the queue.

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty.")
        return self._tail._element

    def rotate(self):
        """Rotate front element to the back of the queue."""
        if self._size > 1:
            self._tail = self._tail._next   # old head becomes new tail

    def enqueue(self, elem):
        """Add an element to the back of the queue."""
        newest = self._Node(elem, None)
        if self.is_empty():
            newest._next = newest
        else:
            newest._next = self._tail._next
            self._tail._next = newest
        self._tail = newest
        self._size += 1

    def dequeue(self):
        """Remove and return the first element of the queue. (i.e., FIFO)

        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty.")
        oldhead = self._tail._next
        if self._size == 1:
            self._tail = None
        else:
            self._tail._next = oldhead._next
        self._size -= 1
        return oldhead._element

