from decimal import Decimal
from num2words import num2words
import random

from ai import AI

# Class representing the type of a card. Only one such object should exist for
# every valid card type, to enable global modifications of type effects.
#
# name (str): The name of the card type.
# strength (int): The relative strength of this card type's effects. Generally,
#   cards of strength i will affect colors of strength at most i.
# speed (int): How quickly during the turn a card's effects will be processed.
# defensiveEffect (bool): Whether this cards effects, if applied before the
#   penalties are processed, could conceivably deflect the penalty. Currently
#   only used by sap to determine whether a card is a legal play.

class CardType(object):

    def __init__(
        self,
        name,
        strength=0,
        speed=0,
        defensiveEffect=False,
    ):
        self.name = name
        self.strength = strength
        self.speed = speed
        self.defensiveEffect = defensiveEffect


    # Check that determines whether cards of this type can be played on 
    # cards of another type.
    def playCheck(self, cardType):
        return self == cardType


    # Side effect of playing a card of this type.
    def playEffect(self, ub):
        pass


    # Side effect of having this card in your hand for a turn.
    def waitEffect(self, ub):
        pass


# Subclasses for specific non-penalty card effects
class CardTypeSkip(CardType):

    def playEffect(self, ub):
        ub.say("{} has been skipped!".format(ub.currentPlayer))
        ub.players = ub.players[1:] + [ub.players[0]]
        ub.currentPlayer = ub.players[0]


class CardTypeReverse(CardType):

    def playEffect(self, ub):
        ub.say("Order of play reversed!")
        ub.players.reverse()
        # We need to add the last player back onto the front of the list, 
        # since it's still their turn
        ub.players = [ub.players[-1]] + ub.players[:-1]


class CardTypeDiscardAll(CardType):

    def playEffect(self, ub):
        ub.say("All cards of the same color discarded!")
        ub.currentPlayer.discard(ub=ub, limit=None, color=ub.topCard.color)


class CardTypeShuffleDeck(CardType):

    def playEffect(self, ub):
        ub.say("The deck has been shuffled!")
        # Shuffle deck actually shuffles the deck now!
        ub.discard = [ub.topCard]
        rand = random.randint(1, 20)
        if rand < 4:
            ub.say("You feel unlucky today...")
            ub.currentPlayer.luck -= Decimal(1)
        elif rand < 8:
            pass
        elif rand < 15:
            ub.say("You feel somewhat lucky today.")
            ub.currentPlayer.luck += Decimal(1)
        else:
            ub.say("You feel very lucky today!")
            ub.currentPlayer.luck += Decimal(2)


class CardTypeQueueSubmit(CardType):

    def playEffect(self, ub):
        # Check for victory before doing the effect, to avoid getting stuck
        # asking a player to choose a card from an empty hand.
        if len(ub.currentPlayer.hand) == 0:
            return

        ub.pmHand(ub.currentPlayer)
        
        while 1:
            response = ub.ask(
                message="Choose one additional discard",
                player=ub.currentPlayer
            )
             
            if isinstance(ub.currentPlayer, AI):
                card = ub.currentPlayer.chooseBadCard(self)

            else:
                card = ub.currentPlayer.getCardFromHand(response)

            if card:
                ub.jobQueue.append(card)
                # TODO: update mysterious formula from v&7
                ub.jobQueueTime += (2 * len(ub.players) + 1 - len(ub.jobQueue))
                ub.currentPlayer.discard(ub=ub, card=card)
                ub.say("Job submitted.")
                return

            ub.say("Invalid move.")


class CardTypeShield(CardType):

    def playEffect(self, ub):
        # In v&7, we only print one of this message and the 'deflected the
        # penalty' message, so suppress this if there are penalties to deflect.
        if not ub.penaltyQueue:
            ub.say("{} is now shielded!".format(ub.currentPlayer))
        ub.currentPlayer.shield += 1


