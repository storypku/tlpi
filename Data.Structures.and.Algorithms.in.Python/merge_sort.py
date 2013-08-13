from linked_queue import LinkedQueue
def merge_list(S1, S2, S):
    """Merge two sorted Python list S1 and S2 into properly sized list S."""
    i = j = 0
    while i + j < len(S):
        if j==len(S2) or (i < len(S1) and S1[i] < S2[j]):
            S[i+j] = S1[i]
            i += 1
        else:
            S[i+j] = S2[j]
            j += 1

def merge_sort_list(S):
    """Sort the elements of Python list S using the merge-sort algorithm."""
    n = len(S)
    if n < 2:
        return
    mid = n // 2
    S1 = S[0:mid]
    S2 = S[mid:n]
    merge_sort_list(S1)
    merge_sort_list(S2)
    merge_list(S1, S2, S)

def merge_queue(S1, S2, S):
    """Merge two sorted queue instances S1 and S2 into empty queue S."""
    while not S1.is_empty() and not S2.is_empty():
        if S1.first() < S2.first():
            S.enqueue(S1.dequeue())
        else:
            S.enqueue(S2.dequeue())
    while not S1.is_empty():
        S.enqueue(S1.dequeue())
    while not S2.is_empty():
        S.enqueue(S2.dequeue())

def merge_sort_queue(S):
    """Sort the elements of queue S using the merge-sort algorithm."""
    n = len(S)
    if n < 2:
        return
    S1 = LinkedQueue()
    S2 = LinkedQueue()
    while len(S1) < n // 2:
        S1.enqueue(S.dequeue())
    while not S.is_empty():
        S2.enqueue(S.dequeue())
    merge_sort_queue(S1)
    merge_sort_queue(S2)
    merge_queue(S1, S2, S)

def merge_nonrecur(src, result, start, inc):
    """Merge src[start:start+inc] and src[start+inc:start+2*inc] into
    result."""
    end1 = start + inc
    end2 = min(start+2*inc, len(src))
    x, y, z = start, start + inc, start
    while x < end1 and y < end2:
        if src[x] < src[y]:
            result[z] = src[x]; x += 1
        else:
            result[z] = src[y]; y += 1
        z += 1
    if x < end1:
        result[z:end2] = src[x:end1]
    elif y < end2:
        result[z:end2] = src[y:end2]

def merge_sort_nonrecur(S):
    """Sort the elements of Python list S using the merge sort algorithm."""
    from math import log, ceil
    n = len(S)
    if n < 2:
        return
    logn = ceil(log(n, 2))
    src, dest = S, [None]*n
    for i in (2**k for k in range(logn)):
        for j in range(0, n, 2*i):
            merge_nonrecur(src, dest, j, i)
        src, dest = dest, src
    if S is not src:
        S[0:n] = src[0:n]
