from board import Board


class Game:
    """Represents a game of chess"""

    def __init__(self, filename, load=False):
        # Store the filename for saving/loading
        self.filename = filename
        # Create a board
        self.board = Board()
        # White is the first player
        self.next_player = 'W'
        if load:
            # Load the stored state of the game
            self.load_from_file()
        else:
            # Save the initial state to file (overwriting)
            self.save_to_file()

    def load_from_file(self):
        """Loads the state of the game from file"""
        try:
            with open(self.filename, mode='r') as file:
                # First char in the file is the next player
                self.next_player = file.read(1)
                # Each square of each row of the board are the next 64 characters
                for i in range(self.board.size ** 2):
                    square_index = i % self.board.size
                    square_col = chr(square_index + 97)  # chr(97) is 'a'
                    square_row = (i // self.board.size) + 1
                    square_value = file.read(1)
                    self.board.set_square(square_col, square_row, square_value)

        except IOError as err:
            print(f"Error loading file: {err}")

    def save_to_file(self):
        """Saves the current state of the game to file"""
        try:
            with open(self.filename, mode='w+') as file:
                # First char in the file is the next player
                file.write(self.next_player)
                # Then the board as a string of 64 characters
                file.write(str(self.board))

        except IOError as err:
            print(f"Error saving file: {err}")

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
            try:
                self.board.castle(self.next_player == "W", move == "o-o")
                self.toggle_player()
            except RuntimeError as err:
                print(">>> Invalid move :(")
                return True

        else:
            # Try to play a non-castling move
            try:
                from_col, from_row, to_col, to_row = self.parse_move(move)
                self.board.move(from_col, from_row, to_col, to_row)
            except RuntimeError as err:
                print(">>> Invalid move :(")
                return True

        # Switch to the other player
        self.toggle_player()
        return True

    def toggle_player(self):
        """Toggles the next player between black and white"""
        self.next_player = "B" if self.next_player == "W" else "W"

    def parse_move(self, move):
        """Parses a non-castling move from a string containing the from and to squares.
        This may be in the following formats, either:
          - The from and to squares separated by a space, e.g. "f3 d4"
          - The from and to squares separated by an 'x', e.g. "f3xd4"
          - Either of the above prefixed by the piece being moved, e.g. "Nf3xd4"

        :param move: String representation of the move
        :return: from column (letter), from row (number), to column (letter), to row (number)
        """
        # Some basic validation
        if not 5 <= len(move) <= 6:
            raise RuntimeError("Invalid input format")
        # Strip off the piece prefix if present
        if len(move) == 6:
            move = move[1:]
        # Validate the separator between the from/to squares
        if not move[2] in " x":
            raise RuntimeError("Invalid input format")
        # Pick out the columns and rows, then validate them
        from_col = move[0]
        from_row = move[1]
        to_col = move[3]
        to_row = move[4]
        if from_col not in "abcdefgh" or from_row not in "12345678" \
                or to_col not in "abcdefgh" or to_row not in "12345678":
            raise RuntimeError("Invalid input format")
        # return the column letters, and the rows as integers
        return from_col, int(from_row), to_col, int(to_row)


if __name__ == "__main__":
    game = Game("testgame.txt")
    game.play()
