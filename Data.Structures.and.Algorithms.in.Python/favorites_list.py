from linked_deque import PositionalList

class FavoritesList:
    """List of elements ordered from most frequently access to least."""

    class _Item:
        __slots__ = "_value", "_count"

        def __init__(self, elem):
            self._value = elem
            self._count = 0

    # ----------------  Non-public utilities  -----------
    def _find_position(self, elem):
        """Search for element elem and return its Position (Or None if not
        found.)"""
        walker = self._data.first()
        while walker is not None and walker.element()._value != elem:
            walker = self._data.after(walker)
        return walker

    def _move_up(self, pos):
        """Move item at Position pos earlier in the list based on access
        account."""
        if pos != self._data.first():
            cnt = pos.element()._count
            walker = self._data.before(pos)
            if cnt > walker.element()._count:
                while walker != self._data.first() and \
                        cnt > self._data.before(walker).element()._count:
                    walker = self._data.before(walker)
                # delete and reinsert
                self._data.add_before(walker, self._data.delete(pos))

    # --------------  Public methods  ---------------------
    def __init__(self):
        """Create an empty list of favorites"""
        self._data = PositionalList()

    def __len__(self):
        """Return number of entries on the favorites list."""
        return len(self._data)

    def is_empty(self):
        """Return True if the list is empty."""
        return len(self._data) == 0

    def access(self, elem):
        """Access element elem, thereby increasing its access count."""
        pos = self._find_position(elem)
        if pos is None: # if new, place at end
            pos = self._data.add_last(self._Item(elem))
        pos.element()._count += 1   # always increment count
        self._move_up(pos)  # consider moving forward

    def remove(self, elem):
        """Remove element elem from the list of favorites."""
        pos = self._find_position(elem)
        if pos is not None:
            self._data.delete(pos)

    def top(self, k):
        """Generate sequence of top k elements in terms of access count."""
        # Adjust k to accommodate for several special cases rather than raise
        # an exception.
        k = min(k, len(self))
        walk = self._data.first()
        for _ in range(k):
            item = walk.element()
            yield item._value
            walk = self._data.after(walk)

class FavoritesListMTF(FavoritesList):
    """List of elements ordered with move-to-front heuristic."""

    # override _move_up to provide move-to-front semantics
    def _move_up(self, pos):
        """Move accessed item at Position pos to the front of list."""
        if pos != self._data.first():
            self._data.add_first(self._data.delete(pos))

    def top(self, k):
        """Generate sequence of top k elements in terms of access count."""
        k = min(k, len(self))
        temp = PositionalList()
        for item in self._data:
            temp.add_last(item)
        for _ in range(k):
            highPos = temp.first()
            walk = temp.after(highPos)
            while walk is not None:
                if walk.element()._count > highPos.element()._count:
                    highPos = walk
                walk = temp.after(walk)
            yield highPos.element()._value
            temp.delete(highPos)
