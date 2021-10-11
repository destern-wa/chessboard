class GameFile:
    """Handles file operations for loading and saving chess games"""

    def __init__(self, filename):
        self.filename = filename

    def load(self, game):
        """Loads the state of the game from file"

        :param game: Game instance to load data into
        """
        try:
            with open(self.filename, mode='r') as file:
                # First char in the file is the next player
                game.next_player = file.read(1)
                # Each square of each row of the board are the next 64 characters
                for i in range(game.board.size ** 2):
                    square_index = i % game.board.size
                    square_col = chr(square_index + 97)  # chr(97) is 'a'
                    square_row = (i // game.board.size) + 1
                    square_value = file.read(1)
                    game.board.set_square(square_col, square_row, square_value)

        except IOError as err:
            print(f"Error loading file: {err}")

    def save(self, game):
        """Saves the current state of the game to file

        :param game: Game instance to be saved"""
        try:
            with open(self.filename, mode='w+') as file:
                # First char in the file is the next player
                file.write(game.next_player)
                # Then the board as a string of 64 characters
                file.write(str(game.board))

        except IOError as err:
            print(f"Error saving file: {err}")

    def update(self, game, squares):
        """Saves the game's next player and state of specified squares to file using random-access.

        :param game: Game instance to be saved
        :param squares: List of squares, where each square has the column letter at index 0 and
        the row number at index 1. These may be strings like "a8" or tuples like ("h", 1).
        """
        try:
            with open(self.filename, mode='r+') as file:
                # Update the next player
                file.seek(0)
                file.write(game.next_player)
                # Update for each square
                for square in squares:
                    col = square[0]
                    col_index = ord(col.lower()) - 97  # ord('a') is 97
                    row = square[1]
                    row_index = int(row) - 1
                    offset = row_index * 8 + col_index + 1
                    value = game.board.get_square(col, int(row))
                    file.seek(offset)
                    file.write(value)
        except IOError as err:
            print(f"Error saving file with  random-access: {err}")
            # Save the entire state instead
            self.save(game)
