#!/bin/bash

IFS='$%'

read -r -a paths <<< "$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"

if [[ -z $paths ]]
then
    notify-send "No file privided"
else
    notify-send "Uploading file ${paths[0]}"
    "/usr/local/bin/qrTransfer" -p "${paths[0]}"
fi

