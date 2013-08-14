def quick_sort(S):
    n = len(S)
    inplace_quick_sort(S, 0, n - 1)

def _inplace_quick_sort(S, first, last):
    if first >= last:
        return
    pivot = S[last]
    left = first
    right = last - 1
    while left <= right:
        while left <= right and S[left] < pivot:
            left += 1
        while left <= right and S[right] >= pivot:
            right -= 1
        if left < right:
            S[left], S[right] = S[right], S[left]
            left += 1
            right -= 1

    if left != last:
        S[left], S[last] = S[last], S[left]

    _inplace_quick_sort(S, first, left-1)
    _inplace_quick_sort(S, left+1, last)

from linked_queue import LinkedQueue

def quick_sort_queue(S):
    """Sort the elements of queue S using the quick-sort algorithm."""
    n = len(S)
    if n < 2:
        return
    Lt  = LinkedQueue()
    Eq  = LinkedQueue()
    Gt  = LinkedQueue()
    pivot = S.dequeue()
    Eq.enqueue(pivot)
    while not S.is_empty():
        val = S.dequeue()
        if val < pivot:
            Lt.enqueue(val)
        elif val > pivot:
            Gt.enqueue(val)
        else:
            Eq.enqueue(val)
    quick_sort_queue(Lt)
    quick_sort_queue(Gt)
    while not Lt.is_empty():
        S.enqueue(Lt.dequeue())
    while not Eq.is_empty():
        S.enqueue(Eq.dequeue())
    while not Gt.is_empty():
        S.enqueue(Gt.dequeue())
