class Map:
    def __init__(self):
        self._entryList = list()

    def __len__(self):
        return len(self._entryList)

    def __contains__(self, key):
        ndx = self._findPosition(key)
        return ndx is not None

    def add(self, key, value):
        ndx = self._findPosition(key)
        if ndx is not None:
            self._entryList[ndx].value = value
            return False
        else:
            entry = _MapEntry(key, value)
            self._entryList.append(entry)
            return True

    def valueOf(self, key):
        ndx = self._findPosition(key)
        assert ndx is not None, "Invalid map key."
        return self._entryList[ndx].value

    def remove(self, key):
        ndx = self._findPosition(key)
        assert ndx is not None, "Invalid map key."
        self._entryList.pop(ndx)

    def keys(self):
        return [entry.key for entry in self]

    def values(self):
        return [entry.value for entry in self]

    def __iter__(self):
        return _MapIterator(self._entryList)

    def _findPosition(self, key):
        for i in range(len(self)):
            if self._entryList[i].key == key:
                return i
        return None

class _MapIterator:
    def __init__(self, entryList):
        self._entries = entryList
        self._curNdx = 0

    def __iter__(self):
        return self

    def next(self):
        if self._curNdx < len(self._entries):
            entry = self._entries[self._curNdx]
            self._curNdx += 1
            return entry
        else:
            raise StopIteration

class _MapEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
