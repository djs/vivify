@rem Personal Environment Bootstrap
@rem ******************************
@rem This file gets python installed so that more complicated setup can begin

@setlocal
@set PYTHON_VERSION=2.7.3

@echo Downloading Python %PYTHON_VERSION%...
curl\curl http://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%.msi > python-%PYTHON_VERSION%.msi
@if not errorlevel 0 goto abort
@echo Installing...
msiexec /passive /i python-%PYTHON_VERSION%.msi
@if not errorlevel 0 goto abort
@endlocal
@echo Success! Installation complete.
@echo Configuring environment variables...
@setx /m MY_PYTHON_PATH "C:\Python27;C:\Python27\Scripts"
@set MY_PYTHON_PATH="C:\Python27;C:\Python27\Scripts"
cscript addtopath.vbs %%MY_PYTHON_PATH%%
@set PATH=%PATH%;%MY_PYTHON_PATH%
@echo Installing distribute and pip
curl\curl http://python-distribute.org/distribute_setup.py | python
@if not errorlevel 0 goto abort
curl\curl --insecure https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
@if not errorlevel 0 goto abort

@goto end

:abort
@echo Failed to install Python. You're on your own...

:end

