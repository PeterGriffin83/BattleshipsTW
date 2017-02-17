from app import app
from app.config import flaskOptions, mapSize

__author__ = "Peter Griffin <peter_griffin@hotmail.com>, <peter.g@playbasis.com>"
__version__= 0.2
__description__ = "Main entry point into Battleships. Starts and hands off execution to flask"

if __name__ == '__main__':
	app.run(host=flaskOptions['host'], port=flaskOptions['port'], debug=flaskOptions['debug'])
