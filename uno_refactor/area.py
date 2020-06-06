from deck import Deck

import math

# Class representing an area of play.
#
# name (str): The name of the area.
# decks (dict(Deck)): The decks associated with the area, indexed by
#   luck. Under normal circumstances, players will draw from their decks, but
#   luck modifications or certain other cards can make players draw from these
#   decks instead.

class Area(object):

    def __init__(
        self,
        name,
        decks,
    ):
        self.name = name
        self.decks = decks


    def drawOne(self, luck):
        # Round luck away from 0, so luck = 1 will draw twice from the 
        # relevant deck
        if luck > 0:
            luckRounded = int(math.ceil(float(luck)))
        elif luck < 0:
            luckRounded = int(math.floor(float(luck)))
        else:
            luckRounded = 0

        return self.decks[luckRounded].drawOne()


# Initialize the standard areas.
def initAreas(ub):
    areas = {}
    standardDecks = {}

    # In debug mode, prompt the user to input a deck for the standard area.
    if ub.debug:
        response = raw_input("What deck do you want to test? ")
        standardDecks[0] = Deck([
            ub.cardFromString(string) for string in response.split(' ')
        ])

    else:
        raise NotImplementedError

    areas['standard'] = Area(
        name='standard',
        decks=standardDecks,
    )

    return areas

