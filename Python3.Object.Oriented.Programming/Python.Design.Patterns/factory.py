class Person(object):
    def __init__(self):
        self.name = None
        self.gender = None

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

class Male(Person):
    def __init__(self, name):
        self.name = name
        self.gender = "M"
        print "Hello, Mr. %s" % name

class Female(Person):
    def __init__(self, name):
        self.name = name
        self.gender = "F"
        print "Hello, Miss. %s" % name

class Factory(object):
    def getPerson(self, name, gender):
        if gender == "M":
            return Male(name)
        else:
            return Female(name)

if __name__ == "__main__":
    factory = Factory()
    person = factory.getPerson("Green", "F")

