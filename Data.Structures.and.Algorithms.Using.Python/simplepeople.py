class Passenger:
    def __init__(self, idNum, arrivalTime):
        self._idNum = idNum
        self._arrivalTime = arrivalTime
    def idNum(self):
        return self._idNum
    def timeArrived(self):
        return self._arrivalTime

class TicketAgent:
    def __init__(self, idNum):
        self._idNum = idNum
        self._passenger = None
        self._stopTime = -1
    def idNum(self):
        return self._idNum
    def isFree(self):
        return self._passenger is None
    def isFinished(self, curTime):
        return self._passenger is not None and self._stopTime == curTime
    def startService(self, passenger, stopTime):
        self._passenger = passenger
        self._stopTime = stopTime
    def stopService(self):
        thePassenger = self._passenger
        self._passenger = None
        return thePassenger

