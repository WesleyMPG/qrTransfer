# About
----

qrTransfer is a simple utility software to send files between your pc and mobile devices if they are in the **same network**.

### Usage

After installation an option will be added to context menu and you just have to right-click over the file you want to send and then select something like "send to qrTransfer" and in a few seconds a qr code will pop up in your screen, then take your mobile device camera and read it to start the download (older devices may need an external qr code reading app). Also a shortcut is added to your system: "qrTransfer-MTP". It can be used to send files from your **M**obile device **T**o your **P**c. Open it, scan the code and open the upload page.

At terminal you can do:
```shell
$ qrTransfer -p path_to_file # to sendo
$ qrTransfer -mtp # to receive
```

### How it works?

When you select a file to transfer, it is copied to another folder and made available in your local network. So the qr code contains the copy download address.  When closing the qr code window the copy will be erased, that's why you must wait your download finish before close it.

### How secure is it?

This depends most on your local network. If you're in a network that you trust (like your home) is pretty safe. If you're in a public network you are not that secure, but for small (and probably unimportant) files should be no problem. Besides that, there is at least one thing or two to be implemented in the next versions to improve security.

# Install

----

First of all, there is a lot of room for improvements here and I plan to create a graphical installer in a time to come, but for now please continue with these simple versions.

###  Windows

- Download the corresponding release;
- Extract the folder;
- Execute 'Install' file as administrator;
- Agree with the license

Right-click on a file and look for qrTransfer at "send to" sub-menu.

### Linux

- Download the corresponding release;
- Extract the folder;
- Execute 'install.sh' in a terminal;
- Agree with the license;
- Select your file manager

Right-click on a file and look for scripts sub-menu on Nautilus and qrTransfer on Dolphin.

The context menu functionality currently has support only for Nautilus (Gnome) and Dolphin (KDE), but you can search how to add it to your file manager. However you still can use it through command line.

### MacOS

It should work on Mac, but I don't have a way to test it. You could download the source and test through python; checkout the next section for building instructions.

# Build
----

Please read it all before doing.

### Environment

Clone source:

```shell	
$ git clone https://github.com/WesleyMPG/qrTransfer.git
```

To setup the environment you must have at least python 3.6 and run:

```shell
$ pip install -r requirements.txt
$ pip install pyinstaller
```

If you're using a conda env, remove kivy from 'requirements.txt' and do the same. Then to install kivy do:

```shell
$ conda install -c conda-forge kivy
```
After that you're able to run main.py.

### Building
There are scripts to do an automated build and generate a folder with the same content of a release. Just run:

```shell
$ cd qrTransfer 
$ src/scripts/linux/build.sh # on linux

$ src/scripts/windows/build.bat # on windows
```