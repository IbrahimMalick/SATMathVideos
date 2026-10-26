"""Acceptance checks — dry-run a scene and report what would be wrong on screen.

Stage 4 of the brief. A 25-minute render is far too slow a way to find out
that a caption sits on a diagram, so this runs construct() with play() and
wait() stubbed: every mobject is built for real and every animation is
jumped to its end state, but no frames are rendered. A half-hour render
becomes a few seconds.

    python build/verify.py concept.five_patterns
    python build/verify.py shorts.recursion --portrait
    SHOTS=/tmp/frames python build/verify.py concept.data_representation

What it checks, which is the list in CLAUDE.md section 7 plus the two
failures that have actually shipped:

  * no rendered text below 28px at 1080p, after any shrink-to-fit
  * nothing outside the frame, and nothing over the bottom strip
  * no two pieces of text drawn on top of each other
  * every beat resolves, and construct() ends on the narration
  * play() without an explicit run_time, which means a hardcoded duration

The text-against-text check exists because the frame and strip checks
cannot see a caption drawn through a diagram, and two of those shipped.
"""

import argparse
import os
import pathlib
import sys
from contextlib import contextmanager
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import manim                                            # noqa: E402
from manim import config                                # noqa: E402
from manim.animation.animation import prepare_animation  # noqa: E402

import brand                                            # noqa: E402

# 135 px per scene unit is the landscape reference the 28px floor is
# written against; a portrait frame is denser, so the floor in nominal
# font-size terms is lower there.
REFERENCE_DENSITY = 135.0
FLOOR_PX = 28.0

OVERLAP_TOL = 0.06      # scene units of mutual intrusion before it counts
OVERLAP_SHARE = 0.08    # ...and this much of the smaller box's area

REPORT, OVERFLOW, OVERLAPS, SMALL = [], [], [], []
SEEN = set()
CURRENT, PLAYS, PLAY_TIME = [None], [0], [0.0]

# Tracked text, by object id: the nominal size it asked for and its string.
# Measured once, at first display — see check_sizes.
TRACKED = {}

_real_serif, _real_mono = brand.serif, brand.mono


def _tracked(factory, default_size):
    def wrapper(text, size=default_size, *args, **kw):
        mob = factory(text, size, *args, **kw)
        TRACKED[id(mob)] = [size, text, False]
        return mob
    return wrapper


def patch_text_factories(*modules):
    """``from brand import serif`` binds at import time, so the tracking
    wrapper has to be installed into each importing module's globals."""
    for mod in modules:
        if hasattr(mod, "serif"):
            mod.serif = _tracked(_real_serif, brand.BODY_SIZE)
        if hasattr(mod, "mono"):
            mod.mono = _tracked(_real_mono, brand.MARGIN_SIZE)


def make_dry(cls):
    class Dry(cls):
        def play(self, *anims, run_time=None, **kw):
            if run_time is None:
                raise AssertionError(
                    f"play() without run_time in beat {CURRENT[0]!r} — "
                    "every duration must come from the beat timer")
            # Jump each animation to its end state, the way the scene looks
            # after the real play() returns. Without this a later next_to()
            # measures a mobject that has not moved yet.
            for anim in anims:
                anim = prepare_animation(anim)   # .animate -> Animation
                anim._setup_scene(self)
                anim.begin()
                anim.interpolate(1)
                anim.finish()
                anim.clean_up_from_scene(self)
            PLAYS[0] += 1
            PLAY_TIME[0] += run_time
            self.renderer.time += run_time
            check_frame(self)
            check_overlap(self)
            check_sizes(self)

        def wait(self, duration=1.0, **kw):
            self.renderer.time += duration

    return Dry


