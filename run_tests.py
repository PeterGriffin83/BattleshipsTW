from json import loads
from pprint import pprint
from tests import test_game

__author__ = "Peter Griffin <peter_griffin@hotmail.com>, <peter.g@playbasis.com>"
__version__= 0.2
__description__ = "Entrypoint into the Unitttest. Run this file to run tests."

import unittest

def main():
	unittest.main(test_game)

if __name__ == '__main__':
	main()