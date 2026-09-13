import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    PageBreak,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#334155"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(
                40, 755, "CS3002: Information Security — Operation Lost Drive Investigation Report"
            )
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 40, 755, "Roll No: 23L-0515 | Version 1")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(40, 747, letter[0] - 40, 747)

        # Running Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 30, "CONFIDENTIAL INVESTIGATION ARCHIVE — NORTHBRIDGE CIVIC RESEARCH")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 30, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(40, 42, letter[0] - 40, 42)

        self.restoreState()


def build_pdf(filename: str):
    # Printable area: 8.5 x 11 inches -> 612 x 792 pt.
    # Margins: 38 pt horizontal, 46 pt top, 44 pt bottom. Usable width: 536 pt. Usable height: 702 pt.
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=44,
        bottomMargin=44,
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1E3A8A")    # Deep Navy
    secondary_color = colors.HexColor("#0D9488")  # Teal
    accent_color = colors.HexColor("#B45309")     # Amber/Bronze
    dark_slate = colors.HexColor("#0F172A")       # Very Dark Slate
    body_color = colors.HexColor("#1E293B")       # Slate Charcoal

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=primary_color,
        spaceAfter=4,
    )

    meta_header_style = ParagraphStyle(
        "MetaHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=12,
        textColor=dark_slate,
    )

    meta_style = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14.5,
        textColor=primary_color,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12.5,
        textColor=secondary_color,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.2,
        textColor=body_color,
        spaceAfter=3,
    )

    bullet_style = ParagraphStyle(
        "BulletDark",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2,
    )

    code_style = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A"),
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE SUMMARY, TOKEN TABLE, EVIDENCE TRAIL
    # =========================================================================
    story.append(Paragraph("OPERATION LOST DRIVE: DIGITAL FORENSICS INVESTIGATION", title_style))

    meta_table_data = [
        [
            Paragraph("<b>Course:</b> CS3002 Information Security", meta_header_style),
            Paragraph("<b>Roll Number:</b> 23L-0515", meta_header_style),
            Paragraph("<b>Assignment:</b> Project 1 (v1)", meta_header_style),
            Paragraph("<b>Date:</b> September 13, 2026", meta_header_style),
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[140, 130, 126, 140])
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                ("PADDING", (0, 0), (-1, -1), 4),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("EXECUTIVE SUMMARY", h1_style))
    summary_text = (
        "During an IT migration at Northbridge Civic Research, disaster-recovery records, routine operations logs, "
        "and failed transmission dumps became intermingled across an unmanaged workstation drive. As lead forensic "
        "investigator, I systematically reconstructed the genuine recovery procedure without relying on mutable filesystem "
        "timestamps or brute-forcing unbounded spaces. By cross-referencing internal UTC+05:00 logs, communication conventions, "
        "and message references, I implemented four Python solvers to break each classical encryption stage: "
        "Monoalphabetic Substitution, Vigenère Polyalphabetic, Rail Fence Transposition, and One-Time Pad XOR decryption. "
        "All four authorization tokens (ALPHA, BETA, GAMMA, FINAL), the full 96-byte OTP key, and the confidential payload "
        "were recovered with complete mathematical and cryptographic integrity."
    )
    story.append(Paragraph(summary_text, body_style))

    # Token Summary Table
    token_table_data = [
        [
            Paragraph("<b>Cipher Scheme / Stage</b>", meta_header_style),
            Paragraph("<b>Source Artifact Path</b>", meta_header_style),
            Paragraph("<b>Recovered Token & Case Identifier</b>", meta_header_style),
        ],
        [
            Paragraph("<b>Stage 1:</b> Monoalphabetic Substitution", meta_style),
            Paragraph("<code>Messages/recovery_message.txt</code>", code_style),
            Paragraph("<code>ALPHA=OLD-ALPHA-7E0A0EA897E6D2961BCC</code>", code_style),
        ],
        [
            Paragraph("<b>Stage 2:</b> Vigenère Polyalphabetic", meta_style),
            Paragraph("<code>Messages/project_dispatch.txt</code>", code_style),
            Paragraph("<code>BETA=OLD-BETA-101C35084262110E5936</code>", code_style),
        ],
        [
            Paragraph("<b>Stage 3:</b> Rail Fence Transposition", meta_style),
            Paragraph("<code>Archive/rail_payload.txt</code>", code_style),
            Paragraph("<code>GAMMA=OLD-GAMMA-2B00CC8F23A35118E57E</code>", code_style),
        ],
        [
            Paragraph("<b>Stage 4:</b> One-Time Pad (XOR Stream)", meta_style),
            Paragraph("<code>Archive/final_cipher.hex</code>", code_style),
            Paragraph("<code>FINAL=OLD-FINAL-E6BA000431D515D9AAA7</code> (Case: <b>8A2D446073</b>)", code_style),
        ],
    ]
    t_tokens = Table(token_table_data, colWidths=[130, 160, 246])
    t_tokens.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 3.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ]
        )
    )
    story.append(t_tokens)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. CHRONOLOGICAL EVIDENCE DISCOVERY & CORRELATION", h1_style))
    story.append(
        Paragraph(
            "The investigation followed a 24-step verifiable trail logged in <code>evidence_log.csv</code>, using internal "
            "timestamps and explicit records as authoritative evidence while discarding external filesystem metadata.",
            body_style,
        )
    )

    trail_points = [
        "<b>Directive & Lead:</b> <code>START_HERE.txt</code> ordered inspection of handover material and correlation of the successful transfer immediately preceding documented maintenance.",
        "<b>Handover Note:</b> Inez Ward's memo (<code>Documents/handover_note.txt</code>) established that recovery messages utilized 'alphabet replacement' (monoalphabetic substitution) and fixed our temporal boundary at the 2026-04-11 maintenance shutdown.",
        "<b>Maintenance Cutoff:</b> <code>Logs/maintenance.log</code> established that system maintenance began precisely at <code>2026-04-11 22:00:00</code>.",
        "<b>Transfer Log Triage:</b> Evaluating <code>Logs/transfers.csv</code> identified three candidates: <code>TX-OLD</code> at 20:10:00 (too early; superseded), <code>TX-LATE</code> at 22:04:00 (after maintenance cutoff; status <code>ABORTED</code>), and <b><code>TX-814D</code> at 21:43:00</b> (successfully finished 17 minutes before maintenance, transferring message reference <code>MSG-88D4FA</code>).",
        "<b>File Reference Resolution:</b> <code>Messages/message_index.csv</code> confirmed reference <code>MSG-88D4FA</code> corresponded directly to <code>Messages/recovery_message.txt</code>.",
        "<b>Cryptographic Conventions & Cribs:</b> <code>Documents/communication_conventions.md</code> documented single-alphabet substitution preserving punctuation, A–P nibble encoding (two characters per byte, high nibble first, A=0..P=15), and CRLF/CR normalization for Rail Fence. <code>Documents/crib_sheet.txt</code> provided two guaranteed anchors: opening word <code>RECOVERY</code> and trailing label <code>PROJECT</code>.",
    ]
    for pt in trail_points:
        story.append(Paragraph(f"• {pt}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: STAGE 1, STAGE 2, STAGE 3, AND STAGE 4 CRYPTANALYSIS
    # =========================================================================
    story.append(Paragraph("2. STAGE 1: MONOALPHABETIC SUBSTITUTION ANALYSIS (mono_solver.py)", h1_style))
    s2_desc = (
        "<code>Messages/recovery_message.txt</code> contains 1,220 letters. Unigram frequency analysis identified that "
        "cipher character <b>R</b> occurred 200 times (16.39%), closely matching English <b>E</b> (~12.7%). "
        "Matching the opening ciphertext word <code>URTOERUM</code> against Crib 1 (<code>RECOVERY</code>) yielded six mappings: "
        "<code>U=R, R=E, T=C, O=O, E=V, M=Y</code>. In the concluding record, matching <code>IUOHRTS=TRPNU</code> against Crib 2 "
        "(<code>PROJECT=CEDAR</code>) confirmed <code>I=P, H=J, S=T, P=D, N=A, U=R</code>, unlocking the project name <b>CEDAR</b>.<br/>"
        "<b>Solver Implementation & Bijective Mapping:</b> <code>mono_solver.py</code> accepts <code>--input</code> and an external "
        "<code>--mapping</code> file, validating against duplicate keys or values to enforce a strict permutation over &Sigma;<sub>26</sub>. "
        "By analyzing high-frequency digraphs and common roots (<i>THE, INVESTIGATOR, NOTES, CONFIDENTIAL</i>), 25 letter pairs were deduced. "
        "The sole remaining pair, <code>X=Z</code>, completed the 26-letter bijection (saved in <code>mapping.txt</code>).<br/>"
        "• <b>Token Alpha:</b> <code>TOKENAP=EPEMEECNEBEMFAEIEBCNDHEFDAEBDAEFEBDIDJDHEFDGEEDCDJDGDBECEDED</code> &rarr; "
        "<code>OLD-ALPHA-7E0A0EA897E6D2961BCC</code><br/>"
        "• <b>Component Alpha:</b> <code>MCDLJODAOOLDHCBCBEABFPFBOAGPGPPLCKODJCAFJCNJDJHHHGENDKDICLEIKIOK</code> (32 bytes)<br/>"
        "• <b>Next Stage Clue:</b> <code>PROJECT=CEDAR EVENT=RENAME. CONFIRM THE HISTORICAL PROJECT RECORD BEFORE SELECTING A DISPATCH.</code>"
    )
    story.append(Paragraph(s2_desc, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. STAGE 2: VIGENÈRE CIPHER ANALYSIS (vigenere_solver.py)", h1_style))
    s3_desc = (
        "<b>Historical Project Triage:</b> Clue 1 instructed verification of historical project records. "
        "<code>Documents/project_history.csv</code> (event <code>REN-44</code>) confirmed Project <b>CEDAR</b> was renamed to "
        "<b>JUNIPER</b> on <code>2026-04-12 09:00:00</code>. Because our recovery message was transmitted on April 11, the active project "
        "was strictly <b>CEDAR</b>. In <code>Messages/dispatch_index.json</code>, entry <code>DSP-A88CCD</code> (dated April 11) linked CEDAR "
        "to <code>Messages/project_dispatch.txt</code> with keyword <b>TUNDRA</b>.<br/>"
        "<b>Solver Logic & Header Preservation:</b> <code>vigenere_solver.py</code> implements modular subtraction "
        "<i>P<sub>i</sub> = (C<sub>i</sub> - K<sub>i mod m</sub>) mod 26</i>. Critically, <code>project_dispatch.txt</code> begins with "
        "an unencrypted header (<code>DISPATCH=DSP-A88CCD</code>). Decrypting it would burn 15 keyword cycles and desynchronize subsequent text. "
        "The solver preserves <code>DISPATCH=</code> headers intact and advances key indices strictly on alphabetic characters.<br/>"
        "• <b>Plaintext:</b> <code>RECOVERY DISPATCH FOR CEDAR... THE EXPERIMENTAL RAIL CHANNEL USED TRANSFER BATCH-6F34...</code><br/>"
        "• <b>Token Beta:</b> <code>TOKENAP=EPEMEECNECEFFEEBCNDBDADBEDDDDFDADIDEDCDGDCDBDBDAEFDFDJDDDG</code> &rarr; "
        "<code>OLD-BETA-101C35084262110E5936</code><br/>"
        "• <b>Component Beta:</b> <code>INBDCJFOIKNCCFBHEMFDPCOPKMEIKMNLAGGGDNCHDKBKMBJMAJGKHMDIOMGHPJPM</code> (32 bytes)<br/>"
        "• <b>Next Stage Clue:</b> <code>THE EXPERIMENTAL RAIL CHANNEL USED TRANSFER BATCH-6F34. RESOLVE THAT BATCH IN THE CHANNEL RECORD.</code>"
    )
    story.append(Paragraph(s3_desc, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. STAGE 3: RAIL FENCE TRANSPOSITION ANALYSIS (rail_solver.py)", h1_style))
    s4_desc = (
        "<b>Channel Log Correlation:</b> In <code>Logs/channel_tests.log</code>, <code>BATCH-6F34</code> mapped to "
        "<code>Archive/rail_payload.txt</code> with transmission mode <code>STANDARD_ZIGZAG</code> at <b>depth 4</b>.<br/>"
        "<b>Transposition Solver & Normalization Trap:</b> <code>rail_solver.py</code> evaluates candidate depths 2 through 8. "
        "An off-by-one trap was discovered: on Linux, reading <code>rail_payload.txt</code> with a trailing newline (<code>\\n</code>) "
        "yielded 246 characters instead of 245, disrupting matrix alignment. Stripping trailing whitespace (<code>.rstrip('\\r\\n')</code>) "
        "restored the true 245-character block. Depths 2, 3, 5, 6, 7, and 8 generated scrambled anagrams; depth 4 yielded fluent English:<br/>"
        "• <b>Plaintext:</b> <code>RECOVERY CHANNEL RESULT... COMBINE ALPHA THEN BETA THEN GAMMA UNDER THE ARCHIVE RECOVERY CONVENTION.</code><br/>"
        "• <b>Token Gamma:</b> <code>TOKENAP=EPEMEECNEHEBENENEBCNDCECDADAEDEDDIEGDCDDEBDDDFDBDBDIEFDFDHEF</code> &rarr; "
        "<code>OLD-GAMMA-2B00CC8F23A35118E57E</code><br/>"
        "• <b>Component Gamma:</b> <code>EFPJBNAENHLPPAENIEAHFICGGKNGJHEMOOBIABHFGFDCCHNCLIOGKNCMHCLMHLOL</code> (32 bytes)"
    )
    story.append(Paragraph(s4_desc, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5. STAGE 4: ONE-TIME PAD / XOR STREAM DECRYPTION (otp_solver.py)", h1_style))
    s5_desc = (
        "<b>Assembly Protocol:</b> Per <code>Archive/recovery_convention.txt</code>, sensitive components were decoded from A–P strings "
        "into binary bytes (two letters per byte: <i>high &times; 16 + low</i>, where A=0..P=15). Each 64-character component decoded to "
        "32 bytes (64 / 2 = 32). The components were concatenated in order: <code>Master Key = Alpha (32B) + Beta (32B) + Gamma (32B) = 96 Bytes</code>.<br/>"
        "<b>Ciphertext Decryption:</b> <code>Archive/final_cipher.hex</code> contained 192 hex digits, parsing to exactly 96 ciphertext bytes. "
        "<code>otp_solver.py</code> validates input characters (A–P only, even length) and performs bitwise XOR (<i>P<sub>i</sub> = C<sub>i</sub> &oplus; K<sub>i</sub></i>), "
        "decoding directly to clean UTF-8 plaintext without padding errors:<br/>"
        "• <b>Decrypted String:</b> <code>CONFIDENTIAL: fictional recovery confirmed. CASE=8A2D446073 TOKEN=OLD-FINAL-E6BA000431D515D9AAA7</code><br/>"
        "• <b>Case Identifier:</b> <code>8A2D446073</code> | <b>Final Token:</b> <code>OLD-FINAL-E6BA000431D515D9AAA7</code>"
    )
    story.append(Paragraph(s5_desc, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: REJECTED ALTERNATIVES & CONCEPTUAL REFLECTIONS (PART 1)
    # =========================================================================
    story.append(Paragraph("6. IN-DEPTH ANALYSIS OF REJECTED ALTERNATIVES", h1_style))
    story.append(
        Paragraph(
            "Forensic integrity demands comprehensive justification for why plausible competing leads were evaluated and rejected:",
            body_style,
        )
    )

    alt_table_data = [
        [
            Paragraph("<b>Candidate Lead</b>", meta_header_style),
            Paragraph("<b>Source Artifact</b>", meta_header_style),
            Paragraph("<b>Investigative Context & Reason for Rejection</b>", meta_header_style),
        ],
        [
            Paragraph("<b>TX-LATE</b>", meta_style),
            Paragraph("<code>Logs/transfers.csv</code>", code_style),
            Paragraph(
                "Logged at <code>2026-04-11 22:04:00</code> with status <code>ABORTED</code>. Initiated 4 minutes after the "
                "22:00:00 maintenance cutoff. System logs confirm network termination occurred mid-handshake; no valid payload was transmitted.",
                body_style,
            ),
        ],
        [
            Paragraph("<b>DSP-CURRENT</b><br/>(Project JUNIPER)", meta_style),
            Paragraph("<code>Messages/dispatch_index.json</code><br/><code>Messages/current_dispatch.txt</code>", code_style),
            Paragraph(
                "Dated <code>2026-04-13</code> under project <code>JUNIPER</code>. Historical record <code>REN-44</code> confirmed CEDAR was renamed "
                "to JUNIPER on April 12. Since recovery communication occurred on April 11, JUNIPER was chronologically invalid. Manual inspection "
                "confirmed <code>current_dispatch.txt</code> was a post-rename operational memo lacking recovery tokens.",
                body_style,
            ),
        ],
        [
            Paragraph("<b>BATCH-DEMO</b>", meta_style),
            Paragraph("<code>Logs/channel_tests.log</code><br/><code>Archive/demo_channel.txt</code>", code_style),
            Paragraph(
                "Transmitted <code>2026-04-11 15:30:00</code>. Log metadata confirmed this was a diagnostic telemetry test. "
                "Inspection of <code>demo_channel.txt</code> revealed generic demo text containing no A–P keying components.",
                body_style,
            ),
        ],
        [
            Paragraph("<b>BATCH-ABORT</b>", meta_style),
            Paragraph("<code>Logs/channel_tests.log</code><br/><code>Archive/aborted.txt</code>", code_style),
            Paragraph(
                "Logged at <code>2026-04-11 17:45:00</code> with status <code>CHANNEL_FAILURE</code> due to severe parity check errors. "
                "The payload was unfinalized, corrupt, and truncated before session termination.",
                body_style,
            ),
        ],
    ]
    t_alt = Table(alt_table_data, colWidths=[110, 140, 286])
    t_alt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 3),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ]
        )
    )
    story.append(t_alt)
    story.append(Spacer(1, 4))

    story.append(Paragraph("7. CONCEPTUAL SECURITY REFLECTIONS (PART 1)", h1_style))

    story.append(Paragraph("1. Why do language natural frequencies defeat monoalphabetic substitution?", h2_style))
    r1_text = (
        "Monoalphabetic substitution is a one-to-one bijection over the alphabet (&Sigma; &rarr; &Sigma;). While it masks letter identities, "
        "it preserves the probability distribution of the plaintext language entirely intact. In English, unigram frequencies are heavily skewed: "
        "'E' occurs ~12.7%, 'T' ~9.1%, 'A' ~8.2%, while 'Z', 'Q', and 'X' occur &lt; 0.2%. Furthermore, digraph frequencies (such as 'TH', 'HE', 'IN') "
        "and morphological word structures remain invariant. An analyst constructs a frequency histogram of ciphertext letters, correlates peaks with "
        "natural language baselines, and applies known cribs to systematically unravel the mapping. This reduces a theoretical keyspace of "
        "26! (&approx; 4 &times; 10<sup>26</sup>) to trivial manual or heuristic resolution without brute-force search."
    )
    story.append(Paragraph(r1_text, body_style))

    story.append(Paragraph("2. Why does the Rail Fence cipher preserve character counts?", h2_style))
    r2_text = (
        "Rail Fence is a pure transposition (permutation) cipher. Unlike substitution systems, it performs zero symbol replacements; "
        "rather, it applies a positional permutation &pi; to character coordinates: <i>C<sub>&pi;(i)</sub> = P<sub>i</sub></i>. "
        "Because characters are simply routed along diagonal zigzag rails without modification, the multiset of characters in the ciphertext "
        "is strictly identical to that of the plaintext: <i>Count(c, C) = Count(c, P)</i> for all symbols <i>c</i>. The unigram frequency "
        "histogram of the ciphertext matches natural language perfectly, immediately signaling to a cryptanalyst that transposition—not "
        "substitution—was employed."
    )
    story.append(Paragraph(r2_text, body_style))

    story.append(Paragraph("3. What does One-Time Pad key reuse reveal, and what does it NOT automatically reveal?", h2_style))
    r3_text = (
        "When an OTP keystream <i>K</i> is reused across two messages (<i>C<sub>1</sub> = P<sub>1</sub> &oplus; K</i> and "
        "<i>C<sub>2</sub> = P<sub>2</sub> &oplus; K</i>), calculating <i>C<sub>1</sub> &oplus; C<sub>2</sub> = (P<sub>1</sub> &oplus; K) &oplus; (P<sub>2</sub> &oplus; K) = P<sub>1</sub> &oplus; P<sub>2</sub></i> "
        "completely strips the key.<br/>"
        "<b>What it reveals:</b> The mutual XOR difference of the plaintexts. In ASCII natural language, spaces (0x20) XORed with letters toggle "
        "case. Using <i>crib-dragging</i> (sliding probable words across <i>P<sub>1</sub> &oplus; P<sub>2</sub></i>), legible text appears in the "
        "counterpart stream, allowing both plaintexts to be recovered simultaneously.<br/>"
        "<b>What it does NOT automatically reveal:</b> It does not directly output plaintext in isolation without statistical or linguistic analysis. "
        "If one message is high-entropy pseudorandom data (e.g., compressed or pre-encrypted), <i>P<sub>1</sub> &oplus; P<sub>2</sub></i> remains "
        "statistically uniform, preventing crib-dragging. Furthermore, it never reveals the key itself unless one plaintext is fully reconstructed."
    )
    story.append(Paragraph(r3_text, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: REFLECTIONS (PART 2), SOLVER CLI COMMANDS, INTEGRITY & CONCLUSION
    # =========================================================================
    story.append(Paragraph("7. CONCEPTUAL SECURITY REFLECTIONS (PART 2)", h1_style))

    story.append(Paragraph("4. Why is single DES obsolete?", h2_style))
    r4_text = (
        "The Data Encryption Standard (DES), standardized in 1977, is cryptographically obsolete due to its short 56-bit effective key length "
        "(2<sup>56</sup> &approx; 7.2 &times; 10<sup>16</sup> keys). In 1998, the Electronic Frontier Foundation (EFF) built 'Deep Crack' "
        "for under $250,000, which brute-forced a DES key in 56 hours. Modern GPU clusters and cloud compute can exhaust the entire keyspace "
        "in minutes. In addition, DES's 64-bit block size introduces severe vulnerability under the birthday bound: after encrypting 2<sup>32</sup> "
        "blocks (~32 GB) under the same key in CBC mode, block collision attacks (such as Sweet32) leak plaintext. Single DES lacks the key size "
        "and block width required for modern security."
    )
    story.append(Paragraph(r4_text, body_style))

    story.append(Paragraph("5. How do Shannon's confusion and diffusion support modern design, and why is transposition not strong diffusion?", h2_style))
    r5_text = (
        "Claude Shannon established two criteria for secure symmetric ciphers: <b>Confusion</b> (obscuring the complex relationship "
        "between the key and ciphertext, realized via non-linear Substitution Boxes or S-boxes) and <b>Diffusion</b> (spreading the statistical "
        "influence of an individual plaintext or key bit across many ciphertext bits). Modern block ciphers like AES achieve strong diffusion "
        "through iterative rounds combining non-linear S-boxes (SubBytes), cyclic row permutations (ShiftRows), and linear finite field mixing (MixColumns). "
        "Flipping a single plaintext bit triggers an <b>avalanche effect</b>, altering ~50% of the ciphertext bits within two rounds.<br/>"
        "In contrast, Rail Fence merely rearranges character indices. Flipping one plaintext bit alters exactly one ciphertext bit at a deterministic "
        "spatial offset. It provides zero bit-level dispersion, zero non-linearity, and no avalanche effect, completely failing as a modern diffusion mechanism."
    )
    story.append(Paragraph(r5_text, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("8. SOLVER COMMAND-LINE INVOCATION REFERENCE", h1_style))
    cli_commands = (
        "<code># Stage 1: Monoalphabetic Substitution Solver</code><br/>"
        "python mono_solver.py --input Messages/recovery_message.txt --mapping mapping.txt<br/>"
        "<code># Stage 2: Vigenère Polyalphabetic Cipher Solver</code><br/>"
        "python vigenere_solver.py --input Messages/project_dispatch.txt --keyword TUNDRA<br/>"
        "<code># Stage 3: Rail Fence Transposition Solver (evaluates depths 2 to 8)</code><br/>"
        "python rail_solver.py --input Archive/rail_payload.txt<br/>"
        "<code># Stage 4: One-Time Pad / XOR Decryptor (concatenates 3 A-P components into 96B key)</code><br/>"
        "python otp_solver.py --ciphertext Archive/final_cipher.hex --alpha MCDLJODAOOLDHCBCBEABFPFBOAGPGPPLCKODJCAFJCNJDJHHHGENDKDICLEIKIOK "
        "--beta INBDCJFOIKNCCFBHEMFDPCOPKMEIKMNLAGGGDNCHDKBKMBJMAJGKHMDIOMGHPJPM "
        "--gamma EFPJBNAENHLPPAENIEAHFICGGKNGJHEMOOBIABHFGFDCCHNCLIOGKNCMHCLMHLOL"
    )
    t_cli = Table([[Paragraph(cli_commands, code_style)]], colWidths=[536])
    t_cli.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_cli)
    story.append(Spacer(1, 4))

    story.append(Paragraph("9. ACADEMIC INTEGRITY & METHODOLOGICAL CONCLUSION", h1_style))
    conclusion_text = (
        "<b>Assistance Disclosure:</b> In accordance with course integrity policy, AI assistance (Google DeepMind Antigravity) "
        "was utilized during solver development for syntactic code validation, CLI argument parsing structures, and formatting verification. "
        "All investigative hypotheses, evidence correlations, frequency deductions, mathematical verifications, and report analyses were "
        "conducted, verified, and directed independently by the student.<br/>"
        "<b>Conclusion:</b> Operation Lost Drive successfully demonstrated the practical limitations of classical encryption systems: "
        "frequency analysis dismantled monoalphabetic substitution, chronological correlation bypassed polyalphabetic key ambiguity, "
        "rail fence transposition failed to hide letter distributions, and key combination enabled exact OTP decryption. "
        "All four flags were authenticated against project specifications."
    )
    story.append(Paragraph(conclusion_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename} with clean 4-page structure.")


if __name__ == "__main__":
    build_pdf("submission/report.pdf")
    build_pdf("work/report.pdf")
