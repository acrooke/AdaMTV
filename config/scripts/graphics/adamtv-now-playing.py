#!/usr/bin/env python3

import sys
import json
import subprocess

data = json.load(sys.stdin)

artist = data.get("MediaItem_Artist", "")
title = data.get("MediaItem_Title", "")

cmd = [
    "/usr/local/bin/ffmpeg",
    "-hide_banner",
    "-loglevel", "error",
    "-re",

    "-f", "lavfi",
    "-i", "color=c=black@0.0:s=1280x720:r=30",

    "-vf",
    (
        "format=rgba,"
        "drawtext="
        "fontfile=/fonts/Montserrat.ttf:"
        "text='" + artist.replace("'", "\\'") + "':"
        "x=90:y=585:"
        "fontsize=40:"
        "fontcolor=white,"
        "drawtext="
        "fontfile=/fonts/Montserrat.ttf:"
        "text='" + title.replace("'", "\\'") + "':"
        "x=90:y=625:"
        "fontsize=30:"
        "fontcolor=#CC66FF,"
        "format=bgra"
    ),

    "-f", "rawvideo",
    "-pix_fmt", "bgra",
    "-"
]

subprocess.run(cmd, check=True)
