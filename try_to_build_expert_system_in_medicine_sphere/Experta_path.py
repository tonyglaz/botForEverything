from random import choice
from experta import *


class Light(Fact):
    """Info about the traffic light."""
    pass


class RobotCrossStreet(KnowledgeEngine): # This is the LHS
    @Rule(Light(color='green'))
    def green_light(self):
        """This rule will match with every instance of `Light`."""
        # This is the RHS
        print("Walk")

    @Rule(Light(color='red'))
    def red_light(self):
        print("Don't walk")

    @Rule(AS << Light(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is", light["color"])


engine = RobotCrossStreet()
engine.reset()
engine.declare(Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red'])))
engine.run()