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
    "cs.ap_csa_strategy": [
        ("open", "Which exam you are actually preparing for"),
        ("exam", "The format: two sections, 42 questions, four FRQs"),
        ("quickref", "The Java Quick Reference, and your pacing"),
        ("units", "The four units"),
        ("weighting", "Where the marks are, unit by unit"),
        ("changed", "What the revision added: data, ethics, text files"),
        ("inheritance", "What is out, and what is still in"),
        ("trace", "Multiple choice: trace the code"),
        ("watch", "Where the marks are lost"),
        ("frq_spec", "Free response: the prompt is a checklist"),
        ("four_frq", "The four free-response focuses"),
        ("practice", "Building a practice routine"),
        ("recap", "Recap: your exam strategy"),
    ],
    "concept.cpu_cycle": [
        ("open", "The question: how a program becomes actions"),
        ("stored", "The stored-program idea, and the Von Neumann model"),
        ("inside", "Inside the processor: the CU, the ALU, the registers"),
        ("four_regs", "The four registers: PC, MAR, MDR, CIR"),
        ("mix_up", "MAR against MDR: the two that get mixed up"),
        ("follow", "The fetch stage, traced through the diagram"),
        ("once_more", "The fetch stage in five steps"),
        ("cir_holds", "Decode: the operation and the operand address"),
        ("two_accesses", "Two separate trips to memory"),
        ("example", "One instruction, with real values"),
        ("buses", "What the address, data and control buses carry"),
        ("as_level", "AS Level: the accumulator, index and status registers"),
        ("rtn", "Register-transfer notation, one step at a time"),
        ("challenge", "Your turn: predict the accumulator"),
        ("mistakes", "Three mistakes to avoid"),
        ("recap", "The whole cycle, once"),
    ],
    "concept.g9_model_paper": [
        ("open", "Grade 9 Mathematics 2026: model paper, Chapters 1 to 4"),
        ("mcq1", "MCQ: conjugates, and why the answer is rational"),
        ("mcq2", "MCQ: the base of a common logarithm"),
        ("mcq3", "MCQ: the power set of the empty set"),
        ("mcq4", "MCQ: finding an intersection from a union"),
        ("mcq5", "MCQ: the LCM of algebraic terms"),
        ("mcq6", "MCQ: taking out a common factor"),
        ("sq1", "Short: two rational numbers between 2 and 3"),
        ("sq2", "Short: negative and fractional indices"),
        ("sq3", "Short: solving a logarithmic equation"),
        ("sq4", "Short: the characteristic of a small decimal"),
        ("sq5", "Short: writing out a power set"),
        ("sq6", "Short: defining the difference of two sets"),
        ("sq7", "Short: factorizing a quadratic by splitting"),
        ("sq8", "Short: the difference of two cubes"),
        ("lq1", "Question 5(a): simplifying with fractional indices"),
        ("lq2", "Question 5(b): finding x from its logarithm"),
        ("lq3", "Question 6(a): overlapping sets at the sports club"),
        ("lq4", "Question 6(b): factorizing a quartic expression"),
        ("recap", "Recap, and what to do before the next video"),
    ],
    "concept.matrices": [
        ("title", "Matrices are not just a table of numbers"),
        ("students_come", "A cricket tournament: three students, two samosas each"),
        ("not_only", "Teachers and players too, and they need different things"),
        ("calc_students", "Counting the samosas group by group"),
        ("more_items", "Water and bananas: one table for every need"),
        ("matrix_named", "This table is a matrix"),
        ("vector", "The column vector: how many people in each group"),
        ("how", "Multiplying the matrix by the vector"),
        ("output", "The shopping list that comes out"),
        ("order", "Why the order of the columns matters"),
        ("function", "A matrix as a function: inputs to outputs"),
        ("scaling", "Scaling: double the people, double the order"),
        ("additivity", "Additivity: two groups, two routes, one answer"),
        ("linear", "Scaling plus additivity is a linear function"),
        ("geometry", "Matrices in geometry: stretch and rotate"),
        ("not_just", "What to remember next time you see a matrix"),
    ],
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
