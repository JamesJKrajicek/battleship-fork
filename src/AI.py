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

    def getPoints(self, gs):
        """!
        @pre The game is running and it is the AI's turn to fire
        @post
        @return
        """
        if self.difficulty == 2:
            return self.easy(gs)
        elif self.difficulty == 3:
            self.medium()
        else:
            return self.hard(gs)

    def easy(self, gs):
     
        enemy_ships = gs.p2Ships if gs.is_P1_turn else gs.p1Ships
        squares = []
        for ship in enemy_ships:
            for square in ship.shipSquares:
                squares.append(square)

        while True:
            x = r.randint(1, 9)
            y = r.randint(1, 9)

            flag = True
            for square in squares:
                if square.x == x and square.y == y:
                    if not square.hit:
                        return x, y
                    else:
                        flag = False
                        break

            if flag:
                return x, y

    def medium(self):
      
        pass

    def hard(self, gs):

        enemy_ships = gs.p2Ships if gs.is_P1_turn else gs.p1Ships
        for ship in enemy_ships:
            for square in ship.shipSquares:
                if not square.hit:
                    return square.x, square.y

        return 1, 1

