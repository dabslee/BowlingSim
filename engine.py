from enum import Enum
import random

# The default probability that a pin goes down
SKILL = 0.8

# Represents a single bowling pin
# Keeps track of which pins it's dependent on and also
# decides when it falls
class Pin():
    def __init__(self, dependent):
        # The list of pins this pin is dependent on
        self.dependent = dependent
        # Whether the pin has been knocked down (True) or not (False)
        self.downed = False

    # Tries knocking the pin down.
    # The default probability a pin is knocked down is SKILL; this
    # probabilty is reduced by a factor of 3 for every pin that this pin
    # is dependent on that has not been knocked down
    def knock(self):
        if self.downed:
            return True

        prob = SKILL
        for parent in self.dependent:
            if not parent.downed:
                prob /= 3

        if random.random() < prob:
            self.downed = True
            return True
        return False

# Represents a set of 10 bowling pins, indexed:
# 6 8 9 7
#  3 5 4
#   1 2
#    0
# Handles simulation of rolls on the bowling pins
class PinSet():
    # Creates 10 bowling pins and stores them; the pins' indexing and
    # their dependencies can be seen in pingraph.png in this directory
    def __init__(self):
        self.pinList = [] # A list that stores the Pins
        self.pinList.append(Pin([])) #0
        self.pinList.append(Pin([self.pinList[0],])) #1
        self.pinList.append(Pin([self.pinList[0],])) #2
        self.pinList.append(Pin([self.pinList[1],])) #3
        self.pinList.append(Pin([self.pinList[2],])) #4
        self.pinList.append(Pin([self.pinList[1],self.pinList[2],self.pinList[3],self.pinList[4],])) #5
        self.pinList.append(Pin([self.pinList[3],])) #6
        self.pinList.append(Pin([self.pinList[4],])) #7
        self.pinList.append(Pin([self.pinList[3],self.pinList[5],self.pinList[6],])) #8
        self.pinList.append(Pin([self.pinList[4],self.pinList[5],self.pinList[7],self.pinList[8],])) #9
        
    # Simulates a roll, knocking every pin in the list in order such
    # that no pin is knocked before the pins it's dependent have
    # been knocked
    def roll(self):
        result = []
        for pin in self.pinList:
            result.append(pin.knock())
        return result

    # Prints the state of the bowling pins, where x is knocked down
    # and o is standing
    def stringBooleanResult(result):
        return ("%c %c %c %c\n %c %c %c\n  %c %c\n   %c\n" % (
            'x' if result[6] else 'o',
            'x' if result[8] else 'o',
            'x' if result[9] else 'o',
            'x' if result[7] else 'o',
            'x' if result[3] else 'o',
            'x' if result[5] else 'o',
            'x' if result[4] else 'o',
            'x' if result[1] else 'o',
            'x' if result[2] else 'o',
            'x' if result[0] else 'o'
        ))

# An enum representing the state that a frame can be in after it's done
class FrameState(Enum):
    OPEN = 0
    SPARE = 1
    STRIKE = 2
# Represents a bowling frame; that is, two rolls on one PinSet.
# Simulates a frame and stores the results at the end of each roll.
class Frame():
    def __init__(self):
        # A FrameState var storing the state of the frame
        self.state = None
        # A boolean list representing which pins have been knocked down
        # (True=knocked down) after the first roll
        self.result1 = [False, False, False, False, False, False, False, False, False, False]
        # A boolean list representing which pins have been knocked down
        # (True=knocked down) after the second roll (if there is one)
        self.result2 = None

    # Simulates a frame and stores the ending state (strike, spare, or
    # open), as well as the results of the first and second rolls
    def simulateFrame(self):
        pinset = PinSet()
        self.result1 = pinset.roll()
        if (sum(self.result1) == 10):
            self.state = FrameState.STRIKE
            self.result2 = self.result1
            return self.state
        self.result2 = pinset.roll()
        if (sum(self.result2) == 10):
            self.state = FrameState.SPARE
            return self.state
        self.state = FrameState.OPEN
        return self.state

