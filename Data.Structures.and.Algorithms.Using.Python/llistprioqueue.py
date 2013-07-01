class PriorityQueue:
    """ the unbounded priority queue class """
    def __init__(self):
        self._qhead = None
        self._qtail = None
        self._count = 0

    def isEmpty(self):
        return self._count == 0

    def __len__(self):
        return self._count

    def enqueue(self, item, priority):
        destNode = _PriorityQueueNode(item, priority)
        if self.isEmpty():
            self._qhead = destNode
        else:
            self._qtail.next = destNode
        self._qtail = node
        self._count += 1

    def dequeue(self):
        assert not self.isEmpty(), "Can't dequeue from an empty queue."
        if self._qhead is self._qtail: # Only one item in queue
            destNode = self._qhead
            self._qhead = None
            self._qtail = None
        else:   # More than one item in queue
            destNode = self._qhead
            destPrevNode = None
            curNode = self._qhead
            prevNode = None
            while curNode is not None:
                if curNode.priority <  destNode.priority:
                    destNode = curNode
                    destPrevNode = prevNode
                prevNode = curNode
                curNode = curNode.next
            if destNode is self._qhead:
                self._qhead = self._qhead.next
            else:
                destPrevNode.next = destNode.next
                if destNode is self._qtail:
                    self._qtail = destPrevNode
        self._count -= 1
        return destNode.item

class _PriorityQueueNode(object):
    """ storage class for unbounded priority queue """
    def __init__(self, item, priority):
        self.item = item
        self.priority = priority
        self.next = None

