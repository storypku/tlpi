#!/usr/bin/env python3
class StudentRecord:
    def __init__(self):
        self.idNum = 0
        self.firstName = None
        self.lastName  = None
        self.classCode = 0
        self.gpa = 0.0

class StudentFileReader:
    def __init__(self, inputsrc):
        self._inputsrc = inputsrc
        self._inputfd = None
    def open(self):
        self._inputfd = open(self._inputsrc, "r")

    def close(self):
        self._inputfd.close()
        self._inputfd = None

    def fetchAll(self):
        theRecords = list()
        student = self.fetchRecord()
        while student != None:
            theRecords.append(student)
            student = self.fetchRecord()
        return theRecords

    def fetchRecord(self):
        line = self._inputfd.readline().rstrip()
        if line == "":
            return None
        recFields = line.split()
        student = StudentRecord()
        student.idNum = int(recFields[0])
        student.firstName = recFields[1]
        student.lastName = recFields[2]
        student.classCode = int(recFields[3])
        student.gpa = float(recFields[4])
        return student

