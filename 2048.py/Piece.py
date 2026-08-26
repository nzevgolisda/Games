
class Piece:
    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return f"Piece({self.value})"

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return str(self.value)