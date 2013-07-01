from array_m import Array2D
class Matrix:
    def __init__(self, numRows, numCols):
        self._theGrid = Array2D(numRows, numCols)
        self._theGrid.clear(0)

    def numRows(self):
        return self._theGrid.numRows()

    def numCols(self):
        return self._theGrid.numCols()

    def __getitem__(self, ndxTuple):
        return self._theGrid.__getitem__(ndxTuple)

    def __setitem__(self, ndxTuple, scalar):
        return self._theGrid.__setitem__(ndxTuple, scalar)

    def clear(self, value):
        self._theGrid.clear(value)

    def scaleBy(self, scalar):
        for r in range(self.numRows()):
            for c in range(self.numCols()):
                self[r, c] *= scalar

    def tranpose(self):
        numCols = self.numRows()
        numRows = self.numCols()
        newMatrix = Matrix(numRows, numCols)
        for r in range(numRows):
            for c in range(numCols):
                newMatrix[r, c] = self[c, r]
        return newMatrix

    def __add__(self, rhsMatrix):
        numRows = self.numRows()
        numCols = self.numCols()
        assert rhsMatrix.numRows() == numRows and \
                rhsMatrix.numCols() == numCols, \
                "Matrix sizes not compatible for the add operation"
        newMatrix = Matrix(numRows, numCols)
        for r in range(numRows):
            for c in range(numCols):
                newMatrix[r, c] = self[r, c] + rhsMatrix[r, c]
        return newMatrix

    def __sub__(self, rhsMatrix):
        numRows = self.numRows()
        numCols = self.numCols()
        assert rhsMatrix.numRows() == numRows and \
                rhsMatrix.numCols() == numCols, \
                "Matrix sizes not compatible for the sub operation"
        newMatrix = Matrix(numRows, numCols)
        for r in range(numRows):
            for c in range(numCols):
                newMatrix[r, c] = self[r, c] - rhsMatrix[r, c]
        return newMatrix

    def __mul__(self, rhsMatrix):
        comm = self.numCols()
        assert rhsMatrix.numRows() == comm, \
                "Matrix sizes not compatible for the multiply operation"
        numRows = self.numRows()
        numCols = rhsMatrix.numCols()
        newMatrix = Matrix(numRows, numCols)
        for r in range(numRows):
            for c in range(numCols):
                tsum = 0
                for t in range(comm):
                    tsum += self[r, t] * rhsMatrix[t, c]
                newMatrix[r, c] = tsum
        return newMatrix

