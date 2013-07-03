""" Implementation of the Map ADT using closed hashing and a probe
with double hashing """

from array_m import Array

class _MapEntry:
    """ storage class for HashMap """
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, rhsEntry):
        return isinstance(rhsEntry, self.__class__) and \
              self.key   == rhsEntry.key   and \
              self.value == rhsEntry.value

    def __ne__(self, rhsEntry):
        return not self.__eq__(rhsEntry)

class _HashMapIterator:
    """ Iterator class for HashMap """
    def __init__(self, table):
        self._table = table
        self._curPos = 0

    def __iter__(self):
        return self

    def next(self):
        while self._curPos < len(self._table):
            entry = self._table[self._curPos]
            if entry is HashMap.UNUSED or entry == HashMap.EMPTY:
                self._curPos += 1
            else:
                self._curPos += 1
                return entry
        raise StopIteration

class HashMap:
    """ the HashMap ADT with closed hashing and a double hashing probe. """

    # Define constants to represent the status of each table entry
    UNUSED = None
    EMPTY = _MapEntry(None, None) # Placeholder to show off its existence ...

    def __init__(self):
        """ Creates an empty map instance """
        self._table = Array(7)
        self._count = 0
        self._maxCount = len(self._table) - len(self._table) // 3

    def __len__(self):
        """ Returns the number of entries in the map."""
        return self._count

    def __contains__(self, key):
        """ Determine if the map contains the given key """
        slot = self._findSlot(key, False)
        return slot is not None

    def add(self, key, value):
        """ Adds a new entry to the map if the key doesn't exist. Otherwise,
        the new value replaces the current value associated with the key """
        if key in self:
            slot = self._findSlot(key, False)
            self._table[slot].value = value
            return False
        else:
            slot = self._findSlot(key, True)
            self._table[slot] = _MapEntry(key, value)
            self._count += 1
            if self._count == self._maxCount:
                self._rehash()
            return True

    def __getitem__(self, key):
        return self.valueOf(key)

    def __delitem__(self, key):
        self.remove(key)

    def __setitem__(self, key, value):
        self.add(key, value)

    def valueOf(self, key):
        """ Returns the value associated with the key. """
        slot = self._findSlot(key, False)
        assert slot is not None, "Invalid map key."
        return self._table[slot].value

    def remove(self, key):
        """ Removes the entry associated with the key. """
        slot = self._findSlot(key, False)
        assert slot is not None, "Invalid map key."
        self._table[slot] = HashMap.EMPTY
        self._count -= 1

    def __iter__(self):
        return _HashMapIterator(self._table)

    def _findSlot(self, key, forInsert):
        """ Find the slot containing the key or where the key can be added.
        forInsert indicates if the search is for the insertion, which locates
        the slot into which the new key can be added."""
        assert key is not None, "Can't use None as the search key"
        # Computes the home slot and the step size
        origSlot = self._hash1(key)
        step = self._hash2(key)

        # Probe for the key
        slot = origSlot
        tabSize = len(self._table)
        while self._table[slot] is not HashMap.UNUSED:
            if forInsert and self._table[slot] == HashMap.EMPTY:
                return slot
            elif not forInsert and (self._table[slot] != HashMap.EMPTY and \
                    self._table[slot].key == key) :
                return slot
            else:
                slot = (slot + step) % tabSize
                if slot == origSlot and not forInsert:
                    # To avoid the infinite loop when no UNUSED slot exists
                    return None
        if forInsert:
            return slot
        else:
            return HashMap.UNUSED

    def _rehash(self):
        """ Rebuild the hash table """

        # Create a new large table
        origTable = self._table
        newSize = len(self._table) * 2 + 1
        self._table = Array(newSize)

        # reset the size attributes.
        self._count = 0
        self._maxCount = newSize - newSize//3

        for entry in origTable:
            if entry is not HashMap.UNUSED and entry != HashMap.EMPTY:
                slot = self._findSlot(entry.key, True)
                self._table[slot] = entry
                self._count += 1

    # slot = (h(key) + i*hp(key)) % M
    def _hash1(self, key):
        """ The main hash function for mapping keys to table entries. """
        return abs(hash(key)) % len(self._table)

    def _hash2(self, key):
        """ The second hash function used with double hashing probes. """
        return 1 + abs(hash(key)) % (len(self._table) - 2)

if __name__ == "__main__":
    mm = HashMap()
    mm.add(3, 33)
    mm.add(5, 55)
    mm.add(7, 77)
    mm.add(2, 22)
    mm.add(6, 66)
    mm.add(4, 44)
    for ent in mm:
        print ent.key, ent.value
