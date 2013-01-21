@rem Personal Environment Bootstrap
@rem ******************************
@rem This file gets python installed so that more complicated setup can begin

@setlocal
@set PYTHON_SHORT_VERSION=2.7
@set PYTHON_VERSION=2.7.3
@set PYTHON_SUFFIX=.amd64
@set PYWIN32_SUFFIX=-amd64
@set PYWIN32_VERSION=218

where python > NUL 2>&1
@if %errorlevel% equ 0 goto distribute
@echo Downloading Python %PYTHON_VERSION%...
curl\curl http://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%%PYTHON_SUFFIX%.msi > python-%PYTHON_VERSION%%PYTHON_SUFFIX%.msi
@if not errorlevel 0 goto abort
@echo Installing...
msiexec /passive /i python-%PYTHON_VERSION%%PYTHON_SUFFIX%.msi
@if not errorlevel 0 goto abort
@echo Success! Installation complete.
@echo Configuring environment variables...
@if not defined MY_PYTHON_PATH (
    @setx /m MY_PYTHON_PATH "C:\Python27;C:\Python27\Scripts"
    @set MY_PYTHON_PATH="C:\Python27;C:\Python27\Scripts"
)
cscript addtopath.vbs %%MY_PYTHON_PATH%%
@set PATH=%PATH%;%MY_PYTHON_PATH%

:distribute
@echo Installing distribute and pip
curl\curl http://python-distribute.org/distribute_setup.py | python
@if not errorlevel 0 goto abort
curl\curl --insecure https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
@if not errorlevel 0 goto abort
@echo Installing pywin32
curl\curl -L http://downloads.sourceforge.net/project/pywin32/pywin32/Build%%20%PYWIN32_VERSION%/pywin32-%PYWIN32_VERSION%.win%PYWIN32_SUFFIX%-py%PYTHON_SHORT_VERSION%.exe > pywin32.exe
easy_install pywin32.exe
@if not errorlevel 0 goto abort

@if exist %USERPROFILE%\bin goto end
mkdir %USERPROFILE%\bin
@set MY_USER_BIN=%USERPROFILE%\bin
@setx MY_USER_BIN %USERPROFILE%\bin
@set PATH=%PATH%;%MY_USER_BIN%
cscript addtopath.vbs /user %%MY_USER_BIN%%

@goto end

:abort
@echo Failed to install Python. You're on your own...

:end
@endlocal
