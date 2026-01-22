import tkinter as tk
import random
import json
import os

# Game variables
board_size = 400
cell_size = 40
home_positions = {
    'red': [(50, 50), (90, 50), (50, 90), (90, 90)],
    'blue': [(310, 50), (350, 50), (310, 90), (350, 90)],
    'green': [(50, 310), (90, 310), (50, 350), (90, 350)],
    'yellow': [(310, 310), (350, 310), (310, 350), (350, 350)]
}
path_positions = [
    # Red path
    (170, 10), (210, 10), (250, 10), (290, 10), (330, 10), (370, 10),
    (410, 10), (410, 50), (410, 90), (410, 130), (410, 170), (410, 210),
    (370, 210), (330, 210), (290, 210), (250, 210), (210, 210), (170, 210),
    (130, 210), (90, 210), (50, 210), (10, 210), (10, 250), (10, 290),
    (10, 330), (10, 370), (10, 410), (50, 410), (90, 410), (130, 410),
    (170, 410), (210, 410), (250, 410), (290, 410), (330, 410), (370, 410),
    (410, 410), (410, 370), (410, 330), (410, 290), (410, 250), (410, 210),
    (450, 210), (450, 250), (450, 290), (450, 330), (450, 370), (450, 410),
    (490, 410), (530, 410), (570, 410), (610, 410), (650, 410), (650, 370),
    (650, 330), (650, 290), (650, 250), (650, 210), (610, 210), (570, 210),
    (530, 210), (490, 210), (450, 210), (450, 170), (450, 130), (450, 90),
    (450, 50), (450, 10), (410, 10), (370, 10), (330, 10), (290, 10),
    (250, 10), (210, 10), (170, 10), (130, 10), (90, 10), (50, 10),
    (10, 10), (10, 50), (10, 90), (10, 130), (10, 170), (10, 210)
]

pieces = {
    'red': [{'pos': -1, 'id': None} for _ in range(4)],
    'blue': [{'pos': -1, 'id': None} for _ in range(4)]
}
current_player = 'red'
dice_value = 0
scores = {'red': 0, 'blue': 0}
high_score = 0

# Load high score
def load_high_score():
    global high_score
    if os.path.exists("Game/high_score_ludo.json"):
        with open("Game/high_score_ludo.json", "r") as f:
            data = json.load(f)
            high_score = data.get("high_score", 0)

# Save high score
def save_high_score():
    with open("Game/high_score_ludo.json", "w") as f:
        json.dump({"high_score": high_score}, f)

load_high_score()

def draw_board():
    canvas.delete("all")
    # Draw board background
    canvas.create_rectangle(0, 0, board_size, board_size, fill="#f0e68c", outline="black")
    # Draw home areas
    canvas.create_rectangle(40, 40, 120, 120, fill="#ffcccc", outline="red")
    canvas.create_rectangle(280, 40, 360, 120, fill="#ccccff", outline="blue")
    canvas.create_rectangle(40, 280, 120, 360, fill="#ccffcc", outline="green")
    canvas.create_rectangle(280, 280, 360, 360, fill="#ffffcc", outline="yellow")
    # Draw path
    for i, pos in enumerate(path_positions):
        x, y = pos
        canvas.create_rectangle(x, y, x+cell_size, y+cell_size, fill="#ffffff", outline="black")
    # Draw center
    canvas.create_rectangle(170, 170, 230, 230, fill="#ffd700", outline="black")
    # Draw pieces
    for color, piece_list in pieces.items():
        for piece in piece_list:
            if piece['pos'] == -1:
                pos = home_positions[color][piece_list.index(piece)]
            elif piece['pos'] >= len(path_positions):
                pos = (200, 200)  # Center
            else:
                pos = path_positions[piece['pos']]
            piece['id'] = canvas.create_oval(pos[0]+5, pos[1]+5, pos[0]+35, pos[1]+35, fill=color, outline="black")

def roll_dice():
    global dice_value
    dice_value = random.randint(1, 6)
    dice_label.config(text=f"Dice: {dice_value}")
    if dice_value == 6:
        dice_label.config(fg="green")
    else:
        dice_label.config(fg="black")

