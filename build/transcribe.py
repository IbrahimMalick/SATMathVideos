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


def transcribe_faster_whisper(path, model_size):
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        str(path), word_timestamps=True, temperature=0.0, beam_size=5
    )
    words = []
    for segment in segments:
        for w in segment.words:
            words.append(
                {"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
            )
    return words


def transcribe_assemblyai(path, _model_size):
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


def transcribe(audio_path, backend="faster-whisper", model_size="base"):
    """Return {"duration": float, "words": [...]} for a recording."""
    words = BACKENDS[backend](audio_path, model_size)
    return {"duration": round(audio_duration(audio_path), 3), "words": words}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("audio", type=Path)
    parser.add_argument("--backend", choices=BACKENDS, default="faster-whisper")
    parser.add_argument("--model", default="base", help="faster-whisper model size")
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    result = transcribe(args.audio, args.backend, args.model)
    out = args.output or args.audio.with_suffix(".words.json")
    out.write_text(json.dumps(result, indent=2))
    print(f"{len(result['words'])} words, {result['duration']}s -> {out}")


if __name__ == "__main__":
    main()
