import pygame as pg
import sys
import math
from src.BattleshipView import BattleshipView
from src.grid import Grid
from src.ship import Ship, ShipNode
import src.constants as c

class Battleship:
    """
        This class handles the game logic
    """
    
    def __init__(self):

        """
        @pre none
        @post Battleship class is created and is ready to be run
        @param none
        @author Daniel and Saher
        """
        
        self.view = BattleshipView()
        
        # These members are "public", to be used in BattleshipView
        self.grid = Grid()
        self.shipDir = 0 # Direction of the ship currently being placed (index of c.DIRS)
        self.lenShip = 1 # Length of the ship to place next
        self.msg = "Awaiting number of ships..." # Message to display below game board
        
        self.view.draw(self, False, False, False)
        
        self.numShipsPerPlayer = self.view.get_num_ships()

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
        
        # Initialize the clock to control framerate
        clock = pg.time.Clock()

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
                elif event.type == pg.KEYDOWN:
                    # If the user types "r" and someone is placing, rotate to the next direction
                    if event.key == pg.K_r and is_placing:
                        self.shipDir = (self.shipDir + 1) % len(c.DIRS)
                # When the user clicks, do one of three things
                elif event.type == pg.MOUSEBUTTONDOWN:
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
                                        self.view.play_hit_sound()
                                        self.msg = player_name + " hit!"
                                        square.hit = True
                                        # Check if they sunk the ship
                                        if not ship.sunk and ship.checkSunk():
                                            self.view.play_sunk_sound()
                                            self.msg = player_name + " sunk a ship!"
                                            # Check if they won the game
                                            if self.grid.check_winner(self.numShipsPerPlayer):
                                                self.msg = player_name + " wins!"
                                                is_shooting = False
                                        break
                        else:
                            self.msg = player_name + " invalid space! Try again."
            # Update the screen for this frame
            self.view.draw(self, is_P1_turn, is_placing, is_shooting)
            # Advance the while loop at increments of 60FPS
            clock.tick(60)