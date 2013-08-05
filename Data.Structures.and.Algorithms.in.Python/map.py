from collections import MutableMapping

class MapBase(MutableMapping):
    """Abstract Map base class that includes a nonpublic _Item class."""

    class _Item:
        """Lightweight composite to store key-value pairs as map items."""
        __slots__ = "_key", "_value"

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, rhs):
            return self._key == rhs._key

        def __ne__(self, rhs):
            return not (self == rhs)

        def __lt__(self, rhs):
            return self._key < rhs._key

class UnsortedTableMap(MapBase):
    """Inefficient Map implementation using an unordered list."""

    def __init__(self):
        """Create an empty map."""
        self._table = []

    def __getitem__(self, k): # O(n)
        """Return value associated with key k (raise KeyError if not
        found)."""
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError("Key Error: " + repr(k))

    def __setitem__(self, k, v): # O(n)
        """Assign value v to key k, overwriting existing value if present."""
        for item in self._table:
            if k == item.__key:
                item._value = v
                return
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):   # O(n)
        """Remove item associated with key k (raise KeyError if not found)."""
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)
                return
        raise KeyError("Key Error: " + repr(k))

    def __len__(self):
        """Return number of items in the map."""
        return len(self._table)

    def __iter__(self):
        """Generate iteration of the map's keys."""
        for item in self._table:
            yield item._key

def hash_code(s):
    """Return cyclic-shift hash code for string s."""
    mask = (1<<32) - 1
    h = 0
    for character in s:
        h = (h << 5 & mask) | (h >> 27)
        h += ord(character)
    return h
