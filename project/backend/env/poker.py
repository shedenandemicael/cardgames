from mechanics import fillDeck, dealCards, placeBets, updateHands, determineWinner
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
import firebase_admin
from firebase_admin import firestore

# Application Default credentials are automatically created.
firebaseApp = firebase_admin.initialize_app()
db = firestore.client()

app = Flask(__name__)
api = Api(app)


deck = fillDeck()
players = int(input("how many player? "))
while players < 3 and players > 8:
    players = int(input("how many player? "))
hands = dealCards(deck, players)
cardData = {}
for index, player in enumerate(hands):
    cardData[index] = [player.hand]

doc_ref = db.collection(u'gameData').document(u'cards')
doc_ref.set({cardData})

doc_ref = db.collection(u'gameData').document(u'bets')
doc_ref.set({})

users_ref = db.collection(u'gameData')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')


@app.get('/api/cards')
def cards():
    return cardData

@app.get('/api/bets')
def bets():
    bets = {}
    return bets

@app.route("/", methods=["GET", "POST"])
def index():
    # Game setup
    deck = fillDeck()
    players = int(input("how many player? "))
    while players < 3 and players > 8:
        players = int(input("how many player? "))
    hands = dealCards(deck, players)
    cardData = {}
    for index, player in enumerate(hands):
        cardData[index] = [player.playerBet, player.stack, player.hand]
    return cardData

@app.route("/game")
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
        player, players = placeBets(hands, player, players)

    # Betting on the turn
    if players > 1:
        turn = deck[players * 2 + 6]
        updateHands(hands, turn)
        player, players = placeBets(hands, player, players)

    # Betting on the river
    if players > 1:
        river = deck[players * 2 + 8]
        updateHands(hands, river)
        player, players = placeBets(hands, player, players)

    return render_template("./game.html", winner=determineWinner(hands))
