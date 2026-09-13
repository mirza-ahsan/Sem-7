import argparse
import sys


def normalise(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()

    text = text.removesuffix("\n")
    return text


def decrypt(ciphertext: str) -> None:
    for depth in range(2, 9):
        rows = depth
        cols = len(ciphertext)

        grid = [[None for _ in range(cols)] for _ in range(rows)]
        rail = 0
        direction = 1

        for col in range(cols):
            grid[rail][col] = "*"

            if rail == depth - 1:
                direction = -1

            if rail == 0 and col > 0:
                direction = 1

            rail += direction

        char_index = 0
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "*":
                    grid[row][col] = ciphertext[char_index]
                    char_index += 1

        plaintext = ""
        rail = 0
        direction = 1

        for col in range(cols):
            if grid[rail][col] is not None:
                plaintext += grid[rail][col]

            if rail == depth - 1:
                direction = -1

            if rail == 0 and col > 0:
                direction = 1

            rail += direction

        print(f"Depth: {depth}\n{plaintext}\n\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Railfence Cipher Decryptor")
    parser.add_argument("--input", required=True, help="Path to the ciphertext file")

    args = parser.parse_args()
    filepath = args.input

    try:
        ciphertext = normalise(filepath)
    except (ValueError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    if len(ciphertext) == 0:
        print("Error: Ciphertext file is empty")
        sys.exit(1)

    decrypt(ciphertext)


if __name__ == "__main__":
    main()
