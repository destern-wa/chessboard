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


if __name__ == "__main__":
    game = Game("testgame.txt")
    game.board.move("e", 2, "e", 4)
    game.save_to_file()
    game.board.print()

    game2 = Game("testgame.txt", True)
    game2.board.print()

