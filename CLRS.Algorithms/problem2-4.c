/*
 * Problem 2-4  Inversions
 * Let A[1...n] be an array of n distinct numbers. If i < j and A[i] > A[j],
 * then the pair (i,j) is called an inversion of A.
 *
 * Give an algorithm that determines the number of inversions in any permu-
 * tation on n elements in THETA(nlogn) worst-case time. (Hint: Modify merge
 * sort.)
 *
 * Initially, INVERSION-NUMBER(A, 1, n) was called.
 *
 */
INVERSION-NUMBER(A, p, r) //A[p...r]
    if p >= r
        return 0
    else
        q = floor((p+r)/2)
        return INVERSION-NUMBER(A, p, q) + 
               INVERSION-NUMBER(A, q + 1, r) +
               INVERSION-NUMBER-MERGE(A, p, q, r)

INVERSION-NUMBER-MERGE(A, p, q, r)
    count = 0
    n1 = q - p + 1
    n2 = r - q
    Let L[1...n1+1] and R[1...n2+1] be new arrays
    for i = 1 to n1
        L[i] = A[p + i - 1]
    for j = 1 to n2
        R[j] = A[q + j]
    L[n1 + 1] = +inf    //inf: infinite, servers as sentinel value
    R[n2 + 1] = +inf
    i = 1
    j = 1
    for k = p to r
        if L[i] < R[j]
        // Note: As the elements of array A are distinct,
        //       there exists no equal elements.
            A[k] = L[i]
            i = i + 1
        else
            count = count + n1 - i + 1
            A[k] = R[j]
            j = j + 1

    return count

