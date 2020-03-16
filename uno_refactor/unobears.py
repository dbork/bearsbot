from card import Card
from cardtype import CardType, initCardTypes
from color import Color, initColors
from deck import initDecks
from player import Player, initPlayers

import copy
import ircmessage
import random
import traceback

# Top-level UnoBEARS class representing the complete game state, though we have 
# to violate encapsulation somewhat to allow the game to communicate with IRC.
# 
# s (Session): The IRC session object.
# chan (str): The IRC channel name.
# players (list(Player)): The list of players.
# cardTypes (dict(CardType)): The currently defined card types.
# colors (dict(Color)): The currently defined colors.
# topCard (Card): The top card in the discard pile.
# discard (list(Cards)): The rest of the discard pile.
# currentColor (Color): The current color.
# debug (bool): If true, the game is played in single-player in the terminal.

class UnoBEARS:

    def __init__(
        self,
        s,
        chan,
        playerNames,
        debug,
    ):
        self.s = s
        self.chan = chan
        self.cardTypes = initCardTypes()
        self.colors = initColors()
        self.decks = initDecks(self.cardTypes, self.colors)
        self.players = initPlayers(playerNames, self.decks['standard'])
        self.topCard = copy.copy(random.choice(self.decks['standard']))
        self.discard = []

        if self.topCard.color == self.colors['w']:
            self.currentColor = random.choice([
                colors['b'],
                colors['r'],
                colors['y'],
                colors['g'],
            ])
        else:
            self.currentColor = self.topCard.color

        self.debug = debug


    # Publicly say something in IRC.
    def say(self, message):
        if self.debug:
            print ircmessage.unstyle(message)
        else:
            s.send("PRIVMSG {} :{} \r\n".format(self.chan, message))


    # Private-message a player in IRC.
    def pm(self, message, player):
        if self.debug:
            self.say(ircmessage.unstyle("(PM {}): {}".format(player, message)))
        else:
            s.send("PRIVMSG {} :{} \r\n".format(player, message))


    # Publicly ask a player something in IRC, accepting when the response
    # satisfies a certain condition.
    def ask(self, message, player, acceptIf=None, rejectPrompt=None):
        raise NotImplementedError()


    # Send a player their hand.
    def pmHand(self, player):
        self.pm(player.handToStr(), player)


    # Check whether a player's input is a legal play.
    def isPlayLegal(self, response):
        raise NotImplementedError()


    # Check for victory
    def wincon(self, player):
        if len(players[0].hand) == 0:
            self.say("{} has won the game! They are eaten by bears as " \
                     "congratulations!".format(players[0]))
            return True
        return False


    # Main run loop
    def run(self):
        self.say("Welcome to UnoBEARS! Type the card you'd like to play.")
        self.say("Type draw to draw a card. Type UNO when you or another " \
                 "player has one card left.")
        self.say("The top card of the discard pile is {}.".format(self.topCard))
        self.say("The current color is {}.".format(self.currentColor))
        for player in self.players:
            self.pmHand(player)

        while True:
            self.say("Hand sizes are: ")
            for player in self.players:
                self.say("{}: {} cards".format(player, len(player.hand)))

            self.ask(
                message="{}, what will you play?".format(self.players[0]),
                player=self.players[0],
                acceptIf=self.isPlayLegal,
                rejectPrompt="Invalid move."
            )

            if self.wincon(players[0]):
                return

            players = players[1:] + players[0]


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

