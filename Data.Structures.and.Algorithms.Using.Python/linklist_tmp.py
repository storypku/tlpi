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

def prepend(head, data):
    newNode = ListNode(data)
    newNode.next = head
    head = newNode

def remove(head, target):
    prevNode = None
    curNode = head
    while curNode is not None and curNode.data != target:
        prevNode = curNode
        curNode = curNode.next
    if curNode is not None:
        if curNode is head:
            head = curNode.next
        else:
            prevNode.next = curNode.next

def sortedSearch(head, target):
    curNode = head
    while curNode is not None and curNode.data < target:
        curNode = curNode.next
    if curNode is not None and curNode.data == target:
        return True
    else:
        return False


