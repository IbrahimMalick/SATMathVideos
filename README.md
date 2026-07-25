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

## Rendering (Stage 1)

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
