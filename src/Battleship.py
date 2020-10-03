import pygame as pg
import sys
import math
from src.BattleshipView import BattleshipView
from src.GameState import GameState
from src.grid import Grid
from src.ship import Ship, ShipNode
import src.constants as c
from src.AI import AI

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
        self.gs = GameState()
        self.gs.msg = "Awaiting number of ships..."
        self.view.draw(self.gs)
        self.gs.numShipsPerPlayer = self.view.get_num_ships()
        self.gs.playerType = self.view.get_player_type()
        if not self.gs.playerType == 1:
            self.AI = AI(self.gs.playerType)

    def checkValidShip(self, is_P1_turn, effectiveX, effectiveY):

        """
        @pre game is running, one player is placing
        @post returns true if that ship placement results in no overslow/index errors/another ship is in the way, else false
        @param is_P1_turn indicates if player 1 is the one placing (otherwise player 2)
        @param effectiveX/Y is the converted mouse input mapped to the grid
        @author Daniel, Saher, Drake
        """

        # Loop through all "ship squares", checking they are within the correct board and unoccupied
        for i in range(self.gs.lenShip):
            squareX = effectiveX + c.DIRS[self.gs.shipDir][0] * i #c.DIRS is the direction of the ship. 2-D Array Ex. arr[i][j]
            squareY = effectiveY + c.DIRS[self.gs.shipDir][1] * i
            # If the Y coordinate is not in the bottom board area, the ship is not valid
            if (squareY >= (c.NUM_ROWS) or # Bottom edge
                squareY <= (0) or # Top edge
                squareX <= (0 if is_P1_turn else c.NUM_COLS) or # Left edge
                squareX >= (c.NUM_COLS if is_P1_turn else (c.NUM_COLS*2)) or # Right edge
                self.gs.grid.grid[squareY][squareX] != "Open"): # Space occupied
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
        @author James Krajicek
        """

        # Loop through all "ship squares" and place them on the grid
        for i in range(self.gs.lenShip):
            squareX = effectiveX + c.DIRS[self.gs.shipDir][0] * i
            squareY = effectiveY + c.DIRS[self.gs.shipDir][1] * i
            self.gs.grid.grid[squareY][squareX] = "Ship"
            ship.addSquare(squareX, squareY) #Same for both players.

    def placing(self, effectiveX, effectiveY, gs, player_name):
        player_ships = gs.p1Ships if gs.is_P1_turn else gs.p2Ships
        if self.checkValidShip(gs.is_P1_turn, effectiveX, effectiveY):
            newShip = Ship()
            self.placeShip(gs.is_P1_turn, effectiveX, effectiveY, newShip)
            player_ships.append(newShip)
            gs.lenShip += 1
            gs.msg = "P1 place your " + str(gs.lenShip) + " ship. Press \"R\" to rotate."
            # If player one finishes placing, reset things for player two's turn
            if gs.lenShip > gs.numShipsPerPlayer:
                if gs.is_P1_turn:
                    gs.msg = "Now P2, place your 1 ship. Press \"R\" to rotate."
                    gs.shipDir = 0
                    gs.is_P1_turn = False
                    gs.lenShip = 1
                else: #P2 turn
                    gs.is_P1_turn = True
                    gs.is_placing = False
                    gs.is_shooting = True
                    gs.msg = "All ships placed. P1 shoot first."
        else:
            gs.msg = player_name + " invalid ship location! Press \"R\" to rotate."

    def shooting(self, effectiveX, effectiveY, gs, player_name):
        enemy_ships = gs.p2Ships if gs.is_P1_turn else gs.p1Ships
        # If the player fired at an open space on the correct board
        if (0 < effectiveY < c.NUM_ROWS and
            ((c.NUM_COLS if gs.is_P1_turn else 0) < effectiveX < ((c.NUM_COLS*2) if gs.is_P1_turn else c.NUM_COLS)) and 
            ((gs.grid.grid[effectiveY][effectiveX] == "Open") or (gs.grid.grid[effectiveY][effectiveX] == "Ship")) 
        ):
            gs.grid.shoot(effectiveY, effectiveX)
            gs.msg = player_name + " miss."
            gs.is_P1_turn = not gs.is_P1_turn
            # Find if the space they attacked has an enemy ship
            for ship in enemy_ships: #For each ship element in the array of enemy ships (assigned above) do the following:
                for square in ship.shipSquares: #For each square contained in the target ship's array of squares do the following:
                    # If player hit a ship
                    if square.x == effectiveX and square.y == effectiveY: #If the point you clicked on is at the same location as a square contained by the ship then do the following:
                        self.view.play_hit_sound()
                        gs.msg = player_name + " hit!"
                        square.hit = True
                        # Check if they sunk the ship
                        if ship.checkSunk():
                            self.view.play_sunk_sound()
                            gs.msg = player_name + " sunk a ship!"
                            # Check if they won the game
                            if gs.grid.check_winner(gs.numShipsPerPlayer):
                                gs.msg = player_name + " wins!"
                                gs.is_shooting = False
        else:
            gs.msg = player_name + " invalid space! Try again."
    def run(self):

        """
        @pre none
        @post The game starts. The function finishes when the game finishes.
        @author Saher and Daniel
        """

        # Initialize the clock to control framerate
        clock = pg.time.Clock()

        gs = self.gs
        gs.is_P1_turn = True
        gs.is_placing = True
        gs.is_shooting = False
        gs.p1Ships = []
        gs.p2Ships = []
        gs.msg = "First P1, place your 1 ship. Press 'R' to rotate."

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
                    if event.key == pg.K_r and gs.is_placing:
                        gs.shipDir = (gs.shipDir + 1) % len(c.DIRS)

                if not gs.is_P1_turn and not gs.playerType == 1:
                    effectiveX, effectiveY  = self.AI.shipPlacement()
                    player_name = "P" + str(2-int(gs.is_P1_turn)) # P1 or P2

                    if gs.is_placing:
                        self.placing(effectiveX, effectiveY, gs, player_name)

                    elif gs.is_shooting:
                        self.shooting(effectiveX, effectiveY, gs, player_name)     

                    break               

                # When the user clicks, do one of three things  
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Get the mouse position and convert it to an X/Y coordinate on the grid
                    mousePos = pg.mouse.get_pos() #mousePos within the game window
                    effectiveX = math.floor(mousePos[0]/(c.SQUARE_SIZE)) #Pixel Count/Pixels per square == Cell that the mouse clicked on.
                    effectiveY = math.floor(mousePos[1]/(c.SQUARE_SIZE))
                    player_name = "P" + str(2-int(gs.is_P1_turn)) # P1 or P2

                    if gs.is_placing:
                        self.placing(effectiveX, effectiveY, gs, player_name)

                    elif gs.is_shooting:
                        self.shooting(effectiveX, effectiveY, gs, player_name)
            # Update the screen for this frame
            self.view.draw(gs)
            # Advance the while loop at increments of 60FPS
            clock.tick(60)
