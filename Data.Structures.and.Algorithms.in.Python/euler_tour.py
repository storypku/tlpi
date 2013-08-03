class EulerTour:
    """Abstract base class for performing Euler tour of a tree."""

    def __init__(self, tree):
        """Prepare an Euler tour template for the given tree."""
        self._tree = tree

    def tree(self):
        """Return reference to the tree being traversed."""
        return self._tree

    def execute(self):
        """Perform the tour and return any result from post visit of root."""
        if len(self._tree) > 0:
            return self._tour(self._tree.root(), 0, [])

    def _tour(self, pos, d, path):
        """Perform tour of subtree rooted at Position pos.

        pos     Position of current node being visited
        d       depth of pos in the tree
        path    list of indices of children on path from root to pos
        """
        self._hook_previsit(pos, d, path)   # pre visit pos
        results = []
        path.append(0)
        for child in self._tree.children(pos):
            results.append(self._tour(child, d+1, path))
            path[-1] += 1
        path.pop()
        answer = self._hook_postvisit(pos, d, path, results)
        return answer

    def _hook_previsit(self, pos, d, path): # can be overriden
        pass

    def _hook_postvisit(self, pos, d, path, results): #can be overriden
        pass

class PreorderPrintIndentedTour(EulerTour):
    """A subclass of EulerTour that produces an indented preorder list of a
    tree's elements."""

    def _hook_previsit(self, pos, d, path):
        print(2*d*" " + str(pos.element()))

class PreorderPrintIndentedLabeledTour(EulerTour):
    """A subclass of EulerTour that produces a labeled and indented, preorder
    list of a tree's elements."""

    def _hook_previsit(self, pos, d, path):
        label = ".".join(str(j+1) for j in path)
        print (2*d*" " + label, str(pos.element()))

class ParenthesizeTour(EulerTour):
    """A subclass of EulerTour that prints a parenthetic string representation
    of a tree."""

    def _hook_previsit(self, pos, d, path):
        if path and path[-1] > 0:           # pos follows a sibling
            print(", ", end="")             # so preface with comma
        print (str(pos.element()), end="")  # then print element
        if not self.tree().is_leaf(pos):    # if pos has children
            print(" (", end="")             # print opening parenthesis

    def _hook_postvisit(self, pos, d, path, results):
        if not self.tree().is_leaf(pos):    # if pos has children
            print (")", end="")             # print closing parenthesis

class BinaryEulerTour(EulerTour):
    """Abstract base class for performing Euler tour of a binary tree.

    This version includes an additional _hook_invisit that is called after the
    tour of the left subtree (if any), yet before the tour of the right
    subtree (if any)."""

    # Note: Right child is always assigned index 1 in path, even if no left
    # siblings.
    def _tour(self, pos, d, path):
        results = [None, None]
        self._hook_previsit(pos, d, path)       # pre visit for pos
        if self.tree().left(pos) is not None:
            path.append(0)
            results[0] = self._tour(self.tree().left(pos), d+1, path)
            path.pop()
        self._hook_invisit(pos, d, path)        # in visit for pos
        if self.tree().right(pos) is not None:
            path.append(1)
            results[1] = self._tour(self.tree().right(pos), d+1, path)
            path.pop()
        answer = self._hook_postvisit(pos, d, path, results) # post visit pos
        return answer

    def _hook_invisit(self, pos, d, path): # can be overriden
        pass