class CardTypeMultipleWild(CardType):

    def __init__(
        self,
        name,
        iterations,
        strength=0,
        speed=0,
    ):
        super(CardTypeMultipleWild, self).__init__(name, strength, speed)
        self.iterations = iterations


    def playEffect(self, ub):
        for i in range(self.iterations - 1):
            ub.topCard.color.playEffect(ub)


class CardTypePurple(CardType):

    def playEffect(self, ub):
        # Check for victory before doing the effect, to avoid getting stuck
        # asking a player to choose a card from an empty hand.
        if len(ub.currentPlayer.hand) == 0:
            return

        ub.pmHand(ub.currentPlayer)
        
        while 1:
            response = ub.ask(
                message="Choose one additional card",
                player=ub.currentPlayer
            )
             
            if isinstance(ub.currentPlayer, AI):
                card = ub.currentPlayer.chooseImprovableCard(self)

            else:
                card = ub.currentPlayer.getCardFromHand(response)

            if card:
                ub.currentPlayer.changeInHand(
                    strength=self.strength,
                    card=card,
                    newColor=ub.topCard.color,
                )
                return

            ub.say("Invalid move.")


class CardTypeSelfApply(CardType):

    def playEffect(self, ub):
        # Check for victory before doing the effect, to avoid getting stuck
        # asking a player to choose a card from an empty hand.
        if len(ub.currentPlayer.hand) == 0:
            return

        ub.pmHand(ub.currentPlayer)
        
        ub.say("String together a penalty to apply to yourself. The first " \
           "card can be anything offensive. Type done when finished.")

        # TODO: so this is going to be kind of a mess, since color effects as
        # currently implemented only know how to change the current color,
        # penalty effects only know how to add to the penalty list (eg frstr),
        # etc. honestly, maybe this card should just store them in temporary
        # variables. that sucks, but the alternative is to have some card
        # effects take an additional parameter for which color or penalty list
        # they're going to affect, which seems much more disruptive.
        # another issue is special-casing for exek and shld, since you can't
        # just run fast effects before checking due to the ww issue, and 
        # because we can't let wilds of any kind change the color and then get
        # dismissed as invalid moves. come to think of it, what does happen in
        # v&7 if someone exeks and then has no penalties? nothing good, i bet
        # (errata: it's ok in v&7...because all exek does is change the false
        # color to purple. not that that's /good/ behavior lol. but also we
        # /can't/ just run the exek effect in sap-land because there's no way
        # to force it to only accept penalties/fast defensives...
        # we might need to add a 'defensiveEffect' flag just to deal with 
        # sap...exek, shld, and skip (at least) should all be playable, but
        # only if their effects are fast enough to actually deflect the
        # penalty (so check speed >= 1 as well as defensiveEffect) and also
        # we can't even attempt to play other cards before screening them out
        # due to w and p color effects and fast card effects. what a mess lol
        # is sap itself in defensiveEffect territory? i think the only way to
        # use it for deflection is via fast-skip...oh, or with oub. that's
        # pretty silly, so yeah i think it's in. though idk if the oub thing
        # would actually work. it /is/ processed mid-turn in the case of
        # drawing, so i can see an argument that it should also be after an
        # inner sap application resolves as well. the basic paradigm there
        # being that, after being oubed, a player should not get to play or
        # draw any more cards until being un-oubed.
        # oh, another awkward fact is that wilds in sap talk about choosing the
        # false color in v&7. which means we can't just store the penalty list
        # and run the play loop as if nothing happened...

        # so i think there are two basic choices here:
        # a) drop a ton of special-casing in ub (isLegalPlay and applyPenalties
        # at least) and both card (exe) and color (w, p) effects and try to
        # re-use everything while storing the old false color, top card, and
        # penalties (and prev color for purple? ugh) via some kind of global
        # ub.isSelfApplying flag
        # b) rebuild the run loop here with special-casing as in v&7, which
        # at least means all the special-casing will be in one location in the
        # code, but which would involve horrible hacks like not calling the
        # exe or w/p effects directly, which would be incompatible with those
        # effects potentially being changed by other cards
        # and i don't like either of them...
        raise NotImplementedError


