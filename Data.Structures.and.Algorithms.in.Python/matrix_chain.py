def matrix_chain(d):    # P.594-596 on matrix chain product
    """d is a list of n+1 numbers such that size of k-th matrix is d[k]-by-
    d[k+1].

    Return an n-by-n table such that N[i][j] represents the minimum number of
    multiplications needed to compute the product of Ai through Aj inclusive.
    """
    n = len(d) - 1  # number of matrices
    N = [[0] * n for _ in range(n)]
    for b in range(1, n):
        for i in range(n-b):
            j = i + b
            N[i][j] = min(N[i][k] + N[k+1][j] + d[i]*d[k+1]*d[j+1] \
                    for k in range(i, j))
    return N

