import stddraw  # the stddraw module is used as a basic graphics library
import random  # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid  # class for modeling the game grid
from tetromino import Tetromino  # class for modeling the tetrominoes
from picture import Picture  # used representing images to display
import os  # used for file and directory operations
import numpy as np
from color import Color  # used for coloring the game menu





def start():
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas
    canvas_h, canvas_w = 40 * grid_h, 40 * grid_w + 100
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.5, grid_w + 3)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino(grid_h, grid_w)
    grid.current_tetromino = current_tetromino


    # display a simple menu before opening the game
    display_game_menu(grid_h, grid_w)

    # initial score
    score = 0
    speed = 243 #initial speed

    # main game loop (keyboard interaction for moving the tetromino)
    while True:
        # check user interactions via the keyboard
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            # if the left arrow key has been pressed
            if key_typed == "left":
                # move the tetromino left by one
                current_tetromino.move(key_typed, grid)
            # if the right arrow key has been pressed
            elif key_typed == "right":
                # move the tetromino right by one
                current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
                # move the tetromino down by one
                # (causes the tetromino to fall down faster)
                current_tetromino.move(key_typed, grid)
            elif key_typed == "up":
                # rotate the tetromino
                current_tetromino.rotateTetromino()
            elif key_typed == "space":
                # drop the tetromino
                for i in range(grid_h):
                 current_tetromino.move("down",grid)

            # clear the queue that stores all the keys pressed/typed
            stddraw.clearKeysTyped()

        # move (drop) the tetromino down by 1 at each iteration
        success = current_tetromino.move("down", grid)
        grid.connected_4_neighbor()


        if not success:

            tiles = current_tetromino.tile_matrix

            game_over = grid.update_grid(tiles)

            rows_score = 0
            tiles_score = 0


            for i in range(grid_h):
                grid.merging(grid.tile_matrix)

                ind_score = grid.update_score(grid.tile_num2)
                if grid.is_full(i, grid.tile_matrix):

                    rows_score = grid.update_score(grid.tile_num)
            grid.tile_num2 = np.zeros(100)
            score_val = tiles_score + rows_score
            score += int(score_val)



            if game_over:
                break



            current_tetromino = create_tetromino(grid_h, grid_w)
            grid.current_tetromino = current_tetromino


        grid.display(score,speed)


    finish_game(grid_h, grid_w)
    print("Game over")



def create_tetromino(grid_height, grid_width):

    tetromino_types = ['I', 'O', 'Z', 'L', 'J', 'S', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]

    tetromino = Tetromino(random_type, grid_height, grid_width)
    return tetromino


def finish_game(grid_height, grid_width):

    background_color = Color(28, 27, 36)

    stddraw.clear(background_color)

    current_dir = os.path.dirname(os.path.realpath(__file__))

    img_file = current_dir + "/game_over.png"

    img_center_x, img_center_y = (grid_width + 2) / 2, grid_height - 10

    image_to_display = Picture(img_file)

    stddraw.picture(image_to_display, img_center_x, img_center_y)
    stddraw.show(1000)

def display_game_menu(grid_height, grid_width):
    background_color = Color(53, 147, 47)
    button_color = Color(23, 23, 23)
    text_color = Color(255, 255, 255)
    stddraw.clear(background_color)
    current_dir = os.path.dirname(os.path.realpath(__file__))

    img_file = current_dir + "/menu_image.png"

    img_center_x, img_center_y = (grid_width + 2) / 2, grid_height - 7

    image_to_display = Picture(img_file)

    stddraw.picture(image_to_display, img_center_x, img_center_y)

    button_w, button_h = grid_width - 1.5, 2

    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4

    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)

    while True:

        stddraw.show(50)

        if stddraw.mousePressed():

            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break





if __name__ == '__main__':
    start()