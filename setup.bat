@echo off
rd build >nul 2>&1
rd dist >nul 2>&1
py setup.py build bdist_wininst
cd %~dp0\build\exe.win-amd64-2.7
rename zmq.libzmq.pyd libzmq.pyd >nul 2>&1
pause
