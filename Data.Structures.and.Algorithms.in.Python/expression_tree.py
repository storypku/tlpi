from linked_binary_tree import LinkedBinaryTree

class ExpressionTree(LinkedBinaryTree):
    """An arithmetic expression tree."""

    def __init__(self, token, left=None, right=None):
        """Create an expression tree.

        In a single parameter form, token should be a leaf value (e.g., '42'),
        and the expression tree will have that value at an isolated node.

        In a tree-parameter version, token should be an operator, and left and
        right should be existing ExpressionTree instances that become the
        operands for the binary operator.
        """
        super().__init__()  # LinkedBinaryTree initialization
        if not isinstance(token, str):
            raise TypeError("Token must be a string.")
        self._add_root(token)
        if left is not None:
            if token not in "+-x*/":
                raise ValueError("Token must be valid operator.")
            self._attach(self.root(), left, right)

    def __str__(self):
        """Return string representation of the expression."""
        pieces = []
        self._parenthesize_recur(self.root(), pieces)
        return "".join(pieces)

    def _parenthesize_recur(self, pos, result):
        """Append piecewise representation of pos's subtree to resulting
        list."""
        if self.is_leaf(pos):
            result.append(str(pos.element()))
        else:
            result.append("(")
            self._parenthesize_recur(self.left(pos), result)
            result.append(pos.element())
            self._parenthesize_recur(self.right(pos), result)
            result.append(")")

    def evaluate(self):
        """Return the numberic result of the expression."""
        return self._evaluate_recur(self.root())

    def _evaluate_recur(self, pos):
        """Return the numberic result of subtree rooted at pos."""
        if self.is_leaf(pos):
            return float(pos.element())
        else:
            op = pos.element()
            left_val = self._evaluate_recur(self.left(pos))
            right_val = self._evaluate_recur(self.right(pos))
            if op == "+": return left_val + right_val
            elif op == "-": return left_val - right_val
            elif op == "/": return left_val / right_val
            else: return left_val * right_val

def build_expression_tree(tokens):
    """Return an ExpressionTree based upon by a tokenized expression."""
    S = []
    for tok in tokens:
        if tok in "+-*x/":
            S.append(tok)
        elif tok not in "( )":
            S.append(ExpressionTree(tok))
        elif tok == ")":
            right = S.pop()
            op = S.pop()
            left = S.pop()
            S.append(ExpressionTree(op, left, right))
            # ignore a left parenthesis and a blank space.
    return S.pop()
