def quickSort(theSeq):
    """sorts an array or list using the recursive quick sort algorithm."""
    n = len(theSeq)
    recQuickSort(theSeq, 0, n-1)

# The recursive implementation using virtual segments.
def recQuickSort(theSeq, first, last):
    # Check the base case
    if first >= last:
        return
    else:
        # Partition the sequence and obtain the pivot position
        pos = partionSeq(theSeq, first, last)

        # Repeat the process on the two subsequences.
        recQuickSort(theSeq, first, pos-1)
        recQuickSort(theSeq, pos+1, last)

# Partitions the subsequence using the first key as the pivot
def partionSeq(theSeq, first, last):
    # Save a copy of the pivot value
    pivot = theSeq[first]

    # Find the pivot postion and move the elements around the pivot
    left = first + 1
    right = last
    while left <= right:
        # Find the first key larger than the pivot
        while left < right and theSeq[left] < pivot:
            left += 1
        # Find the last key in the sequence smaller than the pivot
        while right >= left and theSeq[right] >= pivot:
            right -= 1

        # Swap the two keys if we have not completed this partition
        if left < right:
            tmp = theSeq[left]
            theSeq[left] = theSeq[right]
            theSeq[right] = tmp

    # Put the pivot in the proper position
    if right != first:
        theSeq[first] = theSeq[right]
        theSeq[right] = pivot

    # Return the index postion of the pivot value
    return right

