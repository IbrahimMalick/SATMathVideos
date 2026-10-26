"""Emit YouTube chapter timestamps from a scene's beat timings.

    python build/chapters.py concept.data_transmission

Chapters are named in CHAPTERS below, one entry per scene: a list of
(beat name, chapter title). The times come from timings/<scene>.json, never
from scrubbing the video — the beats are already anchored to the words, so
a chapter opens exactly where the narration turns.

The format is the one YouTube accepts, and the rules it enforces are
checked rather than assumed: the first entry is 00:00, entries ascend, and
no chapter is shorter than ten seconds. A list that breaks one of those is
silently ignored by YouTube, which looks like the feature not working.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MIN_CHAPTER = 10.0   # YouTube drops the whole list if any chapter is shorter

CHAPTERS = {
    "concept.data_transmission": [
        ("open", "Data transmission: the questions this chapter answers"),
        ("part1", "Packets: header, payload, trailer"),
        ("exam_point", "The exam point: what belongs in the header"),
        ("switching", "Packet switching, step by step"),
        ("ps_sequence", "The five-step sequence to write"),
        ("ps_why", "Why packet switching helps, and what it does not promise"),
        ("part2", "Serial and parallel transmission"),
        ("skew", "Skew: the argument against parallel"),
        ("recommend", "Recommending a method in a scenario"),
        ("direction", "Simplex, half-duplex and full-duplex"),
        ("memory", "The memory check, and the trap"),
        ("part3", "USB: a serial interface"),
        ("usb_benefits", "USB benefits and limitations"),
        ("part4", "Why transmission errors happen"),
        ("parity", "Parity checks, worked through"),
        ("parity_limit", "Where parity fails"),
        ("block", "Parity block check: locating the bit"),
        ("four", "Checksum, echo check and check digit"),
        ("part5", "Automatic repeat request"),
        ("arq_why", "Why the timeout matters"),
        ("part6", "Encryption: plaintext, ciphertext, key"),
        ("sym", "Symmetric encryption"),
        ("asym", "Asymmetric encryption"),
        ("hybrid", "Hybrid encryption"),
        ("review", "The chapter in eight lines"),
        ("practise", "How to practise, and your next step"),
    ],
}


def stamp(seconds):
    total = int(seconds)
    if total >= 3600:
        return f"{total // 3600}:{total // 60 % 60:02d}:{total % 60:02d}"
    return f"{total // 60:02d}:{total % 60:02d}"


def build(scene_id):
    path = REPO_ROOT / "timings" / f"{scene_id}.json"
    if not path.exists():
        sys.exit(f"No timing file at {path}")
    timing = json.loads(path.read_text())
    starts = {b["name"]: b["start"] for b in timing["beats"]}

    named = CHAPTERS.get(scene_id)
    if not named:
        sys.exit(f"No chapter list for {scene_id}; add one to CHAPTERS.")

    rows = []
    for beat, title in named:
        if beat not in starts:
            sys.exit(f"Chapter '{title}' names beat {beat!r}, which is not "
                     f"in {path.name}.")
        rows.append([starts[beat], title])

    # The first chapter has to start at zero whatever its beat says, so the
    # opening belongs to it rather than to nothing.
    rows[0][0] = 0.0

    for (start, title), (nxt, _) in zip(rows, rows[1:]):
        if nxt <= start:
            sys.exit(f"Chapters are out of order at {title!r}.")
        if nxt - start < MIN_CHAPTER:
            sys.exit(f"Chapter {title!r} is only {nxt - start:.1f}s long; "
                     f"YouTube needs {MIN_CHAPTER:.0f}s or it ignores the "
                     "whole list.")
    if timing["duration"] - rows[-1][0] < MIN_CHAPTER:
        sys.exit(f"The last chapter {rows[-1][1]!r} is shorter than "
                 f"{MIN_CHAPTER:.0f}s.")

    lines = ["TIMESTAMPS:"]
    lines += [f"{stamp(start)} - {title}" for start, title in rows]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python build/chapters.py <scene id>")
    print(build(sys.argv[1]))
