from game import Game

default_filename = "chessgame.txt"


def print_instructions():
    print("Instructions")
    print("============")
    print("- Pieces on the board are represented by letters:")
    print("   P, p - Pawn   (White, Black)")
    print("   R, r - Rook   (White, Black)")
    print("   N, n - Knight (White, Black)")
    print("   B, b - Bishop (White, Black)")
    print("   Q, q - Queen  (White, Black)")
    print("   K, k - King   (White, Black)")
    print("- Moves must be entered as a \"from square\" and a \"to square\", separated by a space")
    print("   - For example, \"f3 d4\"")
    print("   - Except castling: enter \"O-O\" for kingside, or \"O-O-O\" fro queenside")
    print("   - The \"to square\" may indicate the piece being moved, e.g. \"f3 Nd4\" (optional)")
    print("   - The \"to square\" may also indicate a capture with an 'x', e.g. \"f3 Nxd4\" (optional)")
    print("   - The \"to square\" may indicate a check by adding a '+', e.g. \"f3 d4+\" (optional)")
    print("- Moves are validated in the following ways:")
    print("   - You can only move piece of your own colour")
    print("   - You can only take pieces of your opponent's colour")
    print("   - The piece must be able to move that way, for example bishops can only move diagonally")
    print("- Some aspects are not currently validated or implemented:")
    print("   - If pieces between a \"from square\" and \"to square\" would block a move")
    print("   - When a king has been checked or checkmated, including when pieces are pinned and cannot be moved")
    print("   - Promotion of pawns to other pieces when they reach the end of the board")
    print("   - You can only move piece of your own colour")
    print("- Type \"exit\" or \"quit\" instead of a move to exit the game. The state is saved to file you selected \
when starting the game, so you can continue playing later.")


def main():
    print("Welcome to Chess")
    print("================")
    while True:
        print("\nSelect an option:")
        print("[I]nstructions")
        print("[N]ew game")
        print("[L]oad game from file")
        print("[Q]uit")
        response = input("> ").upper()
        if response == 'I':
            print_instructions()
        elif response == 'N' or response == 'L':
            action = 'save' if response == 'N' else 'load'
            filename = input(f"File to {action} game? [or push enter for default: {default_filename}]\n > ").strip()
            game = Game(filename or default_filename, response == 'L')
            game.play()
        elif response == "Q":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == '__main__':
    main()

