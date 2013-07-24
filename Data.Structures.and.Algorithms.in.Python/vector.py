class Vector:
    """Reprent a vector in a multidimentional space."""

    def __init__(self, dim):
        """Create d-dimensional vector of zeros."""
        if not dim > 0:
            raise ValueError("Positive dimensions required.")
        self._coords = [0] * dim

    def __len__(self):
        """Return the dimension of the vector."""
        return len(self._coords)

    def __getitem__(self, index):
        """Return index-th coordinate of vector."""
        return self._coords[index]

    def __setitem__(self, index, value):
        """Set index-th coordinate to the given value."""
        self._coords[index] = value

    def __add__(self, rhs):
        """Return sum of two vectors."""
        if len(self) != len(rhs):
            raise ValueError("Dimensions must agree.")
        result = Vector(len(self))
        for index in range(len(self)):
            result[index] = self[index] + rhs[index]
        return result

    def __radd__(self, lhs):
        """Return sum of two vectors."""
        return self.__add__(lhs)

    def __eq__(self, rhs):
        """Return True if vector has the same coordinates as rhs."""
        if len(self) != len(rhs):
            return False
        else:
            for index in range(len(self)):
                if self[index] != rhs[index]:
                    return False
            return True

    def __ne__(self, rhs):
        """Return True if vector differs from rhs."""
        return not self == rhs

    def __str__(self):
        """Produce string representation of vector."""
        return '<' + str(self._coords)[1:-1] + '>'


