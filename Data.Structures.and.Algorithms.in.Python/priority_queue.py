from custom_exception import Empty
from linked_deque import PositionalList

class PriorityQueueBase:
    """Abstract base class for a priority queue."""

    class _Item:
        """Lightweight composite to store priority queue items."""
        __slots__ = "_key" , "_value"

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key

    def is_empty(self):
        """Return True if the priority queue is empty."""
        return len(self) == 0

class UnsortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with an unsorted list."""

    def _find_min(self): # O(n)
        """Return Position of item with minimum key."""
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            if walk.element() < small.element():
                small = walk
            walk = self._data.after(walk)
        return small

    def __init__(self):
        """Create a new empty Priority Queue."""
        self._data = PositionalList()

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, key, value): # O(1)
        """Add a key-value pair."""
        self._data.add_last(self._Item(key, value))

    def min(self): # O(n)
        """Return but do not remove (k, v) tuple with minimum key."""
        pos = self._find_min(self)
        item = pos.element()
        return (item._key, item._value)

    def remove_min(self): # O(n)
        """Remove and return (k, v) tuple with minimum key."""
        pos = self._find_min()
        item = self._data.delete(pos)
        return (item._key, item._value)

class SortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a sorted list."""

    def __init__(self):
        """Create a new empty Priority Queue."""
        self._data = PositionalList()

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, key, value): # O(n)
        """Add a key-value pair."""
        newest = self._Item(key, value)
        walk = self._data.last()
        while walk is not None and newest < walk.element():
            walk = self._data.before(walk)
        if walk is None:
            self._data.add_first(newest)
        else:
            self._data.add_after(walk, newest)

    def min(self): # O(1)
        """Return but don't remove (k, v) tuple with minimum key."""
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        pos = self._data.first()
        item = pos.element()
        return (item._key, item._value)

    def remove_min(self): # O(1)
        """Remove and return (k, v) tuple with minimum key."""
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        item = self._data.delete(self._data.first())
        return (item._key, item._value)

class HeapPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a binary heap."""

    # ----------  nonpublic behaviors  --------------
    def _parent(self, j):
        return (j-1) // 2

    def _left(self, j):
        return 2*j + 1

    def _right(self, j):
        return 2*j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        """Swap the elements at indices i and j of array."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    # -----------------  public behaviors  ---------------------
    def __init__(self, contents=()):
        """Create a new priority queue.

        By default, queue will be empty. If contents is given, it should be an
        iterable sequence of (k, v) tuples specifying the initial contents.
        """
        self._data = [self._Item(k, v) for (k, v) in contents]
        if len(self._data) > 1:
            self._heapify()

    def _heapify(self):
        """Bottom-up construction of a heap with time complexity of O(n)."""
        start = self._parent(len(self) - 1)
        for j in range(start, -1, -1):
            self._downheap(j)

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, key, value):
        """Add a key-value pair to the priority queue."""
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)

    def min(self):
        """Return but don't remove (k, v) tuple with minimum key.

        Raise Empty exception if empty.
        """
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (k, v) tuple with minimum key.

        Raise Empty exception if empty.
        """
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        self._downheap(0)
        return (item._key, item._value)

class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    """A locator-based priority queue implemented with a binary heap. Effort
    to make better support for Locator is under the way.
    """

    # ----  nested Locator class  -----
    class Locator(HeapPriorityQueue._Item):
        """Token for locating an entry of the priority queue."""
        __slots__ = "_index"

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j

    # ----  nonpublic behaviors  -------
    # override _swap to record new indices
    def _swap(self, i, j):
        super()._swap(i, j)
        self._data[i]._index = i  # reset locator index (pos-swap)
        self._data[j]._index = j

    def _bubble(self, j):
        """bubbling of element at index j."""
        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)
        else:   # j == 0 or self._data[j] >= self._data[self._parent(j)]
            self._downheap(j)

    def add(self, key, value):
        """Add a key-value pair."""
        token = self.Locator(key, value, len(self._data))
        self._data.append(token)
        self._upheap(len(self._data) - 1)
        return token

    def update(self, loc, newkey, newval):
        """Update the key and value for the entry identified by Locator
        loc."""
        j = loc._index
        if not (0 <= j < len(self._data) and self._data[j] is loc):
            raise ValueError("Invalid locator.")
        loc._key = newkey
        loc._value = newval
        self._bubble(j)

    def remove(self, loc):
        """Remove and return the (k, v) pair identified by Locator loc."""
        j = loc._index
        if not (0 <= j < len(self._data) and self._data[j] is loc):
            raise ValueError("Invalid locator.")
        if j == len(self) - 1:
            self._data.pop()
        else:
            self._swap(j, len(self) - 1)
            self._data.pop()
            self._bubble(j)
        return (loc._key, loc._value)
