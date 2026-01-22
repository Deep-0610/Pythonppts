import tkinter as tk
import random
import json
import os

# Game variables
secret_number = 0
attempts = 0
max_attempts = 10
level = 1
score = 0
high_score = 0
hints_used = 0

# Load high score
def load_high_score():
    global high_score
    if os.path.exists("Game/high_score_guess.json"):
        with open("Game/high_score_guess.json", "r") as f:
            data = json.load(f)
            high_score = data.get("high_score", 0)

# Save high score
def save_high_score():
    with open("Game/high_score_guess.json", "w") as f:
        json.dump({"high_score": high_score}, f)

load_high_score()

def start_new_game():
    global secret_number, attempts, hints_used
    if level == 1:
        secret_number = random.randint(1, 50)
    elif level == 2:
        secret_number = random.randint(1, 100)
    else:
        secret_number = random.randint(1, 200)
    attempts = 0
    hints_used = 0
    result_label.config(text="Guess a number between 1 and " + str(50 * level) + "!", fg="black")
    attempts_label.config(text=f"Attempts: 0/{max_attempts}")
    hint_label.config(text="")
    guess_entry.delete(0, tk.END)

def guess():
    global attempts, score, high_score
    try:
        user_guess = int(guess_entry.get())
        attempts += 1
        attempts_label.config(text=f"Attempts: {attempts}/{max_attempts}")

        if user_guess == secret_number:
            points = max(100 - attempts * 10 - hints_used * 20, 10)
            score += points
            result_label.config(text=f"Correct! You won {points} points! 🎉", fg="green")
            if score > high_score:
                high_score = score
                save_high_score()
            high_score_label.config(text=f"High Score: {high_score}")
            level_up()
        elif user_guess < secret_number:
            result_label.config(text="Too low! Try higher.", fg="blue")
        else:
            result_label.config(text="Too high! Try lower.", fg="red")

        if attempts >= max_attempts and user_guess != secret_number:
            result_label.config(text=f"Game Over! The number was {secret_number}. 😞", fg="red")
            score = max(score - 50, 0)
            level_down()

    except ValueError:
        result_label.config(text="Please enter a valid number!", fg="orange")

def hint():
    global hints_used
    hints_used += 1
    if secret_number % 2 == 0:
        hint_text = "The number is even."
    else:
        hint_text = "The number is odd."
    hint_label.config(text=hint_text, fg="purple")

def level_up():
    global level, max_attempts
    level += 1
    max_attempts = 10 + level * 2
    level_label.config(text=f"Level: {level}")
    start_new_game()

def level_down():
    global level, max_attempts
    if level > 1:
        level -= 1
    max_attempts = 10 + level * 2
    level_label.config(text=f"Level: {level}")
    start_new_game()

def reset_game():
    global level, score
    level = 1
    score = 0
    level_label.config(text="Level: 1")
    score_label.config(text="Score: 0")
    start_new_game()

# UI Setup
root = tk.Tk()
root.title("Guess the Number Game")
root.geometry("500x500")
root.configure(bg="#ffe4e1")  # Misty rose background

title = tk.Label(root, text="Guess the Number!", font=("Arial", 24, "bold"), bg="#ffe4e1", fg="#dc143c")
title.pack(pady=20)

level_label = tk.Label(root, text="Level: 1", font=("Arial", 14), bg="#ffe4e1", fg="#8b0000")
level_label.pack()

score_label = tk.Label(root, text="Score: 0", font=("Arial", 14), bg="#ffe4e1", fg="#006400")
score_label.pack()

high_score_label = tk.Label(root, text=f"High Score: {high_score}", font=("Arial", 12), bg="#ffe4e1", fg="#ff4500")
high_score_label.pack(pady=10)

result_label = tk.Label(root, text="Press Start to begin!", font=("Arial", 14), bg="#ffe4e1", fg="black")
result_label.pack(pady=20)

attempts_label = tk.Label(root, text=f"Attempts: 0/{max_attempts}", font=("Arial", 12), bg="#ffe4e1", fg="#000080")
attempts_label.pack()

hint_label = tk.Label(root, text="", font=("Arial", 12), bg="#ffe4e1", fg="purple")
hint_label.pack(pady=10)

guess_entry = tk.Entry(root, font=("Arial", 14), width=10)
guess_entry.pack(pady=10)

button_frame = tk.Frame(root, bg="#ffe4e1")
button_frame.pack(pady=20)

tk.Button(button_frame, text="Guess", width=10, bg="#32cd32", fg="white", font=("Arial", 12, "bold"), command=guess).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Hint", width=10, bg="#ffa500", fg="white", font=("Arial", 12, "bold"), command=hint).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Start New", width=10, bg="#1e90ff", fg="white", font=("Arial", 12, "bold"), command=start_new_game).grid(row=0, column=2, padx=10)

reset_button = tk.Button(root, text="Reset Game", width=15, bg="#ff6347", fg="white", font=("Arial", 12, "bold"), command=reset_game)
reset_button.pack(pady=20)

start_new_game()
root.mainloop()
