"""Cut false starts and retakes out of a recording, splicing what remains.

A recording is rarely one clean pass. It opens with a slate or a fumbled
first attempt, and somewhere in the middle comes "...let me take that
again". Shipping either is unprofessional, and cutting them by hand with
ad-hoc ffmpeg breaks the rule that the same script plus the same audio
reproduces the same mp4.

Usage:
    python build/retake.py audio/CH01-raw.words.json \\
        --audio audio/CH01-raw.m4a --out CH01-data-representation \\
        --drop "now hexadecimal is based 16"="retakes slide 7"

Each --drop removes everything from the first word of the opening phrase
through the last word of the closing phrase, inclusive, in both the audio
and the transcript. The closing phrase is looked for after the opening one,
so a retake can quote the attempt it replaces. Drops must not overlap, and
a phrase that matches poorly fails loudly rather than cutting blind.

The cut lands in the silence between words rather than on a word boundary,
so the splice does not clip speech. Timestamps after a drop are rebased, so
the output is an ordinary recording plus words.json that the rest of the
pipeline reads without knowing anything was removed.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MIN_SCORE = 0.6


class RetakeError(Exception):
    pass


def normalize(word):
    return re.sub(r"[^a-z0-9]", "", word.lower())


def find_phrase(words, phrase, search_from=0):
    """Best word-overlap match for `phrase`. Returns (score, start, length)."""
    target = [normalize(w) for w in phrase.split() if normalize(w)]
    if not target:
        raise RetakeError("empty anchor phrase")
    best_score, best_index = 0.0, None
    for i in range(search_from, max(search_from, len(words) - len(target) + 1)):
        window = words[i:i + len(target)]
        hits = sum(1 for a, b in zip(target, window)
                   if a == normalize(b["word"]))
        score = hits / len(target)
        if score > best_score:
            best_score, best_index = score, i
    return best_score, best_index, len(target)


def resolve(words, drops):
    """Turn anchor pairs into inclusive word-index spans, left to right."""
    spans = []
    cursor = 0
    for opening, closing in drops:
        score, start, _ = find_phrase(words, opening, cursor)
        if start is None or score < MIN_SCORE:
            raise RetakeError(
                f"opening anchor matched poorly (best {score:.2f}): "
                f"{opening!r}. Quote it from the transcript.")
        score2, end_start, end_len = find_phrase(words, closing, start + 1)
        if end_start is None or score2 < MIN_SCORE:
            raise RetakeError(
                f"closing anchor matched poorly (best {score2:.2f}): "
                f"{closing!r}. Quote it from the transcript.")
        end = end_start + end_len - 1
        if end < start:
            raise RetakeError(f"{closing!r} resolves before {opening!r}")
        spans.append((start, end))
        print(f"  drop words {start}-{end} "
              f"({words[start]['start']:.2f}s to {words[end]['end']:.2f}s, "
              f"{words[end]['end'] - words[start]['start']:.1f}s) "
              f"opening {score:.0%}, closing {score2:.0%}")
        cursor = end + 1
    return spans


def cut_times(words, spans, duration):
    """Where to cut, in seconds: midway through the surrounding silence."""
    cuts = []
    for start, end in spans:
        before = words[start - 1]["end"] if start else 0.0
        after = words[end + 1]["start"] if end + 1 < len(words) else duration
        cuts.append(((before + words[start]["start"]) / 2,
                     (words[end]["end"] + after) / 2))
    return cuts


def keep_spans(cuts, duration):
    keeps, position = [], 0.0
    for cut_from, cut_to in cuts:
        if cut_from > position:
            keeps.append((position, cut_from))
        position = cut_to
    if position < duration:
        keeps.append((position, duration))
    return keeps


def splice(audio, keeps, out_audio, work):
    """Extract each kept span and concatenate them into one recording."""
    work.mkdir(parents=True, exist_ok=True)
    parts = []
    for i, (start, end) in enumerate(keeps):
        part = work / f"keep{i:02d}.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}",
             "-to", f"{end:.3f}", "-i", str(audio),
             "-ar", "48000", "-ac", "2", str(part)], check=True)
        parts.append(part)
    listing = work / "parts.txt"
    listing.write_text("".join(f"file '{p.name}'\n" for p in parts))
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(listing), "-c:a", "aac", "-b:a", "128k", str(out_audio)],
        check=True, cwd=work)
    for part in parts:
        part.unlink()
    listing.unlink()


def rebase(words, cuts):
    """Drop the cut words and shift what follows back by what was removed."""
    kept, removed, index = [], 0.0, 0
    for cut_from, cut_to in cuts:
        gap = cut_to - cut_from
        while index < len(words) and words[index]["start"] < cut_from:
            w = words[index]
            kept.append({"word": w["word"],
                         "start": round(w["start"] - removed, 3),
                         "end": round(w["end"] - removed, 3)})
            index += 1
        while index < len(words) and words[index]["start"] < cut_to:
            index += 1          # inside the drop
        removed += gap
    for w in words[index:]:
        kept.append({"word": w["word"],
                     "start": round(w["start"] - removed, 3),
                     "end": round(w["end"] - removed, 3)})
    return kept, removed


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("words", type=Path, help="the recording's words.json")
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--out", required=True,
                        help="output stem, written into --out-dir")
    parser.add_argument("--drop", action="append", required=True,
                        metavar="OPENING=CLOSING",
                        help="remove from OPENING through CLOSING, inclusive")
    parser.add_argument("--out-dir", type=Path, default=REPO_ROOT / "audio")
    args = parser.parse_args()

    drops = []
    for raw in args.drop:
        opening, sep, closing = raw.partition("=")
        if not sep:
            sys.exit(f"--drop needs OPENING=CLOSING, got {raw!r}")
        drops.append((opening.strip(), closing.strip()))

    data = json.loads(args.words.read_text())
    words, duration = data["words"], data["duration"]

    try:
        spans = resolve(words, drops)
    except RetakeError as e:
        sys.exit(f"retake failed: {e}")

    cuts = cut_times(words, spans, duration)
    keeps = keep_spans(cuts, duration)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_audio = args.out_dir / f"{args.out}.m4a"
    splice(args.audio, keeps, out_audio,
           REPO_ROOT / "media" / "retake_work")

    kept, removed = rebase(words, cuts)
    out_words = args.out_dir / f"{args.out}.words.json"
    out_words.write_text(json.dumps(
        {"duration": round(duration - removed, 3), "words": kept},
        indent=2) + "\n")
    print(f"-> {out_audio}  ({duration - removed:.1f}s, {len(kept)} words; "
          f"removed {removed:.1f}s and {len(words) - len(kept)} words)")


if __name__ == "__main__":
    main()
