# Project Brief: Script-Driven Manim Video Pipeline

This file is the standing spec. It stays in the repo — it is the contract, not a one-time prompt.

## 1. What we are building

A pipeline that turns a narration script plus a voice recording into rendered Manim scenes in a
fixed house style, with every visual reveal landing on the word that motivates it.

The output is SAT prep course content: concept explainers and worked problem solutions.

The non-negotiable ordering: **narration drives visuals.** I record freely, and the animation
timing is derived from what I actually said. We never hand-tune run times to guess at a delivery,
and I never re-record to match a fixed animation. If a design decision would invert that
relationship, it's the wrong decision.

## 2. House style

This is a warm editorial variant of the Manim / 3Blue1Brown grammar. It is not the default Manim
look and must not drift back toward it.

### Palette — `brand.py` is the single source of truth

```python
CREAM      = "#F4F0E6"   # background, always
CHARCOAL   = "#2E2C2A"   # axes, primary text, equations
SLATE      = "#4A6D8C"   # primary curves, functions, main subject
TERRACOTTA = "#C1663F"   # the one thing the viewer should look at
SAGE       = "#6B8F71"   # confirmation, correct answers, underline sweeps
GREY       = "#8A857E"   # margin annotations, de-emphasized material
```

Rules:

* Background is always `CREAM`. Never Manim's default dark.
* `TERRACOTTA` is scarce. One terracotta element on screen at a time. It means "look here."
  If everything is highlighted, nothing is.
* Never introduce a colour outside this list. If something needs distinguishing and the palette
  can't do it, the layout is wrong.

### Typography

* Math and equations: `MathTex` / LaTeX. Computer Modern serif is correct here — do not override it.
* Body and labels: Pango `Text` with a serif family.
* Margin annotations: monospace, `GREY`, small, upper-left. These are asides, not content.
* Minimum rendered font size: 28px at 1080p. A large share of test-prep viewing is on phones.
  Any text below this fails review.

### Animation grammar

* Geometry and diagrams draw themselves on — `Create`, never `FadeIn`. The drawing is the explanation.
* Equations write on — `Write`.
* Equations morph rather than cut — `TransformMatchingTex`. This is the signature transition;
  use it whenever a general form becomes specific, or one step becomes the next.
* Entrances are single. Never stack `FadeIn` + `scale` + `shift` on one object.
* Pacing is calm. Default `run_time` floor of 0.5s; diagram construction typically 1.5–2.5s.

### Sound

* No music bed under problem solving. Openers and closers only.
* Two sound cues total across the whole course: a soft tick on an eliminated answer choice,
  a resolution tone on the correct answer. Nothing else.

## 3. Architecture

```
brand.py              palette, fonts, size constants, spacing scale
scenes/
  base.py             SATScene base class — sets background, loads beats
  concept/            conceptual explainers (parabola, exponential growth, ...)
  worked/             worked problem solutions
components/
  math_step.py        MathStep       — one line of algebra, revealed per beat
  answer_choices.py   AnswerChoices  — A–D, strikethrough elimination
  passage.py          PassageHighlight — sentence-level highlight sweeps
  geometry.py         GeometryFigure — SVG-ish labeled construction
  worked_solution.py  WorkedSolution — persistent problem + accumulating steps
scripts/
  L03-vertex-form.md  narration script with beat markers
audio/
  L03-vertex-form.wav raw recording
build/
  transcribe.py       audio -> word-level timestamps
  sync.py             script + transcript -> timing.json
  render.py           timing.json + scene -> mp4
  verify.py           acceptance checks
out/                  rendered mp4s
```

### The timing mechanism — build this carefully, everything depends on it

**Script format.** Narration in markdown, with inline beat markers:

```markdown
---
scene: concept.vertex_form
---

Every parabola has a lowest or highest point, and we call it the vertex.
[[beat:axes]] Let's set up a coordinate plane. [[beat:curve]] And here's a
parabola — notice it's symmetric about a vertical line through that lowest
point. [[beat:equation]] The vertex form of a quadratic looks like this.
[[beat:vertex]] Here, h and k are the coordinates of the vertex itself.
```

**Pipeline:**

