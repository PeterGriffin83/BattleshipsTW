mapSize = [10,10]

gamePieces = {'Battleship': { 'count': 1, 'size': 4, 'marker': 'B'}, 
			  'Cruiser': {'count': 2, 'size': 3, 'marker': 'C'},
			  'Destroyer': { 'count': 3, 'size': 2, 'marker': 'D'},
			  'Submarine': { 'count': 4, 'size': 1, 'marker': 'S'}}

flaskOptions = { 'host': '0.0.0.0', 'port': 8080, 'debug': True }

database = {'host': '127.0.0.1', 'port': 27017, 'timeout': 3000, 'database': 'battleships' }