"""Align a narration script against a transcript; resolve beat markers to timestamps.

Usage:
    python build/sync.py scripts/L03-vertex-form.md audio/L03-vertex-form.words.json

Reads the script's beat markers ([[beat:name]]), aligns the marker-free script
text against the recording's word timestamps (Needleman-Wunsch, so ad-libs,
skipped words, and transcription errors are tolerated), and resolves each
marker to the start time of the spoken word that follows it. Writes
timings/<scene>.json.

Every marker must resolve. If the words around a marker can't be found in the
recording, this fails loudly with the marker name — it never defaults.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MARKER_RE = re.compile(r"\[\[beat:([A-Za-z0-9_-]+)\]\]")

# A marker resolves to the first *aligned* script word within this many words
# after it. Beyond that, the recording has drifted too far from the script to
# trust the timestamp.
LOOKAHEAD = 5

MATCH, MISMATCH, GAP = 2, -1, -1


class SyncError(Exception):
    pass


def parse_script(path):
    """Return (scene_id, tokens) where tokens are ("word", text) / ("beat", name)."""
    text = Path(path).read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        raise SyncError(f"{path} has no frontmatter; expected 'scene: ...' between --- lines.")
    scene_id = None
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        if key.strip() == "scene":
            scene_id = value.strip()
    if not scene_id:
        raise SyncError(f"{path} frontmatter has no 'scene:' key.")

    body = text[m.end():]
    tokens = []
    pos = 0
    for marker in MARKER_RE.finditer(body):
        for word in body[pos:marker.start()].split():
            tokens.append(("word", word))
        tokens.append(("beat", marker.group(1)))
        pos = marker.end()
    for word in body[pos:].split():
        tokens.append(("word", word))
    return scene_id, tokens


def normalize(word):
    return re.sub(r"[^a-z0-9]", "", word.lower())


def align(script_words, transcript_words):
    """Needleman-Wunsch. Returns script-index -> transcript-index (or None)."""
    a = [normalize(w) for w in script_words]
    b = [normalize(w) for w in transcript_words]
    n, m = len(a), len(b)

    score = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = i * GAP
    for j in range(1, m + 1):
        score[0][j] = j * GAP
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = score[i - 1][j - 1] + (MATCH if a[i - 1] == b[j - 1] else MISMATCH)
            score[i][j] = max(diag, score[i - 1][j] + GAP, score[i][j - 1] + GAP)

    mapping = {}
    i, j = n, m
    while i > 0 and j > 0:
        diag = score[i - 1][j - 1] + (MATCH if a[i - 1] == b[j - 1] else MISMATCH)
        if score[i][j] == diag:
            if a[i - 1] == b[j - 1]:
                mapping[i - 1] = j - 1  # only exact matches anchor timestamps
            i, j = i - 1, j - 1
        elif score[i][j] == score[i - 1][j] + GAP:
            i -= 1
        else:
            j -= 1
    return mapping


def resolve_beats(tokens, words, duration):
    """Return the beats list for timing.json."""
    script_words = [t[1] for t in tokens if t[0] == "word"]
    transcript_words = [w["word"] for w in words]
    mapping = align(script_words, transcript_words)

    beats = []
    word_index = 0
    for kind, value in tokens:
        if kind == "word":
            word_index += 1
            continue
        # Marker sits before script word `word_index`; anchor on the first
        # aligned word at or after it.
        start = None
        for i in range(word_index, min(word_index + LOOKAHEAD, len(script_words))):
            if i in mapping:
                start = words[mapping[i]]["start"]
                break
        if start is None:
            context = " ".join(script_words[word_index:word_index + LOOKAHEAD])
            raise SyncError(
                f"Beat marker '{value}' did not resolve: none of the script words "
                f"following it ({context!r}) were found in the recording."
            )
        beats.append({"name": value, "start": round(start, 3)})

    names = [b["name"] for b in beats]
    if len(set(names)) != len(names):
        raise SyncError(f"Duplicate beat names in script: {names}")
    for prev, cur in zip(beats, beats[1:]):
        if cur["start"] < prev["start"]:
            raise SyncError(
                f"Beat '{cur['name']}' resolved to {cur['start']}s, before "
                f"'{prev['name']}' at {prev['start']}s. The alignment is not "
                "trustworthy — check the recording against the script."
            )
    for beat, nxt in zip(beats, beats[1:]):
        beat["end"] = nxt["start"]
    if beats:
        beats[-1]["end"] = round(duration, 3)
    return beats


def sync(script_path, words_path, output=None):
    scene_id, tokens = parse_script(script_path)
    transcript = json.loads(Path(words_path).read_text())
    beats = resolve_beats(tokens, transcript["words"], transcript["duration"])
    timing = {
        "scene": scene_id,
        "duration": transcript["duration"],
        "beats": beats,
    }
    out = Path(output) if output else REPO_ROOT / "timings" / f"{scene_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(timing, indent=2) + "\n")
    return out, timing


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("script", type=Path)
    parser.add_argument("words", type=Path, help="output of build/transcribe.py")
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()
    try:
        out, timing = sync(args.script, args.words, args.output)
    except SyncError as e:
        sys.exit(f"sync failed: {e}")
    for b in timing["beats"]:
        print(f"  {b['name']:<12} {b['start']:7.2f} -> {b['end']:7.2f}")
    print(f"-> {out}")


if __name__ == "__main__":
    main()
