#!/bin/bash

folder="$HOME/.local/share/qrTransfer"
conf_path="$folder/config.ini"

write_conf() {
    printf "[directories]\n"                   >> "$conf_path"
    printf "STATIC_FOLDER = /tmp/qrTransfer\n" >> "$conf_path"
    printf "UPLOAD_FOLDER = $HOME/Downloads\n" >> "$conf_path"
    printf "\n"                                >> "$conf_path"
    printf "[network]\n"                       >> "$conf_path"
    printf "PORT = 5000\n"                     >> "$conf_path"
    printf "\n"                                >> "$conf_path"
    printf "[lang]\n"                          >> "$conf_path"
    printf "LANGUAGE = en\n"                   >> "$conf_path"
}


copy() {
    echo "chamei"
    cp ./qrTransfer "$folder/qrTransfer"
    if [[ -f $conf_path ]]; then
        echo
    else
        write_conf
    fi
    sudo ln -s "$folder/qrTransfer" "/usr/local/bin/qrTransfer"
    cp ./qrTransfer_nautilus.sh "$HOME/.local/share/nautilus/scripts/qrTransfer"
}


if [[ -d $folder ]]; then
    copy
else
    mkdir "$folder"
    copy
fi

