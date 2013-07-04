class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

def traversal(head):
    curNode = head
    while curNode is not None:
        print curNode.data
        curNode = curNode.next

def unorderedSearch(head, target):
    curNode = head
    while curNode is not None and curNode.data != target:
        curNode = curNode.next
    return curNode is not None

def sortedSearch(head, target):
    curNode = head
    while curNode is not None and curNode.data < target:
        curNode = curNode.next
    if curNode is not None and curNode.data == target:
        return True
    else:
        return False

def llistMergeSort(theList):
    # If the list is empty or only contains one node(base case), return None
    if theList is None or theList.next is None:
        return theList
    # Split the linked list into two sublists of equal size
    rightList = _splitLinedList(theList)
    leftList = theList

    # Perform the same operation on the left half ...
    leftList = llistMergeSort(leftList)

    # ... and the right half
    rightList = llistMergeSort(rightList)

    # Merge the two ordered sublists
    theList = _mergeLinkedList(leftList, rightList)

    # Returns the head pointer of the ordered list
    return theList

def _splitLinedList(subList):

    # Assign a reference to the first and second nodes in the list
    midPoint = subList
    curNode = subList.next

    while curNode is not None:
        curNode = curNode.next

        if curNode is not None:
            midPoint = midPoint.next
            curNode = curNode.next
    rightList = midPoint.next
    midPoint.next = None
    return rightList

def _mergeLinkedList(subListA, subListB):
    newList = ListNode(None)
    newTail = newList

    while subListA is not None and subListB is not None:
        if subListA.data <= subListB.data:
            newTail.next = subListA
            subListA = subListA.next
        else:
            newTail.next = subListB
            subListB = subListB.next
        newTail = newTail.next
        newTail.next = None

    if subListA is not None:
        newTail.next = subListA
    else:
        newTail.next = subListB

    return newList.next

def test():
    head = ListNode(3)
    tail = head
    for num in [12, 13, 5, 8, 0]:
        newNode = ListNode(num)
        tail.next = newNode
        tail = newNode
    sortedList = llistMergeSort(head)
    traversal(sortedList)

if __name__ == "__main__":
    test()
