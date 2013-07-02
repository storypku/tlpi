import numpy as np
from lliststack import Stack

class QueenBoard:
    """ class to solve the n-queens problem """

    # The degree of all guarded position will be no more than 4. So
    # _QueenValue is used to indicate the position where a queen resides.

    _QueenValue = 8

    def __init__(self, n):
        """ create an n x n empty board """

        assert n > 3, "the size of the n-queens board must > 3."
        self._board = np.zeros(shape=(n, n), dtype = int)
        self._numQueens = 0

    def size(self):
        """ returns the size of the board."""
        return self._board.shape[0]

    def numQueens(self):
        """ returns the number of queens currently positioned on the board. """
        return self._numQueens

    def unguarded(self, row, col):
        """ returns True if the given position is currently unguarded """

        assert row >= 0 and row < self.size() and \
                col >= 0 and col < self.size(), "Board index out of range"
        return self._board[row, col] == 0

    def placeQueen(self, row, col):

        """ Places a queen on the board at position (row, col) """
        assert row >= 0 and row < self.size() and \
                col >=0 and col < self.size(), "Board index out of range"

        assert self.unguarded(row, col), \
                "Queen can't be placed on a guarded land."

        self._board[row, :] += 1    # Guarding its row
        self._board[:, col] += 1    # Guarding its col

        # Guarding its diagonol from top-left to bottom-right
        if row > col:
            diff = row - col
            for tmp in range(diff, self.size()):
                self._board[tmp, tmp - diff] += 1
        else:
            diff = col - row
            for tmp in range(diff, self.size()):
                self._board[tmp - diff, tmp] += 1

        # Guarding its diagonal from bottom-left to top-right 
        rcsum = row + col
        if row + col < self.size():
            for tmp in range(0, rcsum + 1):
                self._board[tmp, rcsum - tmp] += 1
        else:
            flagVal = rcsum - self.size() + 1
            for tmp in range(flagVal, self.size()):
                self._board[tmp, rcsum - tmp] += 1

        self._board[row, col] = self._QueenValue
        self._numQueens += 1

    def removeQueen(self, row, col):
        """ Removes the queen from position (row, col) """

        assert row >= 0 and row < self.size() and \
                col >=0 and col < self.size(), "Board index out of range"

        self._board[row, :] -= 1    # Unguarding its row
        self._board[:, col] -= 1    # Unguarding its col

        # Unguarding its diagonol from top-left to bottom-right
        if row > col:
            diff = row - col
            for tmp in range(diff, self.size()):
                self._board[tmp, tmp - diff] -= 1
        else:
            diff = col - row
            for tmp in range(diff, self.size()):
                self._board[tmp - diff, tmp] -= 1

        # Unguarding its diagonal from bottom-left to top-right 
        rcsum = row + col
        if row + col < self.size():
            for tmp in range(0, rcsum + 1):
                self._board[tmp, rcsum - tmp] -= 1
        else:
            flagVal = rcsum - self.size() + 1
            for tmp in range(flagVal, self.size()):
                self._board[tmp, rcsum - tmp] -= 1
        self._board[row, col] = 0
        self._numQueens -= 1

    def reset(self):
        """ Reset the board to its original state by removing all queens
        currently placed on the board. """

        self._board.fill(0)

    def draw(self):
        """ visualize the N-Queens board """

        print "----" * self.size()
        for row in range(self.size()):
            for col in range(self.size()):
                if self._board[row, col] == self._QueenValue:
                    print "| *",
                else:
                    print "|  ",
            print "|"
            print "----" * self.size()

    def solveNQueen(self, findAll = False):
        """ method to solve the n-queens problem. If the findAll flag
        is set to be true, all solutions will be printed. """

        solution = 0

        queen_stack = Stack()
        row = 0
        col = 0
        while True:
            while row < self.size() and not self.unguarded(row, col):
                row += 1
            if row == self.size():
                if col == 0: # All solutions have been found.
                    return False
                (row, col) = queen_stack.pop()
                self.removeQueen(row, col)
                row += 1
            else:
                self.placeQueen(row, col)
                queen_stack.push((row, col))
                if self.numQueens() == self.size():
                    if findAll == False:
                        self.draw()
                        return True
                    else:
                        solution = solution + 1
                        print "Solution %2d found:" % solution
                        self.draw()
                        print ""
                        (row, col) = queen_stack.pop()
                        self.removeQueen(row, col)
                        row += 1
                        continue

                row = 0
                col += 1

if __name__ == "__main__":

    import sys
    if len(sys.argv) < 2:
        print "Usage: %s numQueens [flag]\n  where numQueens must > 3." \
              % sys.argv[0]
        sys.exit(0)

    size = int(sys.argv[1])
    if len(sys.argv) > 2:
        flag = True
    else:
        flag = False

    board = QueenBoard(size)
    board.solveNQueen(flag)
