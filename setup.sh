#!/usr/bin/env bash
# Environment setup — verified on Ubuntu 24.04 / Python 3.12.
# These system packages are required and not obvious from Manim's docs:
#   - manimpango fails to build without the pango/cairo dev headers
#   - MathTex fails at render time without dvisvgm
set -euo pipefail

apt-get install -y libpango1.0-dev libcairo2-dev pkg-config dvisvgm ffmpeg \
    texlive texlive-latex-extra

# Ubuntu's distro-patched setuptools can't build the srt sdist (a
# faster-whisper dependency) — upgrade the build tools first.
pip install --ignore-installed --upgrade pip setuptools wheel
pip install manim faster-whisper