1. `transcribe.py` — recording to word-level timestamps. Support a pluggable backend; default to
   local `faster-whisper` so per-lesson cost is zero at course volume. AssemblyAI as an optional
   backend.

2. `sync.py` — strip markers from the script, align the clean script text against the transcript
   words (Needleman-Wunsch or similar; my delivery will not match the script exactly and the
   aligner must tolerate that), then resolve each marker to the timestamp of the word that follows
   it. Emit `timing.json`:

```json
{
  "scene": "concept.vertex_form",
  "duration": 24.8,
  "beats": [
    {"name": "axes",     "start": 3.10, "end": 6.42},
    {"name": "curve",    "start": 6.42, "end": 12.05},
    {"name": "equation", "start": 12.05, "end": 16.30},
    {"name": "vertex",   "start": 16.30, "end": 24.80}
  ]
}
```

3. Scenes consume beats through a helper on `SATScene`:

```python
class VertexForm(SATScene):
    def construct(self):
        with self.beat("axes") as t:
            self.play(Create(axes), run_time=t.fill(0.6))
        with self.beat("curve") as t:
            self.play(Create(curve), run_time=t.fill(0.5))
            t.hold()   # sit still for the remainder of the beat
```

`t.fill(fraction)` spends that fraction of the beat's span on the animation; `t.hold()` waits out
whatever is left. A scene must never contain a hardcoded `run_time` or `self.wait()` in seconds.
That is the rule the whole design exists to enforce — flag it in review if you see one.

4. `render.py` — invoke Manim, mux the narration audio, write to `out/`.

## 4. Environment

Verified working on Ubuntu 24.04 / Python 3.12. These system packages are required and are not
obvious from Manim's docs — `pip install manim` fails without them:

```bash
apt-get install -y libpango1.0-dev libcairo2-dev pkg-config dvisvgm ffmpeg texlive texlive-latex-extra
pip install manim faster-whisper
```

`manimpango` fails to build without the pango/cairo dev headers. `MathTex` fails at render time
without `dvisvgm`. Put this in `setup.sh` and in the README.

## 5. Constraints

* All practice items must be original. College Board owns released SAT questions. Components are
  parameterized so a new item is new numbers passed into an existing archetype, never a
  reproduction.
* Mobile legibility gates every render. See the 28px floor above.
* Consistency across lessons is the quality signal, not any single lesson's polish. Uniform intro
  length, font scale, and colour usage across 100 videos matters more than a clever animation in
  lesson 12.
* Renders are deterministic — same script plus same audio produces the same mp4.

## 6. Build order

Do not build all of this at once. Stop after each stage and show me the output.

* **Stage 1 — prove the loop.** `brand.py`, `SATScene` base, the beat helper, and one hand-written
  `timing.json` (skip transcription entirely). Port the existing `vertex.py` scene to use beats.
  Success: I change a number in `timing.json`, re-render, and the reveal moves.
* **Stage 2 — real sync.** `transcribe.py` and `sync.py`. Success: I record myself reading
  `L03-vertex-form.md`, run one command, and get a video where the parabola draws exactly as I say
  "and here's a parabola."
* **Stage 3 — the archetype library.** `MathStep`, `AnswerChoices`, `WorkedSolution`.
  `WorkedSolution` is the important one and is structurally different from the concept scenes:
  the problem stays on screen for 60–120 seconds while steps accumulate beneath it. It is one
  scene with a state machine, not a sequence of shots.
* **Stage 4 — batch and verify.** `verify.py` plus a batch renderer over a whole module.

## 7. Acceptance checks — `verify.py`

* No rendered text below 28px at 1080p.
* No hardcoded `run_time=` or `self.wait(` with a numeric literal in any file under `scenes/`.
* Audio duration and video duration match within 100ms.
* Every beat marker in the script resolves to a timestamp; unresolved markers fail loudly rather
  than defaulting.
* Every colour literal in `scenes/` and `components/` is imported from `brand.py`.

## 8. Working style

* Show me a rendered frame or clip after any change to visual style. I judge this by eye, not by
  reading code.
* When a design choice is ambiguous, ask before building. A wrong abstraction in `WorkedSolution`
  costs more than a round trip.
* Prefer boring, obvious Python. This repo will be read by me months from now while I'm thinking
  about pedagogy, not architecture.
