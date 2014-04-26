
[Setup]
AppName=systray-notify
AppVersion=1.0.0
DefaultDirName={pf}\systray-notify
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\systray-notify
OutputBaseFilename=systray_notify

[Files]
Source: "build\exe.win-amd64-2.7\*"; DestDir: "{app}"; Flags: recursesubdirs

