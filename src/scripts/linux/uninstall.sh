#!/bin/bash

folders=(
    "$HOME/.local/share/qrTransfer"
)

files=(
    "/usr/local/bin/qrTransfer"
    "$HOME/.local/share/nautilus/scripts/qrTransfer"
    "$HOME/.local/share/kservices5/qrTransfer-service.desktop"
)

for f in ${files[@]}; do
    if [[ -f $f || -L $f ]]; then
        echo "removing $f"
        sudo rm  $f
    fi
done

for d in ${folders[@]}; do
    if [[ -d $d ]]; then
        echo "removing $d"
        sudo rm -rf $d
    fi
done

echo "Uninstalled successfully."
