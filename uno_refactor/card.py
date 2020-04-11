from cardtype import CardType
from color import Color

# Card class. Unlike for card types and colors, each card is stored in its
# own object. Thus, a card can locally change the type of color of another 
# card, or globally modify the properties of types and colors.
#
# cardType (CardType): The type of the card.
# color (Color): The color of the card.

class Card(object):

    def __init__(
        self,
        cardType,
        color,
    ):
        self.cardType = cardType
        self.color = color


    def __str__(self):
        return "\x03{},{}{}\x03".format(
            self.color.fgCode,
            self.color.bgCode,
            self.name(),
        )


    # Gets the string representation without IRC formatting. This needs to be
    # a function, rather than a data member, so that it will respect cardType
    # and color changes.
    def name(self):
        return self.cardType.name + self.color.abbr

