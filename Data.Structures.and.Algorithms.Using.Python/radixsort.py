"""sorts a sequence of positive integers using the radix sort algorithm"""
from llistqueue import Queue
from array_m import Array

def radixSort(uintList, numDigits):
    # Create an array of queues to reprents the bins
    binArray = Array(10)
    for k in range(10):
        binArray[k] = Queue()
    # The value of the current column
    column = 1

    # Iterate over the number of digits in the largest value
    for d in range(numDigits):

        # Distribute the keys across the 10 bins
        for key in uintList:
           digit = (key // column) % 10
           binArray[digit].enqueue(key)

        # Gather the keys from the bins and places them back in intList
        i = 0
        for binc in binArray:
            while not bin.isEmpty():
                key = binc.dequeue()
                uintList[i] = key
                i += 1
        # Advance to the next column value
        column *= 10

