import pygame as pg
import tkinter as tk
import tkinter.simpledialog
import os
import sys
import src.constants as c

class BattleshipView:
    """
        This class handles all of the GUI components of the game
    """
    def __init__(self):
    
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
        self.boardHighlight = pg.Surface((int(c.WIN_X / 2), int(c.WIN_Y / 2)))
        self.boardHighlight.set_alpha(99)
        self.boardHighlight.fill(c.RED)
        self.bg = pg.transform.scale(pg.image.load("media/background-day.jpg"), (c.WIN_X, c.WIN_Y))
        self.hit = pg.transform.scale(pg.image.load("media/redX.png"), (c.SQUARE_SIZE, c.SQUARE_SIZE))
        self.miss = pg.transform.scale(pg.image.load("media/blackX.png"), (c.SQUARE_SIZE, c.SQUARE_SIZE))
        self.sunk_sound = pg.mixer.Sound("media/sunk.wav")
        self.hit_sound = pg.mixer.Sound("media/hit.wav")
        self.font = pg.font.Font('freesansbold.ttf', 44)
        self.msg_font = pg.font.Font('freesansbold.ttf', c.MSG_FONT_SIZE)
        
    def get_num_ships(self):
        # Get the number of ships per player, and protect from bad input
        root = tk.Tk()
        root.eval('tk::PlaceWindow . center') # Approximately center the dialog
        root.withdraw()
        numShipsPerPlayer = tkinter.simpledialog.askinteger("Battleship", "How many ships per player? (1-5)", minvalue=1, maxvalue=5)
        if numShipsPerPlayer is None: # User pressed cancel
            pg.quit()
            sys.exit()
        return numShipsPerPlayer
        
    def play_hit_sound(self):
        self.channel1.play(self.hit_sound)
    
    def play_sunk_sound(self):
        self.channel2.play(self.sunk_sound)
        
    def draw(self, gs):
        """
        @pre game is running
        @post The screen is updated for the next frame
        @param gs The GameState object representing the current state of the game
        @author Daniel, Saher, Drake
        """

        # Draw the background
        self.screen.blit(self.bg, (0,0))
        pg.draw.rect(self.screen, c.BLACK, (0, c.WIN_Y, c.WIN_X, c.MSG_FONT_SIZE))
        
        # Render message centered below board
        text = self.msg_font.render(gs.msg, 1, c.WHITE)
        self.screen.blit(text, text.get_rect(centerx=c.WIN_X//2, top=c.WIN_Y))
        
        # Loop through all squares on the grid
        for i in range(len(gs.grid.grid)):
            for j in range(len(gs.grid.grid[0])):
                # Draw thin vertical line on grid
                pg.draw.line(self.screen, c.BLACK, (j * c.SQUARE_SIZE, 0), (j * c.SQUARE_SIZE, c.WIN_Y), 1)
                # If the square is a ship, draw the ship only when that player is placing
                if gs.grid.grid[i][j] == "Ship" and gs.is_placing and i > 10 and ((gs.is_P1_turn and j < 10) or (not gs.is_P1_turn and j > 10)):
                    pg.draw.rect(self.screen, c.RED, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                elif gs.grid.grid[i][j] == "hit": # Draw hit marker
                    self.screen.blit(self.hit, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                elif gs.grid.grid[i][j] == "miss": # Draw miss marker
                    self.screen.blit(self.miss, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                if i % 10 == 0:
                    # Draw a thick horizontal seperator between boards
                    pg.draw.line(self.screen, c.BLACK, (i * c.SQUARE_SIZE, 0), (i * c.SQUARE_SIZE, c.WIN_Y), 5)
                    if j % 10 == 0: 
                        # Draw a thick vertical seperator AND skip axis label in board corners by "continue"
                        pg.draw.line(self.screen, c.BLACK, (0, j * c.SQUARE_SIZE), (c.WIN_X, j * c.SQUARE_SIZE), 5)
                        continue
                    # Draw axis labels
                    self.screen.blit(self.font.render(c.Alpha[(j - 1) % 10], True, c.BLACK), (int(j * c.SQUARE_SIZE), int(i * c.SQUARE_SIZE)))
                    self.screen.blit(self.font.render(str(j % 10), True, c.BLACK), (int(i * c.SQUARE_SIZE + c.SQUARE_SIZE / 4), int(j * c.SQUARE_SIZE)))
            # Draw thin horizontal line on the grid between boards
            pg.draw.line(self.screen, c.BLACK, (0, i * c.SQUARE_SIZE), (c.WIN_X, i * c.SQUARE_SIZE), 1)
        if gs.is_placing:
            #display a mock ship and the direction it's being placed
            mousePos = pg.mouse.get_pos()
            pg.draw.line(self.screen, c.RED, (mousePos[0], mousePos[1]), (mousePos[0] + c.SQUARE_SIZE * gs.lenShip * c.DIRS[gs.shipDir][0], mousePos[1] + (c.SQUARE_SIZE * gs.lenShip * c.DIRS[gs.shipDir][1])), 10)
        
        # Highlight the active board
        if gs.is_placing or gs.is_shooting:
            self.screen.blit(self.boardHighlight, (
                int(not gs.is_P1_turn)*10*c.SQUARE_SIZE, # Right half if player 2
                int(gs.is_placing)*10*c.SQUARE_SIZE, # Bottom half if placing
                10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE))
        
        pg.display.update()