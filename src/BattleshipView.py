import pygame as pg
import tkinter as tk
import tkinter.simpledialog
import os
import sys
import src.constants as c

class BattleshipView:
    """!
    This class handles the user interface of the game, including the game window, dialog boxes for selecting the number of ships and opponent, and sound effects.
    """
    
    def __init__(self):
        """!
        @pre None
        @post The PyGame assets are initialized and the game window is created and displayed to the user
        """
        # Center window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # Initialize pygame
        pg.init()
        # Set up the mixer to play sounds in two channels, so sink sound and hit sound can happen at the same time
        pg.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
        self.channel1 = pg.mixer.Channel(0)
        self.channel2 = pg.mixer.Channel(1)
        # Set the name of the window
        pg.display.set_caption("Battleship by team 14, upgraded by team 13")
        # Initialize the screen to the desired size
        self.screen = pg.display.set_mode((c.WIN_X, c.WIN_Y + c.MSG_FONT_SIZE))

        # Initialize PyGame assets
        self.boardHighlight = pg.Surface((int(c.WIN_X / 2), int(c.WIN_Y)))
        self.boardHighlight.set_alpha(99)
        self.boardHighlight.fill(c.RED)
        self.boardHighlight_grey = pg.Surface((int(c.WIN_X), int(c.WIN_Y)))
        self.boardHighlight_grey.set_alpha(99)
        self.boardHighlight_grey.fill(c.GREY)
        self.bg = pg.transform.scale(pg.image.load("media/background-day.jpg"), (c.WIN_X, c.WIN_Y))
        self.hit = pg.transform.scale(pg.image.load("media/redX.png"), (c.SQUARE_SIZE, c.SQUARE_SIZE))
        self.miss = pg.transform.scale(pg.image.load("media/blackX.png"), (c.SQUARE_SIZE, c.SQUARE_SIZE))
        self.sunk_sound = pg.mixer.Sound("media/sunk.wav")
        self.hit_sound = pg.mixer.Sound("media/hit.wav")
        self.font = pg.font.Font('freesansbold.ttf', c.AXIS_FONT_SIZE)
        self.msg_font = pg.font.Font('freesansbold.ttf', c.MSG_FONT_SIZE)

    def get_num_ships(self):
        """!
        @pre None
        @post If the user presses cancel, the program exits
        @return int: The number of ships the selected by the player (1-5)
        """
        # Get the number of ships per player, and protect from bad input
        root = tk.Tk()
        root.eval('tk::PlaceWindow . center') # Approximately center the dialog
        root.withdraw()
        numShipsPerPlayer = tkinter.simpledialog.askinteger("Battleship", "How many ships per player? (1-5)", minvalue=1, maxvalue=5)
        if numShipsPerPlayer is None: # User pressed cancel
            pg.quit()
            sys.exit()
        return numShipsPerPlayer

    def get_player_type(self):
        """!
        @pre None
        @post If the user presses cancel, the program exits
        @return int: A number indicating which opponent the player is playing agianst (1-4)
        """
        root = tk.Tk()
        root.eval('tk::PlaceWindow . center') # Approximately center the dialog
        root.withdraw()
        playerType = tkinter.simpledialog.askinteger("Opponent", "Opponent Type? (1-4)\n1: Player, 2: EasyAI, 3: MediumAI, 4: HardAI.", minvalue=1, maxvalue=4)
        if playerType is None: # User pressed cancel
            pg.quit()
            sys.exit()
        return playerType

    def play_hit_sound(self):
        """!
        @pre None
        @post self.hit_sound starts playing on self.channel1, overriding anything currently playing
        """
        self.channel1.play(self.hit_sound)

    def play_sunk_sound(self):
        """!
        @pre None
        @post self.sunk_sound starts playing on self.channel1, overriding anything currently playing
        """
        self.channel2.play(self.sunk_sound)

    def draw(self, gs):
        """!
        @pre gs contains valid values
        @post The PyGame window is redrawn to reflect the values in gs
        @param gs GameState: The GameState object representing the current state of the game
        """
        # Draw the background
        self.screen.blit(self.bg, (0,0))
        pg.draw.rect(self.screen, c.BLACK, (0, c.WIN_Y, c.WIN_X, c.MSG_FONT_SIZE))

        # Render message centered below board
        text = self.msg_font.render(gs.msg, 1, c.WHITE)
        self.screen.blit(text, text.get_rect(centerx=c.WIN_X//2, top=c.WIN_Y))

        # Loop through all squares on the grid, drawing the space contents, grid lines, and axis labels
        for row in range(len(gs.grid.grid)): #row
            for column in range(len(gs.grid.grid[0])): #column
                # If the square is a ship, draw the ship only when that player is placing
                if gs.grid.grid[row][column] == "Ship" and (gs.in_transition == False) and ((gs.is_P1_turn and column < 10) or (not gs.is_P1_turn and column > 10)):
                    pg.draw.rect(self.screen, c.RED, (column * c.SQUARE_SIZE, row * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                elif gs.grid.grid[row][column] == "hit" and (gs.in_transition == False): # Draw hit marker
                    self.screen.blit(self.hit, (column * c.SQUARE_SIZE, row * c.SQUARE_SIZE))
                elif gs.grid.grid[row][column] == "miss" and (gs.in_transition == False): # Draw miss marker
                    self.screen.blit(self.miss, (column * c.SQUARE_SIZE, row * c.SQUARE_SIZE))

                # Draw a thick vertical seperator AND skip axis label in board corners by "continue"
                pg.draw.line(self.screen, c.BLACK, (c.WIN_X/2, 0), (c.WIN_X/2, c.WIN_Y), 5)
                # Draw thin vertical grid lines.
                pg.draw.line(self.screen, c.BLACK, (column * c.SQUARE_SIZE, 0), (column * c.SQUARE_SIZE, c.WIN_Y), 1)
                # Draw thin horizontal line on the grid between boards
                pg.draw.line(self.screen, c.BLACK, (0, row * c.SQUARE_SIZE), (c.WIN_X, row * c.SQUARE_SIZE), 1) 
                # Draw column labels (A, B, C, ...)
                if row == 0 and column != 0 and column != c.NUM_COLS:
                    self.screen.blit(self.font.render(c.Alpha[(column - 1) % 10], True, c.BLACK), (column * c.SQUARE_SIZE, row))
                    
                # Draw row labels (1, 2, 3, ...)
                if row != 0 and (column == 0 or column == c.NUM_COLS):
                    self.screen.blit(self.font.render(str(row), True, c.BLACK), (int(column*c.SQUARE_SIZE + c.SQUARE_SIZE/4), row * c.SQUARE_SIZE))
                    
        if (gs.is_placing and (gs.in_transition == False)):
            #display a mock ship and the direction it's being placed
            mousePos = pg.mouse.get_pos()
            pg.draw.line(self.screen, c.RED, (mousePos[0], mousePos[1]), (mousePos[0] + c.SQUARE_SIZE * gs.lenShip * c.DIRS[gs.shipDir][0], mousePos[1] + (c.SQUARE_SIZE * gs.lenShip * c.DIRS[gs.shipDir][1])), 10)

        # Highlight the active board
        if (gs.is_placing):
            if (gs.in_transition):
                self.screen.blit(self.boardHighlight_grey, (0,0)) #Right Half is player 2
            else:
                self.screen.blit(self.boardHighlight, ( 0 if gs.is_P1_turn else c.NUM_COLS*c.SQUARE_SIZE,0)) #Right Half is player 2
        elif (gs.is_shooting):
            if (gs.in_transition):
                self.screen.blit(self.boardHighlight_grey, (0,0))
            else:
                self.screen.blit(self.boardHighlight, (c.NUM_COLS*c.SQUARE_SIZE if gs.is_P1_turn else 0, 0))
            
        pg.display.update()
