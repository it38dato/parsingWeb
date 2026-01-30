@echo off
:: Загрузка переменных из config.txt
if exist config.txt (
    for /f "tokens=1,2 delims== " %%A in (config.txt) do (
        if "%%A"=="REGKEY" set "RegKey=%%B"
        if "%%A"=="REGVAL1" set "RegValue1=%%B"
        if "%%A"=="REGVAL2" set "RegValue2=%%B"
    )
) else (
    echo Config file not found!
    pause
    exit /b
)

echo Checking %RegValue2%...
REG QUERY %RegKey% /v %RegValue2% > nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    echo The Yandex Browser installer has been found.
    REM Изменяем FOR /F, чтобы захватить всю строку после "="
    FOR /F "tokens=2,*" %%A IN ('REG QUERY %RegKey% /v %RegValue2%') DO (
        REM %%A будет типом REG_SZ, %%B будет значением (включая пробелы)
        echo Parameter value "%RegValue2%": %%B
    )
) ELSE (
    echo The Yandex Browser registry key was not found. Yandex Browser may not be installed.
)

echo.
echo Checking %RegValue1%...
REG QUERY %RegKey% /v %RegValue1% > nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    echo The Yandex Browser version has been found.
    REM Изменяем FOR /F для ypv аналогичным образом, хотя там пробелов обычно нет
    FOR /F "tokens=2,*" %%A IN ('REG QUERY %RegKey% /v %RegValue1%') DO (
        echo Parameter value "%RegValue1%": %%B
    )
) ELSE (
    echo The Yandex Browser registry key was not found. Yandex Browser may not be installed.
)
pause