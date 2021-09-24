#!/bin/bash

root="."
out="$root/build"

pyinstaller \
--add-data "$root/display/kvFiles:display/kvFiles" \
--onefile --windowed --distpath "$out/dist" \
--workpath "$out/build" -n qrTransfer "$root/main.py"