# Represents the entire Game--that is, all 10 frames
# Simulates the entire Game and stores its results
class Game():
    def __init__(self):
        # A list of the scores of each frame, represented as strings
        # "A B" where A is the result of the first frame and B is the
        # result of the second frame (e.g. "6 /" or "X  " or "3 4")
        self.scorecard = []
        # A full string representation of each frame of the game
        self.display = ""
        # The total score of the game
        self.totalscore = 0

    # Runs the game simulation, filling out the scorecard, display,
    # and calculating the final totalscore
    def runGame(self):
        # Keeps track of the previous and previous-previous frames'
        # results to determine how to add up scores
        prevState = FrameState.OPEN
        prevPrevState = FrameState.OPEN

        # Run the first 9 frames and the first 1 or 2 rolls of the
        # 10th frame (does not run rolls after spare or strike in
        # this loop)
        for i in range(10):
            # Create and simulate a new frame
            frame = Frame()
            newState = frame.simulateFrame()

            # add to scorecard
            if newState == FrameState.OPEN:
                self.scorecard.append("%d %d" % (sum(frame.result1), sum(frame.result2) - sum(frame.result1)))
            elif newState == FrameState.SPARE:
                self.scorecard.append("%d /" % (sum(frame.result1)))
            elif newState == FrameState.STRIKE:
                self.scorecard.append("X  ")

            # add to totalscore
            score = sum(frame.result2)
            self.totalscore += score
            if prevState == FrameState.SPARE:
                self.totalscore += score
            if prevState == FrameState.STRIKE:
                if prevPrevState == FrameState.STRIKE:
                    self.totalscore += score
                self.totalscore += score

            # add to display
            self.display += "\n"
            self.display += "Frame %d\n" % (i + 1)
            self.display += "Roll 1:\n"
            self.display += PinSet.stringBooleanResult(frame.result1)
            if frame.state != FrameState.STRIKE:
                self.display += "Roll 2:\n"
                self.display += PinSet.stringBooleanResult(frame.result2)

            prevState = newState
            prevPrevState = prevState

        # If the 10th frame was a spare, perform one more roll
        if prevState == FrameState.SPARE:
            result = PinSet().roll()

            # Update scorecard
            if sum(result) == 10:
                self.scorecard.append("X  ")
            else:
                self.scorecard.append("%d  " % (sum(result)))

            # Update totalscore
            self.totalscore += sum(result)

            # add to display
            self.display += "Roll 3:\n"
            self.display += PinSet.stringBooleanResult(result)
            self.display += "\n"
        
        # If the 10th frame was a strike, perform two more rolls
        elif prevState == FrameState.STRIKE:
            frame = Frame()
            frame.simulateFrame()
            result1 = frame.result1
            result2 = frame.result2

            # If the second roll of the 10th frame was a strike...
            if (frame.state == FrameState.STRIKE):
                # Update scorecard
                result2 = (PinSet()).roll()
                if sum(result2) == 10:
                    self.scorecard.append("X X")
                else:
                    self.scorecard.append("X %d" % (sum(result2)))

                # Update totalscore
                self.totalscore += sum(result1)
                self.totalscore += sum(result2)

            # If the second roll of the 10th frame was not a strike...
            else:
                # Update scorecard
                if sum(result2) == 10:
                    self.scorecard.append("%d /" % (sum(result1)))
                else:
                    self.scorecard.append("%d %d" % (sum(result1), sum(result2) - sum(result1)))

                # Update totalscore
                self.totalscore += sum(result2)

            # Update display
            self.display += "Roll 2:\n"
            self.display += PinSet.stringBooleanResult(result1)
            self.display += "Roll 3:\n"
            self.display += PinSet.stringBooleanResult(result2)
            self.display += "\n"