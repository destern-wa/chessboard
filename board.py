class Board:
    """A chess board"""

    def __init__(self):
        # Initialise 2d array for current state of board
        self.state = [[]]
        self.size = 8  # board is size 8*8
        self.reset()

    def reset(self):
        """Resets the board to its initial state at the start of a game"""
        self.state = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P'] * 8,
            [' '] * 8,
            [' '] * 8,
            [' '] * 8,
            [' '] * 8,
            ['p'] * 8,
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]

    def get_square(self, col, row) -> str:
        """Gets the piece at a sqaure

        :param col: column letter, 'a' to 'h'
        :param row: row number, 1 to 8
        :return: Letter indicating the piece at the square, or a space if the square is empty
        """
        row_index = row - 1
        col_index = ord(col.lower()) - 97  # ord('a') is 97
        return self.state[row_index][col_index]

    def set_square(self, col, row, value):
        """Sets the value of a square on the board

        :param col: column letter, 'a' to 'h'
        :param row: row number, 1 to 8
        :param value: Value to be set (letter of a piece, or a space)
        """
        row_index = row - 1
        col_index = ord(col.lower()) - 97  # ord('a') is 97
        self.state[row_index][col_index] = value

    def piece_colour(self, col, row):
        """Gets the colour of a piece at a particular square

        :param col: square column letter, 'a' to 'h'
        :param row: square row number, 1 to 8
        :return: 'W' for a white piece, 'B' for a black piece, or None if square is empty
        """
        square = self.get_square(col, row)
        if square == ' ':
            return None
        return 'W' if square.isupper() else 'B'

    def print(self):
        """Prints the board to the screen"""
        print("    a   b   c   d   e   f   g   h  ")
        print("  ┼───┼───┼───┼───┼───┼───┼───┼───┼")
        for row in range(8, 0, -1):
            pieces = " │ ".join(self.state[row - 1])
            print(f"{row} │ {pieces} │ {row}")
            print("  ┼───┼───┼───┼───┼───┼───┼───┼───┼")
        print("    a   b   c   d   e   f   g   h  ")

    def __str__(self):
        """Returns a string representation of the current state of the board

        :return: String representation of the board
        """
        return "".join(list(map(lambda row: ''.join(row), self.state)))

    def move(self, player_colour, from_col, from_row, to_col, to_row):
        """Moves a piece from one square to another

        :param player_colour: 'W' for white player, 'B' for black player
        :param from_col: column letter of piece to move, 'a' to 'h'
        :param from_row: row number of piece to move, 1 to 8
        :param to_col: column letter of square to move to, 'a' to 'h'
        :param to_row: row number of square to move to, 1 to 8
        :raises RuntimeError: if move is invalid
        """
        # Validate from square is a piece
        from_square = self.get_square(from_col, from_row)
        if from_square == ' ':
            raise RuntimeError(f"No piece located at {from_col}{from_row}")

        # Validate the from square is a piece of the player's colour.
        if player_colour != self.piece_colour(from_col, from_row):
            raise RuntimeError(f"An opponent's piece cannot be moved")

        # Validate the to square is not a piece of the player's color
        if player_colour == self.piece_colour(to_col, to_row):
            raise RuntimeError(f"A player cannot take their own piece")

        # Validate the piece can move that way
        if not self.validate_movement(from_square, from_col, from_row, to_col, to_row):
            raise RuntimeError(f"The piece cannot move that way")

        # Make the move
        self.set_square(to_col, to_row, from_square)
        self.set_square(from_col, from_row, ' ')

    def castle(self, is_white, is_kingside):
        """Performs a castling move

        :param is_white: True for white, False for black
        :param is_kingside: True for a kingside castle, False for a queenside castle
        :raises: RuntimeError: if move is invalid
        """
        if is_white and is_kingside:
            # Validate castling is possible
            if self.get_square('e', 1) != "K" or self.get_square('f', 1) != " " or self.get_square('g', 1) != " " \
                    or self.get_square('h', 1) != 'R':
                raise RuntimeError("White can not castle kingside")
            # Make the move
            self.set_square('e', 1, ' ')
            self.set_square('f', 1, 'R')
            self.set_square('g', 1, 'K')
            self.set_square('h', 1, ' ')

        elif is_white and not is_kingside:
            # Validate castling is possible
            if self.get_square('e', 1) != "K" or self.get_square('d', 1) != " " or self.get_square('c', 1) != " " \
                    or self.get_square('b', 1) != " " or self.get_square('a', 1) != 'R':
                raise RuntimeError("White can not castle queenside")
            # Make the move
            self.set_square('e', 1, ' ')
            self.set_square('d', 1, 'R')
            self.set_square('c', 1, 'K')
            self.set_square('a', 1, ' ')

        elif is_kingside:  # for black
            # Validate castling is possible
            if self.get_square('e', 8) != "k" or self.get_square('f', 8) != " " or self.get_square('g', 8) != " " \
                    or self.get_square('h', 8) != 'r':
                raise RuntimeError("Black can not castle kingside")
            # Make the move
            self.set_square('e', 8, ' ')
            self.set_square('f', 8, 'r')
            self.set_square('g', 8, 'k')
            self.set_square('h', 8, ' ')

        else:  # black, queenside
            # Validate castling is possible
            if self.get_square('e', 8) != "k" or self.get_square('d', 8) != " " or self.get_square('c', 8) != " " \
                    or self.get_square('b', 8) != " " or self.get_square('a', 8) != 'r':
                raise RuntimeError("Black can not castle queenside")
            # Make the move
            self.set_square('e', 8, ' ')
            self.set_square('d', 8, 'r')
            self.set_square('c', 8, 'k')
            self.set_square('a', 8, ' ')

    def validate_movement(self, piece, from_col, from_row, to_col, to_row):
        """Validates whether a piece can move from one square to another.
        Only validates the movement, without considering other pieces on
        the board, or if the king will be checked.

        :param piece: Letter denoting the piece
        :param from_col: column letter of piece to move, 'a' to 'h'
        :param from_row: row number of piece to move, 1 to 8
        :param to_col: column letter of square to move to, 'a' to 'h'
        :param to_row: row number of square to move to, 1 to 8
        :return: True if the movement is valid, false otherwise
        """
        col_diff = abs(ord(from_col) - ord(to_col))
        row_diff = abs(from_row - to_row)

        # For any piece, it must actually move
        if col_diff == 0 and row_diff == 0:
            return False

        # White pawn
        if piece == 'P':
            if col_diff != 0:
                # Can't change columns (en-passant is not considered)
                return False
            elif from_row == 2:
                # From initial position, can go up one or two rows
                return to_row == 3 or to_row == 4
            else:
                # Otherwise, can only move up one row
                return to_row - from_row == 1
        # Black pawn
        elif piece == 'p':
            if col_diff != 0:
                # Can't change columns (en-passant is not considered)
                return False
            elif from_row == 7:
                # From initial position, can go down one or two rows
                return to_row == 6 or to_row == 5
            else:
                # Otherwise, can only move down one row
                return from_row - to_row == 1
        # Rook
        elif piece.lower() == 'r':
            # Must remain in same column or same row
            return col_diff == 0 or row_diff == 0
        # Knight
        elif piece.lower() == 'n':
            # Jumps in a 2+1 pattern
            return (col_diff == 2 and row_diff == 1) or (col_diff == 1 and row_diff == 2)
        # Bishop
        elif piece.lower() == 'b':
            # Moves along diagonals
            return col_diff == row_diff
        # Queen
        elif piece.lower() == 'q':
            # Can move along columns, rows, or diagonals
            return col_diff == 0 or row_diff == 0 or col_diff == row_diff
        # King
        elif piece.lower() == 'k':
            # Can move a single square in any direction
            return (0 <= col_diff <= 1) and (0 <= row_diff <= 1)


if __name__ == "__main__":
    b = Board()
    b.print()
    print(str(b))
    print(b.get_square('a', 1))
    b.set_square('f', 1, ' ')
    b.set_square('g', 1, ' ')
    b.castle(True, True)
    b.print()
    b.move('W', 'g', 1, 'h', 1)
    b.print()
    print(str(b))
