#!/bin/bash


read -r -a paths <<< "$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"
notify-send "Uploading file ${paths[0]}"
~/.local/bin/qrTransfer -p "${paths[0]}"

#~/.local/bin/qrTransfer $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
