# Class representing the color of a card. Only one such object should exist for
# every valid color, to enable global modifications of color effects.
#
# name (str): The full name of the color. 
# abbr (str): The abbreviated name of the color.
# bgCode (int): IRC code for the background color.
# fgCode (int): IRC code for the foreground color, typically 01 (black) or 00
#   (white).
# strength (int): How difficult it is to change the color of cards with this
#   color via the effect of another card.

class Color(object):

    def __init__(
        self, 
        name, 
        abbr,
        bgCode, 
        fgCode, 
        strength=0,
    ):
        self.name = name
        self.abbr = abbr
        self.bgCode = bgCode
        self.fgCode = fgCode
        self.strength = strength


    def __str__(self):
        return "\x03{},{}{}\x03".format(
            self.fgCode,
            self.bgCode,
            self.name,
        )

    
    # Check that determines whether cards of this color can be played on
    # another color.
    def playCheck(self, color):
        return self == color


    # Check that determines whether a card of a given color can be played when
    # this is the current color.
    def playOnCheck(self, color):
        return self == color


    # Side effect of playing a card of this color.
    def playEffect(self, ub):
        pass


# Subclasses for distinct color checks and effects.

# Wild cards can always be played, but, if the color is wild, standard rules
# apply, and only other wild or purple cards can be played.
# TODO: this behavior is left in for now to preserve patch stealth, but it's
# a bit unbalanced, and should probably be changed to match the purple logic.
class ColorWild(Color):

    def playCheck(self, color):
        return True


    def playEffect(self, ub):
        response = ub.ask(
            message="Choose the color.",
            player=ub.currentPlayer,
        )
        while 1:
            if response in ub.colors.keys():
                ub.currentColor = ub.colors[response]
                return
            # Code duplication is because v&7 doesn't re-prompt on an invalid
            # color
            response = ub.ask(
                message=None,
                player=ub.currentPlayer,
            )


# Purple cards can always be played, but anything can be played on them.
class ColorPurple(Color):

    def playCheck(self, color):
        return True


    def playOnCheck(self, color):
        return True


    def playEffect(self, ub):
        # TODO: storing the prevColor is a hack to allow the v&7 behavior
        # of only printing this when the color actually /changes/ to purple
        # to be replicated
        # TODO: i think v&7 also doesn't print this if the card types matched,
        # which would require storing prevCard as well to fix...maybe we 
        # should rethink this and try to find a better solution...
        if ub.prevColor != self:
            ub.say("Color forced to purple!")


# Initialize the standard colors
def initColors():
    colors = {}

    colors['blue'] = Color(
        name='blue',
        abbr='b',
        bgCode='01',
        fgCode='11',
    )
    colors['b'] = colors['blue']

    colors['red'] = Color(
        name='red',
        abbr='r',
        bgCode='01',
        fgCode='04',
    )
    colors['r'] = colors['red']

    colors['green'] = Color(
        name='green',
        abbr='g',
        bgCode='01',
        fgCode='09',
    )
    colors['g'] = colors['green']

    colors['yellow'] = Color(
        name='yellow',
        abbr='y',
        bgCode='01',
        fgCode='08',
    )
    colors['y'] = colors['yellow']

    colors['wild'] = ColorWild(
        name='wild',
        abbr='w',
        bgCode='00',
        fgCode='14',
        strength=2,
    )
    colors['w'] = colors['wild']

    colors['black'] = Color(
        name='black',
        abbr='k',
        bgCode='00',
        fgCode='01',
        strength=1,
    )
    colors['k'] = colors['black']

    colors['purple'] = ColorPurple(
        name='purple',
        abbr='p',
        bgCode='00',
        fgCode='06',
        strength=1,
    )
    colors['p'] = colors['purple']

    return colors

