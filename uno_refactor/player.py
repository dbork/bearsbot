from deck import Deck

import copy
from decimal import Decimal
import random

# Class representing a player.
#
# name (str): The name of the player.
# hand (list(Card)): The list of cards in a player's hand.
# deck (list(Card)): The player's current deck.
# area (Area): The area the player is in.
# luck (decimal): How lucky the player is. Used when drawing cards.
# luckDecay (decimal): How quickly the player's luck regresses toward 0.
# shield (int): The number of penalties the player is shielded against.

class Player(object):

    def __init__(
        self,
        name,
        deck,
        area,
    ):
        self.name = name
        self.hand = []
        # Copy the deck so that each player's deck changes seperately.
        self.deck = Deck([copy.copy(card) for card in deck.cards])
        self.area = area
        self.luck = Decimal(0)
        self.luckDecay = Decimal(0.5)
        self.shield = 0

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
            elif self.luck == 0:
                self.hand.append(self.deck.drawOne())
            else:
                self.hand.append(self.area.drawOne(luck=self.luck))
                if self.luck > 0:
                    self.luck = max(self.luck - self.luckDecay, Decimal(0))
                if self.luck < 0:
                    self.luck = min(self.luck + self.luckDecay, Decimal(0))


    # Return the first card from a player's hand with string representation
    # matching an input string, or None if none exist
    def getCardFromHand(self, string):
        for card in self.hand:
            if card.name() == string:
                return card
        return None


    # General-purpose for discarding cards that match certain conditions.
    #
    # ub (UnoBears): This needs to be passed so discarded cards can be added
    #   to the discard pile.
    # limit (int): Up to this many cards matching the conditions will be
    #   discarded, or, if limit is None, all cards will be discarded.
    # card (Card): If passed, instances of this specific Card object will be
    #   discarded.
    # randomCards (list[Card]): If passed, Card objects will be chosen randomly
    #   from this list (without replacement) and discarded.
    # cardType (CardType) If passed, cards with this CardType will be deleted.
    # color (Color) If passed, cards with this Color will be deleted.

    def discard(
        self,
        ub,
        limit=1,
        card=None,
        randomCards=None,
        cardType=None,
        color=None,
    ):
        # We do this in two passes to avoid issues with removing elements 
        # while iterating over a list.
        if card:
            discards = filter(lambda c: c is card, self.hand)
        elif randomCards:
            discards = random.sample(randomCards, len(randomCards))
        elif cardType:
            if color:
                discards = filter(
                    lambda c: c.color == color and c.cardType == cardType, 
                    self.hand,
                )
            else:
                discards = filter(lambda c: c.cardType == cardType, self.hand)
        elif color:
            discards = filter(lambda c: c.color == color, self.hand)

        if limit is not None:
            discards = discards[:limit]

        for handCard in discards:
            ub.discard.append(handCard)
            self.hand.remove(handCard)


    # General-purpose method for changing cards in a player's hand.
    #
    # strength (int): The strength of the card-changing effect.
    # limit (int): Up to this many cards matching the conditions will be
    #   changed, or, if limit is None, all cards will be changed.
    # card (Card): If passed, instances of this specific Card object will be
    #   changed.
    # randomCards (list[Card]): If passed, Card objects will be chosen randomly
    #   from this list (with replacement) and changed.
    #   TODO: sampling with replacement here is v&7 behavior
    #   TODO: i think the in operator for objects uses is rather than ==? if
    #   not, this logic will always take the first limit cards in a sequence
    #   of identical cards, which is not what we want...
    # oldCardType (CardType) If passed, cards with this CardType will be 
    #   changed.
    # oldColor (Color) If passed, cards with this Color will be changed.
    # newCardType (CardType) If passed, cards will be changed to this cardType.
    # oldColor (Color) If passed, cards will be changed to this Color.
    # randomNewCardType (list[CardType]) If passed, cards will be changed to a 
    #   CardType randomly chosen from this list (with replacement).
    # randomNewColor (list[Color]) If passed, cards will have color changed to
    #   a Color randomly chosen from this list (with replacement).

    def changeInHand(
        self,
        strength,
        limit=1,
        card=None,
        randomCards=None,
        oldCardType=None,
        oldColor=None,
        newCardType=None,
        newColor=None,
        randomNewCardTypes=None,
        randomNewColors=None,
    ):
        # Sample from randomCards with replacement.
        if limit is None or randomCards is None:
            randomSample = randomCards
        else:
            randomSample = [
                random.choice(randomCards) for i in range(limit)
            ]

        limitRemaining = limit

        if card:
            toChange = filter(lambda c: c is card, self.hand)
        elif randomCards:
            toChange = filter(lambda c: c in randomSample, self.hand)
        elif oldCardType:
            if oldColor:
                toChange = filter(
                    lambda c: c.color == oldColor 
                        and c.cardType == oldCardType, 
                    self.hand,
                )
            else:
                toChange = filter(
                    lambda c: c.cardType == oldCardType, 
                    self.hand,
                )
        elif oldColor:
            toChange = filter(lambda c: c.color == oldColor, self.hand)

        if limit is not None:
            toChange = toChange[:limit]

        for handCard in toChange:
            if newCardType:
                handCard.cardType = newCardType
            if newColor and strength >= handCard.color.strength:
                handCard.color = newColor
            if randomNewCardTypes:
                handCard.cardType = random.choice(randomNewCardTypes)
            if randomNewColors and strength >= handCard.color.strength:
                handCard.color = random.choice(randomNewColors)


# Initialize players given a list of names and a starting area.
def initPlayers(playerNames, area):
    players = []
    for name in playerNames:
        players.append(
            Player(
                name=name,
                deck=area.decks[0],
                area=area,
            )
        )
    return players

