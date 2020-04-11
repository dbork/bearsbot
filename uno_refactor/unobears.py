from collections import deque
import copy
from decimal import Decimal
import ircmessage
import random
import traceback

from ai import AI
from area import initAreas
from card import Card
from cardtype import CardType, CardTypePenalty, initCardTypes
from color import Color, initColors
from player import Player, initPlayers

# Top-level UnoBEARS class representing the complete game state, though we have 
# to violate encapsulation somewhat to allow the game to communicate with IRC.
# 
# s (Session): The IRC session object.
# chan (str): The IRC channel name.
# players (list(Player)): The list of players.
# currentPlayer (Player): The player whose turn it is.
# cardTypes (dict(CardType)): The currently defined card types.
# colors (dict(Color)): The currently defined colors.
# areas (dict(Area)): The currently defined areas.
# topCard (Card): The top card in the discard pile.
# discard (list(Cards)): The discard pile. 
#   TODO: Note, however, that certain cards (such as dall) can discard other 
#   cards mid-turn, so it's not always true that topCard == discard[0].
# currentColor (Color): The current color.
# penaltyQueue (collections.deque): The queue of penalty cards that will be 
#   applied to the current player if they do not play a penalty card.
# jobQueue (collections.deque): A secondary queue that accumulates cards
#   submitted by qsu cards and then expels them into a player's hand.
# jobQueueTime (int): Turns remaining until the jobQueue completes.
# debug (bool): If true, the game is played in single-player in the terminal.

