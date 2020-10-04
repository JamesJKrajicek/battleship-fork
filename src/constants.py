import string 

"""!
This file store constants referenced in other modules
"""

MSG_FONT_SIZE = 30 #pixels
SQUARE_SIZE = 40 #pixels
NUM_ROWS = 10 #row count
NUM_COLS = 10 # column count
WIN_X, WIN_Y = SQUARE_SIZE * (NUM_ROWS*2), SQUARE_SIZE * (NUM_COLS*2)
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
BLUE = [0,0,255]
Alpha = list(string.ascii_uppercase) #list of alphabet. string lib needed

# Used for ship placement, in clockwise order. Order: Down, Left, Up, Right.
DIRS = [[0, 1], [-1, 0], [0, -1], [1, 0]]