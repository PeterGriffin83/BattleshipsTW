import requests
import unittest

from app.config import mapSize, database
from json import loads
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

__author__ = "Peter Griffin <peter_griffin@hotmail.com>, <peter.g@playbasis.com>"
__version__= 0.2
__description__ = "Unittest TestCases for Battleships. Call from the run_tests.py file"

class test_game(unittest.TestCase):

	def testCheckMapSizeValid(self):
		'''
		Check generated MapSize is the same as specified in Config
		'''
		r = requests.get('http://localhost:8080/api/debug/mapSize')
		response = loads(r.text)
		
		self.failUnless(response['status']==200 and response['X']==mapSize[0] and response['Y']==mapSize[1] and mapSize[0]>0 and mapSize[1]>0)
	
	def testNewGameConnect(self):
		'''
		Test connection to Flask (The API) and response is 200 (OK) for new_game
		'''
		r = requests.get('http://localhost:8080/api/new_game')
		
		self.failIf(r.status_code!=200) # If not 200, Fail
		
	def testMongoConnection(self):
		m = MongoClient(database['host'], database['port'], serverSelectionTimeoutMS=database['timeout'])
		
		try:
			v = m.server_info()
		except ServerSelectionTimeoutError:
			v = ''
			
		self.failUnless(v!='')
			
	def testMongoValidDatabase(self):
		m = MongoClient(database['host'], database['port'], serverSelectionTimeoutMS=database['timeout'])
		
		databaseCheck = False
		if database['database'] not in m.database_names():
			databaseCheck = False
		else:
			databaseCheck = True

		self.failUnless(databaseCheck)
	
		
	def testNewGameCorrectResponse(self):
		'''
		Check response is valid for new game 
		'''

		r = requests.get('http://localhost:8080/api/new_game')
		response = loads(r.text)

		self.failUnless(response['status']==200 and response['message']=='New Game Ready') # If not expect response, Fail
		
	def testTakeShotConnect(self):
		'''
		Test connection to Flask (The API) and response is 200 (OK) for shot/x/y
		'''

		r = requests.get('http://localhost:8080/api/shot/1/1')
		
		self.failIf(r.status_code!=200) # If not 200, Fail
		
	def testTakeShotCorrectResponse(self):
		'''
		Check response is valid. Checking for 'Already hit this spot' as the testTakeShotConnect will hit the same X,Y before this method is called.
		'''
		
		r = requests.get('http://localhost:8080/api/shot/1/1')
		response = loads(r.text)
		self.failUnless(response['status']==200 and response['message']=='Already hit this spot' and response['state']=='repeat') # If not expect response, Fail
		
	def testZSetWinConditionAndCheck(self):
		''' 
		Set a new Game and hit each square on the board until a win condition. If win condition exit. If not fail. 
		'''
		r = requests.get('http://localhost:8080/api/new_game')
		gameCompleted = False
		for y in range(mapSize[1]):
			for x in range(mapSize[0]):
						url = 'http://localhost:8080/api/shot/%s/%s' % (x, y)
						r = requests.get(url)
						response = loads(r.text)
						if response['state'] == 'completed':
							gameCompleted = True
							break
		
		if gameCompleted == False: # It's possible the winning square was the last one, so we will fire off shot one more time to check
				url = 'http://localhost:8080/api/shot/%s/%s' % (x, y)
				r = requests.get(url)
				response = loads(r.text)
				if response['state'] == 'completed':
					gameCompleted = True
				
		self.failUnless(gameCompleted)

	def testZSetWinConditionAndCheckShotCount(self):
		''' 
		Set a new Game and hit each square on the board until a win condition. If win condition exit. If not fail. 
		'''
		r = requests.get('http://localhost:8080/api/new_game')
		gameCompleted = False
		for y in range(mapSize[1]):
			for x in range(mapSize[0]):
						url = 'http://localhost:8080/api/shot/%s/%s' % (x, y)
						r = requests.get(url)
						response = loads(r.text)
						if response['state'] == 'completed':
							gameCompleted = True
							break
		
		if gameCompleted == False: # It's possible the winning square was the last one, so we will fire off shot one more time to check
				url = 'http://localhost:8080/api/shot/%s/%s' % (x, y)
				r = requests.get(url)
				response = loads(r.text)
				if response['state'] == 'completed':
					gameCompleted = True
		
		self.failUnless(gameCompleted and response['shots'] > 0 and response['shots'] <= (mapSize[0] * mapSize[1]))
		
		
		