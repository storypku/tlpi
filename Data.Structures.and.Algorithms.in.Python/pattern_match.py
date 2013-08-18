# ---- Boyer-Moore Algorithm for Pattern Matching ----
def find_boyer_moore(Text, Pattern):
    """Return the lowest index of Text at which substring Pattern begins (or
    else -1). The time complexity is O(mn)."""
    n, m = len(Text), len(Pattern)
    if m == 0:  # trivial search for empty string
        return 0
    last = {}   # build last dictionary
    for k in range(m):
        last[Pattern[k]] = k
    # align end of pattern at index m - 1 of text
    i = m - 1 # an index into Text
    k = m - 1 # an index into Pattern
    while i < n:
        if Text[i] == Pattern[k]:   # a matching character
            if k == 0:
                return i    # pattern begins at index i of text
            else:
                i -= 1      # examine previous character
                k -= 1      # of both Text and Pattern
        else:
            j = last.get(Text[i], -1)  # last(Text[i]) is -1 if not found
            i += m - min(k, j + 1)  # case analysis for jump step, better than
                                    # i += m - (j+1 if j < k else k)
            k = m -1    # restart at end of pattern
    return -1

# ---- Knuth-Morris-Pratt Algorithm for Pattern Matching ----
def compute_kmp_fail(Pattern):
    """Utility that computes and return KMP "fail" list."""
    m = len(Pattern)
    fail = [0] * m  # by default, presume overlap of 0 everywhere
    j = 1
    k = 0
    while j < m:    # compute fail[j] during this pass, if non-zero
        if Pattern[j] == Pattern[k]:    # k + 1 characters match thus far
            fail[j] += 1 + k
            j += 1
            k += 1
        elif k > 0:                     # k follows a matching prefix
            k = fail[k-1]
        else:                           # no match found starting at j
            j += 1
    return fail

def find_kmp(Text, Pattern):
    """Return the lowest index of Text at which substring Pattern begins (or
    else -1). The time complexity is O(n+m)."""
    n, m = len(Text), len(Pattern)
    if m > n:
        return -1
    if m == 0:
        return 0
    fail = compute_kmp_fail(Pattern)    # rely on utility to precompute
    j = 0       # index into Text
    k = 0       # index into Pattern
    while j < n:
        if Text[j] == Pattern[k]:       # Pattern[0:k+1] matched thus far
            if k == m -1:               # match is complete
                return j - m + 1
            j += 1                      # try to extend match
            k += 1
        elif k > 0:
            k = fail[k-1]               # fail list reuse
        else:
            j += 1
    return -1
