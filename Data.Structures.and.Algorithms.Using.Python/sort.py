def bubbleSort(theSeq): # ascending order
    n = len(theSeq)
    for i in range(n-1):
        for j in range(n-1-i):
            if theSeq[j] > theSeq[j+1]:
                tmp = theSeq[j]
                theSeq[j] = theSeq[j+1]
                theSeq[j+1] = tmp

def selectionSort(theSeq):
    n = len(theSeq)
    for i in range(n-1):
        smallIdx = i
        for j in range(i+1, n):
            if theSeq[j] < theSeq[smallIdx]:
                smallIdx = j
        if smallIdx != i:
            tmp = theSeq[i]
            theSeq[i] = theSeq[smallIdx]
            theSeq[smallIdx] = tmp

def insertionSort(theSeq):
    n = len(theSeq)
    for i in range(1, n):
        value = theSeq[i]
        pos = i
        while pos > 0 and value < theSeq[pos - 1]:
            theSeq[pos]=theSeq[pos-1]
            pos -= 1
        theSeq[pos] = value

def mergeVirtualSeq(theSeq, left, right, end, tmpArray):
    # Merges the two sorted virtual sequences: [left...right) [right, end)
    # using the tmpArray for intermediate storage.
    a = left
    b = right
    m = 0
    while a < right and b < end:
        if theSeq[a] < theSeq[b]:
            tmpArray[m] = theSeq[a]
            a += 1
        else:
            tmpArray[m] = theSeq[b]
            b += 1
        m += 1
    while a < right:
        tmpArray[m] = theSeq[a]
        a += 1
        m += 1
    while b < end:
        tmpArray[m] = theSeq[b]
        b += 1
        m += 1
    # Copy the sorted subsequence back into the original sequence structure
    for i in range(end - left):
        theSeq[i+left] = tmpArray[i]

def recMergeSort(theSeq, first, last, tmpArray):
    # The elements that comprise the virtual subsequence are indicated
    # by the range [first, last]. tmpArray is temporary storage used in
    # the merging phase of the merge sort algorithms.

    # Compute the base case: the virtual sequence contains a single item
    if first == last:
        return
    else:
        mid = (first + last) // 2

        # Split the sequence and perform the recursive step.
        recMergeSort(theSeq, first, mid, tmpArray)
        recMergeSort(theSeq, mid+1, last, tmpArray)

        # Merge the two ordered subsequences.
        mergeVirtualSeq(theSeq, first, mid+1, last+1, tmpArray)


def mergeSort(theSeq):  # O(nlogn)
    """ Sort an array or list in ascending order using merge sort. """
    from array_m import Array
    n = len(theSeq)
    # Create a temporary array for use when merging subsequences
    tmpArray = Array(n)
    recMergeSort(theSeq, 0, n-1, tmpArray)

