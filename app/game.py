import pprint
from config import mapSize, gamePieces, database
from flask import jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from random import randint
import sys

__author__ = "Peter Griffin <peter_griffin@hotmail.com>, <peter.g@playbasis.com>"
__version__= 0.2
__description__ = "Core game class for Battleships. Handles grid and ship generation, hit detection, and end-game (win) conditions"

class game(object):

	def __init__(self):
		'''
		The Game Class constructor.

		Generates a new board, generates an array of Ships, and places those ships on the board.  
		Ships and Board Size are customization in the config.py file. 	

		Also sets up the Mongo connection. 
		
		'''
		self.battleBoard = self.generateBoard()
		self.completedGame = False
		self.playerMoves = 0

		self.mongo = MongoClient(database['host'], database['port'], serverSelectionTimeoutMS=database['timeout'])
		self.db = database['database']

		try:
			self.gameID = self.newGameId()
		except ServerSelectionTimeoutError:
			print "Error: Please ensure Mongo is running, and is accessible at %s on port %s " % (database['host'], database['port'])
			sys.exit()
			
		self.shipPositions = {}
		for item in gamePieces:
			self.shipPositions[item] = {}
			for count in range(gamePieces[item]['count']):
				#print item, count
				self.shipPositions[item][count] = []
			
		self.placeShips()

	def newGame(self):
		'''
		The Game Class constructor.

		Generates a new board, generates an array of Ships, and places those ships on the board.  
		Ships and Board Size are customization in the config.py file. 	
		
		'''
		self.playerMoves = 0
		self.completedGame = False
		self.battleBoard = self.generateBoard()
		self.gameID = self.newGameId()

		self.shipPositions = {}
		for item in gamePieces:
			self.shipPositions[item] = {}
			for count in range(gamePieces[item]['count']):
				#print item, count
				self.shipPositions[item][count] = []
			
		self.placeShips()
		response = {'status': 200, 'message':'New Game Ready'}
		return response
	
	def getBoard(self):
		return self.battleBoard
		
	def generateBoard(self):	
		'''
		generateBoard is called by the __init__ constructor and creates a X by Y array and zero-fills it.
		
		board size is customizable in the config.py file
		'''
		
		board = [["0" for x in range(mapSize[0])] for y in range(mapSize[1])] 
		return board
	
	
	
	def printBoard(self):
		'''
		printBoard is used during development and debugging. The API client has no visibility into this. 
		
		This method reads the board array and prints it out to screen.
		'''
		board = self.battleBoard
		pboard = ''
		
		for y in range(len(board)):
			line = ''
			for x in range(mapSize[0]):
				line += board[x][y] + " "
			pboard += line + "\r\n"
		return pboard

	def placeShips(self):
		'''
		placeShips is the main game logic for placing the various set pieces (ships) onto the board.
		It iterates across the gamePieces dictionary (from config) and then iterates across the number of pieces.

		For example, there are 4 submarine pieces. 
		
		For each piece of each ship type, this method then uses a pseudorandom number generator to provide a set of x,y
		coordinates and a orientation. 
		
		These are fed into the checkValidity method to check that this piece can be safely placed at those coordinates.

		If it cannot, the while(not valid) loop continues until it can. 
				
		Next this method places the ship in the place specified, in the orientation specified. 
		'''

		for item in gamePieces:
			for count in range(gamePieces[item]['count']):
				marker = gamePieces[item]['marker']
				size = gamePieces[item]['size']
				# print item, gamePieces[item]['marker'], gamePieces[item]['count']

				valid = False
				while(not valid):
					# Get coord to place Ship
					x, y, o = randint(0,mapSize[0]-1),randint(0,mapSize[1]-1), randint(0,9)

					if o >= 0 and o < 5:
						orientation = 'h'
					elif o >= 5 and o <= 9:
						orientation = 'v'
					
				
					valid = self.checkValidity(x,y,orientation,marker,size)
					

				# Valid position, add marker to Map Array, add ship coords to shipPosition array
				# Map array used for hit detection, Ship array used to ship sinking recognition.
				if orientation == 'h':
						for spot in range(x,x+size):
							self.battleBoard[spot][y] = marker
							coords = [ spot, y ]
							self.shipPositions[item][count].append(coords)

				elif orientation == 'v':
						for spot in range(y,y+size):
							self.battleBoard[x][spot] = marker
							coords = [ x, spot ]

							self.shipPositions[item][count].append(coords)
				

	def checkValidity(self, x, y, orientation, marker, size):
		'''
		Description: checkValidity accepts input of a set of coordinates, an orientation (horizontal/vertical), a marker (Ship designation. i.e Subs are 'S'), and a size, where size is the number of board spots a ship uses.

		It firstly checks the initial X,Y coordinates are empty, and checks that placing a ship in these coordinates in the specified orientation will not cause it to go out of bounds (exceed the boards X or Y boundaries).
		
		As long as the above steps are successful, it then loops the checkNeighborSpots method across every coordinate the ship
		will fill. This checks all adjacent spots to the X,Y are also empty. 
		
		Returns: True for success, False for failure
		'''
			
		if self.battleBoard[x][y] != '0': # Check to see if X, Y coords for first block are empty
			return False
		else:
			
			if orientation == 'h':
				if x+size-1 > 9:
					return False # Ship would be outside grid
			elif orientation =='v':
				if y+size-1 > 9:
					return False # Ships would be outside grid

			
			#print "--Valid Position--"
			if orientation=='h':
				#print "X %s, Y %s, Size %s, End X %s, End Y %s" % (x,y,size,x+size-1,y)
				
				for spot in range(x,x+size): # Check range for adjacent squares
					valid = self.checkNeighborSpots(spot,y)
					if valid==False:
						return False
				
			elif orientation=='v':
				#print "X %s, Y %s, Size %s, End X %s, End Y %s" % (x,y,size,x,y+size-1)
				for spot in range(y,y+size): # Check range for adjacent squares
					valid = self.checkNeighborSpots(x,spot)
					if valid==False:
						return False
					
			return valid	
	
	
	def checkNeighborSpots(self,x,y):
		'''
		This method accepts a set of x,y coordinates and passes them to a lambda function, which returns a list 		
		of neighbors.
		
		For example, in a 3x3 grid, the neighbors would be:

		000
		0X0
		000

		The zeroes, and the main coordinate would be the X

		returns False for invalid coordinates, True for valid
		'''

		neighbors = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x <= mapSize[0] and
                                   -1 < y <= mapSize[1] and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 <= mapSize[0]-1) and
                                   (0 <= y2 <= mapSize[1]-1))]
		for coords in neighbors(x,y):
			if self.battleBoard[coords[0]][coords[1]] != '0': # If spot is not empty, not valid
				return False
		 
		return True
	
	def removeCoordsAndUpdateHit(self,x,y,p):
		'''
		If the hitOrMiss method detects a hit (that's not a repeated attempt on a previously hit square) it calls this function to
		remove the coordinates from the shipPosition dictionary as well as updating the battleMap with an 'X' to replace the previous
		marker.

		Additionally, this method also controls the end-game logic. If the shipPositions dictionary is empty, there are no more ships in place, so notify of a win.
		'''
		#print x,y,p
		
		# Find out which piece
		for piece in gamePieces:
			if gamePieces[piece]['marker'] == p:
				message = 'Hit' #a %s' % piece
				shipHit = piece
				self.battleBoard[x][y] = 'X'
				break
				
		for items in self.shipPositions[shipHit]:
			#print items
			count = 0
			for hitX, hitY in self.shipPositions[shipHit][items]:
				#print x,y, self.shipPositions[shipHit][items] 
				if x == hitX and y == hitY:
					#print "Match x %s, y %s | hitX %s, hitY %s" % (x, y, hitX, hitY)
					del self.shipPositions[shipHit][items][count]
					break
				count +=1
		
		#print "-------"
		for items in self.shipPositions[shipHit]:
			if self.shipPositions[shipHit][items] == []:
				message = 'You just sunk the %s' % piece
				del self.shipPositions[shipHit][items]
				break
			#print items, self.shipPositions[shipHit][items]
		
		#print "Pieces Left"
		
		for items in self.shipPositions:
			if self.shipPositions[items] == {}:
				del self.shipPositions[items]
				break

		#print self.shipPositions
		#for items in self.shipPositions:
			#print items, self.shipPositions[items]
		
		
		if len(self.shipPositions.keys()) == 0:
			self.completedGame = True
			moves = int(self.playerMoves) + 1 
			message = 'Win! You completed the game in %s moves' % moves 
 			
		return message
			
	def hitOrMissAPI(self, x, y):
		'''
		hitOrMiss is the main API access point into the game class. 

		It checks the gameboard with a set of coordinates, and if those coordinates are not empty (0), have not already
		been attempted with a miss (*) and have not already been hit (X), then register a hit.
		
		To register the hit, it grabs the marker value at the x,y coordinates (for example S for submarine) and passes it along with the coords to the removeCoordsAndUpdateHit method. 
		
		'''
		if self.completedGame != True:
			if self.battleBoard[x][y] != '0' and self.battleBoard[x][y]!='*' and self.battleBoard[x][y]!='X':
				# We hit something. Detect what, and remove from those co-ords from the playboard
				# if a ship has been sunk, detect that, and notify.
				p = self.battleBoard[x][y]
				message = self.removeCoordsAndUpdateHit(x,y,p)
				state = "hit"
				self.playerMoves += 1

			elif self.battleBoard[x][y]=='*' or self.battleBoard[x][y]=='X':
				message = 'Already hit this spot'
				state = "repeat"
			else:
				self.battleBoard[x][y] = '*'
				message = 'Miss'
				state = "miss"
				self.playerMoves += 1

			print self.printBoard()
			self.updateMoves(message,self.playerMoves, x, y)
			response = {'status': 200, 'state': state, 'message': message, 'shots': self.playerMoves}
			return jsonify(response)
		else:
			response = {'status': 200, 'state': 'completed', 'message':'You have already completed this game.', 'shots': self.playerMoves}
			return jsonify(response)
		
		
	def getPlayerMoves(self):
		''' 
		getter method to return the number of moves the Player has performed
		'''
		return self.playerMoves
	
	
	def newGameId(self):	
		'''
		create a new session in MongoDb and return a string referencing that session.
		
		This is used to relate the sessions to the moves performed
		'''
		return str(self.mongo[self.db].sessions.insert({}))
	
	def updateMoves(self, message, shots, x, y):
		'''
		When a move is performed, store it in a new record in the moves collection.
		Attach the session id to this record so the moves are able to be related to the sessions.
		'''
		self.mongo[self.db].moves.insert({'session': ObjectId(self.gameID), 'message': message, 'x':x, 'y': y, 'shots': shots})
		