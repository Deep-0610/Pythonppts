import tkinter as tk
import random
import json
import os

# Game variables
width = 400
height = 400
cell_size = 20
snake = [(200, 200)]
direction = 'right'
food = None
score = 0
high_score = 0
game_running = False
speed = 200

# Load high score
def load_high_score():
    global high_score
    if os.path.exists("Game/high_score_snake.json"):
        with open("Game/high_score_snake.json", "r") as f:
            data = json.load(f)
            high_score = data.get("high_score", 0)

# Save high score
def save_high_score():
    with open("Game/high_score_snake.json", "w") as f:
        json.dump({"high_score": high_score}, f)

load_high_score()

def place_food():
    global food
    while True:
        x = random.randint(0, (width // cell_size) - 1) * cell_size
        y = random.randint(0, (height // cell_size) - 1) * cell_size
        if (x, y) not in snake:
            food = (x, y)
            break

def draw():
    canvas.delete("all")
    # Draw snake
    for segment in snake:
        canvas.create_rectangle(segment[0], segment[1], segment[0] + cell_size, segment[1] + cell_size, fill="#32cd32", outline="black")
    # Draw food
    if food:
        canvas.create_oval(food[0], food[1], food[0] + cell_size, food[1] + cell_size, fill="#ff4500", outline="black")
    # Draw score
    canvas.create_text(50, 10, text=f"Score: {score}", font=("Arial", 14), fill="black")

def move():
    global snake, food, score, game_running, speed
    if not game_running:
        return
    head = list(snake[0])
    if direction == 'up':
        head[1] -= cell_size
    elif direction == 'down':
        head[1] += cell_size
    elif direction == 'left':
        head[0] -= cell_size
    elif direction == 'right':
        head[0] += cell_size
    head = tuple(head)
    # Check wall collision
    if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
        game_over()
        return
    # Check self collision
    if head in snake:
        game_over()
        return
    snake.insert(0, head)
    # Check food
    if head == food:
        score += 10
        place_food()
        speed = max(50, speed - 5)  # Increase speed
        score_label.config(text=f"Score: {score}")
    else:
        snake.pop()
    draw()
    root.after(speed, move)

def change_direction(new_direction):
    global direction
    opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    if new_direction != opposites.get(direction):
        direction = new_direction

def start_game():
    global snake, direction, food, score, game_running, speed
    snake = [(200, 200)]
    direction = 'right'
    score = 0
    speed = 200
    game_running = True
    place_food()
    score_label.config(text="Score: 0")
    result_label.config(text="", fg="black")
    draw()
    move()

def game_over():
    global game_running, high_score
    game_running = False
    result_label.config(text="Game Over! Press Start to play again.", fg="red")
    if score > high_score:
        high_score = score
        save_high_score()
    high_score_label.config(text=f"High Score: {high_score}")

def reset_game():
    global game_running
    game_running = False
    result_label.config(text="", fg="black")

# Key bindings
def on_key_press(event):
    if event.keysym == 'Up':
        change_direction('up')
    elif event.keysym == 'Down':
        change_direction('down')
    elif event.keysym == 'Left':
        change_direction('left')
    elif event.keysym == 'Right':
        change_direction('right')

# UI Setup
root = tk.Tk()
root.title("Snake Game")
root.geometry("500x550")
root.configure(bg="#f0f8ff")

title = tk.Label(root, text="Snake Game", font=("Arial", 24, "bold"), bg="#f0f8ff", fg="#ff4500")
title.pack(pady=10)

score_label = tk.Label(root, text="Score: 0", font=("Arial", 16), bg="#f0f8ff", fg="#000080")
score_label.pack()

high_score_label = tk.Label(root, text=f"High Score: {high_score}", font=("Arial", 14), bg="#f0f8ff", fg="#006400")
high_score_label.pack()

canvas = tk.Canvas(root, width=width, height=height, bg="#ffffff", highlightthickness=2, highlightbackground="black")
canvas.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f8ff", fg="black")
result_label.pack(pady=5)

button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Start Game", width=12, bg="#32cd32", fg="white", font=("Arial", 12, "bold"), command=start_game).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Reset", width=12, bg="#ff6347", fg="white", font=("Arial", 12, "bold"), command=reset_game).grid(row=0, column=1, padx=10)

instructions = tk.Label(root, text="Use arrow keys to control the snake.\nEat the red food to grow and score points!", font=("Arial", 10), bg="#f0f8ff", fg="#8b0000")
instructions.pack(pady=10)

root.bind('<Key>', on_key_press)
root.focus_set()

root.mainloop()