class CardTypeExecute(CardType):

    def playEffect(self, ub):
        # TODO: after you finish this, remember defensiveEffect = True
        raise NotImplementedError


# Subclass for cards that can be applied as a penalty.
class CardTypePenalty(CardType):

    # Effect of this card being applied as as a penalty.
    def penalty(self, player, ub):
        raise NotImplementedError


# Subclasses for drawing-based penalty card types
class CardTypeDraw(CardTypePenalty):

    def __init__(
        self, 
        name,
        numCards,
        strength=0,
        speed=0,
    ):
        super(CardTypeDraw, self).__init__(name, strength, speed)
        self.numCards = numCards


    def penalty(self, player, ub):
        ub.say("{} drew {} cards!".format(player, num2words(self.numCards)))
        player.draw(self.numCards)


class CardTypeDrawIdentical(CardTypeDraw):

    def penalty(self, player, ub):
        ub.say("{} drew {} cards!".format(player, num2words(self.numCards)))
        player.draw(1)
        player.draw(self.numCards - 1, player.hand[-1])


# Subclasses for other penalty card types
class CardTypeBEARS(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeTradeHands(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeWillOWisp(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeWhiteBlindness(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeColonyCollapse(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeOubliette(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeFirestorm(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeDread(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeReveal(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeBlackPlague(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeNeutralize(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeDouble(CardTypePenalty):

    def penalty(self, player, ub):
        # TODO: be careful with this one, just doubling the rest of the list
        # leads to an infinite loop if there's another double there. how did
        # v&7 handle this?
        raise NotImplementedError


class CardTypeLoveCanal(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeGroundswell(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


class CardTypeHerring(CardTypePenalty):

    def penalty(self, player, ub):
        raise NotImplementedError


# Initialize the standard card types
def initCardTypes():
    cardTypes = {}

    cardTypes['0'] = CardType(
        name='0',
    )

    cardTypes['2'] = CardType(
        name='2',
    )

    cardTypes['3'] = CardType(
        name='3',
    )

    cardTypes['4'] = CardType(
        name='4',
    )

    cardTypes['5'] = CardType(
        name='5',
    )

    cardTypes['6'] = CardType(
        name='6',
    )

    cardTypes['7'] = CardType(
        name='7',
    )

    cardTypes['8'] = CardType(
        name='8',
    )

    cardTypes['9'] = CardType(
        name='9',
    )

    cardTypes['13'] = CardType(
        name='13',
    )

    cardTypes['18'] = CardType(
        name='18',
    )

    cardTypes['27'] = CardType(
        name='27',
    )

    cardTypes['49'] = CardType(
        name='49',
    )

    # This is for the standard wild card (w).
    cardTypes[''] = CardType(
        name='',
    )

    cardTypes['sk'] = CardTypeSkip(
        name='sk',
        speed=-1,
        defensiveEffect=True,
    )

    cardTypes['rv'] = CardTypeReverse(
        name='rv',
    )

    cardTypes['dall'] = CardTypeDiscardAll(
        name='dall',
    )

    cardTypes['shd'] = CardTypeShuffleDeck(
        name='shd',
    )

    cardTypes['qsu'] = CardTypeQueueSubmit(
        name='qsu',
    )

    cardTypes['shld'] = CardTypeShield(
        name='shld',
        speed=1,
        defensiveEffect=True,
    )

    cardTypes['w'] = CardTypeMultipleWild(
        name='w',
        speed=2,
        iterations=2,
    )

    cardTypes['wwww'] = CardTypeMultipleWild(
        name='wwww',
        speed=2,
        iterations=5,
    )

    cardTypes['pur'] = CardTypePurple(
        name='pur',
        strength=2,
    )

    cardTypes['d2'] = CardTypeDraw(
        name='d2',
        numCards=2,
    )

    cardTypes['d3'] = CardTypeDraw(
        name='d3',
        numCards=3,
    )

    cardTypes['d4'] = CardTypeDraw(
        name='d4',
        numCards=4,
    )

    cardTypes['d4i'] = CardTypeDrawIdentical(
        name='d4i',
        numCards=4,
    )

    return cardTypes

