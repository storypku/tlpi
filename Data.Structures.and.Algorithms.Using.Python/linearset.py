class Set:
    def __init__(self):
        self._theElements = list()
    def __len__(self):
        return len(self._theElements)
    def __contains__(self, element):
        return element in self._theElements
    def add(self, element):
        if element not in self:
            self._theElements.append(element)
    def remove(self, element):
        assert element in self, "The element must be in the set"
        self._theElements.remove(element)
    def __eq__(self, setB):
        if len(self) != len(setB):
            return False
        else:
            return self.isSubsetOf(setB)
    def isSubsetOf(self, setB):
        for elem in self:
            if elem not in setB:
                return False
        return True
    def union(self, setB):
        newSet = Set()
        newSet._theElements.extend(self._theElements)
        for elem in setB:
            if elem not in self:
                newSet._theElements.append(elem)
        return newSet
    def interset(self, setB):
        newSet = Set()
        for elem in self:
            if elem in setB:
                newSet._theElements.append(elem)
        return newSet
    def difference(self, setB):
        newSet = Set()
        for elem in self:
            if elem not in setB:
                newSet._theElements.append(elem)
        return newSet
    def __iter__(self):
        return _SetIterator(self._theElements)

class _SetIterator:
    def __init__(self, theElems):
        self._theElems = theElems
        self._curNdx = 0
    def __iter__(self):
        return self
    def next(self):
        if self._curNdx < len(self._theElems):
            entry = self._theElems[self._curNdx]
            self._curNdx += 1
            return entry
        else:
            raise StopIteration

