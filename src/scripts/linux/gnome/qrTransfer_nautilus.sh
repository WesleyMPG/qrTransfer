#!/bin/bash

IFS='$%'


paths=""
for p in $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS; do
	paths+="${p//$'\n'/ }"
done


if [[ -z $paths ]]
then
    notify-send "No file privided"
else
    notify-send "Uploading file ${paths[@]}"
    sh -c "/usr/local/bin/qrTransfer -p ${paths[@]}"
fi

