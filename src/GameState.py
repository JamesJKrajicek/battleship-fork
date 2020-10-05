from src.grid import Grid
from src.ship import Ship, ShipNode

class GameState:
    """!
    This class stores information about the current state of the game.
    It is used to easily pass information from Battleship to BattleshipView.
    """
    
    def __init__(self):
        """!
        @pre None
        @post GameState is initialized with default values for the beginning of the game
        """
        self.numShipsPerPlayer = 0
        self.playerType = 1 # Whether P2 is a human (1) or AI (2-4 for difficulty)
        
        self.grid = Grid()
        self.shipDir = 0 # Direction of the ship currently being placed (index of c.DIRS)
        self.lenShip = 1 # Length of the ship to place next
        
        self.p1Ships = []
        self.p2Ships = []
        
         # Number of special shots each player has
        self.p1_special_shots = 0
        self.p2_special_shots = 0
        
        self.is_P1_turn = False
        self.is_placing = False
        self.is_shooting = False
        self.in_transition = False
        
        self.msg = "" # Message to display below game board
