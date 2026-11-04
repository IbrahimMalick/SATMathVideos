"""Transcribe a narration recording to word-level timestamps.

Usage:
    python build/transcribe.py audio/L03-vertex-form.wav
    python build/transcribe.py audio/L03-vertex-form.wav --backend assemblyai

Writes <audio>.words.json next to the recording:

    {"duration": 24.8, "words": [{"word": "Every", "start": 0.12, "end": 0.38}, ...]}

Backends are pluggable. The default is local faster-whisper, so per-lesson
cost is zero at course volume. AssemblyAI is optional and needs
ASSEMBLYAI_API_KEY set.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def audio_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def transcribe_faster_whisper(path, model_size, language=None, vad=True,
                              repetition_penalty=1.0):
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    # condition_on_previous_text=False heads off most of the repetition
    # loops whisper falls into on long, evenly-paced narration, but not all
    # of them: an Urdu lecture here still looped on one word for six
    # seconds and swallowed the sentence underneath it, in two separate
    # runs at the same spot. When that happens the fix is --no-vad with a
    # --repetition-penalty above 1; both together recovered the lost
    # sentence. They are not the default because VAD keeps silence out of
    # the timestamps, and a penalty leans against phrases a teacher really
    # does repeat for emphasis.
    segments, _info = model.transcribe(
        str(path),
        word_timestamps=True,
        temperature=0.0,
        beam_size=5,
        condition_on_previous_text=False,
        repetition_penalty=repetition_penalty,
        vad_filter=vad,
        # Auto-detection reads only the opening seconds. A lecture that
        # greets the class in Urdu and then teaches in English gets tagged
        # Urdu, and the whole transcript comes back in Urdu script — which
        # aligns against nothing. Pin the language for mixed delivery.
        language=language,
    )
    words = []
    for segment in segments:
        for w in segment.words:
            words.append(
                {"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
            )
    return words


def transcribe_assemblyai(path, _model_size, language=None, vad=True,
                          repetition_penalty=1.0):
    import urllib.request

    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        sys.exit("ASSEMBLYAI_API_KEY is not set; use --backend faster-whisper instead.")

    def request(url, data=None, headers=None):
        req = urllib.request.Request(url, data=data, headers=headers or {})
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    upload = request(
        "https://api.assemblyai.com/v2/upload",
        data=Path(path).read_bytes(),
        headers={"authorization": api_key},
    )
    job = request(
        "https://api.assemblyai.com/v2/transcript",
        data=json.dumps({"audio_url": upload["upload_url"]}).encode(),
        headers={"authorization": api_key, "content-type": "application/json"},
    )
    import time

    while True:
        result = request(
            f"https://api.assemblyai.com/v2/transcript/{job['id']}",
            headers={"authorization": api_key},
        )
        if result["status"] == "completed":
            break
        if result["status"] == "error":
            sys.exit(f"AssemblyAI failed: {result.get('error')}")
        time.sleep(3)
    return [
        {"word": w["text"], "start": w["start"] / 1000, "end": w["end"] / 1000}
        for w in result["words"]
    ]


BACKENDS = {
    "faster-whisper": transcribe_faster_whisper,
    "assemblyai": transcribe_assemblyai,
}


def silence_points(path, noise_db=-32, min_silence=0.45):
    """Mid-points of the silences in a recording, in seconds.

    Used to choose chunk boundaries that never fall inside a word.
    """
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-af", f"silencedetect=noise={noise_db}dB:d={min_silence}",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    starts, points = [], []
    for line in out.stderr.splitlines():
        if "silence_start:" in line:
            starts.append(float(line.rsplit("silence_start:", 1)[1].strip()))
        elif "silence_end:" in line and starts:
            end = float(line.rsplit("silence_end:", 1)[1].split("|")[0].strip())
            points.append((starts.pop() + end) / 2)
    return sorted(points)


def chunk_bounds(path, target, duration):
    """Cut points roughly `target` seconds apart, each landing in silence.

    Whisper drifts over a long recording: on a 25-minute lecture here it
    dropped fourteen stretches totalling three minutes, including the
    sentence that gave a question's final answer, while the same audio in
    short clips transcribed cleanly. So the long recording is cut up and
    fed in pieces — and the cuts go in the silences between words, because
    a cut through a word loses it from both sides.
    """
    quiet = silence_points(path)
    bounds, position = [0.0], 0.0
    while duration - position > target * 1.5:
        want = position + target
        nearby = [q for q in quiet if position + target * 0.4 < q < position + target * 1.6]
        position = min(nearby, key=lambda q: abs(q - want)) if nearby else want
        bounds.append(position)
    bounds.append(duration)
    return bounds


def transcribe_chunked(path, backend, model_size, language, vad,
                       repetition_penalty, target):
    """Transcribe a long recording in pieces, with timestamps rebased."""
    import tempfile

    duration = audio_duration(path)
    bounds = chunk_bounds(path, target, duration)
    words = []
    with tempfile.TemporaryDirectory() as work:
        for i, (start, end) in enumerate(zip(bounds, bounds[1:])):
            piece = Path(work) / f"chunk{i:03d}.wav"
            subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}",
                 "-t", f"{end - start:.3f}", "-i", str(path), str(piece)],
                check=True,
            )
            part = BACKENDS[backend](piece, model_size, language, vad,
                                     repetition_penalty)
            for w in part:
                words.append({"word": w["word"],
                              "start": round(w["start"] + start, 3),
                              "end": round(w["end"] + start, 3)})
            print(f"  chunk {i + 1}/{len(bounds) - 1}  "
                  f"{start:7.1f}-{end:7.1f}s  {len(part):4d} words")
    return words


def transcribe(audio_path, backend="faster-whisper", model_size="base",
               language=None, vad=True, repetition_penalty=1.0, chunk=None):
    """Return {"duration": float, "words": [...]} for a recording."""
    if chunk:
        words = transcribe_chunked(audio_path, backend, model_size, language,
                                   vad, repetition_penalty, chunk)
    else:
        words = BACKENDS[backend](audio_path, model_size, language, vad,
                                  repetition_penalty)
    return {"duration": round(audio_duration(audio_path), 3), "words": words}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("audio", type=Path)
    parser.add_argument("--backend", choices=BACKENDS, default="faster-whisper")
    parser.add_argument("--model", default="base", help="faster-whisper model size")
    parser.add_argument("-o", "--output", type=Path, default=None)
    parser.add_argument(
        "--language", default=None,
        help="ISO code to pin (e.g. en). Leave unset to auto-detect; pin it "
             "when the delivery mixes languages.",
    )
    parser.add_argument(
        "--no-vad", dest="vad", action="store_false",
        help="turn off voice-activity filtering. Reach for this when the "
             "transcript shows one word repeated many times over: VAD is "
             "usually part of what triggers the loop.",
    )
    parser.add_argument(
        "--repetition-penalty", type=float, default=1.0, metavar="P",
        help="above 1.0 leans the decoder away from repeating itself. "
             "1.25 with --no-vad recovered a sentence a loop had eaten.",
    )
    parser.add_argument(
        "--chunk", type=float, default=None, metavar="SECONDS",
        help="transcribe in pieces of about this length, cut in the "
             "silences between words. Use it on anything long: whisper "
             "drifts over a lecture and drops whole sentences, and the "
             "same audio in short pieces comes back clean.",
    )
    args = parser.parse_args()

    result = transcribe(args.audio, args.backend, args.model, args.language,
                        args.vad, args.repetition_penalty, args.chunk)
    out = args.output or args.audio.with_suffix(".words.json")
    out.write_text(json.dumps(result, indent=2))
    print(f"{len(result['words'])} words, {result['duration']}s -> {out}")


if __name__ == "__main__":
    main()
