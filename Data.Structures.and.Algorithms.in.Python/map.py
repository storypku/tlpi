from collections import MutableMapping
from random import randrange

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
            if k == item._key:
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

class HashMapBase(MapBase):
    """Abstract base class for map using hash-table with MAD (Multiply, Add
    and Divide) compression."""

    def __init__(self, cap=11, p=109345121):
        self._table = cap * [None]
        self._n = 0 # number of entries in the map
        self._prime = p # prime for MAD compression
        self._scale = 1 + randrange(p-1) # scale from 1 to p-1 for MAD
        self._shift = randrange(p) # shift from 0 to p-1 for MAD

    def _hash_function(self, k):
        return (hash(k) * self._scale + self._shift)\
                % self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        j = self._hash_function(k)
        return self._bucket_getitem(j, k) # may raise KeyError

    def __setitem__(self, k, v):
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v)   # subroutine maintains self._n
        if self._n > len(self._table) // 2: # keep load factor <= 0.5
            self._resize(2 * len(self._table) + 1)

    def __delitem__(self, k):
        j = self._hash_function(k)
        self._bucket_delitem(j, k)  # may raise KeyError
        self._n -= 1

    def _resize(self, c): # Resize bucket array to capacity c
        old = list(self.items())
        self._table = c * [None]
        self._n = 0
        for (k, v) in old:
            self[k] = v

class ChainHashMap(HashMapBase):
    """Hash map implemented with separate chaining for collision
    resolution."""

    def _bucket_getitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: " + repr(k))
        return bucket[k]    # may raise KeyError

    def _bucket_setitem(self, j, k, v):
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize:
            self._n += 1

    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: " + repr(k))
        del bucket[k]

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:
                    yield key

class ProbeHashMap(HashMapBase):
    """Hash map implemented with linear probing ofor collision resolution."""
    _AVAIL = object()   # sentinal marks locations of previous deletions

    def _is_available(self, j):
        """Return True if index j is available in table."""
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _find_slot(self, j, k):
        """Search for k in bucket at index j.

        Return (success, index) tuple, described as follows:
        If match was found, success is True and index denotes its location.
        If no match found, success is False and index denotes first available
        slot.
        """
        firstAvail = None
        for _ in range(len(self._table)):
            if self._is_available(j):
                if firstAvail is None:
                    firstAvail = j
                if self._table[j] is None:
                    return (False, firstAvail)
            elif k == self._table[j]._key:
                return (True, j)
            j = (j + 1) % (len(self._table))
        return (False, firstAvail)

    def _bucket_getitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError("Key Error: " + repr(k)) # No match found
        return self._table[s]._value

    def _bucket_setitem(self, j, k, v):
        found, s = self._find_slot(j, k)
        if not found:
            self._table[s] = self._Item(k, v)
            self._n += 1
        else:
            self._table[s]._value = v

    def _bucket_delitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError("Key Error: " + repr(k)) # No match found
        self._table[s] = ProbeHashMap._AVAIL # mark as vacated

    def __iter__(self):
        for j in range(len(self._table)):
            if not self._is_available(j):
                yield self._table[j]._key

class SortedTableMap(MapBase):
    """Map implementation using a sorted table."""

    # ---- non-public behaviors ----
    def _find_index(self, k, low, high):
        """Return index of the leftmost item with key >= k.

        Return high + 1 if no such item qualifies.

        That is, j will be returned such that:
            all items of slice table[low, j] have key < k
            all items of slice table[j, high+1] have key >= k.
        """
        if high < low:
            return high + 1
        else:
            mid = (low + high) // 2
            if k == self._table[mid]._key:
                return mid
            elif k < self._table[mid]._key:
                return self._find_index(k, low, mid - 1)
            else:
                return self._find_index(k, mid + 1, high)

    # ---- public behaviors ----
    def __init__(self):
        """Create an empty map."""
        self._table = []

    def __len__(self):
        """Return number of items in the map."""
        return len(self._table)

    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not
        found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError("Key Error: " + repr(k))
        return self._table[j]._value

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            self._table[j]._value = v
        else:
            self._table.insert(j, self._Item(k, v)) # add new item

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError("Key Error: " + repr(k))
        self._table.pop(j)

    def __iter__(self):
        """Generate keys of the map ordered from minimum to maximum."""
        for item in self._table:
            yield item._key

    def __reversed__(self):
        """Generate keys of the map ordered from maximum to minimum."""
        for item in reversed(self._table):
            yield item._key

    def find_min(self):
        """Return (k, v) pair with minimum key (or None if empty)."""
        if len(self._table) > 0:
            return (self._table[0]._key, self._table[0]._value)
        else:
            return None

    def find_max(self):
        """Return (k, v) pair with maximum key (or None if empty)."""
        if len(self._table) > 0:
            return (self._table[-1]._key, self._table[-1]._value)
        else:
            return None

    def find_ge(self, k):
        """Return (k, v) pair with least key >= k."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_lt(self, k):
        """Return (k, v) pair with greatest key < k."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j > 0:
            return (self._table[j-1]._key, self._table[j-1]._value)
        else:
            return None

    def find_gt(self, k):
        """Return (k, v) pair with least key > k."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            j += 1  # advance past match
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_le(self, k):
        """Return (k, v) pair with greatest key <= k."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if (j < len(self._table) and self._table[j]._key != k)\
                or j == len(self._table):
            j -= 1
        if j >= 0:
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_range(self, start, stop):
        """Iterate all (k, v) pairs such that start <= key < stop

        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if start is None:
            j = 0
        else:
            j = self._find_index(start, 0, len(self._table) - 1)
        while j < len(self._table) and (stop is None or \
                                        self._table[j]._key < stop):
            yield (self._table[j]._key, self._table[j]._value)
            j += 1
