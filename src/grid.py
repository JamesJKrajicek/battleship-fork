import src.constants as c
class gridWrapper:
    def __init__(self):
        self.grid = []
        for row in range(c.NUM_ROWS):
            self.grid.append([])
            for column in range (c.NUM_ROWS):
                self.grid[row].append("Open")
    def __shoot__(self,y,x):
        if x >= 1 and x <= 9:
            if self.grid[y-10][x+10] == "Ship":
                self.grid[y][x] = "hit"
                #print("hit ship")            
            else:
                self.grid[y][x] = "miss"
                #print("You Missed")
        elif x >= 10 and y <= 20:
            if self.grid[y-10][x-10] == "Ship":
                self.grid[y][x] = "hit"
                #print("hit ship")
            else:
                self.grid[y][x] = "miss"
                #print("You Missed")

    def __winner__ (self,win_ships):
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
            print("\n==============\nPlayer 1 wins!\n==============\n")
            return True
        
        if p2_count == win_spaces:
            print("\n==============\nPlayer 2 wins!\n==============\n")
            return True