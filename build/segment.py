"""Split one long recording into per-video segments, transcript included.

A 55-minute lecture becomes several videos, but transcribing it once and
cutting afterwards is much cheaper than transcribing each part — and it
keeps every segment on one consistent set of word timestamps.

Usage:
    python build/segment.py audio/CS01-number-systems.words.json \\
        --audio scratchpad/master.wav \\
        --cut CS01-number-systems-p1 \\
        --cut CS01-number-systems-p2="long binary sequences are easy" \\
        --cut CS01-number-systems-p3="now we are going to add binary numbers"

A --cut without a phrase starts at 0; every other one starts at the phrase
given, located in the transcript by best word overlap. For each segment this
writes audio/<name>.m4a and audio/<name>.words.json with timestamps rebased
to that segment's start, which is exactly what build/render.py expects to
find beside a recording.

A phrase that matches poorly fails loudly with its score rather than
silently cutting in the wrong place.

Recordings normally open with a slate ("starting in one, two, three") and
close with several seconds of room noise after the last word. Giving the
first --cut an anchor drops the slate, and --pad sets how much breathing
room to keep at the two outer ends of the recording:

    python build/segment.py audio/P2-five-patterns-raw.words.json \\
        --audio audio/P2-five-patterns-raw.m4a \\
        --cut P2-five-patterns="suppose a variable called count" --pad 0.5

--pad trims silence at both ends of every segment, so a segment that runs
up to the next anchor does not carry the pause before it. Interior anchors
still place the boundaries; padding never grows one into its neighbour.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Below this word-overlap score the anchor phrase probably isn't really
# there, and cutting on it would put the wrong narration under the scene.
MIN_SCORE = 0.6


class SegmentError(Exception):
    pass


def normalize(word):
    return re.sub(r"[^a-z0-9]", "", word.lower())


def find_phrase(words, phrase, search_from=0):
    """Best word-overlap match for `phrase`. Returns (score, word index)."""
    target = [normalize(w) for w in phrase.split() if normalize(w)]
    if not target:
        raise SegmentError("empty anchor phrase")
    best_score, best_index = 0.0, None
    for i in range(search_from, max(search_from, len(words) - len(target) + 1)):
        window = words[i:i + len(target)]
        hits = sum(1 for a, b in zip(target, window)
                   if a == normalize(b["word"]))
        score = hits / len(target)
        if score > best_score:
            best_score, best_index = score, i
    return best_score, best_index


def cut_points(words, cuts):
    """Resolve each anchor phrase to a transcript index, left to right."""
    points = []
    search_from = 0
    for name, phrase in cuts:
        if phrase is None:
            points.append((name, 0))
            continue
        score, index = find_phrase(words, phrase, search_from)
        if index is None or score < MIN_SCORE:
            raise SegmentError(
                f"anchor for '{name}' matched poorly (best score "
                f"{score:.2f} < {MIN_SCORE}): {phrase!r}. The recording may "
                "word this differently — quote it from the transcript."
            )
        print(f"  {name}: anchor matched {score:.0%} at word {index} "
              f"({words[index]['start']:.2f}s)")
        points.append((name, index))
        search_from = index + 1
    return points


def write_segment(name, words, start, end, audio, out_dir):
    slice_words = [w for w in words if start <= w["start"] < end]
    if not slice_words:
        raise SegmentError(f"segment '{name}' contains no words")
    rebased = [
        {"word": w["word"],
         "start": round(w["start"] - start, 3),
         "end": round(w["end"] - start, 3)}
        for w in slice_words
    ]
    duration = round(end - start, 3)
    out_audio = out_dir / f"{name}.m4a"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}",
         "-to", f"{end:.3f}", "-i", str(audio),
         "-c:a", "aac", "-b:a", "128k", str(out_audio)],
        check=True,
    )
    out_words = out_dir / f"{name}.words.json"
    out_words.write_text(json.dumps(
        {"duration": duration, "words": rebased}, indent=2) + "\n")
    print(f"-> {out_audio}  ({duration:.1f}s, {len(rebased)} words)")
    return out_audio


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("words", type=Path, help="full-recording words.json")
    parser.add_argument("--audio", type=Path, required=True,
                        help="the matching full-length recording")
    parser.add_argument("--cut", action="append", required=True,
                        metavar="NAME[=PHRASE]",
                        help="segment name, optionally =anchor phrase")
    parser.add_argument("--out-dir", type=Path,
                        default=REPO_ROOT / "audio")
    parser.add_argument("--pad", type=float, default=None, metavar="SECONDS",
                        help="trim the recording's outer ends, keeping this "
                             "much breathing room before the first word and "
                             "after the last; without it the segments span "
                             "the whole file as recorded")
    args = parser.parse_args()

    cuts = []
    for raw in args.cut:
        name, sep, phrase = raw.partition("=")
        cuts.append((name.strip(), phrase.strip() if sep else None))

    data = json.loads(args.words.read_text())
    words = data["words"]
    duration = data["duration"]

    try:
        points = cut_points(words, cuts)
    except SegmentError as e:
        sys.exit(f"segment failed: {e}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    # --pad trims silence at both ends of *every* segment, not just the
    # recording's: a segment that runs to the next anchor carries whatever
    # pause came before that anchor, which is dead air on the end of an
    # otherwise finished video. Without --pad the segments span the file
    # exactly as they always have.
    for i, (name, index) in enumerate(points):
        next_index = points[i + 1][1] if i + 1 < len(points) else None
        if args.pad is None:
            start = 0.0 if i == 0 else words[index]["start"]
            end = words[next_index]["start"] if next_index else duration
        else:
            last = (next_index - 1) if next_index else len(words) - 1
            start = max(0.0, words[index]["start"] - args.pad)
            end = min(duration, words[last]["end"] + args.pad)
            # Never let a padded end run into the next segment's padded start.
            if next_index is not None:
                end = min(end, words[next_index]["start"] - args.pad)
        try:
            write_segment(name, words, start, end, args.audio, args.out_dir)
        except SegmentError as e:
            sys.exit(f"segment failed: {e}")


if __name__ == "__main__":
    main()
