class SparseMatrix:
    def __init__(self, numRows, numCols):
        assert numRows > 0 and numCols > 0, \
                "Each dimension of Sparse Matrix must be > 0."
        self._numRows = numRows
        self._numCols = numCols
        self._elemList = list()

    def numRows(self):
        return self._numRows

    def numCols(self):
        return self._numCols

    def __getitem__(self, ndxTuple):
        assert len(ndxTuple) == 2, "Invalid number of matrix subscripts"
        row = ndxTuple[0]
        col = ndxTuple[1]
        assert row >= 0 and row < self.numRows() and \
               col >= 0 and col < self.numCols(), \
                "Matrix subscript out of range."
        ndx = self._findPosition(row, col)
        if ndx is not None:
            return self._elemList[ndx].value
        else:
            return 0.0
    def __setitem__(self, ndxTuple, scalar):
        assert len(ndxTuple) == 2, "Invalid number of matrix subscripts"
        row = ndxTuple[0]
        col = ndxTuple[1]
        assert row >= 0 and row < self.numRows() and \
               col >= 0 and col < self.numCols(), \
                "Matrix subscript out of range."
        ndx = self._findPosition(row, col)
        if ndx is not None:
            if scalar != 0.0:
                self._elemList[ndx].value = scalar
            else:
                self._elemList.pop(ndx)
        else:
            if scalar != 0.0:
                element = _MatrixElement(row, col, scalar)
                self._elemList.append(element)

    def scaleBy(self, scalar):
        for element in self._elemList:
            element.value *= scalar

    def __add__(self, rhsMatrix):
        assert rhsMatrix.numRows() == self.numRows() and \
               rhsMatrix.numCols() == self.numCols(), \
               "Matrix sizes not compatible for the add operation."
        newMatrix = SparseMatrix( self.numRows(), self.numCols() )
        for element in self._elemList :
            dupElement = _MatrixElement(element.row, element.col, element.value)
            newMatrix._elemList.append( dupElement )
        for element in rhsMatrix._elemList :
            newMatrix[ element.row, element.col ] += element.value
        return newMatrix

    def __sub__(self, rhsMatrix):
        assert rhsMatrix.numRows() == self.numRows() and \
               rhsMatrix.numCols() == self.numCols(), \
               "Matrix sizes not compatible for the add operation."
        newMatrix = SparseMatrix( self.numRows(), self.numCols() )
        for element in self._elemList :
            dupElement = _MatrixElement(element.row, element.col, element.value)
            newMatrix._elemList.append( dupElement )
        for element in rhsMatrix._elemList :
            newMatrix[ element.row, element.col ] -= element.value
        return newMatrix

    def __mul__(self, rhsMatrix):
        assert rhsMatrix.numRows() == self.numCols(), \
                "Matrix sizes not compatible for the multiply operation!"
        numRows = self.numRows()
        numCols = self.numCols()
        newMatrix = SparseMatrix(numRows, numCols)
        for elem in self._elemList:
            for relem in rhsMatrix._elemList:
                if elem.col == relem.row:
                    product = elem.value * relem.value
                    newMatrix[elem.row, relem.col] += product
        return newMatrix

    def _findPosition(self, row, col):
        n = len(self._elemList)
        for i in range(n):
            if row == self._elemList[i].row and \
               col == self._elemList[i].col:
                return i
        return None


class _MatrixElement:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
