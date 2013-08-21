import time
class TC(object):
    """The TestCategory Colleague class"""
    def __init__(self):
        self._manager = None
        self._problem = False

    def setup(self):
        print "Setting up the Test"
        time.sleep(1)
        self._manager.prepareReporting()

    def execute(self):
        if not self._problem:
            print "Executing the test"
            time.sleep(1)
        else:
            print "Problem in setup. Test not executed."

    def terDown(self):
        if not self._problem:
            print "Tearing down"
            time.sleep(1)
            self._manager.publishReport()
        else:
            print "Test not executed. No tear down required."

    def setManager(self, manager):
        self._manager = manager

    def setProblem(self, problem):
        self._problem = problem

class Reporter(object):
    """The Reporter Colleague class """
    def __init__(self):
        self._manager = None

    def prepare(self):
        print "Reporter class is preparing to report the results"
        time.sleep(1)

    def report(self):
        print "Reporting the results of Test"
        time.sleep(1)

    def setManager(self, manager):
        self._manager = manager

class DB(object):
    """The Database Colleague class """
    def __init__(self):
        self._manager = None

    def insert(self):
        print "Inserting the execution begin status into database"
        time.sleep(1)
        import random
        return True if random.randrange(1, 4) != 3 else False

    def update(self):
        print "Updating the test results in the database"
        time.sleep(1)

    def setManager(self, manager):
        self._manager = manager

class Manager(object):
    """The Manager Mediator class"""
    def __init__(self):
        self._reporter = None
        self._db = None
        self._tc = None

    def prepareReporting(self):
        flag = self._db.insert()
        if not flag:
            self._tc.setProblem(True)
        else:
            self._reporter.prepare()

    def setReporter(self, reporter):
        self._reporter = reporter

    def setDB(self, db):
        self._db = db

    def setTC(self, tc):
        self._tc = tc

    def publishReport(self):
        self._db.update()
        self._reporter.report()

if __name__ == "__main__":
    reporter = Reporter()
    db = DB()
    tm = Manager()

    tm.setReporter(reporter)
    tm.setDB(db)

    reporter.setManager(tm)
    db.setManager(tm)

    for _ in range(10):
        tc = TC()
        tc.setManager(tm)
        tm.setTC(tc)

        tc.setup()
        tc.execute()
        tc.terDown()
