# Communication conventions
Alphabet replacement means one fixed shuffled A-Z substitution; spaces and punctuation remain.
Vigenere uses uppercase ASCII A-Z, A=0..Z=25, C=(P+K) mod 26. Preserve nonletters and advance the key only on A-Z.
Standard rail means the whole character sequence after CRLF/CR line endings are normalised to LF; start at the top rail moving down in a zigzag. Search depths 2 through 8.
A-P byte encoding maps each nibble 0..15 to A..P, high nibble first. It is encoding, not encryption.
