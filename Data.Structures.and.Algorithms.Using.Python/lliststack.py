class Stack:
    def __init__(self):
        self._top = None
        self._size = 0
    def __len__(self):
        return self._size
    def isEmpty(self):
        return self._top is None
    def pop(self):
        assert not self.isEmpty(), "Can't pop from an empty stack"
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.item

    def peek(self):
        assert not self.isEmpty(), "Can't peek at an empty stack"
        return self._top.item

    def push(self, item):
        self._top = _StackNode(item, self._top)
        self._size += 1

class _StackNode:
    def __init__(self, item, link):
        self.item = item
        self.next = link
