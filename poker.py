from mechanics import fillDeck, dealCards, placeBets, updateHands, determineWinner
from flask import Flask, render_template, request, redirect, jsonify
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

class Game(Resource):
    def get(self):
        d



@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return redirect("/game")


@app.route("/game")
def game():
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

    return render_template("game.html", winner=determineWinner(hands))


if __name__ == '__main__':
    main()