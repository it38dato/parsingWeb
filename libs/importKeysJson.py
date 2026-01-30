from pathlib import Path
import os
import json
BASE_DIR = Path(__file__).resolve().parent.parent
print(Path(__file__).resolve())
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.json")
# Функция для загрузки конфигурации
def funcLoadConfig(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл конфигурации '{file_path}' не найден.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: Не удалось декодировать JSON из файла '{file_path}'. Проверьте синтаксис.")
        exit(1)
# Загружаем все данные из файла
#CONFIG_DATA = funcLoadConfig(CONFIG_FILE_PATH)
#print(CONFIG_DATA.get('test1'))