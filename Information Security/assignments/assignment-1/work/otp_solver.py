import argparse
import string
import sys


def decode_ap(component: str) -> bytes:
    byte_list = []
    for i in range(0, len(component), 2):
        high = ord(component[i]) - ord("A")
        low = ord(component[i + 1]) - ord("A")
        byte_val = high * 16 + low
        byte_list.append(byte_val)

    return bytes(byte_list)


def decrypt(filepath: str, master_key: bytes) -> None:
    with open(filepath, "r", encoding="utf-8") as file:
        hex_str = "".join(file.read().split())

    if not all(char in string.hexdigits for char in hex_str):
        print("Ciphertext must only have hexadecimal characters 0-9 and A-F")
        sys.exit(1)

    if len(hex_str) % 2 != 0:
        print("Ciphertext must have an even number of hexadecimal digits")
        sys.exit(1)

    cipher_bytes = bytes.fromhex(hex_str)

    if len(master_key) != len(cipher_bytes):
        print("The lengths of the ciphertext and master key do not match")
        sys.exit(1)

    plaintext_bytes = bytes([c ^ k for c, k in zip(cipher_bytes, master_key)])

    try:
        print(plaintext_bytes.decode("utf-8"))
    except UnicodeDecodeError:
        print("Decrypted bytes are not valid UTF-8, check the components and their order")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="One-Time Pad Decryptor")
    parser.add_argument("--ciphertext", required=True, help="Path to the ciphertext file")
    parser.add_argument("--alpha", required=True, help="Your alpha component recovered from monoalphabetic decryption")
    parser.add_argument("--beta", required=True, help="Your beta component recovered from vigenere decryption")
    parser.add_argument("--gamma", required=True, help="Your gamma component recovered from railfence decryption")

    args = parser.parse_args()
    filepath = args.ciphertext
    alpha = args.alpha
    beta = args.beta
    gamma = args.gamma

    for name, comp in [("alpha", alpha), ("beta", beta), ("gamma", gamma)]:
        if len(comp) % 2 != 0:
            print(f"{name} component must have an even length")
            sys.exit(1)
        elif not all("A" <= char <= "P" for char in comp):
            print(f"{name} must only have characters A-P")
            sys.exit(1)

    master_key = decode_ap(alpha) + decode_ap(beta) + decode_ap(gamma)

    try:
        decrypt(filepath, master_key)
    except (ValueError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
