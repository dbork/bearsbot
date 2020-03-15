# Class representing the color of a card
#
# Data members
#   name (str): The full name of the color. 
#   abbr (str): The abbreviated name of the color.
#   bgCode (int): IRC code for the background color.
#   fgCode (int): IRC code for the foreground color, typically 01 (black) or
#   00 (white).
#   playCheck (fn: self, UnoBEARS -> bool): Check that determines whether 
#   cards of this color can be played on cards of another color.
#   self.playEffect (fn): Side effect of playing a card of this color.
#   strength (int): How difficult it is to change the color of cards with this
#   color via the effect of another card.

class Color:

    def __init__(
        self, 
        name, 
        abbr,
        bgCode, 
        fgCode, 
        playCheck, 
        playEffect,
        strength,
    ):
        self.name = name
        self.abbr = abbr
        self.bgCode = bgCode
        self.fgCode = fgCode
        self.playCheck = playCheck
        self.playEffect = playEffect
        self.strength = strength

    def __str__(self):
        return "\x03{},{}{}\x03".format(
            self.fgCode,
            self.bgCode,
            self.name,
        )


# Standard color check functions
def standardColorCheck(self, ub):
    return self == ub.currentColor

def freeColorCheck(self, ub):
    return True

# Standard color effect functions
def nullColorEffect(self, ub):
    pass

def purpleEffect(self, ub):
    ub.say("Color forced to purple! \r\n")

def wildEffect(self, ub):
    choice = ub.ask(
        prompt="Choose the color. \r\n",
        acceptIf=lambda x: x in ub.colors.keys(),
        rejectPrompt=None,
    )
    ub.currentColor = ub.colors[choice]

# Initialize the standard colors
def initColors():
    colors = {}

    colors['blue'] = Color(
        name='blue',
        abbr='b',
        bgCode='01',
        fgCode='11',
        playCheck=standardColorCheck,
        playEffect=nullColorEffect,
        strength=0,
    )
    colors['b'] = colors['blue']

    colors['red'] = Color(
        name='red',
        abbr='r',
        bgCode='01',
        fgCode='04',
        playCheck=standardColorCheck,
        playEffect=nullColorEffect,
        strength=0,
    )
    colors['r'] = colors['red']

    colors['green'] = Color(
        name='green',
        abbr='g',
        bgCode='01',
        fgCode='09',
        playCheck=standardColorCheck,
        playEffect=nullColorEffect,
        strength=0,
    )
    colors['g'] = colors['green']

    colors['yellow'] = Color(
        name='yellow',
        abbr='y',
        bgCode='01',
        fgCode='08',
        playCheck=standardColorCheck,
        playEffect=nullColorEffect,
        strength=0,
    )
    colors['y'] = colors['yellow']

    colors['wild'] = Color(
        name='wild',
        abbr='w',
        bgCode='00',
        fgCode='14',
        playCheck=freeColorCheck,
        playEffect=wildEffect,
        strength=2,
    )
    colors['w'] = colors['wild']

    colors['black'] = Color(
        name='black',
        abbr='k',
        bgCode='00',
        fgCode='01',
        playCheck=standardColorCheck,
        playEffect=nullColorEffect,
        strength=2,
    )
    colors['k'] = colors['black']

    colors['purple'] = Color(
        name='purple',
        abbr='p',
        bgCode='00',
        fgCode='06',
        playCheck=freeColorCheck,
        playEffect=purpleEffect,
        strength=1,
    )
    colors['p'] = colors['purple']

    return colors

