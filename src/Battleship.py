import pygame as pg
import sys
from time import sleep
import math
from src.BattleshipView import BattleshipView
from src.GameState import GameState
from src.grid import Grid
from src.ship import Ship, ShipNode
import src.constants as c
from src.AI import AI

class Battleship:
    """!
    This class handles the game's core logic, including setup, listening for events from the user, placing ships, attacking, switching turns, and verifying moves are valid.
    """

    def __init__(self):
        """!
        @pre none
        @post The members of the Battleship object are initialized, including the game view and state. The number of ships and opponent are determined and stored in the game state.
        """
        self.transition_next = False
        self.transition_clicks = 0
        self.view = BattleshipView()
        self.gs = GameState()
        self.gs.msg = "Awaiting number of ships..."
        self.view.draw(self.gs)
        self.gs.numShipsPerPlayer = self.view.get_num_ships()
        self.gs.playerType = self.view.get_player_type()
        if not self.gs.playerType == 1:
            self.ai = AI(self.gs.playerType)

    def checkValidShip(self, is_P1_turn, effectiveX, effectiveY, lenShip, shipDir):
        """!
        @pre None
        @post None
        @param bool: is_P1_turn Indicates if player 1 is the one placing (otherwise player 2)
        @param effectiveX int: The X-coordinate of the grid the ship is attempting to be placed (0-19)
        @param effectiveY int: The Y-coordinate of the grid the ship is attempting to be placed (0-9)
        @param lenShip int: The length of the ship to place (1-5)
        @param shipDir [int, int]: The direction to place the ship in the form of an [x, y] pair where x and y are -1, 0, or 1 (from c.DIRS)
        @return bool: Whether the ship fits entirely within the correct player's board and does not overlap an existing ship
        """
        # Loop through all "ship squares", checking they are within the correct board and unoccupied
        for i in range(lenShip):
            squareX = effectiveX + c.DIRS[shipDir][0] * i #c.DIRS is the direction of the ship. 2-D Array Ex. arr[i][j]
            squareY = effectiveY + c.DIRS[shipDir][1] * i
            # If the Y coordinate is not in the bottom board area, the ship is not valid
            if (squareY >= (c.NUM_ROWS) or # Bottom edge
                squareY <= (0) or # Top edge
                squareX <= (0 if is_P1_turn else c.NUM_COLS) or # Left edge
                squareX >= (c.NUM_COLS if is_P1_turn else (c.NUM_COLS*2)) or # Right edge
                self.gs.grid.grid[squareY][squareX] != "Open"): # Space occupied
                return False

		# All ship squares are valid, so placement is valid
        return True

    def placeShip(self, ship, effectiveX, effectiveY, lenShip, shipDir):
        """!
        @pre effectiveX, effectiveY, lenShip, and shipDir together are a valid ship placement for the current player
        @post Ship object is placed on self.gs.grid and has its ShipSpaces initialized
        @param ship Ship: The Ship object to place on the grid and populate with ShipSpaces
        @param effectiveX int: The X-coordinate of the grid the ship will be placed (0-19)
        @param effectiveY int: The Y-coordinate of the grid the ship will be placed (0-9)
        @param lenShip int: The length of the ship to place (1-5)
        @param shipDir [int, int]: The direction to place the ship in the form of an [x, y] pair where x and y are -1, 0, or 1 (one of c.DIRS)
        """
        # Loop through all "ship squares" and place them on the grid
        for i in range(lenShip):
            squareX = effectiveX + c.DIRS[shipDir][0] * i
            squareY = effectiveY + c.DIRS[shipDir][1] * i
            self.gs.grid.grid[squareY][squareX] = "Ship"
            ship.addSquare(squareX, squareY) #Same for both players.

    def placing(self, effectiveX, effectiveY, gs, player_name):
        """!
        @pre A player has selected a location on the grid to attempt to place a ship
        @post The message is updated. If the location is valid, the ship is placed and the game proceeds to the next ship placement (or to shooting if all ships placed).
        @param effectiveX int: The X-coordinate of the grid the ship will attempt to be placed (0-19)
        @param effectiveY int: The Y-coordinate of the grid the ship will attempt to be placed (0-9)
        @param gs GameState: The object representing the current state of the game. This will be modified upon successful ship placement.
        @param player_name string: The name of the current player to include in the message
        """
        player_ships = gs.p1Ships if gs.is_P1_turn else gs.p2Ships
        if (self.transition_next == False):
            if self.checkValidShip(gs.is_P1_turn, effectiveX, effectiveY, gs.lenShip, gs.shipDir):
                newShip = Ship()
                self.placeShip(newShip, effectiveX, effectiveY, gs.lenShip, gs.shipDir)
                player_ships.append(newShip)
                gs.lenShip += 1
                gs.msg = player_name + " place your " + str(gs.lenShip) + " ship. Press \"R\" to rotate."
                # If player one finishes placing, reset things for player two's turn
                if gs.lenShip > gs.numShipsPerPlayer:
                    if (gs.is_P1_turn):
                        gs.msg = "Now P2, place your 1 ship. Press \"R\" to rotate."
                        gs.shipDir = 0
                        gs.is_P1_turn = False
                        gs.lenShip = 1
                    else:
                        self.transition_next = True

            else:
                gs.msg = player_name + " invalid ship location! Press \"R\" to rotate."

    def shooting(self, effectiveX, effectiveY, gs, player_name):
        """!
        @pre A player has selected a location on the grid to attempt to fire
        @post The message is updated. If the location is valid (correct board and not already attacked), checks for a hit, sink, or win. If not a win, switches turns.
        @param effectiveX int: The X-coordinate of the grid being fired at (0-19)
        @param effectiveY int: The Y-coordinate of the grid being fired at (0-9)
        @param gs GameState: The object representing the current state of the game. This will be modified upon successful firing.
        @param player_name string: The name of the current player to include in the message
        """
        enemy_ships = gs.p2Ships if gs.is_P1_turn else gs.p1Ships
        # If the player fired at an open space on the correct board
        if (0 < effectiveY < c.NUM_ROWS and
            ((c.NUM_COLS if gs.is_P1_turn else 0) < effectiveX < ((c.NUM_COLS*2) if gs.is_P1_turn else c.NUM_COLS)) and
            ((gs.grid.grid[effectiveY][effectiveX] == "Open") or (gs.grid.grid[effectiveY][effectiveX] == "Ship"))
        ):
            self.transition_next = True
            gs.grid.shoot(effectiveY, effectiveX)
            gs.msg = player_name + " miss (left click to change turn)"
            if (gs.playerType != 1) and (not gs.is_P1_turn):
                self.ai.hit_shot = False
            # Find if the space they attacked has an enemy ship
            for ship in enemy_ships: #For each ship element in the array of enemy ships (assigned above) do the following:
                for square in ship.shipSquares: #For each square contained in the target ship's array of squares do the following:
                    # If player hit a ship
                    if square.x == effectiveX and square.y == effectiveY: #If the point you clicked on is at the same location as a square contained by the ship then do the following:
                        self.view.play_hit_sound()
                        gs.msg = player_name + " hit! (left click to change turn)"
                        square.hit = True
                        if (gs.playerType != 1) and (not gs.is_P1_turn):
                            self.ai.hit_shot = True
                        # Check if they sunk the ship
                        if ship.checkSunk():
                            self.view.play_sunk_sound()
                            gs.msg = player_name + " sunk a ship! (left click to change turn)"
                            # Check if they won the game
                            if gs.grid.check_winner(gs.numShipsPerPlayer):
                                gs.msg = player_name + " wins!"
                                gs.is_shooting = False
                                self.transition_next = False
        else:
            gs.msg = player_name + " invalid space! Try again."

    def special_shot(self, effectiveX, effectiveY, gs, player_name):
        """!
        @pre A player has selected a location on the grid to attempt to fire a special shot
        @post The message is updated. If the player has a special shot available and is firing within their board, fires at all spaces in a 3x3 area
        @param effectiveX int: The X-coordinate of the grid being fired at (0-19)
        @param effectiveY int: The Y-coordinate of the grid being fired at (0-9)
        @param gs GameState: The object representing the current state of the game. This will be modified upon successful firing.
        @param player_name string: The name of the current player to include in the message
        """

        # Ensure the player has special shots available
        special_shots = gs.p1_special_shots if self.gs.is_P1_turn else gs.p2_special_shots
        if special_shots <= 0:
            gs.msg = "No special shots available. Left click for normal shot."
            return

        # Ensure the entire 3x3 area is within the player's board
        board_left_edge = c.NUM_COLS + 2 if gs.is_P1_turn else 2
        board_right_edge = c.NUM_COLS*2 + 2 if gs.is_P1_turn else c.NUM_COLS - 2
        if effectiveY < 2 or effectiveY > c.NUM_COLS - 2 or effectiveX < board_left_edge or effectiveX > board_right_edge:
            gs.msg = "The 3x3 shot will not fit there. Try again."
            return

        enemy_ships = gs.p2Ships if gs.is_P1_turn else gs.p1Ships
        # Attack all spaces in the 3x3 area
        hit_or_miss = False # If any spaces got attacked
        hit_count = 0 # Number of ship spaces hit
        sink_count = 0 # Number of ships sunk
        for y in range(effectiveY-1, effectiveY+2):
            for x in range(effectiveX-1, effectiveX+2):
                if gs.grid.grid[y][x] == "hit" or gs.grid.grid[y][x] == "miss": # Skip already attacked spaces
                    continue
                gs.grid.shoot(y, x)
                hit_or_miss = True
                for ship in enemy_ships:
                    for square in ship.shipSquares:
                        if square.x == x and square.y == y:
                            self.view.play_hit_sound()
                            sleep(0.05) # So sounds don't overlap
                            square.hit = True
                            hit_count += 1
                            if ship.checkSunk():
                                self.view.play_sunk_sound()
                                sleep(0.05) # So sounds don't overlap
                                sink_count += 1
                                if gs.grid.check_winner(gs.numShipsPerPlayer):
                                    gs.msg = player_name + " wins!"
                                    gs.is_shooting = False
                                    self.transition_next = False

        if not hit_or_miss:
            gs.msg = "The 3x3 shot will not hit anything there. Try again."
        elif gs.is_shooting: # Make sure game wasn't won
            gs.msg = player_name + " hits:" + str(hit_count) + " and sinks:" + str(sink_count)
            self.transition_next = True # To switch turns
            # Remove the special shot
            if self.gs.is_P1_turn:
                gs.p1_special_shots -= 1
            else:
                gs.p2_special_shots -= 1

    def run(self):
        """!
        Runs the main game loop during gameplay (ship placement and attacking)
        @pre The number of ships and opponent has been selected
        @post The game has been exited
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

                # When the user clicks, do one of three things
                elif event.type == pg.MOUSEBUTTONDOWN: #NOTE: When AI methods are ready change condition to: gs.is_P1_turn and event.type == pg.MOUSEBUTTONDOWN
                    # Get the mouse position and convert it to an X/Y coordinate on the grid
                    mousePos = pg.mouse.get_pos() #mousePos within the game window
                    effectiveX = math.floor(mousePos[0]/(c.SQUARE_SIZE)) #Pixel Count/Pixels per square == Cell that the mouse clicked on.
                    effectiveY = math.floor(mousePos[1]/(c.SQUARE_SIZE))
                    player_name = "P1" if gs.is_P1_turn else "P2"

                    if event.button == 1: #Left click
                        if self.transition_next:
                            self.transition() #If the player's turn is done then move into the transition phase.
                        elif gs.is_placing:
                            self.placing(effectiveX, effectiveY, gs, player_name)
                            if (self.transition_next):
                                self.transition()

                        elif gs.is_shooting:
                            self.shooting(effectiveX, effectiveY, gs, player_name)

                    elif event.button == 3 and gs.is_shooting and not self.transition_next: # Right click
                        self.special_shot(effectiveX, effectiveY, gs, player_name)


            if not gs.is_P1_turn and not gs.playerType == 1:
                player_name = "P" + str(2 - int(gs.is_P1_turn))  # P1 or P2

                if gs.is_placing:
                    effectiveX, effectiveY = self.ai.shipPlacement(gs)
                    self.placing(effectiveX, effectiveY, gs, player_name)

                elif gs.is_shooting:
                    effectiveX, effectiveY = self.ai.getPoints(gs)
                    self.shooting(effectiveX, effectiveY, gs, player_name)

            while self.transition_next and gs.playerType != 1: # AI
                self.transition() # Skip transition when playing against AI

            if gs.is_P1_turn or gs.playerType == 1 or (not gs.is_placing and not gs.is_shooting):
                self.view.draw(gs)

            # Advance the while loop at increments of 60FPS
            clock.tick(60 if gs.is_placing else 15)

    def transition(self):
        """!
        Transitions the gameplay from a player's turn to a blank transition state (transition_clicks == 0) and back to the second player's board (transition_clicks == 1).
        @post The second player's board is displayed and ready for gameplay.
        """
        #if self.gs.playerType != 1: # AI
        #    self.transition_clicks = 1 # Skip transition

        if self.transition_clicks == 0:
            self.gs.in_transition = True
            self.gs.is_P1_turn = not self.gs.is_P1_turn
            player_name = "P1" if self.gs.is_P1_turn else "P2"
            self.gs.msg = player_name + ", left click to start your turn."
            self.transition_clicks = 1
        elif self.transition_clicks == 1:
            self.gs.in_transition = False
            self.transition_next = False
            self.transition_clicks = 0

            if self.gs.is_placing:
                #self.gs.is_P1_turn = True
                self.gs.is_placing = False
                self.gs.is_shooting = True
                self.gs.msg = "All ships placed. P1 shoot first."

            else: # Shooting
                # Update round and special shots
                if self.gs.is_P1_turn:
                    self.gs.round += 1
                    if self.gs.round % c.SPECIAL_SHOT_RATE == 0:
                        self.gs.p1_special_shots += 1
                        self.gs.p2_special_shots += 1

                player_name = "P1" if self.gs.is_P1_turn else "P2"
                special_shots = self.gs.p1_special_shots if self.gs.is_P1_turn else self.gs.p2_special_shots
                self.gs.msg = player_name + " make your shot. Special shots (right click): " + str(special_shots)
