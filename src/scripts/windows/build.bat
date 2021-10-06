@echo off

setlocal 
cd /d %~dp0

set root=..\..
set out=..\%root%\build

if not exist %out% (
	mkdir %out%
)

if exist %out%\dist (
	rmdir /Q /S %out%\dist
)


pyinstaller^
 --add-data "%root%\display\kvFiles;display\kvFiles"^
 --add-data "%root%\resources;resources"^
 --add-data "%root%/server/templates;server/templates"^
 --icon "%root%\resources\icon.ico"^
 --onefile --distpath "%out%\dist"^
 --workpath "%out%\build" -n qrTransfer.exe "%root%\main.py"
 

mkdir %out%\dist\scripts
Xcopy /E %root%\scripts\windows %out%\dist\scripts\
copy ..\%root%\LICENSE %out%\dist\
copy %root%\resources\icon.ico %out%\dist\
move "%out%\dist\scripts\install.bat" "%out%\dist\"
move "%out%\dist\scripts\uninstall.bat" "%out%\dist\"
del "%out%\dist\scripts\build.bat"
del "%out%\dist\scripts\qrTransfer.exe.spec"
pause