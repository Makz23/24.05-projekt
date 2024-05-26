import tkinter as tk
from tkinter import messagebox
import subprocess

def play_game(game):
    if game == "Snake Game":
        subprocess.run(['python', 'game1.py'])
    elif game == "Tic-Tac-Toe":
        subprocess.run(['python', 'game2.py'])
    elif game == "Minesweeper":
        subprocess.run(['python', 'game3.py'])
    elif game == "Connect Four":
        subprocess.run(['python', 'game4.py'])
    elif game == "Hangman":
        subprocess.run(['python', 'game5.py'])
    elif game == "Dodge":
        subprocess.run(['python', 'Dodge.py'])
    elif game == "Pong":
        subprocess.run(['python', 'Pong.py'])
    elif game == "Tetris":
        subprocess.run(['python', 'Tetris.py'])
    elif game == "Spaceship":
        subprocess.run(['python', 'Spaceship.py'])
    else:
        messagebox.showerror("Error", "Invalid game selection.")

def show_menu():
    root = tk.Tk()
    root.title("Game Menu")

    label = tk.Label(root, text="Select a game to play:")
    label.pack()

    games = ["Snake Game", "Tic-Tac-Toe", "Minesweeper", "Connect Four", "Hangman", "Dodge", "Pong", "Tetris", "Spaceship"]

    for game in games:
        button = tk.Button(root, text=game, command=lambda g=game: play_game(g))
        button.pack()

    root.mainloop()

if __name__ == "__main__":
    show_menu()
