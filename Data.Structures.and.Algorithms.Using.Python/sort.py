def bubbleSort(theSeq): # ascending order
    n = len(theSeq)
    for i in range(n-1):
        for j in range(n-1-i):
            if theSeq[j] > theSeq[j+1]:
                tmp = theSeq[j]
                theSeq[j] = theSeq[j+1]
                theSeq[j+1] = tmp

def selectionSort(theSeq):
    n = len(theSeq)
    for i in range(n-1):
        smallIdx = i
        for j in range(i+1, n):
            if theSeq[j] < theSeq[smallIdx]:
                smallIdx = j
        if smallIdx != i:
            tmp = theSeq[i]
            theSeq[i] = theSeq[smallIdx]
            theSeq[smallIdx] = tmp

def insertionSort(theSeq):
    n = len(theSeq)
    for i in range(1, n):
        value = theSeq[i]
        pos = i
        while pos > 0 and value < theSeq[pos - 1]:
            theSeq[pos]=theSeq[pos-1]
            pos -= 1
        theSeq[pos] = value
