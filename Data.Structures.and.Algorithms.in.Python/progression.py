class Progression:
    """Iterator producing a generic progression.

    Default iterator produces the whole natural numbers 0, 1, 2, ...
    """

    def __init__(self, start=0):
        """Initialize current to the first value of the progression."""
        self._current = start

    def _advance(self):
        """Update self._current to a new value.

        This should be overridden by a subclass to customize progression.

        By convention, if current is set to None, this designates the end
        of a finite progression.
        """
        self._current += 1

    def __next__(self):
        """Return the next element, or else raise StopIteration error."""
        if self._current is None:   # our convention to end a progression
            raise StopIteration()
        else:
            ans = self._current # record current value to return
            self._advance()     # advance to prepare for next time
            return ans          # return the answer

    def __iter__(self):
        """By convention, an iterator must return itself as an iterator."""
        return self

    def print_progression(self, n):
        """Print next n values of the progression."""
        print (' '.join(str(next(self)) for j in range(n)))

class ArithmeticProgression(Progression):   # inherit from Progression
    """Iterator producing an arithmetic progression."""

    def __init__(self, start=0, increment=1):
        """Create a new arithmetic progression.
        start       the first term of the progression (default 0)
        increment   the fixed constant to add to each term (default 1)
        """
        super().__init__(start)
        self._increment = increment

    def _advance(self):
        """Update current value by adding the fixed increment."""
        self._current += self._increment

class GeometricProgression(Progression):
    """Iterator producing a geometric progression."""

    def __init__(self, start=1, base=2):
        """Create a new geometric progression.
        start       the first term of the progression (default 1)
        base        the fixed constant multiplied to each term (default 2)
        """
        super().__init__(start)
        self._base = base

    def _advance(self):
        """Update current value by multiplying it by the base value."""
        self._current *= self._base

class FibonacciProgression(Progression):
    """Iterator producing a fibonacci progression."""

    def __init__(self, first=0, second=1):
        """Create a new fibonacci progression.
        first       the first term of the progression (default 0)
        second      the second term of the progression (default 1)
        """
        super().__init__(first)
        self._next = second

    def _advance(self):
        """Update current value and prepare for the next time"""
        self._current, self._next = self._next, self._current + self._next
