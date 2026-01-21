import tkinter as tk
import random

choices = ["Stone", "Paper", "Scissors"]
user_score = 0
computer_score = 0

def play(user_choice):
    global user_score, computer_score

    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = "It's a Tie 🤝"
    elif (
        (user_choice == "Stone" and computer_choice == "Scissors") or
        (user_choice == "Paper" and computer_choice == "Stone") or
        (user_choice == "Scissors" and computer_choice == "Paper")
    ):
        result = "You Win 😎"
        user_score += 1
    else:
        result = "Computer Wins 💀"
        computer_score += 1

    result_label.config(
        text=f"You chose {user_choice}\nComputer chose {computer_choice}\n\n{result}"
    )
    score_label.config(
        text=f"Score → You: {user_score} | Computer: {computer_score}"
    )

root = tk.Tk()
root.title("Stone Paper Scissors")
root.geometry("400x400")

title = tk.Label(root, text="Stone Paper Scissors", font=("Arial", 18, "bold"))
title.pack(pady=20)

result_label = tk.Label(root, text="Make your move 👇", font=("Arial", 12))
result_label.pack(pady=20)

score_label = tk.Label(root, text="Score → You: 0 | Computer: 0", font=("Arial", 12))
score_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Stone", width=10, command=lambda: play("Stone")).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Paper", width=10, command=lambda: play("Paper")).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Scissors", width=10, command=lambda: play("Scissors")).grid(row=0, column=2, padx=10)

root.mainloop()
