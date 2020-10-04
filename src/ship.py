class ShipNode:
    """!
    The ShipNode class represents a single space within a ship. It is used when checking if a ship is sunk.
    """
    
    def __init__(self, x, y):
        """!
        @pre The provided coordinates are within the bounds of the grid
        @post ShipNode is created at the specified location
        @param x int: The X coordinate of this node on the grid
        @param y int: The Y coordinate of this node on the grid
        """
        self.x = x
        self.y = y
        self.hit = False

class Ship:
    """!
    The Ship class represents a single ship. It stores all of the spaces on the grid it occupies and whether it has been sunk.
    """
    
    def __init__(self):
        """!
        @pre None
        @post Ship is created with no spaces and not sunk
        """
        self.shipSquares = []
        self.sunk = False

    def checkSunk(self):
        """!
        @pre None
        @post If the ship is sunk, updates the member variable sunk accordingly
        @return bool: whether all ShipNodes within the shipSquares list have been hit
        """
        for square in self.shipSquares:
            if not square.hit:
                return False
        self.sunk = True
        return True

    def addSquare(self, x, y):
        """!
        @pre The provided coordinates are within the bounds of the grid
        @post a ShipNode is added to this Ship's shipSquares list
        @param x int: The X coordinate of this node on the grid
        @param y int: The Y coordinate of this node on the grid
        """
        self.shipSquares.append(ShipNode(x,y))