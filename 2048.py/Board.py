import random

from Piece import Piece


class Board:
    SIZE = 4

    def __init__(self):
        self.board = [[Piece(0) for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.score = 0
        self.game_over = False
        self._place_value(2)
        self._place_value(2)

    def _place_value(self, value):
        empty_positions = [
            (row, col)
            for row in range(self.SIZE)
            for col in range(self.SIZE)
            if self.board[row][col].value == 0
        ]
        if not empty_positions:
            return False
        row, col = random.choice(empty_positions)
        self.board[row][col].value = value
        return True

    def _normalize_row(self, row):
        normalized = []
        for cell in row:
            if isinstance(cell, Piece):
                normalized.append(cell)
            else:
                normalized.append(Piece(cell))
        return normalized

    def _normalize_board(self):
        self.board = [self._normalize_row(row) for row in self.board]

    def _snapshot(self):
        return [[cell.value for cell in row] for row in self.board]

    def add_random_tile(self):
        empty_positions = [
            (row, col)
            for row in range(self.SIZE)
            for col in range(self.SIZE)
            if self.board[row][col].value == 0
        ]
        if not empty_positions:
            return False

        row, col = random.choice(empty_positions)
        self.board[row][col].value = 4 if random.random() < 0.1 else 2
        return True

    def _collapse_line(self, values):
        compact = [value for value in values if value != 0]
        merged = []
        index = 0
        while index < len(compact):
            if index + 1 < len(compact) and compact[index] == compact[index + 1]:
                merged_value = compact[index] * 2
                merged.append(merged_value)
                self.score += merged_value
                index += 2
            else:
                merged.append(compact[index])
                index += 1

        merged.extend([0] * (self.SIZE - len(merged)))
        return merged

    def _move_row_left(self, row):
        values = [piece.value for piece in row]
        collapsed = self._collapse_line(values)
        return [Piece(value) for value in collapsed]

    def _move_row_right(self, row):
        values = [piece.value for piece in row][::-1]
        collapsed = self._collapse_line(values)[::-1]
        return [Piece(value) for value in collapsed]

    def _move_column_up(self, column):
        values = [piece.value for piece in column]
        collapsed = self._collapse_line(values)
        return [Piece(value) for value in collapsed]

    def _move_column_down(self, column):
        values = [piece.value for piece in column][::-1]
        collapsed = self._collapse_line(values)[::-1]
        return [Piece(value) for value in collapsed]

    def move(self, direction):
        self._normalize_board()
        before = self._snapshot()

        if direction == "left":
            self.board = [self._move_row_left(row) for row in self.board]
        elif direction == "right":
            self.board = [self._move_row_right(row) for row in self.board]
        elif direction == "up":
            columns = [[self.board[row][col] for row in range(self.SIZE)] for col in range(self.SIZE)]
            new_columns = [self._move_column_up(column) for column in columns]
            self.board = [
                [new_columns[col][row] for col in range(self.SIZE)]
                for row in range(self.SIZE)
            ]
        elif direction == "down":
            columns = [[self.board[row][col] for row in range(self.SIZE)] for col in range(self.SIZE)]
            new_columns = [self._move_column_down(column) for column in columns]
            self.board = [
                [new_columns[col][row] for col in range(self.SIZE)]
                for row in range(self.SIZE)
            ]
        else:
            raise ValueError(f"Unsupported direction: {direction}")

        changed = self._snapshot() != before
        if changed:
            self.add_random_tile()
        self.game_over = not self.can_move()
        return changed

    def can_move(self):
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                value = self.board[row][col].value
                if value == 0:
                    return True
                if col + 1 < self.SIZE and value == self.board[row][col + 1].value:
                    return True
                if row + 1 < self.SIZE and value == self.board[row + 1][col].value:
                    return True
        return False

    def count_non_zero(self):
        return sum(piece.value != 0 for row in self.board for piece in row)

    def __str__(self):
        rows = []
        for row in self.board:
            rows.append(" | ".join(str(piece.value).rjust(4) if piece.value else "   " for piece in row))
        return "\n".join(rows)

