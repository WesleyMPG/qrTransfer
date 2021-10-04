@echo off
set root=.
set out=%root%\build

@echo on
pyinstaller^
 --add-data "%root%\display\kvFiles;display\kvFiles"^
 --onefile --distpath "%out%\dist"^
 --workpath "%out%\build" -n qrTransfer.exe "%root%\main.py"