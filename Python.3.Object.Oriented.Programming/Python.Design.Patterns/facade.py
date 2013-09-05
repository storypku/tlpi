"""A simple example demostrating the Facade design pattern in Python."""

import time
class MemeryTestCase(object):
    def run(self):
        print "### Test Case for Memery Usage: ###"
        print "Setting up..."
        time.sleep(1)
        print "Running test"
        time.sleep(2)
        print "Tearing down"
        time.sleep(1)
        print "Test finished\n"

class CPUTestCase(object):
    def run(self):
        print "### Test Case for CPU Usage: ###"
        print "Setting up..."
        time.sleep(1)
        print "Running test"
        time.sleep(2)
        print "Tearing down"
        time.sleep(1)
        print "Test finished\n"

class HardDriveTestCase(object):
    def run(self):
        print "### Test Case for HardDrive Usage: ###"
        print "Setting up..."
        time.sleep(1)
        print "Running test"
        time.sleep(2)
        print "Tearing down"
        time.sleep(1)
        print "Test finished\n"

class TestRunner(object):
    """The Facade class"""
    def __init__(self):
        self._testcases = MemeryTestCase(), CPUTestCase(), HardDriveTestCase()

    def runAll(self):
        for testcase in self._testcases:
            testcase.run()

if __name__ == "__main__":
    testrunner = TestRunner()
    testrunner.runAll()
