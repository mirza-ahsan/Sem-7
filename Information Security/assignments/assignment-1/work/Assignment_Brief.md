# Operation Lost Drive
Undergraduate Information Security investigation

# Scenario and objectives
Northbridge Civic Research is migrating an old workstation. An employee created a recovery archive, but current records and backups became intermingled. Reconstruct the documented recovery procedure, identify relevant ciphertexts, write small Python solvers, recover three intermediate tokens and one final case token, and support every choice with evidence.

# Scope and tools
Work offline with the supplied TXT, CSV, JSON, LOG, Markdown, and HEX files. Internal timestamps and explicit version records are evidence; extracted filesystem and ZIP timestamps are not. Python 3.11+ and a text editor are enough. Do not brute-force unbounded spaces. No forensic suite, internet service, AES, or DES implementation is required.

# Public conventions
The searchable communication-conventions record defines the classical operations. Sensitive bytes use A-P nibble encoding: A=0 through P=15, two letters per byte, high nibble first. This is encoding, not encryption. Rail processing normalises CRLF and CR line endings to LF, then transposes the entire character sequence. The search range is 2-8.

# Required submission
Submit identity.json; mono_solver.py; vigenere_solver.py; rail_solver.py; otp_solver.py; flags.txt; evidence_log.csv; report.pdf; and README.txt. Solvers must use command-line inputs: mono accepts ciphertext and a derived mapping; Vigenere accepts ciphertext and keyword; rail accepts ciphertext and prints every depth 2-8; OTP accepts ciphertext hex and three A-P components. Do not hardcode only the answer. README lists commands and discloses assistance.

The evidence log columns are stage, source path, record/line reference, observed clue, inference, next action, result. A concise 3-5 page report is enough. Explain at least two plausible alternatives you rejected. Prefer meaningful excerpts to excessive screenshots.

# Rubric (100)
Evidence discovery, correlation, and rejected alternatives 25; monoalphabetic analysis and working solver 20; Vigenere key selection and working solver 15; Rail Fence search and justified recovery 10; OTP reconstruction and working decryption 15; four correct tokens 10 (2 per classical stage, 4 final); short conceptual reflections 5.

# Reflection prompts
Why do language frequencies help against substitution? Why does Rail Fence preserve counts? What does OTP key reuse reveal, and not automatically reveal? Why is single DES obsolete? How do confusion and diffusion support modern design without calling a simple transposition strong diffusion?

# Integrity policy - INSTRUCTOR REVIEW REQUIRED BEFORE RELEASE
Default policy: tools and AI assistance are permitted only when disclosed in README and when the student can explain every submitted inference and script. Generic algorithm discussion may be shared; another student's ciphertexts, evidence references, keys, and flags are not valid for this package. AI-detection claims are never evidence of misconduct. Your instructor must review and may replace this policy.

# Troubleshooting
Start with chronology and identifiers. Make a frequency table before completing a substitution mapping. Preserve punctuation and advance Vigenere keys only on letters. Print all Rail Fence candidates. Verify byte lengths before XOR. If blocked, request a logged rescue clue; partial credit remains available for sound later work.
