#!/usr/bin/env python3
import os
def disk_usage(path):
    """Return the number of bytes used by a file/directory and any
    descendents."""
    total = os.path.getsize(path)
    if os.path.isdir(path):
        for filename in os.listdir(path):
            childpath = os.path.join(path, filename)
            total += disk_usage(childpath)

    print ("{0:<7}".format(total), path)    # descriptive output (optional)
    return total

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 or sys.argv[1] == "--help":
        print("Usage: {0} pathname".format(sys.argv[0]))
        raise SystemExit
    disk_usage(sys.argv[1])
