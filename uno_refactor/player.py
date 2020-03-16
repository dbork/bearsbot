import copy
import random

# Class representing a player.
#
# name (str): The name of the player.
# hand (list(Card)): The list of cards in a player's hand.
# deck (list(Card)): The player's current deck.

class Player:

    def __init__(
        self,
        name,
        deck,
    ):
        self.name = name
        self.hand = []
        # Copy the deck so that each player's deck changes seperately.
        self.deck = [copy.copy(card) for card in deck]

        self.draw(7)


    def __str__(self):
        return self.name


    def handToStr(self):
        return ' '.join(map(str, self.hand))


    # The player draws num cards from their deck, or, if card is specified,
    # num copies of card.
    def draw(self, num, card=None):
        for i in range(num):
            if card:
                self.hand.append(copy.copy(card))
            else:
                self.hand.append(copy.copy(random.choice(self.deck)))
        #TODO: implement luck


# Initialize players given a list of names.
def initPlayers(playerNames, deck):
    players = []
    for name in playerNames:
        players.append(
            Player(
                name=name,
                deck=deck,
            )
        )
    return players

