@echo off

set folder="C:\Program Files\qrTransfer"

rmdir /Q /S %folder%
del "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\SendTo\qrTransfer.lnk"

echo Uninstalled successfully.
pause