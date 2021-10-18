from board import Board
from gamefile import GameFile


class Game:
    """Represents a game of chess"""

    def __init__(self, filename, load=False):
        # Store the filename for saving/loading
        self.game_file = GameFile(filename)
        # Create a board
        self.board = Board()
        # White is the first player
        self.next_player = 'W'
        if load:
            # Load the stored state of the game
            self.game_file.load(self)
        else:
            # Save the initial state to file (overwriting)
            self.game_file.save(self)

    def update_file_with_castle(self, isWhite, isKingside):
        if isWhite and isKingside:
            self.game_file.update(self, ["e1", "f1", "g1", "h1"])
        elif isWhite and isKingside:
            self.game_file.update(self, ["a1", "c1", "d1", "e1"])
        elif isKingside:  # for black
            self.game_file.update(self, ["e8", "f8", "g8", "h8"])
        else:  # queenside black
            self.game_file.update(self, ["a8", "c8", "d8", "e8"])

    def play(self):
        """Plays the game by repeatedly asking for moves"""
        # Show the current state of the board
        print('\n')
        self.board.print()
        # Keep making moves and showing the board
        while self.play_move():
            self.board.print()

    def play_move(self):
        """Asks for a move, then updates the board (in memory and file).

        :return True if gameplay should continue, False otherwise
        """
        # Ask for the next player's move
        player_colour = "White" if self.next_player == "W" else "Black"
        move = input(f"{player_colour} player's move: ").lower()
        if move == "exit" or move == "quit":
            # Quit the game
            print(f"Thanks for playing, goodbye!")
            return False

        elif move == "o-o" or move == "o-o-o":
            # Try to play a castling move
            is_white = self.next_player == "W"
            is_kingside = move == "o-o"
            try:
                self.board.castle(is_white, is_kingside)
                self.toggle_player()
                self.update_file_with_castle(is_white, is_kingside)
            except RuntimeError as err:
                print(">>> Invalid move :(")
                return True

        else:
            # Try to play a non-castling move
            try:
                from_col, from_row, to_col, to_row = self.parse_move(move)
                is_en_passant = self.board.is_en_passant(from_col, from_row, to_col, to_row)
                self.board.move(self.next_player, from_col, from_row, to_col, to_row)
                self.toggle_player()
                squares_to_update = [(from_col, from_row), (to_col, to_row)]
                if is_en_passant:
                    squares_to_update.append((to_col, from_row))
                self.game_file.update(self, squares_to_update)
            except RuntimeError as err:
                print(f">>> Invalid move: {err}")
                return True

        # Switch to the other player
        return True

    def toggle_player(self):
        """Toggles the next player between black and white"""
        self.next_player = "B" if self.next_player == "W" else "W"

    def parse_move(self, move):
        """Parses a non-castling move from a string containing the from and to squares, separated by a space.
        This may be in the following formats:
        - Just the squares, e.g. "f3 d4"
        - The "to square" may also indicate the piece being moved, e.g. "f3 Nd4"
        - The "to square" may also indicate a capture with an 'x', e.g. "f3 Nxd4"
        - The "to square" may indicate a check by adding a '+', e.g. "f3 d4+" or "f3 Nd4+" or "f3 Nxd4+"

        :param move: String representation of the move
        :return: from column (letter), from row (number), to column (letter), to row (number)
        """
        # Some basic validation - length must be between 5 and 8
        if not 5 <= len(move) <= 8:
            raise RuntimeError("Invalid input format")
        # Strip off the plus sign, if present
        move = move.strip('+')
        # Validate the separator between the from/to squares
        if move[2] != ' ':
            raise RuntimeError("Invalid input format")
        # Pick out the columns and rows, then validate them
        from_col = move[0]
        from_row = move[1]
        to_col = move[-2]
        to_row = move[-1]
        if from_col not in "abcdefgh" or from_row not in "12345678" \
                or to_col not in "abcdefgh" or to_row not in "12345678":
            raise RuntimeError("Invalid input format")
        # return the column letters, and the rows as integers
        return from_col, int(from_row), to_col, int(to_row)


if __name__ == "__main__":
    game = Game("testgame.txt")
    # game = Game("testgame.txt", True)
    game.play()
