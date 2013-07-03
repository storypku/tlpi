""" Implementation of the Histogram ADT using a Hash Map """
from hashmap import HashMap
class Histogram:
    """ Implementation of the Histogram ADT using a Hash Map """

    # Creates a histogram containing the given categories
    def __init__(self, catSeq):
        self._freqCounts = HashMap()
        for cat in catSeq:
            self._freqCounts.add(cat, 0)

    def getCount(self, category):
        """ Returns the frequency count for the given category. """
        assert category in self._freqCounts, "Invalid histogram category."
        return self._freqCounts.valueOf(category)
    def incCount(self, category):
        """ Increments the counter for the given category """
        assert category in self._freqCounts, "Invalid histogram category."
        value = self._freqCounts.valueOf(category)
        self._freqCounts.add(category, value + 1)
    def totalCount(self):
        """ Returns the sum of the frequency counts. """
        total = 0
        for cat in self._freqCounts:
            total += self._freqCounts.valueOf(cat)
        return total
    def __iter__(self):
        """ Returns an iterator for traversing the categories """
        return iter(self._freqCounts)

def letterGrade(grade):
    if grade >= 90:
        return 'A'
    elif grade >= 80:
        return 'B'
    elif grade >= 70:
        return 'C'
    elif grade >= 60:
        return 'D'
    else:
        return 'F'
if __name__ == "__main__":
    gradeHist = Histogram("ABCDF")
    gradeFile = open("grades.txt", "r")
    for line in gradeFile:
        grade = int(line)
        gradeHist.incCount(letterGrade(grade))
    print "A: %d" % gradeHist.getCount('A')
    print "Total : %d" % gradeHist.totalCount()
