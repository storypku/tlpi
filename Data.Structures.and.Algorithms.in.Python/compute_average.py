from time import time
def compute_average(n):
    """Perform n appends to an empty list and return average time elapsed."""
    data = []
    start = time()
    for k in range(n):
        data.append(None)
    end = time()
    return (end-start)/n

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 or sys.argv[1] == "--help":
        print("Usage: {0} number-of-times".format(sys.argv[0]))
        raise SystemExit
    n = int(sys.argv[1])
    avg = compute_average(n)
    print("Average per append op (in us): {0}".format(avg * 10e6))

