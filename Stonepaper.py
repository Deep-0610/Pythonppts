import tkinter as tk
import random
import json
import os

# Choices and game variables
choices = ["Stone", "Paper", "Scissors"]
user_score = 0
computer_score = 0
round_count = 0
max_rounds = 5
user_streak = 0
computer_streak = 0
user_history = {"Stone": 0, "Paper": 0, "Scissors": 0}
high_score = 0

# Load high score from file
def load_high_score():
    global high_score
    if os.path.exists("high_score.json"):
        with open("high_score.json", "r") as f:
            data = json.load(f)
            high_score = data.get("high_score", 0)

# Save high score to file
def save_high_score():
    with open("high_score.json", "w") as f:
        json.dump({"high_score": high_score}, f)

load_high_score()

# Weighted random choice based on user history
def weighted_choice():
    total = sum(user_history.values()) + 3  # Add small bias to avoid division by zero
    weights = []
    for choice in choices:
        # Slightly favor countering the most chosen user move
        if choice == "Stone":
            counter = "Paper"
        elif choice == "Paper":
            counter = "Scissors"
        else:
            counter = "Stone"
        weight = (user_history[choice] + 1) / total * 0.7 + (user_history.get(counter, 0) + 1) / total * 0.3
        weights.append(weight)
    return random.choices(choices, weights=weights)[0]

def play(user_choice):
    global user_score, computer_score, round_count, user_streak, computer_streak

    user_history[user_choice] += 1
    computer_choice = weighted_choice()

    # Power-up: 10% chance for double points or auto-win
    power_up = random.random() < 0.1
    if power_up:
        if random.random() < 0.5:
            result = "Power-Up! You Win Double Points! 🚀"
            user_score += 2
            user_streak += 1
            computer_streak = 0
        else:
            result = "Power-Up! Auto-Win! 🎉"
            user_score += 1
            user_streak += 1
            computer_streak = 0
    elif user_choice == computer_choice:
        result = "It's a Tie 🤝"
        user_streak = 0
        computer_streak = 0
    elif (
        (user_choice == "Stone" and computer_choice == "Scissors") or
        (user_choice == "Paper" and computer_choice == "Stone") or
        (user_choice == "Scissors" and computer_choice == "Paper")
    ):
        result = "You Win 😎"
        user_score += 1
        user_streak += 1
        computer_streak = 0
    else:
        result = "Computer Wins 💀"
        computer_score += 1
        computer_streak += 1
        user_streak = 0

    round_count += 1

    # Update result label with color
    if "Win" in result:
        result_label.config(text=f"You chose {user_choice}\nComputer chose {computer_choice}\n\n{result}", fg="green")
    elif "Tie" in result:
        result_label.config(text=f"You chose {user_choice}\nComputer chose {computer_choice}\n\n{result}", fg="orange")
    else:
        result_label.config(text=f"You chose {user_choice}\nComputer chose {computer_choice}\n\n{result}", fg="red")

    score_label.config(text=f"Score → You: {user_score} | Computer: {computer_score}\nRound: {round_count}/{max_rounds}\nStreak: You {user_streak} | Comp {computer_streak}")

    # Check for game end
    if round_count >= max_rounds:
        if user_score > computer_score:
            result_label.config(text="Game Over! You Won the Best of 5! 🎉", fg="green")
        elif computer_score > user_score:
            result_label.config(text="Game Over! Computer Won the Best of 5! 💀", fg="red")
        else:
            result_label.config(text="Game Over! It's a Tie! 🤝", fg="orange")
        # Update high score
        if user_score > high_score:
            high_score = user_score
            save_high_score()
        high_score_label.config(text=f"High Score: {high_score}")

def reset_game():
    global user_score, computer_score, round_count, user_streak, computer_streak, user_history
    user_score = 0
    computer_score = 0
    round_count = 0
    user_streak = 0
    computer_streak = 0
    user_history = {"Stone": 0, "Paper": 0, "Scissors": 0}
    result_label.config(text="Make your move 👇", fg="black")
    score_label.config(text=f"Score → You: 0 | Computer: 0\nRound: 0/{max_rounds}\nStreak: You 0 | Comp 0")

# UI Setup
root = tk.Tk()
root.title("Enhanced Stone Paper Scissors")
root.geometry("600x600")
root.configure(bg="#f0f8ff")  # Light blue background

title = tk.Label(root, text="Stone Paper Scissors", font=("Arial", 24, "bold"), bg="#f0f8ff", fg="#ff4500")
title.pack(pady=20)

result_label = tk.Label(root, text="Make your move 👇", font=("Arial", 14), bg="#f0f8ff", fg="black")
result_label.pack(pady=20)

score_label = tk.Label(root, text="Score → You: 0 | Computer: 0\nRound: 0/5\nStreak: You 0 | Comp 0", font=("Arial", 12), bg="#f0f8ff", fg="#000080")
score_label.pack(pady=10)

high_score_label = tk.Label(root, text=f"High Score: {high_score}", font=("Arial", 12), bg="#f0f8ff", fg="#008000")
high_score_label.pack(pady=10)

button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=20)

# Colorful buttons
tk.Button(button_frame, text="Stone", width=12, bg="#ff6347", fg="white", font=("Arial", 12, "bold"), command=lambda: play("Stone")).grid(row=0, column=0, padx=15, pady=10)
tk.Button(button_frame, text="Paper", width=12, bg="#32cd32", fg="white", font=("Arial", 12, "bold"), command=lambda: play("Paper")).grid(row=0, column=1, padx=15, pady=10)
tk.Button(button_frame, text="Scissors", width=12, bg="#1e90ff", fg="white", font=("Arial", 12, "bold"), command=lambda: play("Scissors")).grid(row=0, column=2, padx=15, pady=10)

reset_button = tk.Button(root, text="Reset Game", width=15, bg="#ffa500", fg="white", font=("Arial", 12, "bold"), command=reset_game)
reset_button.pack(pady=20)

root.mainloop()
