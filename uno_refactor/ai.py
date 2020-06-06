from player import Player

# Class representing an AI player.
# 
# choosePlay (fn: UnoBEARS -> str): Function to choose which card to play.
# chooseColor (fn: UnoBEARS -> str): Function to change the color.
# chooseGoodCard (fn: UnoBEARS -> str): Function to choose a good card.
# chooseBadCard (fn: UnoBEARS -> str): Function to choose a bad card to get rid
#   of via, eg, qsub or frstr
# chooseImprovableCard (fn: UnoBEARS -> str): Function to choose a card with
#   a good type but a bad color to improve with, eg, purp

class AI(Player):

    def __init__(
        self,
        name,
        deck,
        choosePlay,
        chooseColor,
        chooseGoodCard,
        chooseBadCard,
        chooseImprovableCard,
    ):
        Player.__init__(self, name, deck)
        self.choosePlay = choosePlay
        self.chooseColor = chooseColor
        self.chooseGoodCard = chooseGoodCard
        self.chooseBadCard = chooseBadCard
        self.chooseImprovableCard = chooseImprovableCard

