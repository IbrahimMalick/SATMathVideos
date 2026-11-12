"""Beat placement for the AP CSA cohort ad, in both aspect ratios.

Run from the repo root:

    python build/beats_adcohort.py

The voiceover is the audio track of an AI-generated ad the client made
elsewhere. Only the text layer is rebuilt here; the voice and, in the
landscape cut, the footage are his. The audio the pipeline reads is lifted
straight off that file:

    ffmpeg -i <the ad> -vn -c:a aac -b:a 160k audio/APCSA-cohort-ad.m4a

    python build/transcribe.py audio/APCSA-cohort-ad.wav \\
        --language en --chunk 20 --model large-v3

The large model and the short chunks both earn their keep on this one. The
default pass over the whole 53 seconds mis-heard "capped at 10" as "kept
it 10", "$600 in all" as "600 and all", and "when the teacher does it" as
"when the tea tree does it" — three lines that would have gone on screen
as written if the captions were being taken from the transcript rather
than from the client's own caption copy.

Two anchors are deliberately loose. "What's i on the second pass" comes
back as "What's... eye on the second pass", and "capped at 10" as "capped
at $10", because the voice reads the digit. Both still match on overlap.

The phone number is NOT taken from the transcript: the chunked pass hears
"704 -4513" and the unchunked pass hears "646 -704 -4513". The number on
screen is the second, and it wants confirming by a human before this runs
anywhere, because it is the one thing in the ad that cannot be wrong.
"""

import json
import sys
from pathlib import Path

from mkbeats import build

REPO_ROOT = Path(__file__).resolve().parents[1]

BEATS = [
    # ------------------------------------------------------- the problem
    ("stuck", "I get it when the teacher does it"),
    ("alone", "Alone, it looks impossible"),

    # ------------------------------------------------- what is at stake
    ("first_ap", "First AP in our family"),
    ("opens", "This one opens engineering"),

    # ------------------------------------------------------- what they want
    ("structure", "We need structure, not another guess"),
    ("not_200", "Not $200 an hour"),

    # ------------------------------------------------------------ the offer
    ("capped", "A live group capped at"),
    ("tutor", "with Dr. Ibrahim Malik"),
    ("two_hours", "Two hours a week"),

    # ------------------------------------------------------- how it is taught
    ("trace", "Trace it"),
    ("second_pass", "on the second pass"),
    ("topics", "java code tracing arrays"),
    ("frq", "free response questions"),
    ("one_line", "one line at a time until she can do them alone"),

    # ---------------------------------------------------------- it lands
    ("it_runs", "it runs"),

    # ------------------------------------------------------------ the plan
    ("exam_day", "exam day is may 12th"),
    ("a_plan", "now there's a plan to get there"),
    ("price", "100 a month 600 in all"),
    ("when", "live evenings or weekends starting November 16th"),

    # -------------------------------------------------------------- the card
    ("brand", "The Digital Tutor"),
    ("cohort", "AP Computer Science A Support Cohort"),
    ("url", "Join today at ap"),
    ("phone", "or call"),
]

NOTE = ("AP Computer Science A Support Cohort, The Digital Tutor. Caption "
        "layer only: the voiceover is the client's. Beats placed by anchor "
        "phrase against that voiceover, see build/beats_adcohort.py.")

def mirror_timing():
    """Give the vertical cut its own timing file.

    Both cuts are the same voiceover and therefore the same beats, but
    scenes/base.py refuses a timing file whose scene id is not its own --
    which is the right thing for a lecture, where a mismatched timing file
    means a scene is being driven by the wrong recording. Here it just
    means copying one field.

    Run after sync.py has produced the landscape timing:

        python build/beats_adcohort.py          # writes the script
        python build/sync.py scripts/APCSA-cohort-ad.md \\
            audio/APCSA-cohort-ad.words.json
        python build/beats_adcohort.py --mirror
    """
    src = REPO_ROOT / "timings" / "ads.apcsa_cohort.json"
    if not src.exists():
        sys.exit(f"No timing at {src}; run build/sync.py first.")
    data = json.loads(src.read_text())
    data["scene"] = "ads.apcsa_cohort_vertical"
    dst = REPO_ROOT / "timings" / "ads.apcsa_cohort_vertical.json"
    dst.write_text(json.dumps(data, indent=2) + "\n")
    print(f"-> {dst.relative_to(REPO_ROOT)}  {len(data['beats'])} beats")


if __name__ == "__main__":
    if "--mirror" in sys.argv:
        mirror_timing()
    else:
        build("APCSA-cohort-ad", "ads.apcsa_cohort", BEATS,
              "APCSA-cohort-ad", NOTE)
