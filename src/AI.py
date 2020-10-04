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
        for row in range(9):
            self.arr.append([])
            for column in range(9):
                self.arr[row].append(0)
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
                    self.arr[self.rand_y] [self.rand_x] = self.hit
                else:
                    self.arr[self.rand_y] [self.rand_x] = self.miss
            elif self.state == 1:
                if self.hit_shot:
                    if self.shot_type == 20:
                        self.north_hit = true
                    elif self.shot_type == 30:
                        self.east_hit = true
                    elif self.shot_type == 40:
                        self.south_hit = true
                    elif self.shot_type == 50:
                        self.west_hit = true
                    self.arr[self.prev_y] [self.prev_x] = self.hit
                else:
                    self.arr[self.prev_y] [self.prev_x] = self.miss
            elif self.state == 2:
                if self.hit_shot:
                    if self.north_hit:
                        self.arr[self.prev_y] [self.prev_x] = self.hit
                    else:
                        self.north_hit = False
                else:
                    self.arr[self.prev_y] [self.prev_x] = self.miss
                if self.hit_shot:
                    if self.east_hit:
                        self.arr[self.prev_y] [self.prev_x] = self.hit
                    else:
                        self.east_hit = False
                else:
                    self.arr[self.prev_y] [self.prev_x] = self.miss
                if self.hit_shot:
                    if self.south_hit:
                        self.arr[self.prev_y] [self.prev_x] = self.hit
                    else:
                        self.south_hit = False
                else:
                    self.arr[self.prev_y] [self.prev_x] = self.miss
                if self.hit_shot:
                    if self.west_hit:
                        self.arr[self.prev_y] [self.prev_x] = self.hit
                    else:
                        self.west_hit = False
                else:
                    self.arr[self.prev_y] [self.prev_x] = self.miss
        #main code
        if self.state == 0:
            if self.rand_x == int() or self.rand_y == int():
                self.rand_x = r.randint(0,8)
                self.rand_y = r.randint(0,8)
            else:
                while self.arr[self.rand_y] [self.rand_x] != 0:
                    self.rand_x = r.randint(0,8)
                    self.rand_y = r.randint(0,8)
            self.shot_type = 10
            return self.rand_x, self.rand_y
        elif self.state == 1:
            if self.shot_type == 10:
                self.shot_type = self.shot_type + 10
                if self.rand_y-1 >= 0:
                    self.prev_y = self.rand_y - 1
                    self.prev_x = self.prev_x
                    return self.prev_x, self.prev_y
            elif self.shot_type == 20:
                self.shot_type = self.shot_type + 10
                if self.rand_x+1 < 9:
                    self.prev_y = self.rand_y
                    self.prev_x = self.rand_x + 1
                    return self.prev_x, self.prev_y
            elif self.shot_type == 30:
                self.shot_type = self.shot_type + 10
                if self.rand_y+1 < 9:
                    self.prev_y = self.rand_y + 1
                    self.prev_x = self.rand_x
                    return self.prev_x, self.prev_y
            elif self.shot_type == 40:
                self.shot_type = self.shot_type + 10
                if self.rand_x-1 >= 0:
                    self.prev_y = self.rand_y
                    self.prev_x = self.rand_x - 1
                    return self.prev_x, self.prev_y
            else:
                self.shot_type = 10
                self.state = self.state + 1
        elif self.state == 2:
            if self.north_hit:
                if self.rand_y - self.radius >= 0:
                    self.prev_y = self.rand_y - self.radius
                    self.prev_x = self.rand_x
                    return self.prev_x, self.prev_y
                else:
                    self.north_hit = False
            elif self.east_hit:
                if self.rand_x + self.radius >= 0:
                    self.prev_x = self.rand_x + self.radius
                    self.prev_y = self.rand_y
                    return self.prev_x, self.prev_y
                else:
                    self.east_hit = False
            elif self.south_hit:
                if self.rand_y + self.radius >= 0:
                    self.prev_y = self.rand_y + self.radius
                    self.prev_x = self.rand_x
                    return self.prev_x, self.prev_y
                else:
                    self.south_hit = False
            elif self.west_hit:
                if self.rand_x - self.radius >= 0:
                    self.prev_x = self.rand_x - self.radius
                    self.prev_y = self.rand_y
                    return self.prev_x, self.prev_y
                else:
                    self.west_hit = False
            else:
                self.state = 1

    def hard(self):
        """!
        @pre
        @post
        @return
        """
        pass
