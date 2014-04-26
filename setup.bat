@echo off

title systray-notify setup.bat
echo working

pushd %~dp0

rd /S /Q build >nul 2>&1
rd /S /Q dist >nul 2>&1

rem generate protobuf code
protoc --python_out=. api.proto

rem generate icon_rc.py
set PATH=%PATH%;c:\Python27\Lib\site-packages\PySide
del /f /q icon_rc.py
pyside-rcc -py2 -o icon_rc.py icon.qrc

rem run cx_freeze and create py installer
py setup.py build bdist_wininst

rem workaround pyzmq cx_freeze, see README.md
cd %~dp0\build\exe.win-amd64-2.7
copy zmq.libzmq.pyd libzmq.pyd >nul 2>&1
del zmq.libzmq.pyd

popd
pause
