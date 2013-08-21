"""A simple example of Proxy design pattern.

Proxy pattern is an example of structural design patterns. It is also referred
to as "Surrogate" pattern as the intention of this pattern is to create a
surrogate for the real object/class.

Proxy pattern has three essential elements:
    Real Subject ( that performs the business objectives, represented by
        Proxy )
    Proxy Class (that acts as an interface to user requests and shields the
        real subject)
    Client (that makes the requests for getting the job done).
"""

import time

class Manager(object):
    """The Real Subject class"""
    def work(self):
        print "Sales Manager working..."

    def talk(self):
        print "Hello, world"

class Receptionist(object):
    """The Proxy class"""
    def __init__(self):
        self.busy = False # indicate whether Manager is available
        self._manager = None

    def work(self):
        print "Receptionist checking for Manager availability..."
        time.sleep(1)
        if not self.busy:
            print "Manager ready to talk."
            self._manager = Manager()
            time.sleep(1)
            self._manager.talk()
        else:
            print "Sorry, Manager is busy."

if __name__ == "__main__":
    proxy = Receptionist()
    proxy.work()
    proxy.busy = True
    proxy.work()

