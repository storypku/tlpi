class Stack:
    def __init__(self):
        self._theItems = list()
    def __len__(self):
        return len(self._theItems)
    def isEmpty(self):
        return self.len() == 0
    def peek(self):
        assert not self.isEmpty(), "Can't peek at an empty stack"
        return self._theItems[-1]
    def pop(self):
        assert not self.isEmpty, "Can't pop from an empty stack"
        return self._theItems.pop()
    def push(self, item):
        self._theItems.append(item)
