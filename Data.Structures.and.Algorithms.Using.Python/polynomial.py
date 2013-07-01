class Polynomial:
    """The Polynomial ADT"""
    def __init__(self, degree = None, coef = None):
        if degree is None:
            self._polyHead = None
        else:
            self._polyHead = _PolyTermNode(degree, coef)
        self._polyTail = self._polyHead

    def degree(self):
        if self._polyHead is None:
            return -1
        else:
            return self._polyHead.degree

    def __str__(self):
        """ String representation of the polynomial """
        if self.degree() < 0:
            return "<empty polynomial>"
        else:
            curNode = self._polyHead
            mathsym = ""
            while curNode is not None:
                mathsym += "%dX^%d + " % (curNode.coef, curNode.degree)
                curNode = curNode.next
            mathsym = mathsym[:-2]
            return mathsym

    def __getitem__(self, degree):
        """ Usage: x[n] """
        assert self.degree() >= 0, \
            "Operation not permitted on an empty polynomial."
        curNode = self._polyHead
        while curNode is not None and curNode.degree > degree:
            curNode = curNode.next
        if curNode is not None and curNode.degree == degree:
            return curNode.coef
        else:
            return 0.0

    def evaluate(self, scalar):
        assert self.degree() >= 0, \
            "Only non-empty polynomials can be evaluated."
        result = 0.0
        curNode = self._polyHead
        while curNode is not None:
            result += curNode.coef * (scalar ** curNode.degree)
            curNode = curNode.next
        return result

    def _appendNode(self, degree, coef):
        if coef != 0.0:
            newNode = _PolyTermNode(degree, coef)
            if self._polyHead is None:
                self._polyHead = newNode
            else:
                self._polyTail.next = newNode
            self._polyTail = newNode

    def __setitem__(self, degree, coef):
        prevNode = None
        curNode = self._polyHead
        while curNode is not None and curNode.degree > degree:
            prevNode = curNode
            curNode = curNode.next

        if coef == 0.0: # remove the term
            if curNode is not None and curNode.degree == degree:
                if curNode is self._polyHead:
                    self._polyHead = curNode.next
                else:
                    prevNode.next = curNode.next
                if curNode is self._polyTail:
                    self._polyTail = prevNode
        else:
            if curNode is None:
                self._appendNode(degree, coef)
            elif curNode.degree == degree:
                curNode.coef = coef
            else:
                newNode = _PolyTermNode(degree, coef)
                newNode.next = curNode
                if curNode is self._polyHead:
                    self._polyHead = newNode
                else:
                    prevNode.next = newNode
    def __add__(self, rhsPoly):
        assert self.degree() >= 0 and rhsPoly.degree() >= 0, \
                "Addition only allowed on non-empty polynomials."
        newPoly = Polynomial()
        nodeA = self._polyHead
        nodeB = rhsPoly._polyHead

        while nodeA is not None and nodeB is not None:
            if nodeA.degree > nodeB.degree:
                self._appendNode(nodeA.degree, nodeA.coef)
                nodeA = nodeA.next
            elif nodeA.degree < nodeB.degree:
                self._appendNode(nodeB.degree, nodeB.coef)
                nodeB = nodeB.next
            else:
                self._appendNode(nodeA.degree, nodeA.coef + nodeB.coef)
                nodeA = nodeA.next
                nodeB = nodeB.next

        while nodeA is not None:
            self._appendNode(nodeA.degree, nodeA.coef)
            nodeA = nodeA.next
        while nodeB is not None:
            self._appendNode(nodeB.degree, nodeB.coef)
            nodeB = nodeB.next

        return newPoly

    def __mul__(self, rhsPoly):
        assert self.degree() >= 0 and rhsPoly.degree() >= 0, \
                "Multiplication only allowed on non-empty polynomials."
        newPoly = Polynomial()
        curNode = rhs._polyHead
        while curNode is not None:
            tempPoly = self._termMultiply(curNode)
            newPoly.add(tempPoly)
            curNode = curNode.next
        return newPoly

    def _termMultiply(self, termNode):
        newPoly = Polynomial()
        curNode = self._polyHead
        while curNode is not None:
            newDegree = curNode.degree + termNode.degree
            newCoef = curNode.coef * termNode.coef
            newPoly._appendNode(newDegree, newCoef)
            curNode = curNode.next
        return newPoly

class _PolyTermNode(object):
    def __init__(self, degree, coef):
        self.degree = degree
        self.coef = coef
        self.next = None

pom = Polynomial(5, 3)
pom[2] = 12
pom[8] = 18
pom[4] = 4
pom[6] = 0.0
pom[8] = 0.0
print pom


