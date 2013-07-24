import collections

class Range(collections.Sequence):
    """A class that mimic's the built-in range class."""

    def __init__(self, start, stop=None, step=1):
        """Initialize a Range instance.

        Semantics is similar to built-in range class.
        """
        if step == 0:
            raise ValueError("Step can't be 0.")

        if stop is None:
            start, stop = 0, start

        flag = -1 if step > 0 else 1
        self._length = max(0, (stop - start + step + flag)//step)

        self._start = start
        self._step = step

    def __len__(self):
        """Return number of entries in the range."""
        return self._length

    def __getitem__(self, k):
        """Return entry at index k (using standard interpretation if
        negative)."""
        if k < 0:
            k += len(self)
        if not 0 <= k < self._length:
            raise IndexError("Index out of range.")

        return self._start + k * self._step
