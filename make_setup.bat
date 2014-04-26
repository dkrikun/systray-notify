@echo off

pushd %~dp0

iscc /o. systray_notify.iss

popd
pause

