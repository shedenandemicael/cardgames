from random import shuffle

suits = ('diamond', 'heart', 'spade', 'club')
numbers = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
currentBet = 0
bigBlind = 20
stackSize = 1000
pot = bigBlind + (bigBlind // 2)

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
        player = Player()
        player.hand = [deck[i], deck[i + players]]
        hands.append(player)
    flop = deck[players * 2 + 1:players * 2 + 4]
    turn = deck[players * 2 + 6]
    river = deck[players * 2 + 8]
    updateHands(hands, flop)
    updateHands(hands, turn)
    updateHands(hands, river)
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
            return 0, 12

        # Length of numbers - 4
        for i in range(9):
            straightLength = 0
            for x in [numbers[i], numbers[i+1], numbers[i+2], numbers[i+3], numbers[i+4]]:
                if x in numKeys:
                    straightLength += 1
            if straightLength == 5:
                return 1, numbers.index(numbers[i+4])
    
    # Four of a kind
    if numVal[0] == 4:
        return 2, numbers.index(numKeys[0])

    # Full house
    if all(x in numVal for x in [3, 4]):
        return 3, numbers.index(numKeys[0])

    # Flush
    if suitVal[0] >= 5:
        return 4, numbers.index(numKeys[0])

    # Straight
    for i in range(9):
            straightLength = 0
            for x in [numbers[i], numbers[i+1], numbers[i+2], numbers[i+3], numbers[i+4]]:
                if x in numKeys:
                    straightLength += 1
            if straightLength == 5:
                return 5, numbers.index(numbers[i+4])

    # Three of a kind
    if 3 in numVal:
        return 6, numbers.index(numKeys[0])
    
    # Two pair
    if numVal[0] == 2 and numVal[1] == 2:
        if numbers.index(numKeys[0]) > numbers.index(numKeys[1]):
            return 7, numbers.index(numKeys[0])
        else:
            return 7, numbers.index(numKeys[1])

    # Pair
    if 2 in numVal:
        return 8, numbers.index(numKeys[0])

    # High card
    highCard = 0
    for num in numKeys:
        if numbers.index(num) > highCard:
            highCard = numbers.index(num)
    return 9, highCard

def determineWinner(hands):

    playerGrades = []
    tieBreaker = []
    for hand in hands:
        gradedHand = gradeHands(hand.hand)
        playerGrades.append(gradedHand[0])
        tieBreaker.append(gradedHand[1])

    tiedPlayers = [index for index, x in enumerate(playerGrades) if x == min(playerGrades)]
    if len(tiedPlayers) == 1:
        return tiedPlayers[0]
    
    winner = []
    for p in tiedPlayers:
        if len(winner) == 0:
            winner.append(p)
        elif tieBreaker[p] > tieBreaker[winner[0]]:
            winner[0] = tieBreaker
        elif tieBreaker[p] == tieBreaker[winner[0]]:
            winner.append(tieBreaker[p])

    return winner