import tkinter as tk
from tkinter import messagebox
import random
import time

class SudokuGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Game")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        # Game state
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.original_puzzle = [[0 for _ in range(9)] for _ in range(9)]
        self.selected_cell = None
        self.difficulty = "Medium"
        self.difficulty_levels = {"Easy": 30, "Medium": 40, "Hard": 50}
        
        # Undo/Redo
        self.undo_stack = []
        self.redo_stack = []
        self.move_count = 0
        
        # Timer
        self.start_time = None
        self.timer_running = False
        self.timer_id = None
        
        # Error highlighting
        self.show_errors = True
        
        # Create UI
        self.create_menu()
        self.create_toolbar()
        self.create_board()
        self.create_number_pad()
        self.create_status_bar()
        
        self.generate_puzzle()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.generate_puzzle)
        game_menu.add_separator()
        
        diff_menu = tk.Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="Difficulty", menu=diff_menu)
        for level in ["Easy", "Medium", "Hard"]:
            diff_menu.add_command(label=level, command=lambda l=level: self.set_difficulty(l))
        
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Play", command=self.show_help)
        help_menu.add_command(label="Shortcuts", command=self.show_shortcuts)
        
    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(pady=5)
        
        tk.Button(toolbar, text="Undo", command=self.undo, width=8).grid(row=0, column=0, padx=2)
        tk.Button(toolbar, text="Redo", command=self.redo, width=8).grid(row=0, column=1, padx=2)
        tk.Button(toolbar, text="Hint", command=self.give_hint, width=8).grid(row=0, column=2, padx=2)
        tk.Button(toolbar, text="Check", command=self.check_solution, width=8).grid(row=0, column=3, padx=2)
        tk.Button(toolbar, text="Solve", command=self.solve_puzzle, width=8).grid(row=0, column=4, padx=2)
        tk.Button(toolbar, text="Clear", command=self.clear_board, width=8).grid(row=0, column=5, padx=2)
        
        self.error_var = tk.BooleanVar(value=True)
        tk.Checkbutton(toolbar, text="Highlight Errors", variable=self.error_var,
                       command=self.toggle_errors).grid(row=0, column=6, padx=5)
        
    def create_board(self):
        """Build the 9x9 grid with exactly four colored separator lines."""
        board_frame = tk.Frame(self.root, bg='white', bd=0)
        board_frame.pack(pady=10)
        
        # We'll use an 11x11 grid: cells at (0-2,4-6,8-10) for the 3x3 blocks,
        # and separator rows/columns at indices 3 and 7.
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        
        # Create Entry widgets for each of the 81 cells
        for i in range(9):
            for j in range(9):
                # Map entry (i,j) to grid position
                grid_row = i + (1 if i > 2 else 0) + (1 if i > 5 else 0)
                grid_col = j + (1 if j > 2 else 0) + (1 if j > 5 else 0)
                
                cell = tk.Entry(
                    board_frame,
                    width=2,
                    font=('Arial', 24, 'bold'),
                    justify='center',
                    relief='solid',
                    borderwidth=1,
                    highlightthickness=0
                )
                cell.grid(row=grid_row, column=grid_col, ipady=5, padx=1, pady=1, sticky='nsew')
                cell.bind('<Button-1>', lambda e, row=i, col=j: self.select_cell(row, col))
                cell.bind('<Key>', self.on_key_press)
                cell.bind('<FocusIn>', lambda e, row=i, col=j: self.select_cell(row, col))
                self.cells[i][j] = cell
        
        # --- Add only the four colored separator lines ---
        # Two vertical green lines at grid columns 3 and 7
        for col in (3, 7):
            tk.Frame(board_frame, bg='green', width=3).grid(
                row=0, column=col, rowspan=11, sticky='ns', padx=0, pady=0)
        
        # Two horizontal blue lines at grid rows 3 and 7
        for row in (3, 7):
            tk.Frame(board_frame, bg='blue', height=3).grid(
                row=row, column=0, columnspan=11, sticky='ew', padx=0, pady=0)
        
        # Configure column/row weights to make cells expand evenly
        for col in range(11):
            board_frame.grid_columnconfigure(col, weight=1)
        for row in range(11):
            board_frame.grid_rowconfigure(row, weight=1)
        
    def create_number_pad(self):
        number_frame = tk.Frame(self.root)
        number_frame.pack(pady=10)
        
        for i in range(1, 10):
            btn = tk.Button(
                number_frame,
                text=str(i),
                width=4,
                height=2,
                font=('Arial', 14),
                command=lambda num=i: self.insert_number(num)
            )
            btn.grid(row=(i-1)//3, column=(i-1)%3, padx=2, pady=2)
        
        tk.Button(
            number_frame,
            text="⌫",
            width=4,
            height=2,
            font=('Arial', 14),
            command=self.clear_cell
        ).grid(row=3, column=0, padx=2, pady=2)
        
        tk.Button(
            number_frame,
            text="✕",
            width=4,
            height=2,
            font=('Arial', 14),
            command=self.clear_user_entries
        ).grid(row=3, column=1, padx=2, pady=2)
        
    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bd=1, relief='sunken')
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.status_label = tk.Label(status_frame, text="Ready", anchor='w')
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.timer_label = tk.Label(status_frame, text="Time: 00:00", anchor='e')
        self.timer_label.pack(side=tk.RIGHT, padx=5)
        
        self.moves_label = tk.Label(status_frame, text="Moves: 0", anchor='e')
        self.moves_label.pack(side=tk.RIGHT, padx=10)
        
    # ---------- Core game logic (all features intact) ----------
    def set_difficulty(self, level):
        self.difficulty = level
        self.generate_puzzle()
        self.status_label.config(text=f"Difficulty: {level}")
        
    def toggle_errors(self):
        self.show_errors = self.error_var.get()
        self.update_board()
        
    def select_cell(self, row, col):
        if self.selected_cell:
            prev_row, prev_col = self.selected_cell
            self.cells[prev_row][prev_col].config(bg='white')
            self.clear_highlights()
        
        self.selected_cell = (row, col)
        self.cells[row][col].config(bg='lightblue')
        
        num = self.board[row][col]
        if num != 0:
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == num and (i, j) != (row, col):
                        self.cells[i][j].config(bg='lightgreen')
        
    def clear_highlights(self):
        for i in range(9):
            for j in range(9):
                if (i, j) != self.selected_cell:
                    if self.original_puzzle[i][j] != 0:
                        self.cells[i][j].config(bg='lightgray')
                    else:
                        self.cells[i][j].config(bg='white')
        
    def on_key_press(self, event):
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        
        if event.char in '123456789':
            self.insert_number(int(event.char))
        elif event.keysym in ('BackSpace', 'Delete'):
            self.clear_cell()
        elif event.keysym == 'Up' and row > 0:
            self.select_cell(row-1, col)
        elif event.keysym == 'Down' and row < 8:
            self.select_cell(row+1, col)
        elif event.keysym == 'Left' and col > 0:
            self.select_cell(row, col-1)
        elif event.keysym == 'Right' and col < 8:
            self.select_cell(row, col+1)
        elif event.keysym in ('u', 'U'):
            self.undo()
        elif event.keysym in ('r', 'R'):
            self.redo()
        elif event.keysym in ('h', 'H'):
            self.give_hint()
        return 'break'
    
    def insert_number(self, number):
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if self.original_puzzle[row][col] != 0:
            return
        
        old_value = self.board[row][col]
        if old_value != number:
            self.undo_stack.append((row, col, old_value, number))
            self.redo_stack.clear()
            self.move_count += 1
            self.update_moves()
        
        self.board[row][col] = number
        self.cells[row][col].delete(0, tk.END)
        if number != 0:
            self.cells[row][col].insert(0, str(number))
        
        if self.show_errors and number != 0:
            if number != self.solution[row][col]:
                self.cells[row][col].config(bg='red')
            else:
                self.cells[row][col].config(bg='white')
        else:
            self.cells[row][col].config(bg='white')
        
        if col < 8:
            self.select_cell(row, col+1)
        elif row < 8:
            self.select_cell(row+1, 0)
        
        if self.is_board_complete():
            self.timer_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            messagebox.showinfo("Sudoku", "Congratulations! You solved the puzzle!")
        
        self.status_label.config(text=f"Inserted {number}")
        self.start_timer()
        
    def clear_cell(self):
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if self.original_puzzle[row][col] != 0:
            return
        
        old_value = self.board[row][col]
        if old_value != 0:
            self.undo_stack.append((row, col, old_value, 0))
            self.redo_stack.clear()
            self.move_count += 1
            self.update_moves()
        
        self.board[row][col] = 0
        self.cells[row][col].delete(0, tk.END)
        self.cells[row][col].config(bg='white')
        self.status_label.config(text="Cleared cell")
        
    def clear_user_entries(self):
        for i in range(9):
            for j in range(9):
                if self.original_puzzle[i][j] == 0:
                    self.board[i][j] = 0
        self.update_board()
        self.status_label.config(text="Cleared all user entries")
        
    def generate_puzzle(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_label.config(text="Time: 00:00")
        self.start_time = None
        self.move_count = 0
        self.update_moves()
        
        self.undo_stack.clear()
        self.redo_stack.clear()
        
        self.clear_board(keep_original=False)
        
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku(self.solution, generate=True)
        
        self.board = [row[:] for row in self.solution]
        remove_count = self.difficulty_levels.get(self.difficulty, 40)
        self.remove_numbers(remove_count)
        
        self.original_puzzle = [row[:] for row in self.board]
        self.update_board()
        self.status_label.config(text=f"New {self.difficulty} puzzle generated")
        self.selected_cell = None
        
    def remove_numbers(self, count):
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        removed = 0
        for i, j in cells:
            if removed >= count:
                break
            temp = self.board[i][j]
            self.board[i][j] = 0
            if not self.has_unique_solution():
                self.board[i][j] = temp
            else:
                removed += 1
                
    def has_unique_solution(self):
        board_copy = [row[:] for row in self.board]
        solutions = []
        self.count_solutions(board_copy, solutions)
        return len(solutions) == 1
    
    def count_solutions(self, board, solutions):
        if len(solutions) > 1:
            return
        empty = self.find_empty(board)
        if not empty:
            solutions.append([row[:] for row in board])
            return
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                self.count_solutions(board, solutions)
                board[row][col] = 0
                if len(solutions) > 1:
                    return
    
    def solve_sudoku(self, board, generate=False):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty
        numbers = list(range(1, 10))
        if generate:
            random.shuffle(numbers)
        for num in numbers:
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board, generate):
                    return True
                board[row][col] = 0
        return False
    
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, board, row, col, num):
        for j in range(9):
            if board[row][j] == num:
                return False
        for i in range(9):
            if board[i][col] == num:
                return False
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row+3):
            for j in range(box_col, box_col+3):
                if board[i][j] == num:
                    return False
        return True
    
    def update_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if self.board[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.board[i][j]))
                
                if self.original_puzzle[i][j] != 0:
                    self.cells[i][j].config(state='readonly', readonlybackground='lightgray', bg='lightgray')
                else:
                    self.cells[i][j].config(state='normal', bg='white')
                
                if self.show_errors and self.board[i][j] != 0 and self.original_puzzle[i][j] == 0:
                    if self.board[i][j] != self.solution[i][j]:
                        self.cells[i][j].config(bg='red')
        
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].config(bg='lightblue')
    
    def check_solution(self):
        errors = 0
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != self.solution[i][j]:
                    errors += 1
        if errors == 0:
            messagebox.showinfo("Sudoku", "Perfect! You solved it correctly.")
        else:
            messagebox.showwarning("Sudoku", f"There are {errors} incorrect cells.")
            if self.show_errors:
                for i in range(9):
                    for j in range(9):
                        if self.board[i][j] != self.solution[i][j] and self.board[i][j] != 0:
                            self.cells[i][j].config(bg='red')
    
    def solve_puzzle(self):
        board_copy = [row[:] for row in self.board]
        if self.solve_sudoku(board_copy):
            self.board = board_copy
            self.update_board()
            self.status_label.config(text="Solved!")
        else:
            messagebox.showerror("Sudoku", "This puzzle cannot be solved!")
    
    def clear_board(self, keep_original=True):
        if keep_original:
            self.board = [row[:] for row in self.original_puzzle]
        else:
            self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.update_board()
        self.selected_cell = None
    
    def give_hint(self):
        if not self.selected_cell:
            messagebox.showinfo("Hint", "Select a cell first.")
            return
        row, col = self.selected_cell
        if self.original_puzzle[row][col] != 0:
            messagebox.showinfo("Hint", "This is a given number.")
            return
        if self.board[row][col] == self.solution[row][col]:
            messagebox.showinfo("Hint", "This cell is already correct.")
            return
        old_value = self.board[row][col]
        self.board[row][col] = self.solution[row][col]
        self.undo_stack.append((row, col, old_value, self.solution[row][col]))
        self.redo_stack.clear()
        self.move_count += 1
        self.update_moves()
        self.update_board()
        self.select_cell(row, col)
        self.status_label.config(text=f"Hint: placed {self.solution[row][col]}")
        
    def undo(self):
        if not self.undo_stack:
            self.status_label.config(text="Nothing to undo")
            return
        row, col, old_val, new_val = self.undo_stack.pop()
        self.redo_stack.append((row, col, new_val, old_val))
        self.board[row][col] = old_val
        self.update_board()
        self.select_cell(row, col)
        self.move_count -= 1
        self.update_moves()
        self.status_label.config(text="Undo")
        
    def redo(self):
        if not self.redo_stack:
            self.status_label.config(text="Nothing to redo")
            return
        row, col, old_val, new_val = self.redo_stack.pop()
        self.undo_stack.append((row, col, old_val, new_val))
        self.board[row][col] = new_val
        self.update_board()
        self.select_cell(row, col)
        self.move_count += 1
        self.update_moves()
        self.status_label.config(text="Redo")
    
    def update_moves(self):
        self.moves_label.config(text=f"Moves: {self.move_count}")
    
    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()
    
    def update_timer(self):
        if not self.timer_running:
            return
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        self.timer_id = self.root.after(1000, self.update_timer)
    
    def is_board_complete(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def show_help(self):
        help_text = """
How to Play Sudoku:

- Fill the grid so that each row, column, and 3x3 box contains the digits 1-9.
- Click a cell to select it, then type a number or use the number pad.
- Use the toolbar for Undo, Redo, Hint, Check, Solve, Clear.
- Keyboard shortcuts: U=Undo, R=Redo, H=Hint, Arrow keys to navigate.
- The timer starts when you make your first move.
- Highlight Errors shows wrong numbers in red.
        """
        messagebox.showinfo("How to Play Sudoku", help_text)
    
    def show_shortcuts(self):
        shortcuts = """
Keyboard Shortcuts:
- 1-9 : Insert number
- Backspace/Delete : Clear cell
- Arrow keys : Navigate
- U : Undo
- R : Redo
- H : Hint
        """
        messagebox.showinfo("Shortcuts", shortcuts)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = SudokuGame()
    game.run()