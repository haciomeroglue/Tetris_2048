import random  # each tetromino is created with a random x value above the grid
from tile import Tile  # used for representing each tile on the tetromino
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import copy as cp
import math


class Tetromino:

    rotatedBefore = 1
    def __init__(self, type, grid_height, grid_width, is_next=False):
        self.type = type
        self.rotatedBefore = 1
        # set grid_height and grid_width from input parameters
        self.grid_height = grid_height
        self.grid_width = grid_width
        # set the shape of the tetromino based on the given type
        self.occupied_tiles = []
        if type == 'I':
            n = 4  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino I in its initial orientation
            self.occupied_tiles.append((0, 0))  # (column_index, row_index)
            self.occupied_tiles.append((0, 1))
            self.occupied_tiles.append((0, 2))
            self.occupied_tiles.append((0, 3))
        elif type == 'O':
            n = 2  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino O in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((0, 1))
            self.occupied_tiles.append((1, 1))
        elif type == 'Z':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((1, 1))
            self.occupied_tiles.append((2, 1))
        elif type == 'J':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((2, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((2, 1))
        elif type == 'L':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((2, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((0, 1))
        elif type == 'T':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((2, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((1, 1))
        elif type == 'S':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 1))
            self.occupied_tiles.append((2, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((1, 1))
            # create a matrix of numbered tiles based on the shape of the tetromino
        self.tile_matrix = np.full((n, n), None)
        # initial position of the bottom-left tile in the tile matrix just before
        # the tetromino enters the game grid
        self.bottom_left_corner = Point()
        # upper side of the game grid
        self.bottom_left_corner.y = grid_height
        # a random horizontal position
        self.bottom_left_corner.x = random.randint(0, grid_width - n)

        # create each tile by computing its position w.r.t. the game grid based on
        # its bottom_left_corner
        for i in range(len(self.occupied_tiles)):
            col_index, row_index = self.occupied_tiles[i][0], self.occupied_tiles[i][1]
            position = Point()
            # horizontal position of the tile
            position.x = self.bottom_left_corner.x + col_index
            # vertical position of the tile
            position.y = self.bottom_left_corner.y + (n - 1) - row_index
            # create the tile on the computed position
            self.tile_matrix[row_index][col_index] = Tile(position)

    def get_type(self):
        return cp.copy(self.type)

    # Method for drawing the tetromino on the game grid
    def draw(self):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        for row in range(n):
            for col in range(n):
                # draw each occupied tile (not equal to None) on the game grid
                if self.tile_matrix[row][col] != None:
                    # considering newly entered tetrominoes to the game grid that may
                    # have tiles with position.y >= grid_height
                    position = self.tile_matrix[row][col].get_position()
                    if position.y < self.grid_height:
                        self.tile_matrix[row][col].draw()

                        # Method for moving the tetromino in a given direction by 1 on the game grid

    def move(self, direction, game_grid):
        # check if the tetromino can be moved in the given direction by using the
        # can_be_moved method defined below
        if not (self.can_be_moved(direction, game_grid)):
            return False  # tetromino cannot be moved in the given direction
        # move the tetromino by first updating the position of the bottom left tile
        if direction == "left":
            self.bottom_left_corner.x -= 1
        elif direction == "right":
            self.bottom_left_corner.x += 1
        else:  # direction == "down"
            self.bottom_left_corner.y -= 1
        # then moving each occupied tile in the given direction by 1
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] != None:
                    if direction == "left":
                        self.tile_matrix[row][col].move(-1, 0)
                    elif direction == "right":
                        self.tile_matrix[row][col].move(1, 0)
                    else:  # direction == "down"
                        self.tile_matrix[row][col].move(0, -1)
        return True  # successful move in the given direction

    # Moves the tetromino to given x and y position,
    # Adjusts the shift amount according to the upper left tile.
    def move_pos(self, dx, dy):
        # Keeps the leftmost tile position
        pivot_point = Point()

        # Check if the leftmost object is None, looks one unit left and bottom, sets the pivot point relative them
        if self.tile_matrix[0][0] != None:
            pivot_point.x = self.tile_matrix[0][0].get_position().x
            pivot_point.y = self.tile_matrix[0][0].get_position().y
        # If the lestmost object None, looks one to the bottom tile
        elif self.tile_matrix[0][1] != None:
            pivot_point.x = self.tile_matrix[0][1].get_position().x
            pivot_point.y = self.tile_matrix[0][1].get_position().y
        # If the lestmost object None, looks one to the right tile
        else:
            pivot_point.x = self.tile_matrix[1][0].get_position().x
            pivot_point.y = self.tile_matrix[1][0].get_position().y

        # Shifts each tile along with the pivot tile.
        for m in self.tile_matrix:
            for p in m:
                if p != None:
                    p.move(dx-pivot_point.x, dy-pivot_point.y)

    # Rotates tetrominos
    def rotateTetromino(self):
        if self.type == "I":
            if (self.rotatedBefore == 1):
                self.tile_matrix[0][0].move(0, -1)
                self.tile_matrix[1][0].move(1, 0)
                self.tile_matrix[2][0].move(2, 1)
                self.tile_matrix[3][0].move(3, 2)
                self.rotatedBefore = 2
            elif (self.rotatedBefore == 2):
                self.tile_matrix[0][0].move(1, -2)
                self.tile_matrix[1][0].move(0, -1)
                self.tile_matrix[2][0].move(-1, 0)
                self.tile_matrix[3][0].move(-2, 1)
                self.rotatedBefore = 3
            elif (self.rotatedBefore == 3):
                self.tile_matrix[0][0].move(2, 2)
                self.tile_matrix[1][0].move(1, 1)
                self.tile_matrix[2][0].move(0, 0)
                self.tile_matrix[3][0].move(-1, -1)
                self.rotatedBefore = 4
            elif (self.rotatedBefore == 4):
                self.tile_matrix[0][0].move(-3, 1)
                self.tile_matrix[1][0].move(-2, 0)
                self.tile_matrix[2][0].move(-1, -1)
                self.tile_matrix[3][0].move(0, -2)
                self.rotatedBefore = 1
        if self.type == "Z":
            if (self.rotatedBefore == 1):
                self.tile_matrix[0][0].move(2, 0)
                self.tile_matrix[0][1].move(1, -1)
                self.tile_matrix[1][2].move(-1, -1)
                self.rotatedBefore = 2
            elif (self.rotatedBefore == 2):
                self.tile_matrix[0][0].move(0, -2)
                self.tile_matrix[0][1].move(-1, -1)
                self.tile_matrix[1][2].move(-1, 1)
                self.rotatedBefore = 3
            elif (self.rotatedBefore == 3):
                self.tile_matrix[0][0].move(-2, 0)
                self.tile_matrix[0][1].move(-1, 1)
                self.tile_matrix[1][2].move(1, 1)
                self.rotatedBefore = 4
            elif (self.rotatedBefore == 4):
                self.tile_matrix[0][0].move(0, 2)
                self.tile_matrix[0][1].move(1, 1)
                self.tile_matrix[1][2].move(1, -1)
                self.rotatedBefore = 1

        if self.type == "S":
            if (self.rotatedBefore == 1):
                self.tile_matrix[0][1].move(1, -1)
                self.tile_matrix[0][2].move(0, -2)
                self.tile_matrix[1][0].move(1, 1)
                self.rotatedBefore = 2
            elif (self.rotatedBefore == 2):
                self.tile_matrix[0][1].move(-1, -1)
                self.tile_matrix[0][2].move(-2, 0)
                self.tile_matrix[1][0].move(1, -1)
                self.rotatedBefore = 3
            elif (self.rotatedBefore == 3):
                self.tile_matrix[0][1].move(-1, 1)
                self.tile_matrix[0][2].move(0, 2)
                self.tile_matrix[1][0].move(-1, -1)
                self.rotatedBefore = 4
            elif (self.rotatedBefore == 4):
                self.tile_matrix[0][1].move(1, 1)
                self.tile_matrix[0][2].move(2, 0)
                self.tile_matrix[1][0].move(-1, 1)
                self.rotatedBefore = 1

        if self.type == "O":
            if (self.rotatedBefore == 1):
                self.tile_matrix[0][0].move(1, 0)
                self.tile_matrix[0][1].move(0, -1)
                self.tile_matrix[1][0].move(0, 1)
                self.tile_matrix[1][1].move(-1, 0)
                self.rotatedBefore = 2
            elif (self.rotatedBefore == 2):
                self.tile_matrix[0][0].move(0, -1)
                self.tile_matrix[0][1].move(-1, 0)
                self.tile_matrix[1][0].move(1, 0)
                self.tile_matrix[1][1].move(0, 1)
                self.rotatedBefore = 3
            elif (self.rotatedBefore == 3):
                self.tile_matrix[0][0].move(-1, 0)
                self.tile_matrix[0][1].move(0, 1)
                self.tile_matrix[1][0].move(0, -1)
                self.tile_matrix[1][1].move(1, 0)
                self.rotatedBefore = 4
            elif (self.rotatedBefore == 4):
                self.tile_matrix[0][0].move(0, 1)
                self.tile_matrix[0][1].move(1, 0)
                self.tile_matrix[1][0].move(-1, 0)
                self.tile_matrix[1][1].move(0, -1)
                self.rotatedBefore = 1
        if self.type == "L":
            if (self.rotatedBefore == 1):
                self.tile_matrix[0][0].move(1, -1)
                self.tile_matrix[0][1].move(0, -2)
                self.tile_matrix[0][2].move(-1, -3)
                self.rotatedBefore = 2
            elif (self.rotatedBefore == 2):
                self.tile_matrix[0][0].move(-1, -1)
                self.tile_matrix[0][1].move(-2, 0)
                self.tile_matrix[0][2].move(-3, 1)
                self.rotatedBefore = 3
            elif (self.rotatedBefore == 3):
                self.tile_matrix[0][0].move(-1, 1)
                self.tile_matrix[0][1].move(0, 2)
                self.tile_matrix[0][2].move(1, 3)
                self.rotatedBefore = 4
            elif (self.rotatedBefore == 4):
                self.tile_matrix[0][0].move(1, 1)
                self.tile_matrix[0][1].move(2, 0)
                self.tile_matrix[0][2].move(3, -1)
                self.rotatedBefore = 1
        if self.type == "J":
            if (self.rotatedBefore == 1):
                self.tile_matrix[0][0].move(3, 1)
                self.tile_matrix[0][1].move(2, 0)
                self.tile_matrix[0][2].move(1, -1)
                self.rotatedBefore = 2
            elif (self.rotatedBefore == 2):
                self.tile_matrix[0][0].move(1, -3)
                self.tile_matrix[0][1].move(0, -2)
                self.tile_matrix[0][2].move(-1, -1)
                self.rotatedBefore = 3
            elif (self.rotatedBefore == 3):
                self.tile_matrix[0][0].move(-3, -1)
                self.tile_matrix[0][1].move(-2, 0)
                self.tile_matrix[0][2].move(-1, 1)
                self.rotatedBefore = 4
            elif (self.rotatedBefore == 4):
                self.tile_matrix[0][0].move(-1, 3)
                self.tile_matrix[0][1].move(0, 2)
                self.tile_matrix[0][2].move(1, 1)
                self.rotatedBefore = 1
        if self.type == "T":
            if (self.rotatedBefore == 1):
                self.tile_matrix[0][0].move(2, 0)
                self.tile_matrix[0][1].move(1, -1)
                self.tile_matrix[0][2].move(0, -2)
                self.rotatedBefore = 2
            elif (self.rotatedBefore == 2):
                self.tile_matrix[0][0].move(0, -2)
                self.tile_matrix[0][1].move(-1, -1)
                self.tile_matrix[0][2].move(-2, 0)
                self.rotatedBefore = 3
            elif (self.rotatedBefore == 3):
                self.tile_matrix[0][0].move(-2, 0)
                self.tile_matrix[0][1].move(-1, 1)
                self.tile_matrix[0][2].move(0, 2)
                self.rotatedBefore = 4
            elif (self.rotatedBefore == 4):
                self.tile_matrix[0][0].move(0, 2)
                self.tile_matrix[0][1].move(1, 1)
                self.tile_matrix[0][2].move(2, 0)
                self.rotatedBefore = 1

    def draw_next_tet(self, curr_tet):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        for row in range(n):
            for col in range(n):
                # draw each occupied tile (not equal to None) on the game grid
                if self.tile_matrix[row][col] != None:
                    self.tile_matrix[row][col].set_number(curr_tet.tile_matrix[row][col].get_number())
                    self.tile_matrix[row][col].draw_next()





    # Method to check if the tetromino can be moved in the given direction or not
    def can_be_moved(self, dir, game_grid):
        n = len(self.tile_matrix)
        if dir == "left" or dir == "right":
            for row in range(n):
                for col in range(n):
                    # direction = left --> check the leftmost tile of each row
                    if dir == "left" and self.tile_matrix[row][col] != None:
                        leftmost = self.tile_matrix[row][col].get_position()

                        if leftmost.x == 0:
                            return False

                        if leftmost.y >= self.grid_height:
                            break

                        if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                            return False
                        break
                    # direction = right --> check the rightmost tile of each row
                    elif dir == "right" and self.tile_matrix[row][n - 1 - col] != None:
                        rightmost = self.tile_matrix[row][n - 1 - col].get_position()

                        if rightmost.x == self.grid_width - 1:
                            return False

                        if rightmost.y >= self.grid_height:
                            break

                        if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                            return False
                        break

        else:
            for col in range(n):
                for row in range(n - 1, -1, -1):
                    if self.tile_matrix[row][col] != None:
                        bottommost = self.tile_matrix[row][col].get_position()

                        if bottommost.y > self.grid_height:
                            break

                        if bottommost.y == 0:
                            return False

                        if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                            return False
                        break
        return True