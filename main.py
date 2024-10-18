import tkinter as tk
from tkinter import messagebox
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
EMPTY = 0
YELLOW = 1
RED = 2

# Create the game window
window = tk.Tk()
window.withdraw()  # Hide the game window until difficulty is selected
window.title("Connect 4")

# Game board as a 2D array (6 rows, 7 columns)
board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

# Track whose turn it is (1 for yellow, 2 for red)
current_player = random.choice([YELLOW, RED])  # Flip a coin to decide who starts

# Difficulty level: "beginner" or "medium"
difficulty = ""

# Button references and canvas references
buttons = []
canvases = []


def check_for_winner():
    """Checks the board for a winner (4 in a row, vertically, horizontally, or diagonally)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == current_player and all(board[row][col + i] == current_player for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if board[row][col] == current_player and all(board[row + i][col] == current_player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == current_player and all(board[row + i][col + i] == current_player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == current_player and all(board[row - i][col + i] == current_player for i in range(4)):
                return True

    return False


def drop_piece(column):
    """Handles the logic for dropping a piece into the selected column."""
    global current_player

    # Find the lowest empty spot in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            board[row][column] = current_player

            # Update the canvas to show the circular chip
            canvases[row][column].create_oval(5, 5, 75, 75, fill='yellow' if current_player == YELLOW else 'red')

            # Check if this move resulted in a win
            if check_for_winner():
                winner = "Yellow" if current_player == YELLOW else "Red"
                messagebox.showinfo("Game Over", f"{winner} wins!")
                reset_game()
            else:
                # Switch to the other player
                current_player = RED if current_player == YELLOW else YELLOW
                if current_player == RED:
                    window.after(500, ai_move)  # Let AI take its turn after a short delay
            return

    # If the column is full
    messagebox.showwarning("Column Full", "This column is full! Choose another one.")


def ai_move():
    """Simple AI move based on the chosen difficulty."""
    if difficulty == "beginner":
        available_columns = [col for col in range(COLUMNS) if board[0][col] == EMPTY]
        if available_columns:
            drop_piece(random.choice(available_columns))
    elif difficulty == "medium":
        # Medium difficulty AI: First try to block player, if no block, choose random
        if not block_player():
            available_columns = [col for col in range(COLUMNS) if board[0][col] == EMPTY]
            if available_columns:
                drop_piece(random.choice(available_columns))


def block_player():
    """Checks if the AI can block the player's winning move."""
    # Scan columns for potential player wins
    for col in range(COLUMNS):
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == EMPTY:
                board[row][col] = YELLOW  # Temporarily place a yellow piece to simulate the player's move
                if check_for_winner():
                    board[row][col] = RED  # Block the player's move by placing the AI's piece there
                    canvases[row][col].create_oval(5, 5, 75, 75, fill='red')
                    return True
                board[row][col] = EMPTY  # Undo the temporary move
                break
    return False


def create_board():
    """Creates the GUI board with clickable buttons and canvases for circular chips."""
    for row in range(ROWS):
        button_row = []
        canvas_row = []
        for col in range(COLUMNS):
            frame = tk.Frame(window, width=80, height=80, bg='blue')
            frame.grid(row=row, column=col, padx=5, pady=5)

            # Create a canvas to simulate the circular chips
            canvas = tk.Canvas(frame, width=80, height=80, bg='white')
            canvas.pack()

            # Make the canvas clickable for human player moves
            canvas.bind("<Button-1>", lambda event, col=col: drop_piece(col))

            button_row.append(frame)
            canvas_row.append(canvas)

        buttons.append(button_row)
        canvases.append(canvas_row)


def reset_game():
    """Resets the game board to start a new game."""
    global board, current_player
    board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_player = random.choice([YELLOW, RED])  # Flip a coin again for a new game

    # Reset the canvases to white (empty)
    for row in canvases:
        for canvas in row:
            canvas.delete("all")

    # If the AI starts first, let it move
    if current_player == RED:
        window.after(500, ai_move)


def select_difficulty(selected_difficulty):
    """Sets the difficulty based on the button clicked."""
    global difficulty
    difficulty = selected_difficulty
    difficulty_window.destroy()  # Close the difficulty selection window
    window.deiconify()  # Show the game window after difficulty is selected


def ask_for_difficulty():
    """Prompts the user to choose a difficulty level using clickable buttons."""
    global difficulty_window
    difficulty_window = tk.Toplevel(window)
    difficulty_window.title("Select Difficulty")

    # Create Beginner and Medium buttons
    beginner_button = tk.Button(difficulty_window, text="Beginner", width=20, height=2,
                                command=lambda: select_difficulty("beginner"))
    beginner_button.pack(padx=20, pady=10)

    medium_button = tk.Button(difficulty_window, text="Medium", width=20, height=2,
                              command=lambda: select_difficulty("medium"))
    medium_button.pack(padx=20, pady=10)


# Ask the user for the difficulty before starting the game
ask_for_difficulty()

# Wait for the difficulty window to close, then create the game board
window.wait_window(difficulty_window)
create_board()

# If the AI goes first, let it make the first move
if current_player == RED:
    window.after(500, ai_move)

# Run the Tkinter event loop
window.mainloop()
