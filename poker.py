from random import shuffle


suits = ('diamond', 'heart', 'spade', 'club')
numbers = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
currentBet = 0
bigBlind = 20
stackSize = 1000
pot = bigBlind + (bigBlind // 2)

def main():

    # Game setup
    deck = fillDeck()
    players = int(input("how many player? "))
    while players < 3 and players > 8:
        players = int(input("how many player? "))
    hands = dealCards(deck, players)

    # Pre-flop betting begins after big blind
    player = 2
    player = placeBets(hands, player, players)

    # Betting on the flop
    flop = deck[players * 2 + 1:players * 2 + 4]
    updateHands(hands, flop)
    player = placeBets(hands, player, players)

    # Betting on the turn
    turn = deck[players * 2 + 6]
    updateHands(hands, turn)
    player = placeBets(hands, player, players)

    # Betting on the river
    river = deck[players * 2 + 8]
    updateHands(hands, river)
    player = placeBets(hands, player, players)


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

    # Ensures everyone goes at least once
    global currentBet
    turns = 0
    while hands[player].playerBet != currentBet or turns < players:
        decision = input("what will you do? ")
        player, players = handDecision(decision, hands, player, players)
        if player == players - 1:
            player = 0
        else:
            player += 1
        turns += 1
        print(player)

    # Reset bets
    for hand in hands:
        hand.playerBet = 0
    currentBet = 0
    return 0


def handDecision(decision, hands, player, players):

    global currentBet
    global pot

    if decision == "call":
        pot += (currentBet - hands[player].playerBet)
        hands[player].playerBet = currentBet
    
    elif decision == "fold":
        hands.pop(player)
        player -= 1
        players -= 1

    elif decision == "raise":
        raiseAmount = int(input("raise amount? "))
        pot += (raiseAmount - hands[player].playerBet)
        currentBet = hands[player].playerBet = hands[player].playerBet + raiseAmount

    elif decision == "bet":
        currentBet = hands[player].playerBet = betAmount = int(input("bet amount? "))
        pot += betAmount

    elif decision == "check":
        return player, players

    return player, players


def updateHands(hands, round):

    # Adding community cards to players' hands
    for player in hands:
        player.hand.append(round)
        

if __name__ == '__main__':
    main()