class UnoBEARS(object):

    def __init__(
        self,
        s,
        chan,
        playerNames,
        debug,
    ):
        self.s = s
        self.chan = chan
        self.debug = debug

        self.cardTypes = initCardTypes()
        self.colors = initColors()
        self.areas = initAreas(self)
        self.players = initPlayers(playerNames, self.areas['standard'])
        self.currentPlayer = self.players[0]
        self.topCard = self.areas['standard'].drawOne(luck=Decimal(0))
        self.discard = [self.topCard]
        self.penaltyQueue = deque([])
        self.jobQueue = deque([])
        self.jobQueueTime = 0

        if self.topCard.color == self.colors['w']:
            self.currentColor = random.choice([
                self.colors['b'],
                self.colors['r'],
                self.colors['g'],
                self.colors['y'],
            ])
        else:
            self.currentColor = self.topCard.color


    # Publicly say something in IRC.
    def say(self, message):
        if message:
            if self.debug:
                print ircmessage.unstyle(message)
            else:
                s.send("PRIVMSG {} :{} \r\n".format(self.chan, message))


    # Private-message a player in IRC.
    def pm(self, message, player):
        if self.debug:
            self.say(ircmessage.unstyle("(PM {}): {}".format(player, message)))
        else:
            # If we didn't check this, players could change their IRC nick to
            # the AI's name to see their hand.
            if not isinstance(player, AI):
                s.send("PRIVMSG {} :{} \r\n".format(player, message))


    # Publicly ask a player something in IRC, accepting when the response
    # satisfies a certain condition.
    def ask(self, message, player):
        if isinstance(player, AI):
            self.say(message)
            response = None
        else:
            if self.debug:
                if message:
                    response = raw_input(message + " ")
                else:
                    response = raw_input()
            else:
                self.say(message)
                response = None

                # IRC boilerplate
                while not response:
                    # TODO: is this going to drop inputs if we don't make
                    # readbuffer a class variable? eg if you play w and choose
                    # a color before bearsbot has time to catch up... i hope
                    # not, since colorChoice was its own function in v&7 also
                    readbuffer = ""
                    readbuffer = readbuffer + s.recv(1024)
                    rbSplit = string.split(readbuffer, "\n")
                    readbuffer = rbSplit.pop()

                    for line in rbSplit:
                        line = string.rstrip(line)
                        line = string.split(line)
                        print line

                        if (line[0] == "PING"):
                            s.send("PONG %s\r\n" % line[1])
                        elif 'PRIVMSG' in line:
                            user = line[0].lstrip(':')
                            user = user.split('!')[0]

                            # TODO: when we test IRC integration, make sure
                            # this blocks other players from answering
                            if user == player.name:
                                response = line[3].lstrip(':').lower()

            return response


    # Send a player their hand.
    def pmHand(self, player):
        self.pm("Your hand is {}".format(player.handToStr()), player)


    # Helper function for constructing a card from a string, if the string
    # is the concatenation of a defined card type and a defined color.
    def cardFromString(self, string):
        return Card(
            cardType=self.cardTypes[string[:-1]],
            color=self.colors[string[-1]],
        )


    # Check whether a given card can be played on a given card type and color.
    def isLegalPlay(self, playedCard, cardType, color):
        # As in standard UNO, only one of the color and type checks
        # need to be satisfied for a card to be playable.
        return (playedCard.cardType.playCheck(cardType)
            or playedCard.color.playCheck(color)
            or color.playOnCheck(playedCard.color))


    # Apply all penalties in the penalty list to a player, unless they can
    # deflect them with a shield.
    def applyPenalties(self, player):
        if self.currentPlayer.shield > 0:
            self.say(
                "{}'s shield deflected the penalty!".format(
                    self.currentPlayer
                )
            )
            self.say(
                "Penalty list is {}".format(
                    " ".join(map(str, self.penaltyQueue))
                )
            )
            self.currentPlayer.shield -= 1
        else:
            self.say("{} incurred the penalty!".format(player))
            while self.penaltyQueue:
                card = self.penaltyQueue.popleft()
                card.cardType.penalty(player, self)


    # Do the current player's turn. This operates on self.currentPlayer rather
    # than taking a player as input because some cards (notably skip) can
    # change this mid-turn
    def doTurn(self):
        while 1:
            response = self.ask(
                message="{}, what will you play?".format(self.currentPlayer),
                player=self.currentPlayer,
            )
             
            if isinstance(self.currentPlayer, AI):
                response = self.currentPlayer.choosePlay(self)

            if response in ['d', 'draw']:
                self.say("{} draws a card.".format(self.currentPlayer))

                # The maximum hand size applies only to manual draws, which
                # is bad behavior from v&7 reimplemented for patch stealth.
                # TODO: remove this when emma figures it out, ideally by
                # moving it to the player class's draw function
                # TODO: quality of life improvement: implement 'd [card]' to
                # draw until you get a certain card (for use at the max hand
                # size, mostly)
                if len(self.currentPlayer.hand) >= 30:
                    self.say(
                        "{} exceeds the maximum hand size.".format(
                            self.currentPlayer
                        )
                    )
                    self.currentPlayer.hand = self.currentPlayer.hand[:29]

                self.currentPlayer.draw(1)

                if self.penaltyQueue:
                    self.applyPenalties(self.currentPlayer)

                self.pmHand(self.currentPlayer)
                continue

            card = self.currentPlayer.getCardFromHand(response)
            if card:
                if self.isLegalPlay(
                    card, 
                    self.topCard.cardType, 
                    self.currentColor
                ):
                    # Don't remove the card from the player's hand unless it
                    # was actually a legal play.
                    self.currentPlayer.discard(ub=self, card=card)

                    # This is as late as a card effect can occur: just after
                    # the next player chooses a card. Thus, if skip had speed
                    # -2, the next player would get to pick a card before
                    # being skipped, which the following player would then be
                    # forced to effectively play.
                    if self.topCard.cardType.speed <= -2:
                        self.topCard.cardType.playEffect(self)

                    # Change the top card and current color to reflect the
                    # card that was just played.
                    self.topCard = card
                    self.prevColor = self.currentColor
                    self.currentColor = self.topCard.color

                    # Very fast card effects, such as wwwww, occur immediately.
                    if self.topCard.cardType.speed >= 2:
                        self.topCard.cardType.playEffect(self)

                    # Do the color effect before publicly stating the top card
                    # and color, to allow wilds to change the color
                    self.topCard.color.playEffect(self)

                    self.say(
                        "The top card of the discard pile is {}.".format(
                            self.topCard
                        )
                    )
                    self.say(
                        "The current color is {}.".format(self.currentColor)
                    )

                    # Fast card effects, such as exek, occur before penalties
                    # are evaluated.
                    if self.topCard.cardType.speed == 1:
                        self.topCard.cardType.playEffect(self)

                    # If there is a penalty queue, the player must play a
                    # penalty card, or all the penalties will be incurred.
                    if isinstance(self.topCard.cardType, CardTypePenalty):
                        self.penaltyQueue.append(self.topCard)
                        self.say(
                            # Calling this a 'penalty list' is v&7 behavior,
                            # but is too prominent to change for now
                            "Penalty list is {}".format(
                                " ".join(map(str, self.penaltyQueue))
                            )
                        )

                    elif self.penaltyQueue:
                        self.applyPenalties(self.currentPlayer)

                    # By default, card effects come after the update and any 
                    # penalties, mostly to emulate v&7 behavior. Unlike in v&7,
                    # however, this is captured by the notion of effect speed.
                    if self.topCard.cardType.speed == 0:
                        self.topCard.cardType.playEffect(self)

                    return

            # TODO: handle response == 'quit'?
            self.say("Invalid move.")


    # Check for victory
    def wincon(self, player):
        if len(player.hand) == 0:
            return True
        else:
            return False


    # Main run loop
    def run(self):
        self.say("Welcome to UnoBEARS! Type the card you'd like to play.")
        self.say("Type draw to draw a card. Type UNO when you or another " \
                 "player has one card left.")
        for player in self.players:
            self.pmHand(player)

        # Code duplication here is intended to preserve patch stealth by
        # emulating the following bad behavior of v&7: for every turn other
        # than the first, the player about to play is the last one to have
        # their hand size printed.
        # TODO: except for when a reverse card is played :( ...although, you
        # know, i think i'm going to keep that one out as a hint that
        # something has changed, and also because it's awful
        # TODO: remove this when emma figures it out
        self.say(
            "The top card of the discard pile is {}.".format(self.topCard)
        )
        self.say("The current color is {}.".format(self.currentColor))
        self.say("Hand sizes are:")
        for player in self.players:
            self.say("{}: {} cards".format(player, len(player.hand)))

        while True:
            self.doTurn()

            # Win condition should be checked before hand sizes are printed
            # and the last player's updated hand is PMed to avoid printing or
            # PMing a hand size of 0.
            if self.wincon(self.currentPlayer):
                self.say(
                    "{} has won the game! They are eaten by bears as " \
                    "congratulations!".format(self.currentPlayer)
                )
                return

            # Update the job queue after checking the win condition, to avoid
            # wins being snatched away due to the queue completing.
            if self.jobQueueTime > 0:
                self.jobQueueTime -= 1
                if self.jobQueueTime == 0:
                    while self.jobQueue:
                        self.say("Job complete.")
                        self.currentPlayer.draw(1, self.jobQueue.popleft())

            self.pmHand(self.currentPlayer)

            self.say("Hand sizes are:")
            for player in self.players:
                self.say("{}: {} cards".format(player, len(player.hand)))

            self.players = self.players[1:] + [self.players[0]]
            self.currentPlayer = self.players[0]

            # Slow card effects, such as skip, take place just after the turn,
            # thus affecting the next player just before their turn starts.
            if self.topCard.cardType.speed == -1:
                self.topCard.cardType.playEffect(self)


# debug mode
if __name__ == '__main__':
    UnoBEARS(
        s=None,
        chan=None,
        playerNames=[
            #TODO
            'player1',
            'player2',
        ],
        debug=True,
    ).run()

