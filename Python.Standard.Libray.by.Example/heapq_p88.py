import heapq
from math import floor, log
from cStringIO import StringIO
def show_tree(tree, total_width=48, fill=" "):
    """Pretty print a list-based heap."""
    output = StringIO()
    last_row = -1
    print "-" * total_width
    for i, val in enumerate(tree):
        row = int(log(i+1, 2)) if i else 0
        if row != last_row:
            output.write("\n")
        columns = 2**row
        col_width = total_width // columns
        output.write(str(val).center(col_width, fill))
        last_row = row
    print output.getvalue()
    print "-" * total_width
    return

data = [19, 9, 4, 10, 11, 13, 5, 8, 1, 4, 7, 6, 3, 9, 2]
heapq.heapify(data)
show_tree(data)
