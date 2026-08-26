import tkinter as tk

from Board import Board


class GameWindow(tk.Tk):
    TILE_COLORS = {
        0: ("#cdc1b4", "#776e65"),
        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#776e65"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#edc850", "#f9f6f2"),
        1024: ("#edc53f", "#f9f6f2"),
        2048: ("#edc22e", "#f9f6f2"),
    }

    def __init__(self):
        super().__init__()
        self.title("2048")
        self.geometry("420x520")
        self.configure(bg="#faf8ef")
        self.resizable(False, False)

        self.board = Board()
        self.score = tk.IntVar(value=0)
        self.status = tk.StringVar(value="Use arrow keys to play")

        self.build_ui()
        self.bind("<KeyPress>", self.handle_key)
        self.focus_set()
        self.refresh_board()

    def build_ui(self):
        top_bar = tk.Frame(self, bg="#faf8ef", padx=18, pady=18)
        top_bar.pack(fill="x")

        title = tk.Label(
            top_bar,
            text="2048",
            font=("Arial", 28, "bold"),
            fg="#776e65",
            bg="#faf8ef",
        )
        title.pack(side="left")

        sidebar = tk.Frame(top_bar, bg="#faf8ef")
        sidebar.pack(side="right")

        score_label = tk.Label(
            sidebar,
            text="Score",
            font=("Arial", 12, "bold"),
            bg="#bbada0",
            fg="#f9f6f2",
            padx=12,
            pady=6,
        )
        score_label.pack(fill="x")

        score_value = tk.Label(
            sidebar,
            textvariable=self.score,
            font=("Arial", 18, "bold"),
            bg="#bbada0",
            fg="#f9f6f2",
            padx=12,
            pady=6,
        )
        score_value.pack(fill="x")

        controls = tk.Frame(self, bg="#faf8ef", padx=18, pady=12)
        controls.pack(fill="x")

        reset_button = tk.Button(
            controls,
            text="New game",
            command=self.reset_game,
            bg="#8f7a66",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            padx=14,
            pady=8,
            activebackground="#7d685a",
            cursor="hand2",
        )
        reset_button.pack(side="left")

        status_label = tk.Label(
            controls,
            textvariable=self.status,
            font=("Arial", 11, "bold"),
            fg="#776e65",
            bg="#faf8ef",
        )
        status_label.pack(side="right")

        grid_frame = tk.Frame(self, bg="#bbada0", padx=12, pady=12)
        grid_frame.pack(padx=18, pady=18, fill="both", expand=True)

        self.tile_labels = [
            [
                tk.Label(
                    grid_frame,
                    text="",
                    width=5,
                    height=2,
                    font=("Arial", 22, "bold"),
                    bg="#cdc1b4",
                    fg="#776e65",
                    relief="flat",
                    padx=10,
                    pady=10,
                    anchor="center",
                )
                for _ in range(Board.SIZE)
            ]
            for _ in range(Board.SIZE)
        ]

        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                self.tile_labels[row][col].grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        for i in range(Board.SIZE):
            grid_frame.grid_columnconfigure(i, weight=1)
            grid_frame.grid_rowconfigure(i, weight=1)

    def reset_game(self):
        self.board = Board()
        self.score.set(0)
        self.status.set("Use arrow keys to play")
        self.refresh_board()

    def handle_key(self, event):
        direction_map = {
            "Left": "left",
            "Right": "right",
            "Up": "up",
            "Down": "down",
        }
        direction = direction_map.get(event.keysym)
        if not direction:
            return

        moved = self.board.move(direction)
        if moved:
            self.score.set(self.board.score)
            self.status.set("Nice move!")
        elif self.board.game_over:
            self.status.set("Game over! Press New game.")
        else:
            self.status.set("No move available")

        self.refresh_board()

    def refresh_board(self):
        self.score.set(self.board.score)
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                value = self.board.board[row][col].value
                bg, fg = self.TILE_COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                label = self.tile_labels[row][col]
                label.configure(
                    text=str(value) if value else "",
                    bg=bg,
                    fg=fg,
                )

        if self.board.game_over:
            self.status.set("Game over! Press New game.")


def main():
    app = GameWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
