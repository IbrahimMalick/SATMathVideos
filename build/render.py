"""One command: script + recording -> finished mp4 with narration.

Usage:
    python build/render.py scripts/L03-vertex-form.md audio/L03-vertex-form.wav

Steps: transcribe (cached), sync markers to timestamps, render the scene with
Manim, mux the narration audio, write out/<script-stem>.mp4.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from build.sync import sync, parse_script  # noqa: E402
from build.transcribe import transcribe  # noqa: E402

QUALITY = {
    "l": ("-ql", "480p15"),
    "m": ("-qm", "720p30"),
    "h": ("-qh", "1080p60"),
    "k": ("-qk", "2160p60"),
}


def scene_location(scene_id):
    """'concept.vertex_form' -> (scenes/concept/vertex_form.py, 'VertexForm')."""
    *packages, module = scene_id.split(".")
    path = REPO_ROOT / "scenes" / Path(*packages) / f"{module}.py"
    if not path.exists():
        sys.exit(f"Scene '{scene_id}' expects a file at {path}, which does not exist.")
    class_name = "".join(part.title() for part in module.split("_"))
    return path, class_name


def drop_broken_partials(scene_stem, res_dir, class_name):
    """Delete unreadable partial movie files before handing over to Manim.

    A lecture render takes half an hour, and if the machine goes away
    part-way through it leaves a truncated clip behind. Manim's cache
    trusts whatever is on disk, reuses the stub, and the next run gets all
    the way to the concatenation step before failing with an opaque
    'Invalid data found when processing input'. Cheaper to check first.
    """
    partials = (REPO_ROOT / "media" / "videos" / scene_stem / res_dir
                / "partial_movie_files" / class_name)
    if not partials.is_dir():
        return
    for clip in sorted(partials.glob("*.mp4")):
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(clip)],
            capture_output=True, text=True,
        )
        if probe.returncode != 0 or not probe.stdout.strip():
            print(f"discarding truncated partial {clip.name}")
            clip.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("script", type=Path)
    parser.add_argument("audio", type=Path)
    parser.add_argument("-q", "--quality", choices=QUALITY, default="h")
    parser.add_argument("--model", default="base", help="faster-whisper model size")
    parser.add_argument("--backend", default="faster-whisper")
    parser.add_argument(
        "--language", default=None,
        help="ISO code to pin for transcription (e.g. en)",
    )
    parser.add_argument(
        "--retranscribe", action="store_true",
        help="ignore the cached .words.json and transcribe again",
    )
    args = parser.parse_args()

    words_path = args.audio.with_suffix(".words.json")
    if args.retranscribe or not words_path.exists():
        print(f"transcribing {args.audio} ({args.backend}, model={args.model}) ...")
        result = transcribe(args.audio, args.backend, args.model,
                            args.language)
        words_path.write_text(json.dumps(result, indent=2))
        print(f"  {len(result['words'])} words, {result['duration']}s")
    else:
        print(f"using cached transcript {words_path}")

    timing_path, timing = sync(args.script, words_path)
    for b in timing["beats"]:
        print(f"  {b['name']:<12} {b['start']:7.2f} -> {b['end']:7.2f}")

    scene_path, class_name = scene_location(timing["scene"])
    qflag, res_dir = QUALITY[args.quality]
    drop_broken_partials(scene_path.stem, res_dir, class_name)
    subprocess.run(
        [sys.executable, "-m", "manim", "render", qflag,
         str(scene_path.relative_to(REPO_ROOT)), class_name],
        cwd=REPO_ROOT, check=True,
    )
    video = REPO_ROOT / "media" / "videos" / scene_path.stem / res_dir / f"{class_name}.mp4"

    out = REPO_ROOT / "out" / f"{args.script.stem}.mp4"
    out.parent.mkdir(exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(video), "-i", str(args.audio),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
         "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact",
         str(out)],
        check=True,
    )
    print(f"-> {out}")


if __name__ == "__main__":
    main()
