@echo off

setlocal 
cd /d %~dp0

echo ================================================================================
echo                 #######
echo   ####   #####     #     #####     ##    #    #   ####   ######  ######  #####
echo  #    #  #    #    #     #    #   #  #   ##   #  #       #       #       #    #
echo  #    #  #    #    #     #    #  #    #  # #  #   ####   #####   #####   #    #
echo  #  # #  #####     #     #####   ######  #  # #       #  #       #       #####
echo  #   #   #   #     #     #   #   #    #  #   ##  #    #  #       #       #   #
echo   ### #  #    #    #     #    #  #    #  #    #   ####   #       ######  #    #
echo.
echo ================================================================================

::License agreement
echo Do you agree with the license available  
set /p asw=at qrTransfer install folder [yes/no]?: 
if %asw% neq yes (
	exit \B 0
)

::Install folder replacement
set folder="C:\Program Files\qrTransfer"
if exist %folder% (
	rmdir /Q /S %folder%
)
mkdir %folder%


::Write config.ini
(echo [directories]
echo STATIC_FOLDER = C:\Windows\temp\qrTransfer
echo UPLOAD_FOLDER = C:\Users\%USERNAME%\Downloads
echo.
echo [network]
echo PORT = 5000
echo.
echo [lang]
echo LANGUAGE = en) > %folder%\config.ini


::Install
copy qrTransfer.exe %folder%
copy icon.ico %folder%
copy scripts\qrTransfer.lnk "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\SendTo"

echo Installed sucessfully.
pause