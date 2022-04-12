import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the game grid
import numpy as np  # fundamental Python module for scientific computing
import copy as cp
from tetromino import Tetromino
import pygame
import os


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create the tile matrix to store the tiles placed on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create an array that contains full row's tile values
        self.tile_num = np.zeros(grid_w)  # for full row score
        self.tile_num2 = np.zeros(100)  # for merged score
        # the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # game_over flag shows whether the game is over/completed or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(206, 193, 182)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(188, 172, 158)
        self.boundary_color = Color(132, 122, 113)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.002
        self.box_thickness = 8 * self.line_thickness

    # Method used for displaying the game grid
    def display(self, score, speed):
        # clear the background canvas to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the score
        self.draw_score(score)
        # draw the current (active) tetromino
        if self.current_tetromino != None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(speed)

    # Method for drawing the cells and the lines of the grid
    def draw_grid(self):
        # draw each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] != None:
                    self.tile_matrix[row][col].draw()
                    # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value


    def draw_boundaries(self):

        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(self.box_thickness)
        # coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value


    def draw_score(self, score):
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius
        stddraw.setPenRadius(self.box_thickness)
        # coordinates of the bottom left corner of the game grid
        pos_x, pos_y = self.grid_width - 0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, 3.5, self.grid_height)
        stddraw.setPenColor(Color(167, 160, 151))
        stddraw.filledRectangle(pos_x + 0.03, pos_y + 0.09, 3.4, self.grid_height - 0.2)
        # set the text
        text_color = Color(0, 0, 0)
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(30)
        stddraw.setPenColor(text_color)
        text_to_display = "SCORE"
        text_to_display2 = "NEXT"
        stddraw.text(12 + 1.2, 5, text_to_display2)
        stddraw.text(self.grid_width + 1.2, 15, text_to_display)
        stddraw.text(self.grid_width + 1.2, 14, str(score))
        # get the tetromino's type to create next tetromino to show in the next section
        tet_type = self.current_tetromino.get_type()
        if tet_type == 'I':
            width = 4
            height = 11
        elif tet_type == 'O':
            width = 2
            height = 12
        else:
            width = 3
            height = 11
        next_tetromino = Tetromino(tet_type, height, width)
        next_tetromino.draw_next_tet(self.current_tetromino)
        stddraw.setPenRadius()  # reset the pen radius to its default value


    def is_occupied(self, row, col):

        if not self.is_inside(row, col):
            return False

        return self.tile_matrix[row][col] != None


    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True


    def update_grid(self, tiles):

        n_rows, n_cols = len(tiles), len(tiles[0])
        for col in range(n_cols):
            for row in range(n_rows):

                if tiles[row][col] != None:
                    pos = tiles[row][col].get_position()
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles[row][col]

                    else:
                        self.game_over = True

        return self.game_over


    def is_full(self, row_n, tile_matrix):
        z = 0
        for i in range(self.grid_width):
            # check is there any empty column in that row
            if tile_matrix[row_n][i] == None:
                return False

            self.tile_num[z] = tile_matrix[row_n][i].get_number()
            z += 1
        # move down each tile by 1, starting from the above of the row
        for i in range(row_n + 1, self.grid_height):
            for j in range(self.grid_width):
                tile_matrix[i - 1][j] = tile_matrix[i][j]
                if tile_matrix[i][j] != None:
                    tile_matrix[i][j].move(0, -1)
        return True


    def update_score(self, tile_num):
        indv_score = 0
        for i in range(self.grid_width):
            indv_score += tile_num[i]
        return indv_score


    def merging(self, tile_matrix):
        merge = False
        for a in range(self.grid_width):
            for b in range(self.grid_height - 1):
                if tile_matrix[b][a] != None:
                    if tile_matrix[b + 1][a] != None and tile_matrix[b][a].get_number() == tile_matrix[b + 1][
                        a].get_number():
                        tile_matrix[b][a].set_number(2 * tile_matrix[b][a].get_number())
                        tile_matrix[b][a].set_color()
                        self.tile_num2[merge] = tile_matrix[b][a].get_number()
                        merge = True
                        # to drop the tiles above the merged tiles
                        for i in range(b + 2, self.grid_height):
                            tile_matrix[i - 1][a] = tile_matrix[i][a]
                            if tile_matrix[i][a] != None:
                                tile_matrix[i][a].move(0, -1)


    def connected_4_neighbor(self):
        # creating a matrix and fill first row with zeros
        binary_matrix = np.zeros((self.grid_height + 1, self.grid_width), None)
        binary_matrix[0, :] = 1
        # fill binary matrix with 1 if there is a tile in that position
        for col in range(self.grid_width):
            for row in range(self.grid_height):
                if self.tile_matrix[row][col] != None:
                    binary_matrix[row + 1][col] = 1
        # label the matrix to find out if connected with bottom row
        labels, num_labels = connected_component_labeling(binary_matrix)
        x = np.zeros(12)
        y = np.zeros(12)
        k = 0
        for j in range(self.grid_width):
            for i in range(2, self.grid_height):
                # if the tile is unconnected
                if (num_labels != 1 and labels[i][j] != 0 and labels[i][j] != 1):
                    if self.tile_matrix[i - 2][j] == None:
                        self.tile_matrix[i - 2][j] = self.tile_matrix[i - 1][j]
                        if self.tile_matrix[i - 1][j] != None:
                            self.tile_matrix[i - 1][j].move(0, -1)
                    # to keep the location of unconnected tile
                    x[k] = (i - 1)
                    y[k] = (j)
                    k += 1
        # in order not to double the value in 2048 check
        for a in range(k):
            self.tile_matrix[int(x[a])][int(y[a])] = None



