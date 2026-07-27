"""SATScene: cream background, beat-driven timing.

Every scene subclasses SATScene, declares its ``scene_id``, and spends time
only through beats:

    class VertexForm(SATScene):
        scene_id = "concept.vertex_form"

        def construct(self):
            with self.beat("axes") as t:
                self.play(Create(axes), run_time=t.fill(0.6))
            with self.beat("curve") as t:
                self.play(Create(curve), run_time=t.fill(0.5))
                t.hold()

Timing comes from a JSON file (hand-written for now, emitted by sync.py
later): ``timings/<scene_id>.json``, or whatever ``TIMING_FILE`` points at.
Entering a beat waits until that beat's start, so narration-only stretches
between beats need no code at all. After construct() the scene is padded out
to the narration's full duration, so video length always matches audio length.

Scenes never contain a hardcoded run_time or self.wait() in seconds — all
the waits below are derived from the timing file, which is the one place
seconds are allowed to live.
"""

import json
import os
from contextlib import contextmanager
from pathlib import Path

from manim import Scene, config

from brand import CREAM, MIN_RUN_TIME

REPO_ROOT = Path(__file__).resolve().parents[1]


class TimingError(Exception):
    """A beat could not be resolved. Fail loudly, never default."""


def snap(seconds):
    """Round a duration onto the frame grid.

    Manim renders whole frames; handing it durations that aren't frame
    multiples makes the rendered video drift ahead of the narration by a
    frame per animation, which adds up over a long lecture. Every duration
    the beat machinery emits goes through here so the scene clock and the
    frame count always agree.
    """
    frames = max(1, round(seconds * config.frame_rate))
    return frames / config.frame_rate


class BeatTimer:
    """Handed to the scene inside a ``with self.beat(...)`` block."""

    def __init__(self, scene, name, start, end):
        self._scene = scene
        self.name = name
        self.start = start
        self.end = end
        self.span = end - start

    @property
    def remaining(self):
        return self.end - self._scene.renderer.time

    def fill(self, fraction):
        """Return a run_time spending ``fraction`` of the beat's span.

        Clamped up to the house pacing floor and down to whatever is left of
        the beat, so a fast delivery shortens the animation rather than
        pushing the next reveal off its word.
        """
        remaining = self.remaining
        if remaining <= 0:
            raise TimingError(
                f"Beat '{self.name}' is already spent "
                f"(ends at {self.end:.2f}s, scene is at {self._scene.renderer.time:.2f}s). "
                "Earlier animations in this beat used more time than the narration allows."
            )
        run_time = max(MIN_RUN_TIME, fraction * self.span)
        return snap(min(run_time, remaining))

    def hold(self):
        """Sit still for whatever is left of the beat."""
        remaining = self.remaining
        if remaining > 1 / config.frame_rate:
            self._scene.wait(snap(remaining))


class SATScene(Scene):
    """Base class for all course scenes. Sets the house background and
    resolves beat names to narration timestamps."""

    scene_id = None  # e.g. "concept.vertex_form" — every subclass sets this

    def setup(self):
        self.camera.background_color = CREAM
        self._load_timing()

    def _timing_path(self):
        override = os.environ.get("TIMING_FILE")
        if override:
            return Path(override)
        if not self.scene_id:
            raise TimingError(
                f"{type(self).__name__} has no scene_id, so its timing file "
                "cannot be found. Set scene_id = \"concept.example\" on the class."
            )
        return REPO_ROOT / "timings" / f"{self.scene_id}.json"

    def _load_timing(self):
        path = self._timing_path()
        if not path.exists():
            raise TimingError(f"Timing file not found: {path}")
        data = json.loads(path.read_text())
        if self.scene_id and data.get("scene") != self.scene_id:
            raise TimingError(
                f"{path} is for scene '{data.get('scene')}', "
                f"but this scene is '{self.scene_id}'."
            )
        self.narration_duration = data["duration"]
        self._beats = {}
        for b in data["beats"]:
            self._beats[b["name"]] = (b["start"], b["end"])

    @contextmanager
    def beat(self, name):
        if name not in self._beats:
            raise TimingError(
                f"No beat named '{name}' in timing for '{self.scene_id}'. "
                f"Available beats: {', '.join(self._beats) or '(none)'}"
            )
        start, end = self._beats[name]
        now = self.renderer.time
        tolerance = 2 / config.frame_rate
        if now > start + tolerance:
            raise TimingError(
                f"Beat '{name}' starts at {start:.2f}s but the scene is already "
                f"at {now:.2f}s. An earlier beat overran — reveals would drift "
                "off their words, so this fails instead."
            )
        if start - now > 1 / config.frame_rate:
            self.wait(snap(start - now))  # narration-only stretch before this beat
        yield BeatTimer(self, name, start, end)

    def tear_down(self):
        # Pad to the narration's full length so video and audio durations
        # always match, whether or not the last beat held to its end.
        remaining = self.narration_duration - self.renderer.time
        if remaining > 1 / config.frame_rate:
            self.wait(snap(remaining))
        super().tear_down()
