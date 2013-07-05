from llistqueue import Queue
class ExpressionTree:
    """ Expression Tree Class with assuming the following constraints:
        (1) The expression is stored in string with no white space
        (2) The supplied expression is valid and fully parenthesized
        (3) each operand will be a single-digit or single-letter variable
        (4) the operators will consist of +, -, *, /, and %. """

    def __init__(self, expStr):
        """build an expression tree for the expression string"""
        self._expTree = None
        self._buildTree(expStr)

    def evaluate(self, varMap):
        return self._evalTree(self._expTree, varMap)

    def __str__(self):
        return self._buildString(self._expTree)

    def _buildTree(self, expStr):
        expQ = Queue()
        for token in expStr:
            expQ.enqueue(token)
        # Create an empty root node
        self._expTree = _ExpTreeNode(None)
        # Call the recursive function to build the expression tree
        self._recBuildTree(self._expTree, expQ)

    def _recBuildTree(self, curNode, expQ):
        token = expQ.dequeue()

        if token == '(':
            curNode.left = _ExpTreeNode(None)
            self._recBuildTree(curNode.left, expQ)

            # The next token will be an operator: +-*/%
            curNode.element = expQ.dequeue()

            curNode.right = _ExpTreeNode(None)
            self._recBuildTree(curNode.right, expQ)

            # The next token will be ')', remove it
            expQ.dequeue()
        else:
            curNode.element = token

    def _buildString(self, treeNode):
        """ Recursively builds a string repr of the expression tree"""

        # Leaf node indicates an operand
        if treeNode.left is None and treeNode.right is None:
            return str(treeNode.element)
        else:   # Otherwise, an operator
            expStr = '('
            expStr += self._buildString(treeNode.left)
            expStr += str(treeNode.element)
            expStr += self._buildString(treeNode.right)
            expStr += ')'
            return expStr

    def _evalTree(self, subTree, varDict):
        if subTree.left is None and subTree.right is None:
            if subTree.element >= '0' and subTree.element <= '9':
                return int(subTree.element)
            else:
                assert subTree.element in varDict, "Invalid variable"
                return varDict[subTree.element]
        else:
            lvalue = self._evalTree(subTree.left, varDict)
            rvalue = self._evalTree(subTree.right, varDict)
            return self._computeOp(lvalue, subTree.element, rvalue)

    def _computeOp(self, lvalue, op, rvalue):
        """ Compute the arithmetic expr: lvalue op rvalue (op in "+-*/%") """
        if op == '+':
            return lvalue + rvalue
        elif op == '-':
            return lvalue - rvalue
        elif op == '*':
            return lvalue * rvalue
        elif op == '/':
            assert rvalue != 0, "integer division or modulo by zero"
            return lvalue / rvalue
        else:       # op == '%':
            assert rvalue != 0, "integer division or modulo by zero"
            return lvalue % rvalue

class _ExpTreeNode:
    def __init__(self, data):
        self.element = data
        self.left = None
        self.right = None

if __name__ == "__main__":
    exptree = ExpressionTree("((8+3)*(b/(a-1)))")
    vardict = {'a':3, 'b': 4}
    print exptree.evaluate(vardict)
