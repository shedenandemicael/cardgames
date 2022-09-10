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
    player, players = placeBets(hands, player, players)

    # Betting on the flop
    if players > 1:
        flop = deck[players * 2 + 1:players * 2 + 4]
        updateHands(hands, flop)
        print(gradeHands(hands[0].hand))
        print(hands[0].hand)
        player, players = placeBets(hands, player, players)

    # Betting on the turn
    if players > 1:
        turn = list(deck[players * 2 + 6])
        print(turn)
        updateHands(hands, turn)
        print(gradeHands(hands[0].hand))
        print(hands[0].hand)
        player, players = placeBets(hands, player, players)

    # Betting on the river
    if players > 1:
        river = deck[players * 2 + 8]
        updateHands(hands, river)
        print(gradeHands(hands[0].hand))
        print(hands[0].hand)
        player, players = placeBets(hands, player, players)

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
    while players > 1 and (hands[player].playerBet != currentBet or turns < players):
        decision = input("what will you do? ")
        player, players = handDecision(decision, hands, player, players)
        if player == players - 1:
            player = 0
        else:
            player += 1
        turns += 1

    # Reset bets
    for hand in hands:
        hand.playerBet = 0
    currentBet = 0
    return 0, players


def handDecision(decision, hands, player, players):

    global currentBet
    global pot

    if decision == "call":
        pot += (currentBet - hands[player].playerBet)
        hands[player].stack -= (currentBet - hands[player].playerBet)
        hands[player].playerBet = currentBet
    
    elif decision == "fold":
        hands.pop(player)
        player -= 1
        players -= 1

    elif decision == "raise":
        raiseAmount = int(input("raise amount? "))
        hands[player].stack -= (raiseAmount - hands[player].playerBet)
        pot += (raiseAmount - hands[player].playerBet)
        currentBet = hands[player].playerBet = hands[player].playerBet + raiseAmount

    elif decision == "bet":
        currentBet = hands[player].playerBet = betAmount = int(input("bet amount? "))
        hands[player].stack -= betAmount
        pot += betAmount

    elif decision == "check":
        return player, players

    return player, players


def updateHands(hands, round):

    # Adding community cards to players' hands
    if len(round) == 3:
        for player in hands:
            player.hand += round
    else:
        for player in hands:
            player.hand.append(round)


def gradeHands(hand):
    
    handRanking = ('royal flush', 'straight flush', 'four of a kind', 'full house', 
    'flush', 'staight', 'three of a kind', 'two pair', 'pair', 'high card')
    suit = {}
    number = {}
    for card in hand:

        # Counts the number of cards for each suit
        if suit.get(card[0]) == None:
            suit[card[0]] = 1
        else:
            suit[card[0]] += 1

        # Counts the number of cards for each number
        if number.get(card[1]) == None:
            number[card[1]] = 1
        else:
            number[card[1]] += 1

    suit = dict(sorted(suit.items(), key=lambda x: x[1], reverse=True))
    number = dict(sorted(number.items(), key=lambda x: x[1], reverse=True))

    numVal = list(number.values())
    numKeys = list(number.keys())
    suitVal = list(suit.values())

    # Royal flush, straight flush
    if list(suitVal)[0] >= 5:

        if all(x in numKeys for x in ['T', 'J', 'Q', 'K', 'A']):
            return "royal flush"

        # Length of numbers - 4
        for i in range(9):
            if all(x in numKeys for x in [numbers[i], numbers[i+1], numbers[i+2], numbers[i+3], numbers[i+4]]):
                return "straight flush"
    
    if numVal[0] == 4:
        return "four of a kind"

    if all(x in numVal for x in [3, 4]):
        return "full house"

    if suitVal[0] >= 5:
        return "flush"

    for i in range(9):
            if all(x in numKeys for x in [numbers[i], numbers[i+1], numbers[i+2], numbers[i+3], numbers[i+4]]):
                return "straight"

    if 3 in numVal:
        return "three of a kind"
    
    if numVal[0] == 2 and numVal[1] == 2:
        return "two pair"

    if 2 in numVal:
        return "pair"

    return "high card"

if __name__ == '__main__':
    main()