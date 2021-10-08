#!/bin/bash

script_dir=$(dirname "$0")
cd $script_dir

root="../.."
out="../$root/build"


if ! [[ -d $out ]]; then
    mkdir $out
fi


if [[ -d "$out/dist/" ]]; then
    rm -r "$out/dist"
fi


pyinstaller \
--add-data "$root/display/kvFiles:display/kvFiles" \
--add-data "$root/resources:resources" \
--add-data "$root/server/templates:server/templates" \
--icon "$root/resources/icon.png" \
--onefile --windowed --distpath "$out/dist" \
--workpath "$out/build" -n qrTransfer "$root/main.py"


cp -r "$root/scripts/linux/" "$out/dist/scripts"
cp "../$root/LICENSE" "$out/dist/"
cp "$root/resources/icon.png" "$out/dist"

mv "$out/dist/scripts/install.sh" "$out/dist/"
mv "$out/dist/scripts/uninstall.sh" "$out/dist/"

rm "$out/dist/scripts/build.sh"
rm "$out/dist/scripts/qrTransfer.spec"
