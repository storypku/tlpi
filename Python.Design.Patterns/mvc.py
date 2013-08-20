"""A simple example of the Model-View-Controller design pattern."""

import sqlite3

class DefectModel(object):
    """The MODEL class"""

    def getDefectList(self, component):
        query = "select ID from defects where Component = '%s'" % component
        results = self._dbselect(query)
        return [row[0] for row in results]

    def getSummary(self, id_):
        query = "select Summary from defects where ID = %d " % id_
        summaries = self._dbselect(query)
        return summaries[0][0] if summaries else None

    def _dbselect(self, query):
        with sqlite3.connect("mvc.db") as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
        return results

class DefectView(object):
    """The VIEW class"""

    def summary(self, summ, id_):
        print "### Defect Summary for defect # %d ###" % id_
        print summ

    def defectList(self, ids, component):
        print "### Defect List for %s ###" % component
        print "\n".join(str(id_) for id_ in ids) if ids else None

class Controller(object):
    """The CONTROLLER class"""

    def __init__(self):
        self._model = DefectModel()
        self._view = DefectView()

    def getDefectSummary(self, id_):
        summary = self._model.getSummary(id_)
        return self._view.summary(summary, id_)

    def getDefectList(self, component):
        ids = self._model.getDefectList(component)
        return self._view.defectList(ids, component)

if __name__ == "__main__":
    ctrler = Controller()
    ctrler.getDefectList("XYZ")
    ctrler.getDefectList("ABC")
    ctrler.getDefectList("DEF")
    ctrler.getDefectSummary(2)
    ctrler.getDefectSummary(5)
