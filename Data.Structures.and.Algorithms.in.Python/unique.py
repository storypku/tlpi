def unique(S, start, stop):
    """Return True if there are no duplicate elements in slice
    S[start:stop]."""

    if stop - start <= 1: # at most one element
        return True
    for i in range(start+1, stop):
        if S[start] == S[i]: return False
    return unique(S, start+1, stop)

def reverse(S, start, stop):
    """Reverse elements in implicit slice S[start:stop]."""
    if start < stop - 1:
        S[start], S[stop-1] = S[stop-1], S[start]   # swap first and last
        reverse(S, start+1, stop-1)

def reverse_iterative(S):
    """Reverse elements in sequence S."""
    start, stop = 0, len(S)
    while start < stop -1:
        S[start], S[stop-1] = S[stop-1], S[start]   # swap first and last
        start, stop = start + 1, stop -1

def bad_fibonacci(n):
    """Return the n-th Fibonacci number."""
    if n<= 1:
        return n
    else
        return bad_fibonacci(n-2) + bad_fibonacci(n-1)

def good_fibonacci(n):
    """Return pair of Fibonacci numbers, F(n) and F(n-1)."""
    if n <= 1:
        return (n, 0)
    else:
        (a, b) = good_fibonacci(n-1)
        return (a+b, a)


