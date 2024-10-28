import subprocess
import sys
import time
import os

refresh_time = 1
DIR = script_directory = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    """Запускает указанный скрипт и перезапускает его при ошибке."""
    while True:
        print(f"Запуск {script_name}...")
        try:
            result = subprocess.run([sys.executable, script_name], check=True)
            print(f"{script_name} успешно завершен.")
            break  # Выход из цикла, если скрипт завершился успешно
        except subprocess.CalledProcessError as e:
            print(f"{script_name} завершился с ошибкой: {e}. Перезапуск через {refresh_time} секунд...")
            time.sleep(refresh_time)  # Ждем перед перезапуском

if __name__ == "__main__":
    run_script(f'{DIR}/bot.py')
