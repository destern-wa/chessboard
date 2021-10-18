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
    print("- Moves can entered in the following formats")
    print("   - The from and to squares separated by a space, e.g. \"f3 d4\"")
    print("   - The from and to squares separated by an 'x', e.g. \"f3xd4\" (optional; indicates taking a piece)")
    print("   - Either of the above prefixed by the piece being moved, e.g. \"Nf3xd4\" (optional)")
    print("- Invalid moves will be rejected")
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

