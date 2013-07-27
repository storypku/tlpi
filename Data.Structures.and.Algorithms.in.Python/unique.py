def uniq(S, start, stop):
    """Return True if there are no duplicate elements in slice
    S[start:stop]."""

    if stop - start <= 1: # at most one element
        return True
    for i in range(start+1, stop):
        if S[start] == S[i]: return False
    return uniq(S, start+1, stop)

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


