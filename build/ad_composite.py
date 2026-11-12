"""Lay a rendered caption overlay back over the client's footage.

    python build/ad_composite.py --base <the client's mp4> --landscape
    python build/ad_composite.py --base <the client's mp4> --portrait

The footage and the voiceover belong to the client and are not in this
repo; only the text layer is built here. Point --base at the file he
supplied. For the record, the landscape cut was made from the mp4 at
Google Drive id 1hHyMbSPDb9LmmRoECCmPPI_wM8b24XHy, 1920x1080, 30fps,
53.13s, titled "15.1 - Timeline export of 14.1".

The overlay is rendered first, with alpha, at the base's own size and
frame rate, so the composite lands on the client's frame grid rather than
resampling his footage:

    python -m manim render -t -r 1920,1080 --fps 30 \\
        scenes/ads/apcsa_cohort.py ApcsaCohort
    python -m manim render -t -r 1080,1920 --fps 30 \\
        scenes/ads/apcsa_cohort_vertical.py ApcsaCohortVertical

The portrait cut does not crop the footage. A 16:9 frame cropped to 9:16
keeps a third of the picture and cuts people in half, so the landscape
footage is scaled to the full width of the portrait frame and pinned in a
band near the top, with the house cream behind it and the captions below.

Audio is copied, never re-encoded: it is the client's voiceover and there
is nothing to gain by generating a second-generation copy of it.
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CUTS = {
    "landscape": {
        "overlay": "media/videos/apcsa_cohort/1080p30/ApcsaCohort.mov",
        "out": "out/APCSA-cohort-ad.mp4",
        "size": (1920, 1080),
        # The footage fills the frame, but the client's own broken
        # captions are burned into it and the new ones do not cover every
        # one of them: his ran off the left edge, and the new block starts
        # at a margin. So the band they live in is blurred out of the base
        # first. The box was checked against a still from every caption in
        # the original; all of them sit inside it.
        #
        # Full width, and feathered top and bottom by the geq on the alpha
        # channel. A patch the width of the text leaves a vertical seam
        # down the middle of the picture, and a hard-edged one announces
        # itself as a rectangle; 26 pixels of ramp at each edge reads as
        # depth of field instead. Four blur passes rather than one big
        # radius: it smears 32px type into nothing, where a single pass
        # leaves it readable.
        "filter": (
            "[0:v]scale=1920:1080,split=2[a][b];"
            "[b]crop=1920:230:0:770,boxblur=20:4,format=rgba,"
            "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
            "a='255*min(1,min(Y,H-Y)/26)'[patch];"
            "[a][patch]overlay=0:770[base];"
            "[base][1:v]overlay=0:0:format=auto[v]"
        ),
    },
    "client": {
        "overlay": "media/videos/apcsa_client/1080p30/ApcsaClient.mov",
        "out": "out/APCSA-cohort-ad-client.mp4",
        "size": (1920, 1080),
        # His own template: the picture is a window across the top 736
        # rows and a navy band fills the rest. Cropping from the top is
        # what the window wants anyway, and it removes his first ad's
        # burned-in captions for free -- they start at row 795, so there
        # is nothing left to blur.
        "filter": (
            "color=c=0x0A1320:s=1920x1080:r=30[bg];"
            "[0:v]scale=1920:1080,crop=1920:736:0:0[clip];"
            "[bg][clip]overlay=0:0:shortest=1[framed];"
            "[framed][1:v]overlay=0:0:format=auto[v]"
        ),
    },
    "portrait": {
        "overlay": ("media/videos/apcsa_cohort_vertical/1920p30/"
                    "ApcsaCohortVertical.mov"),
        "out": "out/APCSA-cohort-ad-vertical.mp4",
        "size": (1080, 1920),
        # Footage cropped, scaled to the full width and pinned where the
        # overlay leaves a window for it. 1080x432 at y=300 matches
        # CLIP_TOP and CLIP_BOTTOM in scenes/ads/apcsa_cohort_vertical.py;
        # change one and change both.
        "filter": (
            # No blur patch here. In the landscape cut the client's burned
            # -in captions have to be smeared out, because the frame is
            # full of footage and there is nowhere for them to go. In a
            # vertical frame the footage is a window, so the band they
            # live in is simply not in the window: the top 768 rows of
            # 1080 are kept, which stops 27 rows above the highest of his
            # captions. That loses the desks and keeps every face, and it
            # costs nothing, where a blur band across a window this small
            # announces itself.
            # 768 rather than 770 so the downscale lands on 432 exactly.
            "[0:v]crop=1920:768:0:0,scale=1080:432[clip];"
            "color=c=0xF4F0E6:s=1080x1920:r=30[bg];"
            "[bg][clip]overlay=0:300:shortest=1[framed];"
            "[framed][1:v]overlay=0:0:format=auto[v]"
        ),
    },
}


def run(command):
    print(" ".join(str(part) for part in command))
    result = subprocess.run(command)
    if result.returncode != 0:
        sys.exit(f"ffmpeg failed with code {result.returncode}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True,
                        help="the client's original mp4")
    parser.add_argument("--cut", choices=sorted(CUTS), required=True)
    args = parser.parse_args()

    spec = CUTS[args.cut]
    overlay = REPO_ROOT / spec["overlay"]
    if not overlay.exists():
        sys.exit(f"No overlay at {overlay}. Render the scene first; the "
                 "command is in this file's docstring.")
    base = Path(args.base)
    if not base.exists():
        sys.exit(f"No base footage at {base}.")

    out = REPO_ROOT / spec["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-v", "error", "-y",
        "-i", str(base), "-i", str(overlay),
        "-filter_complex", spec["filter"],
        "-map", "[v]", "-map", "0:a",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart", str(out),
    ])
    print(f"-> {out}")


if __name__ == "__main__":
    main()
