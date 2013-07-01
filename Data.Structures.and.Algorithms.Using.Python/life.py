#!/usr/bin/env python
from array_m import Array2D
class LifeGrid:
    DEAD_CELL = 0
    LIVE_CELL = 1
    def __init__(self, numRows, numCols):
        self._grid = Array2D(numRows, numCols)
        # Clear the grid and set all cells to dead
        self.configure(list())

    def numRows(self):
        return self._grid.numRows()

    def numCols(self):
        return self._grid.numCols()

    def configure(self, coordList):
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                self.clearCell(i, j)
        for coord in coordList:
            self.setCell(coord[0], coord[1])

    def isLiveCell(self, row, col):
        if row >= 0 and row < self.numRows() and\
                col >=0 and col < self.numCols():
            return self._grid[row, col] == LifeGrid.LIVE_CELL
        else:
            return False

    def clearCell(self, row, col):
        self._grid[row, col] = LifeGrid.DEAD_CELL

    def setCell(self, row, col):
        self._grid[row, col] = LifeGrid.LIVE_CELL

    def numLiveNeighbors(self, row, col):
        num = 0
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if r == 0 and c == 0:
                    continue
                if self.isLiveCell(row + r, col + c):
                    num += 1
        return num

    def isDeadGrid(self):
        for row in range(self.numRows()):
            for col in range(self.numCols()):
                if self.isLiveCell(row, col):
                    return False
        return True

    def evolve(self):
        nextGenLives = list()
        for row in range(self.numRows()):
            for col in range(self.numCols()):
                neighbors = self.numLiveNeighbors(row, col)
                if ( neighbors == 2 and self.isLiveCell(row, col) ) or \
                   ( neighbors == 3 ):
                        nextGenLives.append((row, col))
        self.configure(nextGenLives)

    def draw(self):
        numRows = self.numRows()
        numCols = self.numCols()
        for row in range(numRows):
            print "-" * (4 * numCols + 1)
            for col in range(numCols):
                if self.isLiveCell(row, col):
                    print "|", "A",
                else:
                    print "|", " ",
            print "|"
        print "-" * (4 * numCols + 1)
        print "\n"

def loadUserConf(numRows, numCols):
    from random import randint
    initialLives = list()
    times = randint( 1, max(numRows * numCols, 1) )
    for i in range(times):
        row = randint(0, numRows - 1)
        col = randint(0, numCols - 1)
        initialLives.append((row, col))
    return initialLives

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: %s numRows numCols numGeneration\n" % sys.argv[0])
        sys.exit(0)
    numRows = int(sys.argv[1])
    numCols = int(sys.argv[2])
    grid = LifeGrid(numRows, numCols)
    # Initial Grid Configuration
    initialLives = loadUserConf(numRows, numCols)
    grid.configure(initialLives)
    print "The initial Configuration"
    grid.draw()
    for gen in range(int(sys.argv[3])):
        grid.evolve()
        print "The %d generation" % (gen + 1)
        if grid.isDeadGrid():
            print "\tbecomes DEAD!\n\nGAME OVER!\n"
            sys.exit(0)
        grid.draw()

