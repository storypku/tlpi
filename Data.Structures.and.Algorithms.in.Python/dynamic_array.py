"""Implementation of a DynamicArray class, using a raw array from the ctypes
module as storage."""

import ctypes   # module providing low-level arrays

class DynamicArray:
    """A dynamical array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty erray."""
        self._length = 0    # count actual elements
        self._capacity = 1  # default array capacity
        self._array = self._make_array(self._capacity)  # low level array

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._length

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._length:
            raise IndexError("invalid index")
        return self._array[k]

    def __setitem__(self, k, obj):
        """Set element at index k to obj."""
        if not 0 <= k < self._length:
            raise IndexError("invalid index")
        self._array[k] = obj

    def append(self, obj):
        """Add object to the end of the array."""
        if self._length == self._capacity:
            self._resize(2 * self._capacity)
        self._array[self._length] = obj
        self._length += 1

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        # for simplicity, we assume 0<=k<=n in this version
        if not 0 <= k <= self._length:
            raise IndexError("invalid index")
        if self._length == self._capacity:
            self._resize(2 * self._capacity)
        for j in range(self._length, k, -1):
            self._array[j] = self._array[j-1]
        self._array[k] = value
        self._length += 1

    def __delitem__(self, k):
        """Remove value at index k."""
        self.pop(k)

    def pop(self, k=None):
        """Pop value at index k, shifting subsequent values leftward."""
        if k is None:   # default k
            k = self._length - 1

        if self._length == 0:
            raise IndexError("pop from empty list")

        # for simplicity, we assume 0<=k<n in this version.
        if not 0 <= k < self._length:
            raise IndexError("index out of range")

        value = self._array[k]

        for j in range(k, self._length-1):
            self._array[j] = self._array[j+1]   # shift others to fill gap

        self._array[self._length -1] = None     # help garbage collection
        self._length -= 1

        if self._length < self._capacity // 2 : # shrink the dynamic array
            self._resize(self._capacity // 2)

        return value

    def _resize(self, cap):
        """Resize internal array to capacity cap."""
        newArray = self._make_array(cap)
        for k in range(self._length):
            newArray[k] = self._array[k]
        self._array = newArray
        self._capacity = cap

    def _make_array(self, cap):      # non-public utility
        """Return new array with capacity cap."""
        return (cap * ctypes.py_object)()

    def remove(self, value):
        """Remove first occurrence of value (or raise ValueError)."""

        for k in range(self._length):
            if self._array[k] == value:

                for j in range(k, self._length -1):
                    self._array[j] = self._array[j+1]

                self._array[self._length - 1] = None
                self._length -= 1

                if self._length < self._capacity // 2: # shrink the array
                    self._resize(self._capacity // 2)

                return                                 # exit immediately

        raise ValueError("value not found")
