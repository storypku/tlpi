class SequenceIterator:
    """An iterator for any of Python's sequence types."""

    def __init__(self, sequence):
        """Create an iterator for the given sequence."""
        self._seq = sequence
        self._pos = -1

    def __next__(self):
        """Return the next element, or else raise StopIteration."""
        self._pos += 1
        if self._pos < len(self._seq):
            self._seq[self._pos]
        else:
            raise StopIteration

    def __iter__(self):
        """By convention, an iterator must return itself as an iterator."""
        return self

