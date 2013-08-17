import random
def quick_select(S, k):
    """Return the k-th smallest element of list S, for k from 1 to len(S)."""
    if len(S) == 1:
        return S[0]
    pivot = random.choice(S)
    LT = [ x for x in S if x < pivot]
    EQ = [ x for x in S if x == pivot ]
    GT = [ x for x in S if x > pivot]
    if k <= len(LT):
        return quick_select(LT, k)
    elif k <= len(LT) + len(EQ):
        return pivot
    else:
        j = k - len(LT) - len(EQ)
        return quick_select(GT, j)
