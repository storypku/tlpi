"""Experimental program to verify the dynamic array nature of list in
python."""

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 or sys.argv[1] == "--help":
        print("Usage: {0} maximum_length".format(sys.argv[0]))
        raise SystemExit
    n = int(sys.argv[1])
    data = []
    for k in range(n):
        a = len(data)
        b = sys.getsizeof(data)
        print ("Length: {0:3d}; Size in bytes: {1:4d}".format(a, b))
        data.append(None)
