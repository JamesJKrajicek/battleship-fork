import pygame as pg
import tkinter as tk
import tkinter.simpledialog
import os
import sys
import math
from src.grid import Grid
from src.ship import Ship, ShipNode
import src.constants as c
class Battleship:
    def __init__(self):

        """
        @pre none
        @post Battleship class is created and is ready to be run
        @param none
        @author Daniel and Saher
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
        # Initialize the clock to control framerate
        self.clock = pg.time.Clock()
        
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
        
        self.shipDir = 0 # Direction of the ship currently being placed (index of c.DIRS)
        self.lenShip = 1 # Length of the ship to place next
        self.msg = "Awaiting number of ships..." # Message to display below game board
        self.grid = Grid()
        
        self.draw(False, False, False)
        
        # Get the number of ships per player, and protect from bad input
        root = tk.Tk()
        root.eval('tk::PlaceWindow . center') # Approximately center the dialog
        root.withdraw()
        self.numShipsPerPlayer = tkinter.simpledialog.askinteger("Battleship", "How many ships per player? (1-5)", minvalue=1, maxvalue=5)
        if self.numShipsPerPlayer is None: # User pressed cancel
            pg.quit()
            sys.exit()

    def draw(self, is_P1_turn, is_placing, is_shooting):

        """
        @pre game is running
        @post The screen is updated for the next frame
        @param is_P1_turn if it is currently player 1's turn, else player 2.
        @param is_placing If ships are currently being placed
        @param is_shooting If ships are currently being shot
        @author Daniel, Saher, Drake
        """

        # Draw the background
        self.screen.blit(self.bg, (0,0))
        pg.draw.rect(self.screen, c.BLACK, (0, c.WIN_Y, c.WIN_X, c.MSG_FONT_SIZE))
        
        # Render message centered below board
        text = self.msg_font.render(self.msg, 1, c.WHITE)
        self.screen.blit(text, text.get_rect(centerx=c.WIN_X//2, top=c.WIN_Y))
        
        # Loop through all squares on the grid
        for i in range(len(self.grid.grid)):
            for j in range(len(self.grid.grid[0])):
                # Draw thin vertical line on grid
                pg.draw.line(self.screen, c.BLACK, (j * c.SQUARE_SIZE, 0), (j * c.SQUARE_SIZE, c.WIN_Y), 1)
                # If the square is a ship, draw the ship only when that player is placing
                if self.grid.grid[i][j] == "Ship" and is_placing and i > 10 and ((is_P1_turn and j < 10) or (not is_P1_turn and j > 10)):
                    pg.draw.rect(self.screen, c.RED, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                elif self.grid.grid[i][j] == "hit": # Draw hit marker
                    self.screen.blit(self.hit, (j * c.SQUARE_SIZE, i * c.SQUARE_SIZE, c.SQUARE_SIZE, c.SQUARE_SIZE))
                elif self.grid.grid[i][j] == "miss": # Draw miss marker
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
        if is_placing:
            #display a mock ship and the direction it's being placed
            mousePos = pg.mouse.get_pos()
            pg.draw.line(self.screen, c.RED, (mousePos[0], mousePos[1]), (mousePos[0] + c.SQUARE_SIZE * self.lenShip * c.DIRS[self.shipDir][0], mousePos[1] + (c.SQUARE_SIZE * self.lenShip * c.DIRS[self.shipDir][1])), 10)
        
        # Highlight the active board
        if is_placing or is_shooting:
            self.screen.blit(self.boardHighlight, (
                int(not is_P1_turn)*10*c.SQUARE_SIZE, # Right half if player 2
                int(is_placing)*10*c.SQUARE_SIZE, # Bottom half if placing
                10*c.SQUARE_SIZE, 10*c.SQUARE_SIZE))
        
        pg.display.update()

    def checkValidShip(self, is_P1_turn, effectiveX, effectiveY):

        """
        @pre game is running, one player is placing
        @post returns true if that ship placement results in no overslow/index errors/another ship is in the way, else false
        @param is_P1_turn indicates if player 1 is the one placing (otherwise player 2)
        @param effectiveX/Y is the converted mouse input mapped to the grid
        @author Daniel, Saher, Drake
        """
        
        # Loop through all "ship squares", checking they are within the correct board and unoccupied
        for i in range(self.lenShip):
            squareX = effectiveX + c.DIRS[self.shipDir][0] * i
            squareY = effectiveY + c.DIRS[self.shipDir][1] * i
            # If the Y coordinate is not in the bottom board area, the ship is not valid
            if (squareY >= 20 or # Bottom edge
                squareY <= 10 or # Top edge
                squareX <= int(not is_P1_turn)*10 or # Left edge
                squareX >= 10+int(not is_P1_turn)*10 or # Right edge
                self.grid.grid[squareY][squareX] != "Open"): # Space occupied
                return False

		# All ship squares are valid, so placement is valid
        return True

    def placeShip(self, is_P1_turn, effectiveX, effectiveY, ship):

        """
        @pre game is running and one of the players is placing
        @post ship is placed on grid
        @param effectiveX/Y are the converted mouse inputs
        @param is_P1_turn indicates if player 1 is the one placing (otherwise player 2)
        @param Ship is the ship to be placed
        @author Daniel
        """

        # Loop through all "ship squares" and place them on the grid
        for i in range(self.lenShip):
            squareX = effectiveX + c.DIRS[self.shipDir][0] * i
            squareY = effectiveY + c.DIRS[self.shipDir][1] * i
            self.grid.grid[squareY][squareX] = "Ship"
            # The -10 and +10 for squareX is because the placing and attacking boards are on opposite sides
            if is_P1_turn:
                ship.addSquare(squareX + 10, squareY - 10)
            else: #Player 2
                ship.addSquare(squareX - 10, squareY - 10)

    def run(self):

        """
        @pre none
        @post The game starts. The function finishes when the game finishes.
        @author Saher and Daniel
        """

        is_P1_turn = True
        is_placing = True
        is_shooting = False
        p1Ships = []
        p2Ships = []
        self.msg = "First P1, place your 1 ship. Press 'R' to rotate."
        # Game loop
        while 1:
            # Loop through all events
            for event in pg.event.get():
                # If the window is closed, exit program
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    # If the user types "r" and someone is placing, rotate to the next direction
                    if event.key == pg.K_r and is_placing:
                        self.shipDir = (self.shipDir + 1) % len(c.DIRS)
                # When the user clicks, do one of three things
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Get the mouse position and convert it to an X/Y coordinate on the grid
                    mousePos = pg.mouse.get_pos()
                    effectiveX = math.floor(mousePos[0]/(c.SQUARE_SIZE))
                    effectiveY = math.floor(mousePos[1]/(c.SQUARE_SIZE))
                    player_name = "P" + str(2-int(is_P1_turn)) # P1 or P2

                    if is_placing:
                        player_ships = p1Ships if is_P1_turn else p2Ships
                        
                        if self.checkValidShip(is_P1_turn, effectiveX, effectiveY):
                            newShip = Ship()
                            self.placeShip(is_P1_turn, effectiveX, effectiveY, newShip)
                            player_ships.append(newShip)
                            self.lenShip += 1
                            self.msg = "P1 place your " + str(self.lenShip) + " ship. Press \"R\" to rotate."
                            # If player one finishes placing, reset things for player two's turn
                            if self.lenShip > self.numShipsPerPlayer:
                                if is_P1_turn:
                                    self.msg = "Now P2, place your 1 ship. Press \"R\" to rotate."
                                    self.shipDir = 0
                                    is_P1_turn = False
                                    self.lenShip = 1
                                else: #P2 turn
                                    is_P1_turn = True
                                    is_placing = False
                                    is_shooting = True
                                    self.msg = "All ships placed. P1 shoot first."
                        else:
                            self.msg = player_name + " invalid ship location! Press \"R\" to rotate."

                    elif is_shooting:
                        enemy_ships = p2Ships if is_P1_turn else p1Ships

                        # If the player fired at an open space on the correct board
                        if (0 < effectiveY < 10 and 
                            (0 if is_P1_turn else 10) < effectiveX < (10 if is_P1_turn else 20) and 
                            self.grid.grid[effectiveY][effectiveX] == "Open"
                        ):
                            self.grid.shoot(effectiveY, effectiveX)
                            self.msg = player_name + " miss."
                            is_P1_turn = not is_P1_turn
                            # Find if the space they attacked has an enemy ship
                            for ship in enemy_ships:
                                for square in ship.shipSquares:
                                    # If player hit a ship
                                    if square.x == effectiveX and square.y == effectiveY:
                                        self.channel1.play(self.hit_sound)
                                        self.msg = player_name + " hit!"
                                        square.hit = True
                                        # Check if they sunk the ship
                                        if not ship.sunk and ship.checkSunk():
                                            self.channel2.play(self.sunk_sound)
                                            self.msg = player_name + " sunk a ship!"
                                            # Check if they won the game
                                            if self.grid.check_winner(self.numShipsPerPlayer):
                                                self.msg = player_name + " wins!"
                                                is_shooting = False
                                        break
                        else:
                            self.msg = player_name + " invalid space! Try again."
            # Update the screen for this frame
            self.draw(is_P1_turn, is_placing, is_shooting)
            # Advance the while loop at increments of 60FPS
            self.clock.tick(60)