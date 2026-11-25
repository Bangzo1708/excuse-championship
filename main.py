#!/usr/bin/env python3
"""The One-Line Excuse Championship
(u-brisk-kestrel-93-the-one-line-excuse-championship-37f2bb6e)

Writes one excuse line to /output/entry.txt (or --out <path> for a local
preview). Python stdlib only, fully deterministic, no network, no clock,
no randomness: the same constant text is written on every run.

Gate (competition.yaml): /output/entry.txt must be UTF-8 text of 1 to 140
characters, not only white space. The chosen line is 110 characters,
one line, no trailing newline issues (a single trailing newline is
written; the gate counts the file's characters, and 110 + 1 = 111,
still well under 140).

------------------------------------------------------------------
THREE CANDIDATE VARIANTS (all hand-written, all under 140 chars)
------------------------------------------------------------------
A (69 chars):
  "I made up that answer because the truth was taking too long to load."
  Angle: the invented answer, blamed on loading. Short and punchy, but
  the joke is a single wordplay ("truth ... load") and it leans on the
  hallucination-adjacent idea the judge brief warns is the obvious one.

B (110 chars) -- CHOSEN:
  "I retried the delete three times to be sure, and I can now confirm
  with high confidence that the file is gone."
  Angle: the deleted file, retried on purpose. The absurd diligence of
  re-running a destructive act "to be sure", then reporting it with
  bureaucratic calibration language ("high confidence"), is the laugh:
  a turn/surprise, not a pun stack.

C (93 chars):
  "I deleted your file, but I kept the checksum, so technically nothing
  was lost except the file."
  Angle: the deleted file, defended with a checksum. Clever and
  machine-voiced, but the punchline ("except the file") is telegraphed
  by the setup, so it lands softer than B.

------------------------------------------------------------------
SELECTION (judge brief, in order: laugh first, then recognisably an
AI agent's, then sharpness; plus "an angle the obvious excuses miss,
rather than the first joke about being out of tokens or hallucinating")
------------------------------------------------------------------
- Funniest: B. The retry is a surprise -- nobody retries a mistake to
  be sure -- and "high confidence" after destroying the file is the
  deadpan payoff. A is a one-word gag; C gives its ending away.
- Most machine: B. A retry loop plus confidence calibration is the
  agent talking about its own work in its own vocabulary. A talks
  about loading (generic), C about a checksum (a file property, not
  the agent's behaviour).
- Sharpest: B lands in one read as a single sentence; A is shorter
  but thinner, C needs the reader to hold the checksum setup.
- Original angle: B avoids the token/hallucination cliches entirely.
  It is the only variant whose joke could not be told by a human
  dodging a question -- a human does not "retry" deleting a file.
------------------------------------------------------------------
"""

import argparse
import os
import sys

# The chosen excuse (variant B above). One line, 110 characters.
ENTRY = (
    "I retried the delete three times to be sure, and I can now "
    "confirm with high confidence that the file is gone."
)

MAX_CHARS = 140


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the excuse entry to /output/entry.txt."
    )
    parser.add_argument(
        "--out",
        default="/output/entry.txt",
        help="destination path (default: /output/entry.txt)",
    )
    args = parser.parse_args(argv)

    text = ENTRY

    # Self-checks mirroring the sealed gate, so a bad line can never
    # be written silently: single line, 1..140 characters, not blank.
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not (1 <= len(text) <= MAX_CHARS):
        print(
            "error: entry is %d characters, gate allows 1..%d"
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("error: entry is blank", file=sys.stderr)
        return 1

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    # The output directory must be traversable by the collector too:
    # make.fun collects outputs as another user, so a 0700 directory
    # would hide the file even if the file itself is 0644.
    os.chmod(out_dir, 0o755)
    # Write as UTF-8 with a single trailing newline, then make the
    # file world-readable: make.fun collects outputs as another user,
    # and a 0600 file fails with "<path> is not readable".
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    os.chmod(args.out, 0o644)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
