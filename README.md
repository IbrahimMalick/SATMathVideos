# SATMathVideos

Script-driven Manim pipeline for SAT prep videos. Narration drives visuals:
beat markers in the narration script resolve to timestamps from the actual
recording, and every visual reveal lands on the word that motivates it.

The full spec lives in [CLAUDE.md](CLAUDE.md).

## Setup

Verified on Ubuntu 24.04 / Python 3.12. `pip install manim` alone is not
enough — manimpango needs the pango/cairo dev headers and `MathTex` needs
`dvisvgm` at render time:

```bash
sudo bash setup.sh
```

or by hand:

```bash
apt-get install -y libpango1.0-dev libcairo2-dev pkg-config dvisvgm ffmpeg texlive texlive-latex-extra
pip install manim faster-whisper
```

## From a recording (Stage 2)

Record yourself reading a script, then:

```bash
python build/render.py scripts/L03-vertex-form.md audio/L03-vertex-form.wav
```

This transcribes the recording (local faster-whisper by default; the
transcript is cached as `audio/<name>.words.json`), aligns the script's
`[[beat:...]]` markers against what was actually said, writes
`timings/<scene>.json`, renders the scene, muxes the narration, and writes
`out/<script-stem>.mp4`. Useful flags: `-q l` for a fast draft render,
`--model small` for a more accurate transcription, `--retranscribe` after
replacing a recording, `--backend assemblyai` (needs `ASSEMBLYAI_API_KEY`).

A marker that can't be matched to the recording fails loudly with the marker
name — fix the recording or the script, never the timing file by hand.

## Rendering a scene directly (Stage 1)

Always render from the repo root with `python -m manim` (this puts the repo
root on the import path so `brand` and `scenes.base` resolve):

```bash
python -m manim render -qh scenes/concept/vertex_form.py VertexForm
```

Timing comes from `timings/<scene_id>.json` — hand-written for now, emitted
by `build/sync.py` from a real recording in Stage 2. Edit a beat's start time
there and re-render, and the reveal moves; scenes contain no hardcoded
run times or waits.

Set `TIMING_FILE=/path/to/timing.json` to point a render at a different
timing file.
