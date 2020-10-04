import src.constants as c
class Grid:
    """!
    This class stores the game grid, a 2D array of strings which represents all spaces on both players' boards, and contains some functions relating to it
    """
    
    def __init__(self):
        """!
        @pre None
        @post The grid is initialzed to contain all empty spaces
        """
        self.grid = []
        for row in range(c.NUM_ROWS*2):
            self.grid.append([])
            for column in range(c.NUM_COLS*2):
                self.grid[row].append("Open")
                
    def shoot(self, y, x):
        """!
        @pre The space being fired at is within the bounds of the grid
        @post The grid space is updated to a hit or a miss, depending on if if it contained a ship
        @param y int: The Y coordinate of the grid to fire at (0-9)
        @param x int: The X coordinate of the grid to fire at (0-19)
        """
        self.grid[y][x] = "hit" if self.grid[y][x] == "Ship" else "miss"
            
    def check_winner(self, win_ships):
        """!
        @pre None
        @post None
        @param win_ships int: The number of sunk ships required to win (1-5)
        @return int: The number of the player that has won the game, or 0 if the game is not won
        """
        p1_count = 0
        p2_count = 0
        for x in range(1,10):
            for y in range(1,10):
                if self.grid[y][x] == "hit":
                    p1_count += 1
        for x in range(11,20):
            for y in range(0,10):
                if self.grid[y][x] == "hit":
                    p2_count += 1
        
        # Determine the total number of spaces the ships required to win would occupy
        win_spaces = win_ships * (win_ships+1) // 2

        if p1_count == win_spaces:
            return 1
        
        if p2_count == win_spaces:
            return 2