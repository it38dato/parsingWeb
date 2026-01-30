#$project = "parserWeb"
$project = Split-Path -Path $PSScriptRoot -Leaf
$envProject = "envParserWeb"
$userProfile = $env:USERPROFILE

# 1. Используем интерполяцию строк (переменные внутри двойных кавычек) для задания пути транскрипта
Start-Transcript -Path "$userProfile\$project\outShellScript.log"

# 2. Активация виртуального окружения с использованием оператора dot sourcing (точки и пробела)
# Это гарантирует, что окружение активируется в текущей сессии PowerShell
cd "$userProfile\$envProject\Scripts\"
. .\Activate.ps1

# 3. Переход в директорию проекта
cd "$userProfile\$project"

# 4. Запуск Python скрипта (теперь в активированном окружении)
python main.py

# 5. Деактивация (теперь должна работать, т.к. окружение было активировано правильно)
deactivate

# 6. Остановка транскрипта
Stop-Transcript