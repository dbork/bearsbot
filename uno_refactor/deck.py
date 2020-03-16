from card import cardFromString

# Initialize the standard decks.
def initDecks(types, colors):
    decks = {}

    standardDeck = ['6b']
    decks['standard'] = [
        cardFromString(string, types, colors) for string in standardDeck
    ]

    return decks

