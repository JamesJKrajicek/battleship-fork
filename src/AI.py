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

        #medium AI data
        self.arr = []
        for row in range(c.Num_ROWS):
            self.grid.append([])
            for column in range(c.NUM_COLS):
                self.arr[row].append(int())
        self.prev_x = int()
        self.prev_y = int()
        self.rand_x = int()
        self.rand_y = int()
        self.hit_shot = False
        """
        10 = random
        20 = north
        30 = east
        40 = south
        50 = west
        """
        self.shot_type = 10
        self.state = 0;
        self.north_hit = False
        self.east_hit = False
        self.south_hit = False
        self.west_hit = False
        self.radius = 2
        self.miss = 1
        self.hit = 2



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
        #data catch
        if self.rand_x != int() and self.rand_y != int():
            if self.state == 0:
                if self.hit_shot:
                    self.arr[self.rand_x] [self.rand_y] = self.shot_type + self.hit
                else:
                    self.arr[self.rand_x] [self.rand_y] = self.shot_type + self.hit
            else if self.state == 1:
                if self.hit_shot:
                    if self.shot_type == 20:
                        self.north_hit = true
                    else if self.shot_type == 30:
                        self.east_hit = true
                    else if self.shot_type == 40:
                        self.south_hit = true
                    else if self.shot_type == 50:
                        self.west_hit = true
                    self.arr[self.prev_x] [self.prev_y] = self.shot_type + self.hit
                else:
                    self.arr[self.prev_x] [self.prev_y] = self.shot_type + self.miss
            else if self.state == 2





        pass

    def hard(self):
        """!
        @pre
        @post
        @return
        """
        pass
