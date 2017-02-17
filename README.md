## Battleships 
###### Date: February 17, 2017<br /> Author: Peter Griffin <peter_griffin@hotmail.com>


### Introduction:

This repository contains a version of Battleships, playable via API calls, as per the requirements of the TaskWorld take home assignment. 

The Battleship board is a 10x10 square grid, and each square is a unique X, Y coordinate. 

Within this grid, there is an "Enemy fleet" that consists of the following ships:

<table style="text-align:center;">
<tr><td colspan=4>Enemy Ships</td></tr> 
<tr><td>Ship Name</td><td>Size</td><td>Marker</td><td>Count</td></tr>
<tr><td>Submarine</td><td>1</td><td>S</td><td>4</td></tr>
<tr><td>Destroyer</td><td>2</td><td>D</td><td>3</td></tr>
<tr><td>Cruiser</td><td>3</td><td>C</td><td>2</td></tr>
<tr><td>Battleship</td><td>4</td><td>B</td><td>1</td></tr>
</table>

Which are randomly placed upon the 10 x 10 board, with the following conditions:

* No ship is allowed to be adjacent to another ship, and 
* Ships must entirely fit within the gameboard (no out-of-bounds errors)

### Implementation

This version has been written in Python, and relies upon the Flask library (for the API framework) and the PyMongo library (for Mongo). 

All the requirements have been frozen into the requirements.txt file. Installation instructions are below.


### Installation:

I use virtual environments (however, you may wish to install the libraries at system level, in which case, ignore the virtual environment instructions and use sudo when running the pip install -r requirements.txt command) 

1. Clone this repository to an appropriate directory
2. Set up a virtual environment to run this project in

	```` 
	$ virtualenv venv
	$ source venv/bin/activate
	````

   If you don't have the virtual environment package installed, install it via:
   
   ````
   $ sudo pip install virtualenv
   ````
   and then activate it as above.


3. Install the required libraries into your virtual environment:

	````
	(venv) $ pip install -r requirements.txt
	````

4. Install mongo and run it on your machine. (You can run it on another accessible machine, as long as you update the config.py file in the app folder

5. Start the run.py file to start the application

6. Start the run_tests.py file to run the test suite against the application. 


### Configuration:

The config.py file consists of the following (default) settings: 

```
mapSize = [10,10]

gamePieces = {'Battleship': { 'count': 1, 'size': 4, 'marker': 'B'}, 
			  'Cruiser': {'count': 2, 'size': 3, 'marker': 'C'},
			  'Destroyer': { 'count': 3, 'size': 2, 'marker': 'D'},
			  'Submarine': { 'count': 4, 'size': 1, 'marker': 'S'}}

flaskOptions = { 'host': '0.0.0.0', 'port': 8080, 'debug': True }

database = {'host': '127.0.0.1', 'port': 27017, 'timeout': 3000, 'database': 'battleships' }

```

mapSize: the X, Y size of the game board. This can be changed as long as both numbers are > 10 and the same (to maintain a square) for example 15x15, 60x60

gamePieces: a Dictionary of the game pieces, their size, marker, and number of them. This can be configured to add/remove pieces

flaskOptions: options used to run Flask (the framework used to expose build the API).

database: options used to access Mongo


### Api Endpoints:

New Game: Load a new game, and (if any) clears previous game details from memory


```
URL: http://127.0.0.1:8080/api/new_game

Response: 

{
  "message": "New Game Ready",
  "status": 200
}

```


Shot: Used to take a shot at the Defender's board.

(The coordinates have to be entered as integers or will be ignore. I.e: If someone uses four instead of 4)

```
URL: http://127.0.0.1:8080/api/shot/<int:x>/<int:y>

Response (on miss): 
{
  "message": "Miss",
  "shots": 1,
  "state": "miss",
  "status": 200
}

Response (on hit):
{
  "message": "Hit",
  "shots": 9,
  "state": "Hit",
  "status": 200
}

Response (on sinking a ship, where <ship> is the name of the Ship, i.e: Submarine):
{
  "message": "You just sunk the <ship>",
  "shots": 3,
  "state": "Hit",
  "status": 200
}


Response (on attempting to attack a previously attacked square, note the counter does not increment as we don't "count" this attempt):
{
  "message": "Already hit this spot",
  "shots": 3,
  "state": "repeat",
  "status": 200
}

Response (on win):
{
  "message": "Win! You completed the game in 30 moves",
  "shots": 31,
  "state": "Hit",
  "status": 200
}

Response (on attempting to continue to play after win):
{
  "message": "You have already completed this game.",
  "shots": 31,
  "state": "completed",
  "status": 200
}

```


Gameplay (Ascii Screenshots):

As there is no frontend, there is no screenshots to provide, however the server does print the board to screen while running as per the following:

New game: <br />

```
0 0 0 0 D D 0 0 0 0
0 0 0 0 0 0 0 0 0 S
0 B B B B 0 0 0 0 0
0 0 0 0 0 0 0 C C C
C C C 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
S 0 0 0 S 0 0 S 0 0
0 0 0 0 0 0 0 0 0 0
0 D 0 0 0 0 0 0 D D
0 D 0 0 0 0 0 0 0 0
```

Game after a few turns: <br />
(0 is ocean, * are misses, X are Hits, and the rest are remaining ships)

```
0 0 0 0 D D 0 0 0 0
0 * 0 0 0 0 0 0 0 S
0 B B B B 0 0 0 0 0
0 0 0 0 0 0 0 X X X
C C C 0 * 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
S 0 0 0 S 0 0 S 0 0
0 0 0 0 0 0 0 0 * 0
0 X 0 0 * 0 0 0 D D
0 D 0 0 0 0 0 0 0 0
```

### Test Suite:

Tests are ran using the run_tests.py file (ensure that the run.py is running first, or the tests will fail to connect to the server) 

The following are tested:

1. Check Map Size Valid: Checks the map size returned from the API and compares it to the configuration file to ensure they match and are valid.
2. New Game Connect: Ensures it can connect to the flask endpoint for new game (http://127.0.0.1:8080/api/new_game)
3. New Game Correct Response: Ensures the response from /api/new_game is valid and correct
4. Test Mongo Connection: Check the mongod daemon is accessible at the IP and port specified in the configuration
5. Test Mongo Valid Databases: Checks the database (as configured in configuration) exists and is accessible
6. Take Shot Connect: Like New Game Connect, but for the /api/shot/x/y endpoint
7. Take Shot Correct Response: Ensures the response from /api/shot/x/y is valid and correct
8. testZSetWinConditionAndCheck: Run a full game (brute force X,Y) until success. Fail if the entire board has been 'hit' without the win condition being generated
9. testZSetWinConditionAndCheckShotCount: The same as the previous test, except counts and validates the shot count 



