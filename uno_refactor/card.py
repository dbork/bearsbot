from cardtype import CardType
from color import Color

# Card class
#
# cardType (CardType): The type of the card.
# color (Color): The color of the card.
# 
# Note that both of these are references to global objects stores in the
# top-level UnoBEARS object; thus, a card can theoretically modify the global
# properties of a color or card type.

class Card:

    def __init__(
        self,
        cardType,
        color,
    ):
        self.cardType = cardType
        self.color = color


    def __str__(self):
        return "\x03{},{}{}{}\x03".format(
            self.color.fgCode,
            self.color.bgCode,
            self.cardType.name,
            self.color.abbr,
        )


# Helper function for creating a card from a string
def cardFromString(string, cardTypes, colors):
    return Card(
        cardType=cardTypes[string[:-1]],
        color=colors[string[-1]],
    )

