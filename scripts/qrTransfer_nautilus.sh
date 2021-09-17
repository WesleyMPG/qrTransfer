#!/bin/bash


read -r -a paths <<< "$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"
notify-send "Uploading file ${paths[0]}"
~/.local/bin/qrTransfer "${paths[0]}"

#~/.local/bin/qrTransfer $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
