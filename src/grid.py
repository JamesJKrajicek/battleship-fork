import src.constants as c
class Grid:
    def __init__(self):
        self.grid = []
        for row in range(c.NUM_ROWS*2):
            self.grid.append([])
            for column in range (c.NUM_COLS*2):
                self.grid[row].append("Open")
    def shoot(self, y, x):
        if x >= 1 and x <= 9: # Player 1
            if self.grid[y-10][x+10] == "Ship":
                self.grid[y][x] = "hit"
                #print("hit ship")            
            else:
                self.grid[y][x] = "miss"
                #print("You Missed")
        elif x >= 10 and y <= 20: # Player 2
            if self.grid[y-10][x-10] == "Ship":
                self.grid[y][x] = "hit"
                #print("hit ship")
            else:
                self.grid[y][x] = "miss"
                #print("You Missed")

    def check_winner(self, win_ships):
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