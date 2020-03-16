# Class representing the type of a card.
#
# name (str): The name of the card type.
# playCheck (fn: self, UnoBEARS -> bool): Check that determines whether cards
#   of this type can be played.
# playEffect (fn: self, UnoBEARS): Side effect of playing a card of this type.
# waitEffect (fn: self, Player, UnoBEARS): Side effect of having this card in 
#   your hand for a turn.
# penalty (fn: self, Player, UnoBEARS): Effect of this card being applied as
#   as a penalty.
# strength (int): The relative strength of this card type's effects.

class CardType:

    def __init__(
        self,
        name,
        playCheck,
        playEffect,
        waitEffect,
        penalty,
        strength,
    ):
        self.name = name
        self.playCheck = playCheck
        self.playEffect = playEffect
        self.waitEffect = waitEffect
        self.penalty = penalty
        self.strength = strength


# Standard card type check functions
def standardCardTypeCheck(self, ub):
    return self == ub.topCard.cardType


# Initialize the standard card types
def initCardTypes():
    cardTypes = {}

    cardTypes['6'] = CardType(
        name='6',
        playCheck=standardCardTypeCheck,
        playEffect=None,
        waitEffect=None,
        penalty=None,
        strength=0,
    )

    return cardTypes

