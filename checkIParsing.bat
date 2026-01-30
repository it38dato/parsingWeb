@echo off
setlocal
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python was not found. First, install Python and add it to the PATH.
    pause
    exit /b 1
)
SET VENV_NAME=envParserWeb
SET VENV_PATH=%USERPROFILE%\%VENV_NAME%
SET REQS_FILE=requirements.txt
SET PARSER_PROJECT_NAME=parserWeb

set /p name="Enter the project name: "
SET VENV_NAME=envParserWeb
SET VENV_PATH=%USERPROFILE%\%VENV_NAME%
SET REQS_FILE=requirements.txt
SET PROJECT_NAME=%name%

echo Home Directory: %USERPROFILE%
echo The path to the virtual environment: %VENV_PATH%
echo Requirements file: %REQS_FILE%
if not exist "%VENV_PATH%" (
    echo Creating a virtual environment "%VENV_NAME%"...
    python -m venv "%VENV_PATH%"
    if %errorlevel% neq 0 (
        echo Error when creating a virtual environment.
        pause
        exit /b 1
    )
    echo The virtual environment has been successfully created.
) else (
    echo The virtual environment "%VENV_NAME%" already exists. Skipping the creation.
)
echo Activating the virtual environment and installing libraries from %REQS_FILE%...
CALL "%VENV_PATH%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo Error when activating the environment.
    pause
    exit /b 1
)

:: Извлекаем значение прокси из config.json через PowerShell
for /f "delims=" %%a in ('powershell -command "(Get-Content config.json | ConvertFrom-Json).proxy"') do set PROXY_URL=%%a
echo Using proxy: %PROXY_URL%
:: Теперь используем переменную в командах pip
pip install --upgrade pip --proxy %PROXY_URL%
pip install -r "%REQS_FILE%" --proxy %PROXY_URL%

if %errorlevel% neq 0 (
    echo Error when installing libraries.
    pause
    exit /b 1
)

echo Everything is ready! The %VENV_NAME% virtual environment is configured.
echo Libraries from %REQS_FILE% are installed:
pip list
echo To activate the environment manually later, use the command (bat or ps1):
echo CALL "%VENV_PATH%\Scripts\activate.bat"
echo OR
echo CALL "%VENV_PATH%\Scripts\activate.ps1"

echo Creating a project "%PROJECT_NAME%" in the current directory...
mkdir %USERPROFILE%\%PROJECT_NAME%

xcopy /s yandexdriver.exe %USERPROFILE%\%PROJECT_NAME%
xcopy /s config.json %USERPROFILE%\%PROJECT_NAME%
xcopy /s startParcsing.ps1 %USERPROFILE%\%PROJECT_NAME%
xcopy /s main.py %USERPROFILE%\%PROJECT_NAME%
xcopy "libs" "%USERPROFILE%\%PROJECT_NAME%\libs" /E /I /H /Y

if %errorlevel% neq 0 (
    echo Error when creating a project.
    pause
    exit /b 1
)

echo The project "%PROJECT_NAME%" has been successfully created in:
echo %USERPROFILE%\%PROJECT_NAME%
pause
endlocal