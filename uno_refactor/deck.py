import copy
import random

# Class representing a deck.
#
# cards (list(card)): The list of cards in the deck.

class Deck(object):

    def __init__(
        self,
        cards,
    ):
        self.cards = cards


    def drawOne(self):
        return copy.copy(random.choice(self.cards))

