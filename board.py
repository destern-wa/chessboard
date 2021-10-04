class Board:
    """A chess board"""
    def __init__(self):
        # Initialise 2d array for current state of board
        self.state = [[]]
        self.reset()

    def reset(self):
        """Resets the board to its initial state at the start of a game"""
        self.state = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P']*8,
            [' ']*8,
            [' ']*8,
            [' ']*8,
            [' ']*8,
            ['p']*8,
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]

    def print(self):
        print("    a   b   c   d   e   f   g   h  ")
        print("  ┼───┼───┼───┼───┼───┼───┼───┼───┼")
        for row in range(8, 0, -1):
            pieces = " │ ".join(self.state[row-1])
            print(f"{row} │ {pieces} │ {row}")
            print("  ┼───┼───┼───┼───┼───┼───┼───┼───┼")
        print("    a   b   c   d   e   f   g   h  ")

    def __str__(self):
        """Returns a string representation of the current state of the board

        :return: String representation of the board
        """
        return "".join(list(map(lambda row: ''.join(row), self.state)))


if __name__ == "__main__":
    b = Board()
    b.print()
    print(str(b))