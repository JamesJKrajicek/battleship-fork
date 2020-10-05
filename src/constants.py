import string 

"""!
This file store constants referenced in other modules
"""

NUM_ROWS = 10 # Row count
NUM_COLS = 10 # Column count

# Sizes in pixels
AXIS_FONT_SIZE = 58
MSG_FONT_SIZE = 40
SQUARE_SIZE = 52
WIN_Y = SQUARE_SIZE * (NUM_ROWS) # Size of full game board
WIN_X = SQUARE_SIZE * (NUM_COLS*2)

# Colors [R, G, B]
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
BLUE = [0,0,255]
GREY = [16,16,16]

#Number of rounds between earning special shots
SPECIAL_SHOT_RATE = 10 

#list of alphabet. string lib needed
Alpha = list(string.ascii_uppercase) 

# Used for ship placement, in clockwise order. Order: Down, Left, Up, Right.
DIRS = [[0, 1], [-1, 0], [0, -1], [1, 0]]