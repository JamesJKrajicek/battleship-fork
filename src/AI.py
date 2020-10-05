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
        for row in range(10):
            self.arr.append([])
            for column in range(10):
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

    def getPoints(self, gs):
        """!
        @pre The game is running and it is the AI's turn to fire
        @post
        @return
        """
        if self.difficulty == 2:
            return self.easy(gs)
        elif self.difficulty == 3:
            return self.medium()
        else:
            return self.hard(gs)

    def easy(self, gs):
        while True:
            x = r.randint(1, 9)
            y = r.randint(1, 9)
            if((gs.grid.grid[y][x] == "Open") or (gs.grid.grid[y][x] == "Ship")):
                return x, y

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
                    self.state = 1
                else:
                    self.arr[self.rand_y] [self.rand_x] = self.miss
            if self.state == 1:
                if self.hit_shot:
                    if self.shot_type == 20:
                        self.north_hit = True
                    elif self.shot_type == 30:
                        self.east_hit = True
                    elif self.shot_type == 40:
                        self.south_hit = True
                    elif self.shot_type == 50:
                        self.west_hit = True
                    self.arr[self.prev_y] [self.prev_x] = self.hit
                else:
                    self.arr[self.prev_y] [self.prev_x] = self.miss
            if self.state == 2:
                if self.hit_shot:
                    if self.north_hit:
                        self.arr[self.prev_y] [self.prev_x] = self.hit
                    else:
                        self.arr[self.prev_y] [self.prev_x] = self.miss
                    if self.east_hit:
                        self.arr[self.prev_y] [self.prev_x] = self.hit
                    else:
                        self.arr[self.prev_y] [self.prev_x] = self.miss
                    if self.south_hit:
                        self.arr[self.prev_y] [self.prev_x] = self.hit
                    else:
                        self.arr[self.prev_y] [self.prev_x] = self.miss
                    if self.west_hit:
                        self.arr[self.prev_y] [self.prev_x] = self.hit
                    else:
                        self.arr[self.prev_y] [self.prev_x] = self.miss
                else:
                    self.arr[self.prev_y] [self.prev_x] = self.miss
        #main code
        while 1:
            if self.state == 0:
                self.north_hit = False
                self.east_hit = False
                self.south_hit = False
                self.west_hit = False
                if self.rand_x == int() or self.rand_y == int():
                    self.rand_x = r.randint(1,9)
                    self.rand_y = r.randint(1,9)
                else:
                    while self.arr[self.rand_y] [self.rand_x] != 0:
                        self.rand_x = r.randint(1,9)
                        self.rand_y = r.randint(1,9)
                self.shot_type = 10
                return self.rand_x, self.rand_y
            elif self.state == 1:
                if self.shot_type == 10:
                    self.shot_type = self.shot_type + 10
                    if self.rand_y-1 > 0:
                        self.prev_y = self.rand_y - 1
                        self.prev_x = self.rand_x
                        return self.prev_x, self.prev_y
                if self.shot_type == 20:
                    self.shot_type = self.shot_type + 10
                    if self.rand_x+1 <= 9:
                        self.prev_y = self.rand_y
                        self.prev_x = self.rand_x + 1
                        return self.prev_x, self.prev_y
                if self.shot_type == 30:
                    self.shot_type = self.shot_type + 10
                    if self.rand_y+1 <= 9:
                        self.prev_y = self.rand_y + 1
                        self.prev_x = self.rand_x
                        return self.prev_x, self.prev_y
                if self.shot_type == 40:
                    self.shot_type = self.shot_type + 10
                    if self.rand_x-1 > 0:
                        self.prev_y = self.rand_y
                        self.prev_x = self.rand_x - 1
                        return self.prev_x, self.prev_y
                self.shot_type = 10
                self.state = 2
                self.hit_shot = True
            elif self.state == 2:
                if self.north_hit:
                    if self.rand_y - self.radius > 0 and self.hit_shot:
                        self.prev_y = self.rand_y - self.radius
                        self.prev_x = self.rand_x
                        self.radius = self.radius+1
                        return self.prev_x, self.prev_y
                    else:
                        self.north_hit = False
                        self.radius = 2
                elif self.east_hit:
                    if self.rand_x + self.radius <= 9 and self.hit_shot:
                        self.prev_x = self.rand_x + self.radius
                        self.prev_y = self.rand_y
                        self.radius = self.radius+1
                        return self.prev_x, self.prev_y
                    else:
                        self.east_hit = False
                        self.radius = 2
                elif self.south_hit:
                    if self.rand_y + self.radius <= 9 and self.hit_shot:
                        self.prev_y = self.rand_y + self.radius
                        self.prev_x = self.rand_x
                        self.radius = self.radius+1
                        return self.prev_x, self.prev_y
                    else:
                        self.south_hit = False
                        self.radius = 2
                elif self.west_hit:
                    if self.rand_x - self.radius > 0 and self.hit_shot:
                        self.prev_x = self.rand_x - self.radius
                        self.prev_y = self.rand_y
                        self.radius = self.radius+1
                        return self.prev_x, self.prev_y
                    else:
                        self.west_hit = False
                        self.radius = 2
                else:
                    self.state = 0


    def hard(self, gs):

        enemy_ships = gs.p2Ships if gs.is_P1_turn else gs.p1Ships
        for ship in enemy_ships:
            for square in ship.shipSquares:
                if not square.hit:
                    return square.x, square.y

        return 1, 1
