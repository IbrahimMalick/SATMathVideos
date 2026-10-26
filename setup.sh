#!/usr/bin/env bash
# Environment setup — verified on Ubuntu 24.04, Python 3.11 and 3.12.
# These system packages are required and not obvious from Manim's docs:
#   - manimpango fails to build without the pango/cairo dev headers
#   - MathTex fails at render time without dvisvgm
set -euo pipefail

# A fresh container ships a stale package index, so apt resolves versions
# that have already been superseded and the downloads 404. Refresh first.
apt-get update

apt-get install -y libpango1.0-dev libcairo2-dev pkg-config dvisvgm ffmpeg \
    texlive texlive-latex-extra

# Always `python3 -m pip`, never bare `pip`. A container can ship a pip
# bound to a different interpreter than `python3` — one image here had
# python3 at 3.11 and pip installing into 3.13, so everything installed
# successfully and nothing could be imported.
PY=${PYTHON:-python3}
echo "installing into $("$PY" --version) at $(command -v "$PY")"

# Ubuntu's distro-patched setuptools can't build the srt sdist (a
# faster-whisper dependency) — upgrade the build tools first.
"$PY" -m pip install --ignore-installed --upgrade pip setuptools wheel

# Manim is pinned: renders have to be reproducible, and a minor release
# moves glyph metrics and spacing enough to shift a layout that was
# verified against the 28px floor.
"$PY" -m pip install "manim==0.21.0" faster-whisper

"$PY" - <<'CHECK'
import manim, faster_whisper  # noqa: F401
print(f"ok: manim {manim.__version__}, faster-whisper importable")
CHECK