def connected_component_labeling(binary_matrix):
    height, width = len(binary_matrix), len(binary_matrix[0])

    labels = np.zeros([height, width], dtype=int)

    min_equivalent_labels = []

    current_label = 1

    for y in range(height):
        for x in range(width):

            pixel = binary_matrix[y][x]

            if pixel == 0:
                continue


            neighbor_labels = get_neighbor_labels(labels, (x, y))

            if len(neighbor_labels) == 0:

                labels[y, x] = current_label
                current_label += 1

                min_equivalent_labels.append(labels[y, x])
            # if there is at least one non-background neighbor
            else:

                labels[y, x] = min(neighbor_labels)

                if len(neighbor_labels) > 1:
                    labels_to_merge = set()
                    # add min equivalent label for each neighbor to labels_to_merge set
                    for l in neighbor_labels:
                        labels_to_merge.add(min_equivalent_labels[l - 1])

                    update_min_equivalent_labels(min_equivalent_labels, labels_to_merge)

    rearrange_min_equivalent_labels(min_equivalent_labels)
    # for each pixel in the given binary image
    for y in range(height):
        for x in range(width):

            pixel = binary_matrix[y][x]

            if pixel == 0:
                continue

            labels[y, x] = min_equivalent_labels[labels[y, x] - 1]
    # return the labels matrix and the number of different labels
    return labels, len(set(min_equivalent_labels))




def get_neighbor_labels(label_values, pixel_indices):
    x, y = pixel_indices
    # using a set to store different neighbor labels without any duplicates
    neighbor_labels = set()

    if y != 0:
        u = label_values[y - 1, x]
        if u != 0:
            neighbor_labels.add(u)

    if x != 0:
        l = label_values[y, x - 1]
        if l != 0:
            neighbor_labels.add(l)
    # return the set of neighbor labels
    return neighbor_labels




def update_min_equivalent_labels(all_min_eq_labels, min_eq_labels_to_merge):
    # find the min value among conflicting neighbor labels
    min_value = min(min_eq_labels_to_merge)
    # for each minimum equivalent label
    for index in range(len(all_min_eq_labels)):
        # if its value is in min_eq_labels_to_merge
        if all_min_eq_labels[index] in min_eq_labels_to_merge:
            # update its value as the min_value
            all_min_eq_labels[index] = min_value




def rearrange_min_equivalent_labels(min_equivalent_labels):
    # find different values of min equivalent labels and sort them in increasing order
    different_labels = set(min_equivalent_labels)
    different_labels_sorted = sorted(different_labels)

    new_labels = np.zeros(max(min_equivalent_labels) + 1, dtype=int)
    count = 1
    for l in different_labels_sorted:
        # determine the new label
        new_labels[l] = count
        count += 1
    for ind in range(len(min_equivalent_labels)):
        old_label = min_equivalent_labels[ind]
        new_label = new_labels[old_label]
        min_equivalent_labels[ind] = new_label



