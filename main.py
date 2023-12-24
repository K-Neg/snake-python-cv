import cv2
import numpy as np
import select
import time
import sys
import os
import random

import sprites
from keyboard_handler import KeyboardHandler


BOARD_SIZE = (8, 8)
SCREEN_SIZE = (512, 512)
INITIAL_POSITION = (1, 1)
STARTER_MOVE = "right"


class Draw:
    def __init__(self) -> None:
        pass

    def draw(img):
        cv2.imshow("Snake", img)
        cv2.waitKey(1)

    def insert_cell(img, graphic_element, x: int, y: int, index=1):
        h, w = graphic_element.shape[:2]
        img[x : (x + w), y : (y + h)] = graphic_element

    @staticmethod
    def insert_metadata(img, data):
        cv2.putText(
            img,
            str(data),
            (5, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )

    def generate_image(matrix: np.ndarray):
        img = np.zeros((BOARD_SIZE[0], BOARD_SIZE[1], 3), dtype=np.uint8)

        img[matrix == 0] = (180, 150, 30)  # Empty
        img[matrix == 1] = (50, 50, 50)  # Box
        img[matrix == 2] = (50, 50, 200)  # Snake head
        img[matrix == 3] = (250, 1, 1)  # Food
        img[matrix == 4] = (30, 30, 150)  # Snake body

        img = cv2.resize(
            img, (SCREEN_SIZE[0], SCREEN_SIZE[1]), interpolation=cv2.INTER_NEAREST
        )
        return img

    def __call__(self, matrix, metadata):
        img = Draw.generate_image(matrix)
        Draw.insert_metadata(img, metadata)
        Draw.draw(img)


class Snake:
    def __init__(self, grid_size) -> None:
        self.grid_size = grid_size

        self.keyboard = KeyboardHandler()
        self.drawer = Draw()

        self.move_counter = 0
        self.points = 0

        self.new_position = INITIAL_POSITION
        self.current_pos = INITIAL_POSITION
        self.snake_tail = [INITIAL_POSITION]

        self.board = self.generate_board(grid_size)
        self.board[INITIAL_POSITION[0], INITIAL_POSITION[1]] = 2

        self.food_coordinates = (0, 0)
        self.generate_food()
        self.board[self.food_coordinates[0], self.food_coordinates[1]] = 3

    @staticmethod
    def generate_board(grid_size):
        board = np.zeros(grid_size, dtype=np.int16)
        board[0] = 1
        board[-1] = 1
        for line in board:
            line[-1] = 1
            line[0] = 1

        return board

    def update_board(self, key):
        self.calculate_move(key)


        target_value = self.board[self.new_position[0], self.new_position[1]]

        if target_value == 1:
            raise Exception("game over")
        elif target_value == 3:
            self.points += 1
            new_tail = [self.new_position]
            new_tail.extend(self.snake_tail)
            self.generate_food()
        else:
            new_tail = [self.new_position]
            new_tail.extend(self.snake_tail[:-1])

        self.snake_tail = new_tail
        self.board = self.generate_board(self.grid_size)
        self.board[self.food_coordinates[0], self.food_coordinates[1]] = 3

        if len(self.snake_tail) > 1:
            for tail_piece in self.snake_tail[0:]:
                self.board[tail_piece[0], tail_piece[1]] = 4
        else:
            pass

        self.board[self.snake_tail[0][0], self.snake_tail[0][1]] = 2

        self.current_pos = self.new_position

        self.drawer(self.board, (self.points, self.move_counter))

    def calculate_move(self, key):
        y, x = self.current_pos

        if key == "esc":
            sys.exit()
        elif key == "up":
            new_position = y - 1, x
        elif key == "right":
            new_position = y, x + 1
        elif key == "down":
            new_position = y + 1, x
        elif key == "left":
            new_position = y, x - 1
        else:
            return

        self.new_position = new_position

        self.move_counter += 1

    def generate_food(self):
        while True:
            coordinates = (
                random.randint(1, self.grid_size[0] - 2),
                random.randint(1, self.grid_size[1] - 2),
            )

            if coordinates not in self.snake_tail:
                break

        self.food_coordinates = coordinates
        print(coordinates)

    def run(self):
        game_delay = 1
        last_update_time = 0
        player_move = STARTER_MOVE
        skip = False

        while True:
            pass

            if key := self.keyboard.get_last_key():
                player_move = key
                skip = True
                key = None

            time.sleep(0.01)

            current_time = time.perf_counter()
            if (current_time > last_update_time + game_delay) or skip:
                self.update_board(player_move)
                last_update_time = current_time
                self.move_counter += 1
                skip = False


def main():
    snake = Snake(BOARD_SIZE)
    snake.run()


if __name__ == "__main__":
    main()
