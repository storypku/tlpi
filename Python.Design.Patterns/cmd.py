"""A simple example of Command design pattern."""

class Switch(object):
    """The INVOKER class"""

    def __init__(self, flipUpCmd, flipDownCmd):
        self.__flipUpCmd = flipUpCmd
        self.__flipDownCmd = flipDownCmd

    def flipUp(self):
        self.__flipUpCmd.execute()

    def flipDown(self):
        self.__flipDownCmd.execute()

class Light(object):
    """The RECEIVER class"""

    def turnOn(self):
        print "The light is on"

    def turnOff(self):
        print "The light is off"

class Command(object):
    """The Command abstract class"""

    def __init__(self):
        pass

    def execute(self):
        pass

class FlipUpCommand(Command):
    """The Command class for turning on the light"""
    def __init__(self, light):
        super(FlipUpCommand, self).__init__()
        self.__light = light

    def execute(self):
        self.__light.turnOn()

class FlipDownCommand(Command):
    """The Command class for turning off the light"""
    def __init__(self, light):
        super(FlipDownCommand, self).__init__()
        self.__light = light

    def execute(self):
        self.__light.turnOff()

class LightSwitch(object):
    """The CLIENT class that represents the one that instantiates the
    encapsulated object."""

    def __init__(self):
        self.__lamp = Light()
        self.__switchUp = FlipUpCommand(self.__lamp)
        self.__switchOff = FlipDownCommand(self.__lamp)
        self.__switch = Switch(self.__switchUp, self.__switchOff)

    def switch(self, cmd):
        cmd = cmd.strip().upper()
        try:
            if cmd == "ON":
                self.__switch.flipUp()
            elif cmd == "OFF":
                self.__switch.flipDown()
            else:
                raise ValueError("Argument 'ON' or 'OFF' is required.")
        except ValueError as e:
            print "Exception: %s" % e

if __name__ == "__main__":
    lightSwitch = LightSwitch()
    lightSwitch.switch("ON")
    lightSwitch.switch("Off")
    lightSwitch.switch("abc")
