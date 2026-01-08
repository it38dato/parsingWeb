@echo off
setlocal
SET VENV_NAME=envParserWeb
SET VENV_PATH=%USERPROFILE%\%VENV_NAME%
SET IMPORT_PY=editBssCes.py
SET PARSER_PROJECT_NAME=parserWeb

cd %USERPROFILE%\%PARSER_PROJECT_NAME%

if not exist "%IMPORT_PY%" (
    echo Error: The %IMPORT_PY% file was not found in the current directory.
    echo Make sure that you run the script from the root of your project.
    pause
    exit /b 1
)

if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Error: The virtual environment "%VENV_NAME%" was not found on the path. "%VENV_PATH%".
    echo Please run setup_venv.bat first.
    pause
    exit /b 1
)

echo Activating the virtual environment %VENV_NAME%...
CALL "%VENV_PATH%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo Error when activating the environment.
    pause
    exit /b 1
)
echo The environment is activated.

echo Launching a Project...
python %IMPORT_PY%

endlocal
pause