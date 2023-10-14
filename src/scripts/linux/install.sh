#!/bin/bash

script_dir=$(dirname "$0")
cd $script_dir

folder="$HOME/.local/share/qrTransfer"

gme_scripts="scripts/gnome"
kde_scripts="scripts/kde"
xfce_scripts="scripts/xfce"

trap "exit 0" SIGINT

license_agreement() {
    less "./LICENSE"
    asw=""
    while [[ -z $asw ]]; do
        read -p "Do you agree with the license? [yes/no]: " asw
        if [[ $asw == 'yes' ]]; then
            break
        elif [[ $asw == 'no' ]]; then
            exit 0
        fi
        asw=""
        echo "Please, type 'yes' or 'no'."
    done
}


write_mtp_shortcut() {
    path="/usr/share/applications/qrTransfer-MTP.desktop"
    if [[ -f $path ]]; then
        return
    fi
    (printf "[Desktop Entry]\n" &&
    printf "Name=Receive from qrTransfer\n" &&
    printf "Name[pt]=Receber pelo qrTransfer\n" &&
    printf "Comment=A way to transfer files from your phone\n" &&
    printf "Comment[pt_BR]=Um jeito de receber arquivos do celular\n" &&
    printf "Type=Application\n" &&
    printf "Exec=qrTransfer -mtp\n" &&
    printf "Categories=Utility\n" &&
    printf "GenericName=FileTransfer\n" &&
    printf "Icon=$folder/icon.png") > ./mtp.temp
    sudo cp ./mtp.temp $path
    rm mtp.temp
}


kde_context_menu() {
    service_folder="$HOME/.local/share/kservices5"
    if ! [[ -d $service_folder ]]; then
        mkdir $service_folder
    fi
    cp "$kde_scripts/qrTransfer-service.desktop" "$service_folder"
}


gnome_context_menu() {
    scripts_folder="$HOME/.local/share/nautilus/scripts"
    if ! [[ -d $scripts_folder ]]; then
        mkdir $scripts_folder
    fi
    cp "$gme_scripts/qrTransfer_nautilus.sh" "$scripts_folder/qrTransfer"
}


xfce_context_menu() {
    sendTo_path="/usr/share/Thunar/sendto"
    filename="thunar-sendto-qrTransfer.desktop"

    asw=""
    (echo "
    At Thunar, qrTransfer will be placed under 'send to' submenu. 
    However this menu doesn't appear on desktop. To use qrTransfer 
    also on desktop files a shortcut can be added so you'll be able
    to open the files through 'open with other application...'.
    ")
    read -p "Add this extra shortcut? [y/N]: " -n1 asw

    sudo cp "$xfce_scripts/$filename" "$sendTo_path/"
    sudo sh -c "echo Icon=$folder/icon.png >> $sendTo_path/$filename"
    if [[ $asw == 'y' ]]; then
        sudo cp "$sendTo_path/$filename" \
        "/usr/share/applications/qrTransfer.desktop"
    fi
}


ask_manager() {
    asw=""
        (echo -e "Please, enter your current file manager:\n\
            \n\tNautilus (GNOME) - [1]\
            \n\tDolphin  (KDE)   - [2]\
            \n\tThunar   (XFCE)  - [3]\
            \n\tOther            - [0]\n")
    while [[ -z $asw ]]; do
        read -p "  :: " asw
        if [[ $asw == '1' ]]; then
            gnome_context_menu
            break
        elif [[ $asw == '2' ]]; then
            kde_context_menu
            break
        elif [[ $asw == '3' ]]; then
            xfce_context_menu
            break
        elif [[ $asw == '0' ]]; then
            echo -e "\tYour file manager still has no qrTransfer\
               \n\tscript to be placed at context menu. However you\
               \n\tcan use it through terminal. Also, you can search\
               \n\thow create one by yourself (it can be easier than\
               \n\tyou think), or open an issue at the repo and I'll\
               \n\ttry to add support as soon as possible."
            break
        else
            asw=""
        fi
    done
}


copy() {
    license_agreement
    cp  qrTransfer \
        uninstall.sh \
        LICENSE \
        icon.png "$folder/"
    # put an "if succeed" on copy

    write_conf
    write_mtp_shortcut
    sudo ln -s "$folder/qrTransfer" "/usr/local/bin/qrTransfer"

    if [[ $? ]]; then
        ask_manager
    fi

    if [[ $? ]]; then
        echo -e "\nInstalled successfully"
    fi
}


if ! [[ -d $folder ]]; then
    mkdir "$folder"
fi

copy

