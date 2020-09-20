import string 

"""
@This file is used to store constant values to be referenced by other modules
"""

MSG_FONT_SIZE = 32
SQUARE_SIZE = 40
NUM_ROWS = 20
WIN_X, WIN_Y = SQUARE_SIZE * NUM_ROWS, SQUARE_SIZE * NUM_ROWS
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
BLUE = [0,0,255]
Alpha = list(string.ascii_uppercase) #list of alphabet. string lib needed

# Used for ship placement, in clockwise order
DIRS = [[0, 1], [-1, 0], [0, -1], [1, 0]]