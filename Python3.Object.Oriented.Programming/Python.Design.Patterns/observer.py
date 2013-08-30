class Publisher(object):
    def __init__(self):
        pass

    def register(self):
        pass

    def unregister(self):
        pass

    def notifyAll(self):
        pass

class TechForum(Publisher):
    def __init__(self):
        self._userList = set()
        self.postName = None

    def register(self, user):
        self._userList.add(user)

    def unregister(self, user):
        self._userList.discard(user)

    def notifyAll(self):
        for user in self._userList:
            user.notify(self.postName)

    def writeNewPost(self, postName):
        self.postName = postName
        self.notifyAll()

class Subscriber(object):
    def __init__(self):
        pass

    def notify(self):
        pass

class User(Subscriber):

    def __init__(self, name):
        self.name = name

    def notify(self, postName):
        print '%s (User) notified of a new post:\n  "%s"' % (self.name, postName)

class SisterSites(Subscriber):

    def __init__(self, sites):
        self._broSites = set(sites)

    def notify(self, postName):
        for site in self._broSites:
            print '%s (Site) notified of a new post:\n  "%s"' % (site, postName)

if __name__ == "__main__":
    techForum = TechForum()
    user1 = User("Li Lei")
    user2 = User("Han Meimei")

    sitesName = ["36Kr", "InfoQ", "CSDN"]
    sites = SisterSites(sitesName)

    for user in user1, user2, sites:
        techForum.register(user)

    techForum.writeNewPost("Observer pattern in Python")
    techForum.unregister(user2)
    techForum.writeNewPost("Facade Pattern Preview")

