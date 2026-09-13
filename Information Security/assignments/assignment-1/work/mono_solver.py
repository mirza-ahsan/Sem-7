import argparse
import string
import sys


def load_mapping(mapping: str) -> dict[str, str]:
    keys = []
    values = []
    with open(mapping, "r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            if not line.strip():
                continue

            parts = line.strip().split("=")
            if len(parts) != 2:
                raise ValueError(f"Mapping line {line_no} must be in the format CIPHER=PLAIN")

            key = parts[0].strip().upper()
            value = parts[1].strip().upper()

            if len(key) != 1 or key not in string.ascii_uppercase:
                raise ValueError(f"Mapping line {line_no} has an invalid cipher letter, it must be one letter A-Z")
            if len(value) != 1 or value not in string.ascii_uppercase:
                raise ValueError(f"Mapping line {line_no} has an invalid plain letter, it must be one letter A-Z")

            keys.append(key)
            values.append(value)

    if len(keys) == 0:
        raise ValueError("Mapping file is empty")

    if len(keys) == len(set(keys)) and len(values) == len(set(values)):
        return dict(zip(keys, values))

    else:
        raise ValueError("Assigning multiple ciphertext characters to same plaintext or vice versa")


def freq_analysis(filepath: str) -> tuple[dict[str, tuple[int, float]], int]:
    freq_dict = {}
    for letter in string.ascii_uppercase:
        freq_dict[letter] = 0

    total = 0
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith(("REFERENCE=", "CIPHERTEXT:")):
                continue
            for char in line:
                if char.isascii() and char.isalpha():
                    total += 1
                    freq_dict[char.upper()] += 1

    if total == 0:
        raise ValueError("Ciphertext does not contain any letters A-Z")

    for k, v in freq_dict.items():
        freq_dict[k] = (v, v * 100 / total)

    return freq_dict, total


def decrypt(filepath: str, mapping: dict) -> str:
    plaintext = ""

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith(("REFERENCE=", "CIPHERTEXT:")):
                plaintext += line
                continue
            for char in line:
                if char.isascii() and char.isalpha() and char.upper() in mapping:
                    plaintext += mapping[char.upper()]
                elif char.isascii() and char.isalpha() and char.upper() not in mapping:
                    plaintext += "_"
                else:
                    plaintext += char

    return plaintext


def main() -> None:
    parser = argparse.ArgumentParser(description="Monoalphabetic Decryptor")
    parser.add_argument("--input", required=True, help="Path to the ciphertext file")
    parser.add_argument(
        "--mapping",
        default=None,
        help="Path to the mapping txt file with ciphertext to plaintext translations",
    )

    args = parser.parse_args()
    filepath = args.input

    mapping = None
    if args.mapping is not None:
        try:
            mapping = load_mapping(args.mapping)
        except (ValueError, OSError) as e:
            print(f"Error: {e}")
            sys.exit(1)

    try:
        freq_dict, total = freq_analysis(filepath)
    except (ValueError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    freq_list = sorted(freq_dict.items(), key=lambda freq: freq[1], reverse=True)

    print(f"Total letters: {total}")
    for k, (count, pct) in freq_list:
        print(f"{k} : {count:3d} ({pct:5.2f}%)")

    if mapping is not None:
        plaintext = decrypt(filepath, mapping)
        print()
        print(plaintext)


if __name__ == "__main__":
    main()
