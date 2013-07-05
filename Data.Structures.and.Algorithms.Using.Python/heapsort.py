""" Heap Sort algorithm in max-heap """
def _siftUp(theSeq, ndx):
    if ndx > 0:
        parent = (ndx -1) // 2
        if theSeq[ndx] > theSeq[parent]:
            theSeq[ndx], theSeq[parent] = theSeq[parent], theSeq[ndx]
            _siftUp(theSeq, parent)

def _siftDown(theSeq, count, ndx):
    left = 2 * ndx + 1
    right = 2 * ndx + 2
    largest = ndx
    if left < count and theSeq[left] > theSeq[largest]:
        largest = left
    if right < count and theSeq[right] > theSeq[largest]:
        largest = right
    if largest != ndx:
        theSeq[ndx], theSeq[largest] = theSeq[largest], theSeq[ndx]
        _siftDown(theSeq, count, largest)

def heapsort(theSeq):
    n = len(theSeq)
    for i in range(n):
        _siftUp(theSeq, i)

    for j in range(n-1, 0, -1):
        theSeq[j], theSeq[0] = theSeq[0], theSeq[j] # Pythonic swap
        _siftDown(theSeq, j, 0)

if __name__ == "__main__":
    theSeq = [10, 51, 2, 18, 4, 31, 13, 5, 23, 64, 29]
    for item in theSeq:
        print item,
    print
    print "=== After sort, ==="
    heapsort(theSeq)
    for item in theSeq:
        print item,
    print
