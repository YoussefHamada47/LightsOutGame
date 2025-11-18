import tkinter as tk
import random
from collections import deque

SIZE = 5

PRESS_MASKS = [[0] * SIZE for _ in range(SIZE)]
for row in range(SIZE):
    for col in range(SIZE):
        mask = 0
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < SIZE and 0 <= new_col < SIZE:
                mask |= 1 << (new_row * SIZE + new_col)
        PRESS_MASKS[row][col] = mask

def board_to_int(board):
    num = 0
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col]:
                num |= 1 << (row * SIZE + col)
    return num

def int_to_board(num):
    return [[(num >> (row * SIZE + col)) & 1 for col in range(SIZE)] for row in range(SIZE)]

def is_solved_int(state):
    return state == 0

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

class LightsOutAI_BFS:
    def __init__(self, root):
        self.root = root
        self.root.title("Lights Out with BFS")
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.buttons = [[None] * SIZE for _ in range(SIZE)]

        for row in range(SIZE):
            for col in range(SIZE):
                btn = tk.Label(root, width=8, height=4, relief="ridge", font=("Arial", 12))
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.buttons[row][col] = btn

        self.create_random_board()
        self.update_buttons()

        start_state = board_to_int(self.board)
        self.solution = self.bfs_solver(start_state)

        if self.solution is not None:
            self.play_solution()

    def create_random_board(self):
        for row in range(SIZE):
            for col in range(SIZE):
                self.board[row][col] = 0
        for _ in range(random.randint(5, 10)):
            row, col = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
            self.board = int_to_board(board_to_int(self.board) ^ PRESS_MASKS[row][col])

    def update_buttons(self):
        for row in range(SIZE):
            for col in range(SIZE):
                if self.board[row][col] == 1:
                    color = "yellow"
                else:
                    color = "gray20"
                self.buttons[row][col].configure(bg=color)

    def bfs_solver(self, start_state):
        queue = deque()
        queue.append((start_state, []))
        visited = set()
        visited.add(start_state)

        while queue:
            current_state, path_so_far = queue.popleft()

            if is_solved_int(current_state):
                return path_so_far

            for row in range(SIZE):
                for col in range(SIZE):
                    next_state = current_state ^ PRESS_MASKS[row][col]
                    if next_state not in visited:
                        visited.add(next_state)
                        new_path = path_so_far + [(row, col)]
                        queue.append((next_state, new_path))

        return None

    def play_solution(self, index=0):
        if self.solution and index < len(self.solution):
            row, col = self.solution[index]
            self.board = int_to_board(board_to_int(self.board) ^ PRESS_MASKS[row][col])
            self.update_buttons()
            self.root.after(500, lambda: self.play_solution(index + 1))
        elif is_solved_int(board_to_int(self.board)):
            print("A.I Solve the game!")

if __name__ == "__main__":
    root = tk.Tk()
    center_window(root, 410, 410)
    game = LightsOutAI_BFS(root)
    root.mainloop()
