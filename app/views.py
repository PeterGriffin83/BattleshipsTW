import sys

from app import app
from config import flaskOptions, mapSize
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from game import game

__author__ = "Peter Griffin <peter_griffin@hotmail.com>, <peter.g@playbasis.com>"
__version__= 0.2
__description__ = "views file for Battleships. Controls API routes and responses (JSON)"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.game = game()

@app.route("/api/new_game")
@cross_origin()
def new_game():
	#response = { 'status': 200, 'message': 'New Game'}
	response = app.game.newGame()
	print app.game.printBoard()
	return jsonify(response)


@app.route("/api/shot/<int:x>/<int:y>")
@cross_origin()
def takeAShot(x, y):
	if x < 0 or x >= mapSize[0] or \
	   y < 0 or y >= mapSize[1]:
		errMsg = 'The coordinates you chose were out of bounds. Please select coordinates between X: %s-%s and Y: %s-%s' % (0, mapSize[0], 0, mapSize[1])
		response = {'status': 500, 'message': errMsg}
		return jsonify(response)

	response = app.game.hitOrMissAPI(x,y)

	return response

@app.route("/api/debug/newMongo")
def newMongo():
	m_id = app.game.newMongo()
	return m_id

@app.route("/api/debug/playerMoves")
def getPlayerMoves():
	moves = app.game.getPlayerMoves()
	response = {'Status': 200, 'moves': moves }
	return jsonify(response)

@app.route("/api/debug/mapSize")
def getBoard():
	board = app.game.getBoard()
	
	response = {'status': 200, 'X': len(board[0]), 'Y': len(board) }
	return jsonify(response)

if __name__ == '__main__':
	app.run(host=flaskOptions['host'], port=flaskOptions['port'], debug=flaskOptions['debug'])
