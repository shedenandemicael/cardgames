from random import shuffle


suits = ('diamond', 'heart', 'spade', 'club')
numbers = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
pot = 0
currentBet = 0
bigBlind = 20
stackSize = 1000

def main():

    deck = fillDeck()
    players = int(input("how many player? "))
    while players < 3 and players > 8:
        players = int(input("how many player? "))
    hands = dealCards(deck, players)
    player = 2
    placeBets(hands, player, players)
    flop = deck[players * 2 + 1:players * 2 + 4]
    turn = deck[players * 2 + 6]
    river = deck[players * 2 + 8]


class Player:

    playerBet = 0
    hand = []
    stack = stackSize
    

def fillDeck():

    deck = []
    for suit in suits:
        for number in numbers:
            deck.append([suit, number])
    shuffle(deck)
    return deck


def dealCards(deck, players):

    global currentBet
    hands = []
    for i in range(players):

        bet = 0
        if i == 0:
            bet = bigBlind // 2
        elif i == 1:
            bet = bigBlind
        
        player = Player()
        player.hand = [deck[i], deck[i + players]]
        player.playerBet = bet
        hands.append(player)

    currentBet = bigBlind
    return hands


def placeBets(hands, player, players):

    while hands[player].playerBet != currentBet:
        decision = input("what will you do? ")
        player, players = handDecision(decision, hands, player, players)
        print(player)
        print(players)
        if player == players - 1:
            player = 0
        else:
            player += 1


def handDecision(decision, hands, player, players):

    global currentBet
    if decision == "call":
        hands[player].playerBet = currentBet
    
    elif decision == "fold":
        hands.pop(player)
        player -= 1
        players -= 1

    elif decision == "raise":
        raiseAmount = int(input("raise amount "))
        currentBet = hands[player].playerBet = hands[player].playerBet + raiseAmount
    
    return player, players
        
if __name__ == '__main__':
    main()