def move_piece(piece_index):
    global current_player, dice_value
    if dice_value == 0:
        result_label.config(text="Roll the dice first!", fg="red")
        return
    piece = pieces[current_player][piece_index]
    if piece['pos'] == -1:
        if dice_value == 6:
            piece['pos'] = 0
        else:
            result_label.config(text="Need 6 to start!", fg="orange")
            return
    else:
        piece['pos'] += dice_value
        if piece['pos'] >= len(path_positions):
            piece['pos'] = len(path_positions)  # Reached center
            scores[current_player] += 10
            score_label.config(text=f"Scores - Red: {scores['red']} | Blue: {scores['blue']}")
            if all(p['pos'] >= len(path_positions) for p in pieces[current_player]):
                result_label.config(text=f"{current_player.capitalize()} Wins! 🎉", fg="green")
                if scores[current_player] > high_score:
                    high_score = scores[current_player]
                    save_high_score()
                high_score_label.config(text=f"High Score: {high_score}")
                return
    # Check for captures
    for color, piece_list in pieces.items():
        if color != current_player:
            for p in piece_list:
                if p['pos'] == piece['pos'] and p['pos'] != -1:
                    p['pos'] = -1
                    result_label.config(text=f"{current_player.capitalize()} captured {color}!", fg="purple")
    draw_board()
    dice_value = 0
    dice_label.config(text="Dice: 0", fg="black")
    if dice_value != 6:
        current_player = 'blue' if current_player == 'red' else 'red'
        turn_label.config(text=f"Turn: {current_player.capitalize()}")
    result_label.config(text="", fg="black")

def reset_game():
    global pieces, current_player, dice_value, scores
    pieces = {
        'red': [{'pos': -1, 'id': None} for _ in range(4)],
        'blue': [{'pos': -1, 'id': None} for _ in range(4)]
    }
    current_player = 'red'
    dice_value = 0
    scores = {'red': 0, 'blue': 0}
    turn_label.config(text="Turn: Red")
    dice_label.config(text="Dice: 0", fg="black")
    score_label.config(text="Scores - Red: 0 | Blue: 0")
    result_label.config(text="", fg="black")
    draw_board()

# UI Setup
root = tk.Tk()
root.title("Ludo Game")
root.geometry("800x600")
root.configure(bg="#add8e6")

title = tk.Label(root, text="Ludo Game", font=("Arial", 24, "bold"), bg="#add8e6", fg="#8b0000")
title.pack(pady=10)

turn_label = tk.Label(root, text="Turn: Red", font=("Arial", 16), bg="#add8e6", fg="#000080")
turn_label.pack()

score_label = tk.Label(root, text="Scores - Red: 0 | Blue: 0", font=("Arial", 14), bg="#add8e6", fg="#006400")
score_label.pack()

high_score_label = tk.Label(root, text=f"High Score: {high_score}", font=("Arial", 12), bg="#add8e6", fg="#ff4500")
high_score_label.pack(pady=5)

canvas = tk.Canvas(root, width=board_size, height=board_size, bg="#f0e68c")
canvas.pack(pady=10)

dice_label = tk.Label(root, text="Dice: 0", font=("Arial", 18), bg="#add8e6", fg="black")
dice_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 14), bg="#add8e6", fg="black")
result_label.pack(pady=5)

button_frame = tk.Frame(root, bg="#add8e6")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Roll Dice", width=12, bg="#32cd32", fg="white", font=("Arial", 12, "bold"), command=roll_dice).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Move Piece 1", width=12, bg="#ff6347", fg="white", font=("Arial", 12, "bold"), command=lambda: move_piece(0)).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Move Piece 2", width=12, bg="#1e90ff", fg="white", font=("Arial", 12, "bold"), command=lambda: move_piece(1)).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Move Piece 3", width=12, bg="#ffa500", fg="white", font=("Arial", 12, "bold"), command=lambda: move_piece(2)).grid(row=0, column=3, padx=10)
tk.Button(button_frame, text="Move Piece 4", width=12, bg="#9370db", fg="white", font=("Arial", 12, "bold"), command=lambda: move_piece(3)).grid(row=0, column=4, padx=10)

reset_button = tk.Button(root, text="Reset Game", width=15, bg="#dc143c", fg="white", font=("Arial", 12, "bold"), command=reset_game)
reset_button.pack(pady=10)

draw_board()
root.mainloop()
