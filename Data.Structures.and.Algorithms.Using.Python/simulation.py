from array_m import Array
from llistqueue import Queue
from simplepeople import TicketAgent, Passenger
import random
class TicketCounterSimulation:
    def __init__(self, numAgents, numMins, arrivalTime, serviceTime):
        self._arrivalProb = 1.0/arrivalTime
        self._serviceTime = serviceTime
        self._numMins = numMins
        self._passengerQ = Queue()
        self._theAgents = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i + 1)
        self._totalWaitTime = 0
        self._numPassengers = 0
    def run(self):
        for curTime in range(0, self._numMins+1):
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)
    def printResults(self):
        numServed = self._numPassengers - len(self._passengerQ)
        avgWaitTime = float(self._totalWaitTime)/numServed
        print ""
        print "Number of passengers served = ", numServed
        print "Number of passengers remaining in line = %2d" % \
                len(self._passengerQ)
        print "The average wait time was %4.2f minutes." % avgWaitTime

    def _handleArrival(self, curTime):
        prob = random.random()/4.0
        if prob >= self._arrivalProb:
            self._numPassengers += 1
            passenger = Passenger(self._numPassengers, curTime)
            self._passengerQ.enqueue(passenger)
            print "Time %2d: Passenger %2d arrived." % (curTime, \
                self._numPassengers)

    def _handleBeginService(self, curTime):
        while not self._passengerQ.isEmpty():
            freeFlag = False
            for i in range(len(self._theAgents)):
                if self._theAgents[i].isFree():
                    freeFlag = True
                    passenger = self._passengerQ.dequeue()
                    self._theAgents[i].startService(passenger, \
                            curTime + self._serviceTime)
                    print "Time %2d: Agent %2d started serving passenger %2d." % \
                          (curTime, self._theAgents[i]._idNum, passenger._idNum)
                    self._totalWaitTime += curTime - passenger.timeArrived()
                    break
            if freeFlag == False:
                return


    def _handleEndService(self, curTime):
        for i in range(len(self._theAgents)):
            if self._theAgents[i].isFinished(curTime):
                passenger = self._theAgents[i].stopService()
                print "Time %2d: Agent %2d stopped serving passenger %2d." % \
                      (curTime, self._theAgents[i]._idNum, passenger._idNum)

