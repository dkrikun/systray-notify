# cx_Freeze zmq + protobuf script

### zmq

There is a problem freezing pyzmq-14.1.1, a workaround have been found to it here >>
https://bitbucket.org/anthony_tuininga/cx_freeze/issue/55/failed-with-pyzmq-1401-py33-win-amd64egg

The workaround says:

    1. Add `zmq.backend.cython` to `packages` cx_Freeze build options in setup.py
    2. After `setup.py build` has been invoked, rename `zmq.libzmq.pyd` --> `libzmq.pyd`
    in build target folder

### protobuf

As you can now guess by yourself, there is a problem freezing protobuf-2.5.0
too. Steps to work around the problem are:

    1. Instead of running `python setup.py build test install` as suggests
    protobuf python readme, run `python setup.py build test bdist_wininst`,
    then go to `dist` and run the installer therein.
    2. Goto yours python site-packages folder, e.g. `C:\Python27\lib\site-packages`,
    then to `google` folder therein, and create empty file `__init__.py`.
    3. Open python interactive interpreter (i.e `python.exe` from the command-line)
    and invoke `import google`, press enter, then Ctrl-Z to exit.
