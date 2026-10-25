"""Write a beat-marked script from a transcript, placing markers by anchor phrase.

The script body has to be the transcript verbatim for sync.py's aligner to
match it exactly, so the only real work is deciding where each
``[[beat:name]]`` marker goes. Counting word indices by hand over three
thousand words is where mistakes live: each beat names a phrase it should
land on, and this finds it by best word overlap.

Usage, from a small driver that holds the beat list:

    from build.mkbeats import build

    BEATS = [
        ("hook",  "Suppose a variable called count currently contains"),
        ("rule",  "If there is no assignment there is no change"),
    ]
    build("P2-five-patterns", "concept.five_patterns", BEATS,
          "P2-five-patterns", "one-line note for the script header")

A phrase that matches poorly, or one that resolves out of order, fails
loudly with its score rather than silently marking the wrong word — a
marker in the wrong place is a reveal landing on the wrong sentence, which
is the one thing this pipeline exists to prevent.
"""

import json
import re
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Below this word-overlap score the anchor probably is not really there.
MIN_SCORE = 0.75


class BeatError(Exception):
    pass


def normalize(word):
    return re.sub(r"[^a-z0-9]", "", word.lower())


def find_phrase(words, phrase, search_from=0):
    """Best word-overlap match for `phrase`. Returns (score, index)."""
    target = [normalize(w) for w in phrase.split() if normalize(w)]
    if not target:
        raise BeatError("empty anchor phrase")
    best_score, best_index = 0.0, None
    for i in range(search_from, max(search_from, len(words) - len(target) + 1)):
        window = words[i:i + len(target)]
        hits = sum(1 for a, b in zip(target, window)
                   if a == normalize(b["word"]))
        score = hits / len(target)
        if score > best_score:
            best_score, best_index = score, i
            if score == 1.0:
                break
    return best_score, best_index


def place(words, beats):
    """Resolve each beat to a word index, left to right."""
    marks, cursor, failures = {}, 0, []
    for name, phrase in beats:
        score, index = find_phrase(words, phrase, cursor)
        if index is None or score < MIN_SCORE:
            failures.append(f"  {name}: best {score:.2f} for {phrase!r}")
            continue
        marks[index] = name
        cursor = index + 1
    if failures:
        raise BeatError("anchors that did not match:\n" + "\n".join(failures))
    return marks


def build(audio_stem, scene_id, beats, out_stem, note, audio_dir=None,
          script_dir=None):
    """Write scripts/<out_stem>.md with the markers in place."""
    audio_dir = audio_dir or REPO_ROOT / "audio"
    script_dir = script_dir or REPO_ROOT / "scripts"
    words = json.loads(
        (audio_dir / f"{audio_stem}.words.json").read_text())["words"]
    try:
        marks = place(words, beats)
    except BeatError as e:
        sys.exit(f"mkbeats failed: {e}")

    out = []
    for i, word in enumerate(words):
        if i in marks:
            out.append(f"[[beat:{marks[i]}]]")
        out.append(word["word"])
    document = (f"---\nscene: {scene_id}\n---\n\n<!-- {note} -->\n\n"
                + "\n".join(textwrap.wrap(" ".join(out), 86)) + "\n")
    script_dir.mkdir(parents=True, exist_ok=True)
    (script_dir / f"{out_stem}.md").write_text(document)
    print(f"{out_stem}.md  {len(marks)} beats over {len(words)} words")
    return marks
