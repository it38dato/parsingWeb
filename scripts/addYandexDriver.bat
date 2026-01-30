@echo off

set /p name="Enter the project name: "
SET PROJECT_NAME=%name%
REM Установка пути к директории с Яндекс.Драйвером
::SET DRIVER_PATH=C:\path\to\yandexdriver\

REM Добавление пути к драйверу в системную переменную PATH
REM Команда SETX изменяет системные/пользовательские переменные
REM Ключ /M используется для системных переменных (требуются права администратора)
::SETX PATH "%PATH%;%DRIVER_PATH%" /M
SETX PATH "%PATH%;%USERPROFILE%\%PROJECT_NAME%\" /M

echo %PATH%
echo The path to Yandex.Added to the PATH environment variable for the driver.
echo To apply the changes, you may need to restart the command line or log out.
pause