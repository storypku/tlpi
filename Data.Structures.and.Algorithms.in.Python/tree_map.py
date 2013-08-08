from map import MapBase
from linked_binary_tree import LinkedBinaryTree

class TreeMap(LinkedBinaryTree, MapBase):
    """Sorted map implementation using a binary search tree."""

    # ---- override Position class  ----
    class Position(LinkedBinaryTree.Position):
        def key(self):
            """Return key of map's key-value pair."""
            return self.element()._key

        def value(self):
            """Return value of map's key-value pair."""
            return self.element()._value

    # ----  nonpublic utilities  ----
    def _subtree_search(self, pos, k):
        """Return Position of pos's subtree having key k, or last node
        searched."""
        if k == pos.key():
            return pos
        elif k < pos.key() and self.left(pos) is not None:
            return self._subtree_search(self.left(pos), k)
        elif k > pos.key() and self.right(pos) is not None:
            return self._subtree_search(self.right(pos), k)
        else:
            return pos  # unsuccessful search

    def _subtree_first_position(self, pos):
        """Return Position of first item in subtree rooted at pos."""
        walk = pos
        while self.left(walk) is not None:
            walk = self.left(walk)
        return walk

    def _subtree_last_position(self, pos):
        """Return Position of last item in subtree rooted at pos."""
        walk = pos
        while self.right(walk) is not None:
            walk = self.right(walk)
        return walk

    def first(self):    # O(h)
        """Return the first Position in the tree (or None if empty)."""
        if not self.is_empty():
            return self._subtree_first_position(self.root())
        else:
            return None

    def last(self):     # O(h)
        """Return the last Position in the tree (or None if empty)."""
        if not self.is_empty():
            return self._subtree_last_position(self.root())
        else:
            return None

    def before(self, pos):  # O(h) for worst case, O(1) amortized
        """Return the Position just before pos in natural order.

        Return None if pos is the first position.
        """
        self._validate(pos)
        if self.left(pos) is not None:
            return self._subtree_last_position(self.left(pos))
        else:
            walk = pos
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, pos):   # O(h) for worst case, O(1) amortized
        """Return the Position just after pos in natural order.

        Return None if pos is the last position.
        """
        self._validate(pos)
        if self.right(pos) is not None:
            return self._subtree_first_position(self.right(pos))
        else:
            walk = pos
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k): # O(h) for worst case
        """Return position with key k, or else neighbor(or None if empty)."""
        if self.is_empty():
            return None
        else:
            pos = self._subtree_search(self.root(), k)
            self._rebalance_access(pos) # hook for balanced tree subclasses
            return pos

    def find_min(self): # O(h)
        """Return (k, v) pair with minimum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            pos = self.first()
            return (pos.key(), pos.value())

    def find_max(self): # O(h)
        """Return (k, v) pair with maximum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            pos = self.last()
            return (pos.key(), pos.value())

    def find_ge(self, k):   # O(h)
        """Return (k, v) pair with least key >= k.

        Return None if there doesn't exist such a key.
        """
        if self.is_empty():
            return None
        else:
            pos = self.find_position(k)
            if pos.key() < k:
                pos = self.after(pos)
            return (pos.key(), pos.value()) if pos is not None else None

    def find_gt(self, k):   # O(h)
        """Return (k, v) pair with least key > k.

        Return None if there doesn't exist such a key.
        """
        if self.is_empty():
            return None
        else:
            pos = self.find_position(k)
            if pos.key() <= k:
                pos = self.after(pos)
            return (pos.key(), pos.value()) if pos is not None else None

    def find_lt(self, k):   # O(h)
        """Return (k, v) pair with largest key < k.

        Return None if there doesn't exist such a key.
        """
        if self.is_empty():
            return None
        else:
            pos = self.find_position(k)
            if pos.key() >= k:
                pos = self.before(pos)
            return (pos.key(), pos.value()) if pos is not None else None

    def find_le(self, k):   # O(h)
        """Return (k, v) pair with largest key <= k.

        Return None if there doesn't exist such a key.
        """
        if self.is_empty():
            return None
        else:
            pos = self.find_position(k)
            if pos.key() > k:
                pos = self.before(pos)
            return (pos.key(), pos.value()) if pos is not None else None

    def find_range(self, start, stop):  # O(s+h), s is the number of items
        """Iterate all (k, v) pairs such that start <= key < stop.

        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if not self.is_empty():
            if start is None:
                pos = self.first()
            else:
                pos = self.find_position(start)
                if pos.key() < start:
                    pos = self.after(pos)
            while pos is not None and (stop is None or pos.key() < stop):
                yield (pos.key(), pos.value())
                pos = self.after(pos)

    def __getitem__(self, k):   # O(h)
        """Return value associated with key k (raise KeyError if not
        found)."""
        if self.is_empty():
            raise KeyError("Key Error: " + repr(k))
        else:
            pos = self._subtree_search(self.root(), k)
            self._rebalance_access(pos) # hook for balanced tree subclasses
            
            if pos.key() != k:
                raise KeyError("Key Error: " + repr(k))
            else:
                return pos.value()

    def __setitem__(self, k, v):    # O(h)
        """Assign value v to key k, overwriting existing value if present."""
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v)) # from LinkedBinaryTree
        else:
            pos = self._subtree_search(self.root(), k)
            if pos.key() == k:
                pos.element()._value = v
                self._rebalance_access(pos) # hook as described above
                
                return
            else:
                item = self._Item(k, v)
                if pos.key() < k:
                    leaf = self._add_right(pos, item)
                else:
                    leaf = self._add_left(pos, item)
        self._rebalance_insert(leaf) # hook for balanced tree subclasses
        


    def __iter__(self): # O(n)
        """Generate an iteration of all keys in the map in order."""
        pos = self.first()
        while pos is not None:
            yield pos.key()
            pos = self.after(pos)

    def __reversed__(self): # O(n)
        """Generate an iteration of all keys in the map in reverse order."""
        pos = self.last()
        while pos is not None:
            yield pos.key()
            pos = self.before(pos)

    def delete(self, pos):  # O(h)
        """Remove the item at given Position."""
        self._validate(pos)
        if self.left(pos) and self.right(pos):
            alternative = self._subtree_last_position(self.left(pos))
            self._replace(pos, alternative.element()) # from LinkedBinaryTree
            pos = alternative
        # now pos has at most one item
        parent = self.parent(pos)
        self._delete(pos) # inherited from LinkedBinaryTree
        self._rebalance_delete(parent) # if root deleted, parent is None
        

    def __delitem__(self, k):   # O(h)
        """Remove item associated with key k (or raise KeyError if not
        found)."""
        if not self.is_empty():
            pos = self._subtree_search(self.root(), k)
            if k == pos.key():
                self.delete(pos)    # rely on positional version
                return
            self._rebalance_access(pos)
            
        raise KeyError("Key Error: " + repr(k))

    def _rebalance_access(self, pos):
        pass

    def _rebalance_insert(self, pos):
        pass

    def _rebalance_delete(self, pos):
        pass
