import random as r
import src.constants as c

class AI:
    """
    docstring
    """
    def __init__(self, difficulty):
        """
        docstring
        """
        self.difficulty = difficulty

    def shipPlacement(self, gs):
        """
        docstring
        """
        gs.shipDir = (gs.shipDir + 1) % len(c.DIRS) #Generates number between 0-3 for direction change
        xcoord = r.randint(c.NUM_ROWS-1 ,2*c.NUM_ROWS-1) #Generates number between 9-19 (boundaries of second board)
        ycoord = r.randint(1, c.NUM_COLS-1) #Generates number between 1 and 9 (boundaries of boards)
        return (xcoord, ycoord)

    def shooting(self):
        """
        docstring
        """
        if self.difficulty == 2:
            self.easy()
        elif self.difficulty == 3:
            self.medium()
        else:
            self.hard()

    def easy(self):
        """
        docstring
        """
        pass

    def medium(self):
        """
        docstring
        """
        pass

    def hard(self):
        """
        docstring
        """
        pass