from cx_Freeze import setup, Executable

# cx_Freeze options
buildOptions = dict(
        packages = ['zmq'],
        includes = 'atexit',                # required for Qt
        include_msvcr = True,               # include msvc redist.
        append_script_to_exe = True
        )

base = 'Win32GUI'
executables = [
    Executable('systray_notify.py', base=base)
]

setup(name='systray-notify',
      version = '1.0',
      description = 'Display user notifications via system tray',
      options = dict(build_exe = buildOptions),
      executables = executables)
