import ctypes
class Array:
    def __init__(self, size):
        assert size > 0, "Array size must be > 0"
        self._size = size
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        self.clear(None)

    def __len__(self):
        return self._size
    def __getitem__(self, index):
        assert index >= 0 and index < len(self), \
                "Array subscription out of range"
        return self._elements[index]
    def __setitem__(self, index, value):
        assert index >= 0 and index < len(self), \
                "Array subscription out of range"
        self._elements[index] = value
    def clear(self, value):
        for i in range(len(self)):
            self._elements[i] = value
    def __iter__(self):
        return _ArrayIterator(self._elements)

class _ArrayIterator:
    def __init__(self, theArray):
        self._arrayRef = theArray
        self._curNdx = 0
    def __iter__(self):
        return self
    def next(self):
        if self._curNdx < len(self._arrayRef):
            entry = self._arrayRef[self._curNdx]
            self._curNdx += 1
            return entry
        else:
            raise StopIteration

class Array2D :
    def __init__( self, numRows, numCols ):
        self._theRows = Array( numRows )
        for i in range( numRows ) :
            self._theRows[i] = Array( numCols )

    def numRows( self ):
            return len( self._theRows )

    def numCols( self ):
        return len( self._theRows[0] )

    def clear( self, value ):
        for row in self._theRows:
            row.clear( value )

    def __getitem__( self, ndxTuple ):
        assert len(ndxTuple) == 2, "Invalid number of array subscripts."
        row = ndxTuple[0]
        col = ndxTuple[1]
        assert row >= 0 and row < self.numRows() \
            and col >= 0 and col < self.numCols(), \
                "Array subscript out of range."
        the1dArray = self._theRows[row]
        return the1dArray[col]

    def __setitem__( self, ndxTuple, value ):
        assert len(ndxTuple) == 2, "Invalid number of array subscripts."
        row = ndxTuple[0]
        col = ndxTuple[1]
        assert row >= 0 and row < self.numRows() \
            and col >= 0 and col < self.numCols(), \
                "Array subscript out of range."
        the1dArray = self._theRows[row]
        the1dArray[col] = value

    def set( self, row, col, value ):
        self.__setitem__((row, col), value)

class MultiArray:
    def __init__(self, *dimensions):
        assert len(dimensions) > 1, "the array must have 2 or more dimensions."
        self._dims = dimensions
        size = 1
        for d in dimensions:
            assert d > 0, "Dimensions must be > 0."
            size *= d
        self._elements = Array(size)
        self._factors = Array(len(dimensions))
        self._computeFactors()

    def numDims(self):
        return len(self._dims)

    def len(self, dim):
        assert dim >= 1 and dim <= self.numDims(), "Dimension component out of range."
        return self._dims[ dim - 1 ]

    def clear(self, value):
        self._elements.clear(value)

    def __getitem__(self, ndxTuple):
        assert len(ndxTuple) == self.numDims(), "Invalid # of array subscripts"
        index = self._computeIndex(ndxTuple)
        assert index is not None, "Array subscript out of range"
        return self._elements[index]

    def __setitem__(self, ndxTuple, value):
        assert len(ndxTuple) == self.numDims(), "Invalid # of array subscripts"
        index = self._computeIndex(ndxTuple)
        assert index is not None, "Array subscript out of range"
        self._elements[index] = value

    def _computeIndex(self, idx):
        offset = 0
        for j in range(len(idx)):
            if idx[j] < 0 or idx[j] >= self._dims[j]:
                return None
            else:
                offset += idx[j] * self._factors[j]
        return offset

    def _computeFactors(self):
        self._factors.clear(1)
        for i in range(self.numDims()):
            for j in range(i+1, self.numDims()):
                self._factors[i] *= self._dims[j]

