# A simplee Snake game with 3 difficulty modes, high score calculator and a few other minor stuff
from tkinter import *
import random

# Constants boissss
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "Blue"
FOOD_COLOR = "Yellow"
BACKGROUND_COLOR = "#000000"

# Global variables (I know they arnt advised but it was the easy way out)
direction = 'down'
after_id = None
snake = None
food = None
score = 0
high_score = 0
SPEED = 100

# The snakeee
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Apple that the snake eats. Its yellow tho
class Food:
    def __init__(self):
        self.position = None
        self.food_item = None
        self.spawn()

    def spawn(self):
        if self.food_item:
            canvas.delete(self.food_item)

        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1)
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1)
        self.position = [x, y]
        self.food_item = canvas.create_oval(
            x * SPACE_SIZE, y * SPACE_SIZE,
            (x + 1) * SPACE_SIZE, (y + 1) * SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )

#all the other functionss required
def next_turn():
    global direction, snake, food, after_id

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.position[0] * SPACE_SIZE and y == food.position[1] * SPACE_SIZE:
        global score, high_score
        score += 1
        if score > high_score:
            high_score = score
        label.config(text="Score: {}".format(score))
        high_score_label.config(text="High Score: {}".format(high_score))
        canvas.delete(food.food_item)
        food.spawn()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        after_id = window.after(SPEED, next_turn)

def change_direction(event):
    global direction

    if event.keysym == 'a' and direction != 'right':
        direction = 'left'
    elif event.keysym == 'd' and direction != 'left':
        direction = 'right'
    elif event.keysym == 'w' and direction != 'down':
        direction = 'up'
    elif event.keysym == 's' and direction != 'up':
        direction = 'down'

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    global after_id
    canvas.delete("all")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=('consolas', 70),
                       text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 100, font=('consolas', 30),
                       text="Press 'R' to Restart", fill="white", tag="restart")
    window.bind('<KeyPress-r>', restart_game)

def restart_game(event):
    global score, high_score, direction, after_id, snake, food
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    canvas.delete("all")
    snake = Snake()
    food = Food()
    after_id = window.after(SPEED, next_turn)
    high_score_label.config(text="High Score: {}".format(high_score))

def set_speed(speed):
    global SPEED
    SPEED = speed
    start_game()

def set_speed(speed):
    global SPEED
    SPEED = speed
    start_game()

def start_game():
    global after_id, direction, snake, food, score, high_score

    direction = 'down'
    score = 0
    label.config(text="Score: {}".format(score))
    high_score_label.config(text="High Score: {}".format(high_score))

    canvas.delete("all")
    snake = Snake()
    food = Food()
    after_id = window.after(SPEED, next_turn)

# Main gameeeee (labels, buttons and stuff)
window = Tk()
window.title("Snake Game")
window.attributes("-fullscreen", True)

title_label = Label(window, text="Best Game Ever", font=('arial', 40))
title_label.pack(side='top', padx=20, pady=5)

Instruction_label = Label(window, text="To start playing, click on any level. Use WASD to move", font=('arial', 15), fg="white", bg=BACKGROUND_COLOR)
Instruction_label.pack(side="top", padx=10, pady=20)

score_frame = Frame(window)
score_frame.pack(side='top', fill='x')


label = Label(score_frame, text="Score:", font=('arial', 20), fg="white", bg=BACKGROUND_COLOR)
label.pack(side='top')

high_score_label = Label(score_frame, text="High Score:", font=('arial', 20), fg="white", bg=BACKGROUND_COLOR)
high_score_label.pack(side='top')

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.place(x=(window.winfo_width() - GAME_WIDTH) / 2, y=(window.winfo_height() - GAME_HEIGHT) / 2)
canvas.pack(anchor='center')


level_label = Label(window, text="Select Level:", font=('arial', 20))
level_label.pack(side="top")
level_label.place(x=80, y=150)

easy_button = Button(window, text="Easy", font=('arial', 15), command=lambda: set_speed(150))
easy_button.pack(side="top")
easy_button.place(x=100, y=200)

medium_button = Button(window, text="Medium", font=('arial', 15), command=lambda: set_speed(100))
medium_button.pack(side="top")
medium_button.place(x=100, y=230)

hard_button = Button(window, text="Hard", font=('arial', 15), command=lambda: set_speed(50))
hard_button.pack(side="top")
hard_button.place(x=100, y=260)

exit_button = Button(window, text="Exit", font=('arial', 20), command=window.destroy)
exit_button.pack(anchor='se')

window.bind('<KeyPress-a>', change_direction)
window.bind('<KeyPress-d>', change_direction)
window.bind('<KeyPress-w>', change_direction)
window.bind('<KeyPress-s>', change_direction)

window.mainloop()
