"""Solution to summation puzzles.

The following lists three summmation puzzle instances:

    pot + pan = bib
    dog + cat = pig
    boy + girl = baby

where each letter represents a unique digit (0, 1, 2, ..., 9).
"""
class _Choice:
    """class for representing unused digit."""

    def __init__(self, digit, availFlag=True):
        """Initialization.

        @param digit       the unused digit within consideration
        @param availFlag   indicate whether the digit is available
        """
        self.digit = digit
        self.availFlag = availFlag

    def setAvailFlag(self, availFlag=True):
        """change the availability of the digit."""
        self.availFlag = availFlag

class SummationPuzzle:
    """class for solving summmation puzzle."""

    def __init__(self, firstAddend, secondAddend, summation):
        """Initialize the summation puzzle instance."""
        self._firstAddend = firstAddend
        self._secondAddend = secondAddend
        self._summation = summation
        self._letters = self._composeLetters()
        self._digits = list()
        self.choices = [_Choice(i) for i in range(10)]

    def _composeLetters(self):
        """Return the set of letters (without duplicates) that appears in the
        puzzle instance."""
        letters = set()
        for iterm in (self._firstAddend, self._secondAddend, self._summation):
            for lett in iterm:
                letters.add(lett)
        return list(letters)

    def getLetters(self):
        """Return all the letters of the puzzle instance."""
        return self._letters

    def _buildNumber(self, term, mapping):
        """Build the numeric value based on the letter-digit mapping."""
        number = 0
        for lett in term:
            number = 10 * number + mapping[lett]
        return number

    def _buildMapping(self):
        """Build the letter-digit mapping."""
        mapping = dict()
        for lett, digit in zip(self._letters, self._digits):
            mapping[lett] = digit
        return mapping

    def _checkExpr(self, mapping):
        """Check whether the puzzle's expression holds with the letter-digit
        map in mapping."""
        firstAddend = self._buildNumber(self._firstAddend, mapping)
        secondAddend = self._buildNumber(self._secondAddend, mapping)
        summation = self._buildNumber(self._summation, mapping)
        return firstAddend + secondAddend == summation

    def _solutionFound(self):
        """Return whether the solution to the puzzle was found."""
        if len(self._letters) != len(self._digits):
            return False
        mapping = self._buildMapping()
        return self._checkExpr(mapping)

    def _puzzleSolve(self, k):
        """Recursive helper method to solve the puzzle. Initially, k is the
        number of non-duplicate letters that appear in the puzzle."""
        for node in self.choices:
            if not node.availFlag:
                continue
            self._digits.append(node.digit)
            node.setAvailFlag(False)
            if k == 1 and self._solutionFound():
                return True
            elif self._puzzleSolve(k-1) == True:
                return True
            else:
                self._digits.pop()
                node.setAvailFlag(True)
        return False

    def solve(self):
        """Method to solve the puzzle."""
        if not self._puzzleSolve(len(self._letters)):
            print("No solution found.")
        else:
            print("Solution found.")
            mapping = self._buildMapping()
            firstAddend = self._buildNumber(self._firstAddend, mapping)
            secondAddend = self._buildNumber(self._secondAddend, mapping)
            summation = self._buildNumber(self._summation, mapping)
            print("{0:>5} + {1:>5} = {2:<5}".format(self._firstAddend,
                    self._secondAddend, self._summation))
            print("{0:>5} + {1:>5} = {2:<5}".format(firstAddend,
                    secondAddend, summation))

if __name__ == "__main__":
    puzzle = SummationPuzzle("boy", "girl", "baby")
    puzzle.solve()
    puzzle = SummationPuzzle("dog", "cat", "pig")
    puzzle.solve()
    puzzle = SummationPuzzle("pot", "pan", "bib")
    puzzle.solve()
