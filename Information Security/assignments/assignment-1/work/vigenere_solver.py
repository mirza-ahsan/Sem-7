import argparse
import sys


def decrypt(filepath: str, keyword: str) -> str:
    ciphertext = ""
    plaintext = ""

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("DISPATCH="):
                plaintext += line
                continue
            ciphertext += line

    index = 0

    for char in ciphertext:
        if char.isascii() and char.isalpha():
            char_val = ord(char.upper()) - ord("A")
            key_val = ord(keyword[index]) - ord("A")
            plain_val = (char_val - key_val) % 26
            plaintext += chr(plain_val + ord("A"))
            index = (index + 1) % len(keyword)
        else:
            plaintext += char

    return plaintext


def main() -> None:
    parser = argparse.ArgumentParser(description="Vigenere Cipher Decryptor")
    parser.add_argument("--input", help="Path to the ciphertext file")
    parser.add_argument("--keyword", help="Keyword to decrypt the vigenere cipher")

    args = parser.parse_args()
    filepath = args.input
    keyword = args.keyword

    if filepath is None:
        print("Error: No input file entered")
        sys.exit(1)

    if keyword is None:
        print("Error: No keyword entered")
        sys.exit(1)

    elif not (keyword.isascii() and keyword.isalpha()):
        print("Error: Keyword must contain only alphabets A-Z")
        sys.exit(1)

    try:
        plaintext = decrypt(filepath, keyword.upper())
    except (ValueError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(plaintext)


if __name__ == "__main__":
    main()
