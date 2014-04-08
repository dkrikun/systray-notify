from cx_Freeze import setup, Executable

# cx_Freeze options
buildOptions = dict(
        packages = ['zmq', 'zmq.backend.cython'],
        excludes = ['PySide.QtNetwork'],
        includes = 'atexit',
        append_script_to_exe = False,
        include_msvcr = True
        )

base = 'Win32GUI'
executables = [
    Executable('systray.py', base=base)
]

setup(name='systray',
      version = '1.0',
      description = 'system tray pilot',
      options = dict(build_exe = buildOptions),
      executables = executables)
