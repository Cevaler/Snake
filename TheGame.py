import random
import time
from tkinter import *


class Constants:
    FIELD_STEP = 10
    BOARD_WIDTH = 400
    BOARD_HEIGHT = 400
    REFRESH_SEC = 0.05
    VECTOR = ''
    PAUSE = False
    SET_VECTOR = False
    NEED_TO_CLOSE = False


class The_Game:

    def __init__(self):
        super().__init__()
        self.window = Tk()
        self.create_animation_window()
        self.canvas = Canvas(self.window)
        self.create_animation_canvas()
        self.snake = self.canvas.create_oval(0, 0, 0, 0, fill='green')
        self.borders = self.canvas.create_rectangle(10, 10, Constants.BOARD_WIDTH - 10, Constants.BOARD_HEIGHT - 10)
        self.apple = self.canvas.create_oval(0, 0, 0, 0, fill='red')
        self.segments = []
        self.vector = ''
        self.score = 0
        self.text_score = self.canvas.create_text(355, 20, text=f"score: {self.score}", justify=CENTER,
                                                  font="Verdana 10")
        self.text = self.canvas.create_text(200, 200, text='', justify=CENTER, font="Verdana 14")

    def create_animation_window(self):
        self.window.bind('<Up>', lambda event: vector(event))
        self.window.bind('<Down>', lambda event: vector(event))
        self.window.bind('<Left>', lambda event: vector(event))
        self.window.bind('<Right>', lambda event: vector(event))
        self.window.bind('r', lambda event: game_class())
        self.window.bind('p', lambda event: pause())
        self.window.bind('<Escape>', lambda event: need_to_close())
        self.window.title('Python Guides')
        self.window.geometry(f'{Constants.BOARD_WIDTH}x{Constants.BOARD_HEIGHT}')

    def create_animation_canvas(self):
        self.canvas.configure(bg="White")
        self.canvas.pack(fil="both", expand=True)

    def new_snake(self, x, y):
        self.canvas.coords(self.snake, x, y, x + Constants.FIELD_STEP, y + Constants.FIELD_STEP)

    def new_apple(self):
        random_position_x = random.randrange(10, Constants.BOARD_WIDTH - 10, Constants.FIELD_STEP)
        random_position_y = random.randrange(10, Constants.BOARD_HEIGHT - 10, Constants.FIELD_STEP)

        self.canvas.coords(self.apple, random_position_x, random_position_y, random_position_x + Constants.FIELD_STEP,
                           random_position_y + Constants.FIELD_STEP)

    def new_segment(self, position_snake):
        if len(self.segments) == 0:
            segment = self.canvas.create_oval(position_snake[0], position_snake[1],
                                              position_snake[2], position_snake[3], fill='green')
        else:
            lost_position_segment = self.canvas.coords(self.segments[-1])
            segment = self.canvas.create_oval(lost_position_segment[0], lost_position_segment[1],
                                              lost_position_segment[2], lost_position_segment[3], fill='green')
        self.segments.append(segment)

    def clear_segments_snake(self):
        for segment in reversed(self.segments):
            self.canvas.delete(segment)
        self.segments.clear()

    def move_snake(self):

        if Constants.VECTOR == 'Up':
            self.canvas.move(self.snake, 0, -Constants.FIELD_STEP)
        elif Constants.VECTOR == 'Down':
            self.canvas.move(self.snake, 0, Constants.FIELD_STEP)
        elif Constants.VECTOR == 'Left':
            self.canvas.move(self.snake, -Constants.FIELD_STEP, 0)
        elif Constants.VECTOR == 'Right':
            self.canvas.move(self.snake, Constants.FIELD_STEP, 0)
        Constants.SET_VECTOR = True

    def move_segment_snake(self, position_snake):

        quantity_segments = len(self.segments)

        if quantity_segments == 0:
            return

        for index_segments in reversed(range(quantity_segments)):
            segment = self.segments[index_segments]
            if index_segments == 0:
                new_position = position_snake
            else:
                parent_segment = self.segments[index_segments] - 1
                new_position = self.canvas.coords(parent_segment)

            self.canvas.coords(segment, new_position[0], new_position[1], new_position[2], new_position[3])

    def update_score(self):
        self.score += 1
        self.canvas.itemconfigure(self.text_score, text=f"score: {self.score}")

    def collided_with_segment(self):
        position_snake = self.canvas.coords(self.snake)
        for segment in self.segments:
            position_segment = self.canvas.coords(segment)
            if position_segment == position_snake:
                return True
        return False

    def collided_board(self):
        position_snake = self.canvas.coords(self.snake)
        return not (10 < position_snake[0] < Constants.BOARD_WIDTH - 10) \
            or not (10 < position_snake[1] < Constants.BOARD_HEIGHT - 10)

    def clear_lettering(self):
        self.canvas.itemconfigure(self.text, text="")
        self.window.update()

    def game_over(self):
        self.canvas.itemconfigure(self.text, text="GAME OVER")
        self.window.update()
        Constants.VECTOR = ''

    def new_game(self):
        self.clear_segments_snake()
        self.clear_lettering()
        self.score = 0
        self.new_snake(200, 200)
        self.new_apple()


def game_class():
    the_game.new_game()

    while True:

        if Constants.NEED_TO_CLOSE:
            break

        if Constants.PAUSE:
            the_game.window.update()
            time.sleep(Constants.REFRESH_SEC)
            continue

        past_position_snake = the_game.canvas.coords(the_game.snake)

        the_game.move_snake()
        the_game.move_segment_snake(past_position_snake)

        position_snake = the_game.canvas.coords(the_game.snake)
        position_apple = the_game.canvas.coords(the_game.apple)

        if position_snake == position_apple:
            the_game.new_apple()
            the_game.new_segment(past_position_snake)
            the_game.update_score()

        if the_game.collided_with_segment() or the_game.collided_board():
            the_game.game_over()

        the_game.window.update()
        time.sleep(Constants.REFRESH_SEC)


def pause():
    Constants.PAUSE = not Constants.PAUSE


def vector(event):
    revers = {'Up': 'Down',
              'Down': 'Up',
              'Left': 'Right',
              'Right': 'Left'}
    if not Constants.SET_VECTOR:
        return

    if Constants.VECTOR == revers[event.keysym]:
        return
    Constants.VECTOR = event.keysym
    Constants.SET_VECTOR = False


def need_to_close():
    Constants.NEED_TO_CLOSE = True


the_game = The_Game()


def main():
    game_class()


if __name__ == '__main__':
    main()
