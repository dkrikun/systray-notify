@echo off
rd build >nul 2>&1
rd dist >nul 2>&1
set PATH=%PATH%;c:\Python27\Lib\site-packages\PySide
del /f /q icon_rc.py
pyside-rcc -py2 -o icon_rc.py icon.qrc
py setup.py build bdist_wininst
cd %~dp0\build\exe.win-amd64-2.7
copy zmq.libzmq.pyd libzmq.pyd >nul 2>&1
del zmq.libzmq.pyd
pause
