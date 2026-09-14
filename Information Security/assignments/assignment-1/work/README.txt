Operation Lost Drive - Submission README

Name: Ahsan Baig
Roll number: 23L-0515
Section: 7C
Course: CS3002 Information Security, Assignment 1
Assignment version: 1
Python version: 3.11 or newer, standard library only


1. Files

identity.json        roll number and assignment version
mono_solver.py       letter frequency table and decryption using a mapping file
vigenere_solver.py   Vigenere decryption using a keyword
rail_solver.py       Rail Fence decryption for every depth from 2 to 8
otp_solver.py        A-P component decoding and XOR of the final ciphertext
mapping.txt          mapping file used by mono_solver.py
flags.txt            the four recovered tokens
evidence_log.csv     evidence log of the investigation
report.pdf           investigation report
README.txt           this file


2. How to run

Run every command from inside the submission folder. The commands expect the
submission folder to be inside the extracted assignment folder, next to the
Messages, Archive, Documents and Logs folders, so every ciphertext path starts
with ../
If the folders are placed differently, only the path given to --input or
--ciphertext needs to change.

A valid run prints the result and exits with status 0. Missing or invalid input
prints an error message and exits with a non-zero status.


2.1 Monoalphabetic solver

python mono_solver.py --input ../Messages/recovery_message.txt --mapping mapping.txt

Prints the A-Z letter frequency table of the ciphertext and then the plaintext.
Without --mapping only the frequency table is printed. The REFERENCE= and
CIPHERTEXT: header lines are not counted in the table and are printed unchanged.

Mapping file format:
- One pair per line in the form CIPHER=PLAIN. For example U=R means ciphertext
  letter U becomes plaintext letter R.
- Each side must be a single letter A-Z. Lowercase letters and spaces around the
  letters are accepted, and blank lines are ignored.
- A partial mapping is allowed. Ciphertext letters without a pair are printed as _
- A mapping that uses the same cipher letter or the same plain letter twice is
  rejected.

Mapping used (same pairs as mapping.txt, one per line in the file):
U=R R=E T=C O=O E=V M=Y I=P H=J S=T P=D F=H Q=I W=N
N=A B=S K=K Z=M D=B L=U Y=F C=G A=L J=W G=Q V=X X=Z


2.2 Vigenere solver

python vigenere_solver.py --input ../Messages/project_dispatch.txt --keyword TUNDRA

The keyword must contain only letters A-Z (lowercase is accepted). Decryption uses
P = (C - K) mod 26 with A=0 to Z=25. The key only advances on letters, and spaces
and punctuation are kept. Lines starting with DISPATCH= are plaintext headers and
are printed unchanged.


2.3 Rail Fence solver

python rail_solver.py --input ../Archive/rail_payload.txt

Prints the candidate plaintext for every depth from 2 to 8, each labelled with its
depth. CRLF and CR line endings are read as LF, and the final newline of the file
is not treated as part of the ciphertext. Depth 4 gives the readable plaintext.


2.4 OTP solver

python otp_solver.py --ciphertext ../Archive/final_cipher.hex --alpha MCDLJODAOOLDHCBCBEABFPFBOAGPGPPLCKODJCAFJCNJDJHHHGENDKDICLEIKIOK --beta INBDCJFOIKNCCFBHEMFDPCOPKMEIKMNLAGGGDNCHDKBKMBJMAJGKHMDIOMGHPJPM --gamma EFPJBNAENHLPPAENIEAHFICGGKNGJHEMOOBIABHFGFDCCHNCLIOGKNCMHCLMHLOL

The three components are the COMPONENTAP values from the monoalphabetic, Vigenere
and Rail Fence plaintexts. Each component must be uppercase A-P with an even
length. Two letters make one byte, high nibble first, with A=0 to P=15. The
decoded components are joined in the order alpha, beta, gamma, and the key must
have the same byte length as the ciphertext (96 bytes) before the XOR. The
ciphertext file must contain only hexadecimal digits with an even count; line
breaks in the file are ignored.


3. Recovered tokens

ALPHA=OLD-ALPHA-7E0A0EA897E6D2961BCC
BETA=OLD-BETA-101C35084262110E5936
GAMMA=OLD-GAMMA-2B00CC8F23A35118E57E
FINAL=OLD-FINAL-E6BA000431D515D9AAA7

Final decrypted message:
CONFIDENTIAL: fictional recovery confirmed. CASE=8A2D446073 TOKEN=OLD-FINAL-E6BA000431D515D9AAA7
