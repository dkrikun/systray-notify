@echo off

pushd %~dp0
rd /Q /S build >nul 2>&1
del systray_notify.exe >nul 2>&1
del /Q /S *_pb2.py >nul 2>&1
del /Q /S *_rc.py >nul 2>&1
del /Q /S *.pyc >nul 2>&1
echo Cleaned
popd
pause