def check_frame(scene):
    """Anything outside the frame is clipped; anything on the strip is hidden."""
    half_w, half_h = config.frame_width / 2, config.frame_height / 2
    strip = getattr(scene, "strip", None)
    if strip is not None and strip not in scene.mobjects:
        strip = None          # faded out; it no longer occupies the band
    note = getattr(scene, "margin", None)
    if strip is not None:
        for m in scene.mobjects:
            if m is strip or m is note:
                continue
            if m.get_bottom()[1] < strip.get_top()[1] + 0.08:
                key = ("strip", CURRENT[0], id(m))
                if key not in SEEN:
                    SEEN.add(key)
                    OVERFLOW.append((CURRENT[0], "OVER STRIP",
                                     getattr(m, "text", type(m).__name__)[:40],
                                     round(m.get_bottom()[1], 2)))
    for m in scene.mobjects:
        if not m.submobjects and m.get_num_points() == 0:
            continue
        left, right = m.get_left()[0], m.get_right()[0]
        bottom, top = m.get_bottom()[1], m.get_top()[1]
        if (left < -half_w - 0.01 or right > half_w + 0.01
                or bottom < -half_h - 0.01 or top > half_h + 0.01):
            key = ("frame", CURRENT[0], id(m))
            if key in SEEN:
                continue
            SEEN.add(key)
            OVERFLOW.append((CURRENT[0], "OFF FRAME",
                             getattr(m, "text", type(m).__name__)[:40],
                             (round(left, 2), round(right, 2),
                              round(bottom, 2), round(top, 2))))


def text_leaves(scene):
    out = []
    for m in scene.mobjects:
        for sub in m.get_family():
            # A Text keeps its points in glyph submobjects, so the Text
            # itself reports zero points — measure the box instead.
            if isinstance(sub, manim.Text) and sub.width > 0 and sub.height > 0:
                out.append(sub)
    return out


def check_overlap(scene):
    """Two pieces of text sitting on top of each other.

    Text against text only: a box is supposed to overlap what it surrounds.
    """
    leaves = text_leaves(scene)
    for i, a in enumerate(leaves):
        for b in leaves[i + 1:]:
            wide = (min(a.get_right()[0], b.get_right()[0])
                    - max(a.get_left()[0], b.get_left()[0]))
            high = (min(a.get_top()[1], b.get_top()[1])
                    - max(a.get_bottom()[1], b.get_bottom()[1]))
            if wide <= OVERLAP_TOL or high <= OVERLAP_TOL:
                continue
            small = min(a.width * a.height, b.width * b.height)
            if small <= 0 or (wide * high) / small < OVERLAP_SHARE:
                continue
            key = ("overlap", CURRENT[0], id(a), id(b))
            if key in SEEN:
                continue
            SEEN.add(key)
            OVERLAPS.append((CURRENT[0], getattr(a, "text", "")[:28],
                             getattr(b, "text", "")[:28],
                             round(wide, 2), round(high, 2)))


def check_sizes(scene):
    """Rendered text size, measured once per Text at its first display.

    Manim's ``Text.font_size`` is derived from the mobject's height, so it
    tracks a real ``scale()`` or shrink-to-fit exactly — and is fooled by
    ``Transform``, which replaces the glyphs and so changes the height for
    reasons that have nothing to do with size. Two strings at the same
    nominal size differ in bounding-box height by a quarter or more
    depending on their ascenders and descenders, which is enough to report
    a caption as undersized when it is nothing of the kind.

    So each Text is measured the first time it appears on screen and never
    again. Shrink-to-fit and scaling both happen at construction, which is
    before first display, so the measurement still catches them. A scene
    that shrank a mobject *after* showing it would slip through; nothing in
    this repo does that, and a still frame would catch it.
    """
    density = (config.pixel_height / config.frame_height) / REFERENCE_DENSITY
    for mob in text_leaves(scene):
        entry = TRACKED.get(id(mob))
        if entry is None or entry[2]:
            continue
        size, text, _ = entry
        entry[2] = True
        rendered = mob.font_size * density
        if rendered < FLOOR_PX - 0.1:
            SMALL.append((CURRENT[0], round(rendered, 1), size, text[:40]))


def snap(scene, name, index, folder):
    cam = scene.renderer.camera
    cam.reset()
    cam.capture_mobjects(scene.mobjects)
    out = pathlib.Path(folder)
    out.mkdir(parents=True, exist_ok=True)
    cam.get_image().save(out / f"{index:03d}_{name}.png")


