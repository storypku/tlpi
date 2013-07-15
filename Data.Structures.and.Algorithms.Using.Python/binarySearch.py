def binarySearch( theValues, target ) :
    """binary search the sorted nondescreasing sequence for target."""
    # Start with the entire sequence of elements.
    low = 0
    high = len(theValues) - 1
    # Repeatedly subdivide the sequence in half until the target is found.
    while low <= high :
        mid = (high + low) // 2
        if theValues[mid] == target :
            return mid
        elif target < theValues[mid] :
            high = mid - 1
        else :
            low = mid + 1
    # If the sequence cannot be subdivided further, we're done.
    return -1
