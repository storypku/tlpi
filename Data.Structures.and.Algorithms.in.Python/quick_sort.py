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