def scene_location(scene_id):
    """'shorts.recursion' -> (scenes/shorts/recursion.py, 'Recursion')."""
    *packages, module = scene_id.split(".")
    path = REPO_ROOT / "scenes" / Path(*packages) / f"{module}.py"
    if not path.exists():
        sys.exit(f"No scene file at {path}")
    class_name = "".join(part.title() for part in module.split("_"))
    return f"scenes.{scene_id}", class_name


def report():
    print(f"{'beat':<26}{'span':>8}{'anim':>8}{'plays':>7}{'slack':>8}")
    for name, span, spent, plays, slack in REPORT:
        flag = "  <-- SATURATED" if slack < 1.5 else ""
        print(f"{name:<26}{span:>8.2f}{spent:>8.2f}{plays:>7}{slack:>8.2f}{flag}")

    print(f"\n--- off-frame or over-strip: {len(OVERFLOW)} ---")
    for row in OVERFLOW or []:
        print("  ", row)
    if not OVERFLOW:
        print("   none")

    print(f"\n--- overlapping text: {len(OVERLAPS)} ---")
    for row in OVERLAPS[:40]:
        print("  ", row)
    if not OVERLAPS:
        print("   none")
    elif len(OVERLAPS) > 40:
        print(f"   ... and {len(OVERLAPS) - 40} more")

    print(f"\n--- text below the {FLOOR_PX:.0f}px floor: {len(SMALL)} ---")
    for row in SMALL[:30]:
        print("  ", row)
    if not SMALL:
        print("   none")
    elif len(SMALL) > 30:
        print(f"   ... and {len(SMALL) - 30} more")
    return len(OVERFLOW) + len(OVERLAPS) + len(SMALL)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("scene_id", help="e.g. concept.five_patterns")
    parser.add_argument("--portrait", action="store_true",
                        help="check against the 1080x1920 Shorts frame")
    parser.add_argument("--shots", default=os.environ.get("SHOTS"),
                        help="write a PNG per beat into this directory")
    args = parser.parse_args()

    config.frame_rate = 60
    if args.portrait:
        config.pixel_width, config.pixel_height = 1080, 1920
        # The scene module pins the matching frame size on import.
    else:
        config.pixel_width, config.pixel_height = 1920, 1080
        config.frame_width, config.frame_height = 14.222222222222221, 8.0

    module_path, class_name = scene_location(args.scene_id)
    mod = __import__(module_path, fromlist=[class_name])
    # Patch every component the scene dragged in, not a hand-kept list —
    # an unpatched component's text simply goes unchecked.
    parts = [m for name, m in list(sys.modules.items())
             if name.startswith("components.") and m is not None]
    patch_text_factories(mod, *parts)

    from scenes.base import TimingError
    import scenes.base as sb

    cls = getattr(mod, class_name)
    scene = make_dry(cls)()
    scene.setup()
    scene.renderer.time = 0.0

    real_beat = sb.SATScene.beat

    @contextmanager
    def traced(self, name):
        CURRENT[0] = name
        PLAYS[0] = 0
        PLAY_TIME[0] = 0.0
        with real_beat(self, name) as timer:
            entered = self.renderer.time
            yield timer
            self.renderer.time - entered
            if args.shots:
                snap(self, name, len(REPORT), args.shots)
            REPORT.append((name, timer.span, PLAY_TIME[0], PLAYS[0],
                           timer.span - PLAY_TIME[0]))

    sb.SATScene.beat = traced
    try:
        scene.construct()
    except TimingError as exc:
        print(f"TIMING ERROR in beat {CURRENT[0]}:\n{exc}")
        report()
        return 1
    except Exception as exc:
        print(f"{type(exc).__name__} in beat {CURRENT[0]}: {exc}")
        import traceback
        traceback.print_exc()
        report()
        return 1

    problems = report()
    print(f"\nconstruct ends at {scene.renderer.time:.2f}s "
          f"/ narration {scene.narration_duration:.2f}s")
    drift = abs(scene.renderer.time - scene.narration_duration)
    if drift > 0.1:
        print(f"  DRIFT {drift * 1000:.0f}ms — video and audio will not match")
        problems += 1
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
