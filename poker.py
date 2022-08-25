from random import shuffle


suits = ('diamond', 'heart', 'spade', 'club')
numbers = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')


def main():

    deck = fillDeck()
    players = int(input("how many player? "))
    while players < 2 and players > 8:
        players = int(input("how many player? "))
    hands = dealCards(deck, players)
    flop = deck[player * 2 + 1:player * 2 + 4]
    turn = deck[player * 2 + 6]
    river = deck[player * 2 + 8]


def fillDeck():

    deck = []
    for suit in suits:
        for number in numbers:
            deck.append([suit, number])
    shuffle(deck)
    return deck


def dealCards(deck, players):

    hands = []
    for i in range(players + 1):
        hands.append([deck[i], deck[i + players]])
    return hands


if __name__ == '__main__':
    main()