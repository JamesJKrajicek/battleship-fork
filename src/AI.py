import random as r
import src.constants as c

class AI:
    """!
    This class stores the state of the AI, inclding its difficulty, and the methods required for it to make its moves
    """
    def __init__(self, difficulty):
        """!
        @pre None
        @post The member variable difficulty is initialized
        @param difficulty int: The difficulty of the AI (2-4, as 1 represents a human)
        """
        self.difficulty = difficulty

    def shipPlacement(self, gs):
        """!
        @pre The game is running and it is the AI's turn to place a ship
        @post gs.shipDir is updated to a random direction
        @param gs GameState: Used by the AI to decide how to place its ship
        @return (int, int): The (X, Y) coordinates the AI wants to place the ship at
        """
        gs.shipDir = r.randint(0, len(c.DIRS)-1) #Generates number between 0-3 for direction change
        xcoord = r.randint(c.NUM_ROWS-1 ,2*c.NUM_ROWS-1) #Generates number between 9-19 (boundaries of second board)
        ycoord = r.randint(1, c.NUM_COLS-1) #Generates number between 1 and 9 (boundaries of boards)
        return (xcoord, ycoord)

    def shooting(self):
        """!
        @pre The game is running ant it is the AI's turn to fire
        @post
        @return
        """
        if self.difficulty == 2:
            self.easy()
        elif self.difficulty == 3:
            self.medium()
        else:
            self.hard()

    def easy(self):
        """!
        @pre
        @post
        @return
        """
        pass

    def medium(self):
        """!
        @pre
        @post
        @return
        """
        pass

    def hard(self):
        """!
        @pre
        @post
        @return
        """
        pass