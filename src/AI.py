import random as r

class AI:
    """
    docstring
    """
    def __init__(self, difficulty):
        """
        docstring
        """
        self.difficulty = difficulty

    def shipPlacement(self):
        """
        docstring
        """
        xcoord = r.randint(9,19)
        ycoord = r.randint(1,9)
        #coord = [xcoord, ycoord]
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