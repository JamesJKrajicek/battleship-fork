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
        if self.difficulty == 1:
            self.easy()
        elif self.difficulty == 2:
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