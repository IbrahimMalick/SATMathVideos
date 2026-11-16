"""Re-transcribe the stretches where the transcriber got stuck in a loop.

    python build/repair_loops.py audio/OS-CH01-operating-system.words.json \\
        --audio audio/OS-CH01-operating-system.m4a --language ur

Whisper sometimes locks onto one word and repeats it for as long as the
speech lasts. On a 21-minute Urdu lecture it did this five times and ate
65 seconds of real speech between them.

A loop is worse than a dropped stretch, and much worse than silence. It
fills the gap with plausible-looking words at plausible-looking
timestamps, so build/mkbeats.py will happily place an anchor inside one
and report a good score for it. The reveal then lands on speech that was
never said, and nothing downstream can tell. This is the pipeline's
worst failure mode: it fails by appearing to succeed.

What fixes it is context. The loop builds up over a long pass; handed
twenty seconds on its own the same model transcribes the same audio
cleanly. So each damaged stretch is cut out with padding, transcribed by
itself, and spliced back over the words it replaces.

Only words whose midpoint falls inside the damaged span are taken from
the replacement. The padding is there to give the model a running start,
not to be used: the words either side of the span are already good and
taking them again would duplicate them.

If a replacement loops in its turn, this says so and leaves that stretch
alone rather than writing one loop over another.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from build.transcribe import transcribe  # noqa: E402


def find_loops(words, min_run, max_period=6, min_reps=3):
    """Spans where the transcriber repeated itself.

    A loop is not always one word over and over. Whisper locks onto a
    phrase just as readily -- "راءعور کی طرف" forty times, "افس کیا ہوتے"
    thirty -- and a detector that only counts single-word runs walks
    straight past those, reports the transcript clean, and lets an anchor
    be placed inside one. So this looks for any period up to
    ``max_period`` repeating at least ``min_reps`` times.

    It also flags a single token longer than 30 characters. That is not a
    word in any script; it is the decoder stuttering inside one token.
    """
    loops, index = [], 0
    while index < len(words):
        if len(words[index]["word"]) > 30:
            loops.append({
                "start": words[index]["start"],
                "end": words[index]["end"],
                "count": 1,
                "word": words[index]["word"][:12] + "...",
            })
            index += 1
            continue

        best = None
        for period in range(1, max_period + 1):
            if index + period * 2 > len(words):
                break
            unit = [w["word"] for w in words[index:index + period]]
            reps, at = 1, index + period
            while (at + period <= len(words)
                   and [w["word"] for w in words[at:at + period]] == unit):
                reps += 1
                at += period
            spanned = reps * period
            if reps >= min_reps and spanned >= min_run:
                if best is None or spanned > best[0]:
                    best = (spanned, reps, period, at)
        if best is None:
            index += 1
            continue

        spanned, reps, period, at = best
        loops.append({
            "start": words[index]["start"],
            "end": words[at - 1]["end"],
            "count": reps,
            "word": " ".join(w["word"] for w in words[index:index + period]),
        })
        index = at
    return loops


def longest_run(words):
    best, run = 0, 0
    previous = None
    for word in words:
        run = run + 1 if word["word"] == previous else 1
        previous = word["word"]
        best = max(best, run)
    return best


def clip(audio, start, end, into):
    subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
         "-i", str(audio), "-ar", "16000", "-ac", "1", str(into), "-y"],
        check=True,
    )


def repair(words, audio, loops, pad, language, model, min_run):
    """Return a new word list with each loop replaced, and a report."""
    patches, report = [], []
    with tempfile.TemporaryDirectory() as scratch:
        piece = Path(scratch) / "piece.wav"
        for loop in loops:
            lo = max(0.0, loop["start"] - pad)
            hi = loop["end"] + pad
            clip(audio, lo, hi, piece)
            fresh = transcribe(str(piece), model_size=model, language=language)
            moved = [{**w, "start": w["start"] + lo, "end": w["end"] + lo}
                     for w in fresh["words"]]
            inside = [w for w in moved
                      if loop["start"] <= (w["start"] + w["end"]) / 2
                      <= loop["end"]]

            if not inside:
                report.append((loop, "nothing came back", 0))
                continue
            if find_loops(inside, min_run):
                report.append((loop, "the replacement loops too", len(inside)))
                continue
            patches.append((loop, inside))
            report.append((loop, "replaced", len(inside)))

    if not patches:
        return words, report

    out, cursor = [], 0
    for loop, inside in patches:
        while cursor < len(words) and words[cursor]["start"] < loop["start"]:
            out.append(words[cursor])
            cursor += 1
        out.extend(inside)
        while cursor < len(words) and words[cursor]["start"] <= loop["end"]:
            cursor += 1          # drop the loop
    out.extend(words[cursor:])
    return out, report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("words", help="output of build/transcribe.py")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--language", default=None)
    parser.add_argument("--model", default="large-v3",
                        help="a short clip can afford the big model")
    parser.add_argument("--min-run", type=int, default=6,
                        help="words a repetition must span to count")
    parser.add_argument("--max-period", type=int, default=6,
                        help="longest repeating phrase to look for")
    parser.add_argument("--min-reps", type=int, default=3,
                        help="times a phrase must repeat to count")
    parser.add_argument("--pad", type=float, default=4.0,
                        help="seconds of run-up given to the model, and "
                             "then discarded")
    parser.add_argument("-o", "--output", default=None)
    args = parser.parse_args()

    path = Path(args.words)
    data = json.loads(path.read_text())
    words = data["words"]

    loops = find_loops(words, args.min_run, args.max_period,
                       args.min_reps)
    if not loops:
        print("No loops found; nothing to repair.")
        return

    damaged = sum(loop["end"] - loop["start"] for loop in loops)
    print(f"{len(loops)} loop(s), {damaged:.0f}s of "
          f"{data['duration']:.0f}s ({100 * damaged / data['duration']:.1f}%)")

    fixed, report = repair(words, Path(args.audio), loops, args.pad,
                           args.language, args.model, args.min_run)
    for loop, outcome, count in report:
        print(f"  {loop['start']:7.1f} -> {loop['end']:7.1f}  "
              f"{loop['count']:4d} x {loop['word']!r}  ->  {outcome}"
              + (f", {count} words" if count else ""))

    data["words"] = fixed
    data["repaired"] = [
        {"start": loop["start"], "end": loop["end"], "outcome": outcome}
        for loop, outcome, _ in report
    ]
    out = Path(args.output) if args.output else path
    out.write_text(json.dumps(data))
    still = find_loops(fixed, args.min_run, args.max_period,
                       args.min_reps)
    print(f"-> {out}  {len(fixed)} words, {len(still)} loop(s) remaining")


if __name__ == "__main__":
    main()
