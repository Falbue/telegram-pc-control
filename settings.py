import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import zipfile
import os
import io

REPO_NAME = "telegram-pc-control"

# Функция для выбора папки установки
def select_path():
    path = filedialog.askdirectory()
    if path:
        path_var.set(path)

# Функция для создания файла config.py
def create_config_file(install_path):
    config_path = os.path.join(install_path, f"{REPO_NAME}-main", "config.py")
    if not os.path.exists(config_path):
        try:
            with open(config_path, "w") as config_file:
                config_file.write("""API = ''\nDEVICE = ''\nADMIN = 0\nMESSAGE = 0\n""")
        except IOError as e:
            print("Не удалось создать файл config.py")

# Функция для сохранения значений в config.py
def save_config_file(install_path):
    config_path = os.path.join(install_path, f"{REPO_NAME}-main", "config.py")
    api_value = api_var.get()
    device_value = device_var.get()
    admin_value = admin_var.get()

    try:
        with open(config_path, "w") as config_file:
            config_file.write(f"API = '{api_value}'\n")
            config_file.write(f"DEVICE = '{device_value}'\n")
            config_file.write(f"ADMIN = {admin_value}\n")
            config_file.write(f"MESSAGE = 0")
            messagebox.showinfo("Успех", "Настройки успешно сохранены.")
    except IOError as e:
        messagebox.showerror("Ошибка", "Не удалось сохранить настройки.")

# Функция для загрузки репозитория
def download_repo():
    repo_url = f"https://github.com/Falbue/{REPO_NAME}/archive/refs/heads/main.zip"
    install_path = path_var.get()

    if not install_path:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите путь для установки.")
        return

    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(install_path)

        messagebox.showinfo("Успех", "Репозиторий успешно загружен и распакован.")
        frame_config.pack(padx=10, pady=20, anchor="w")  # Показываем frame_config после загрузки
        create_config_file(install_path)  # Создаем файл config.py
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки репозитория: {e}")
    except zipfile.BadZipFile:
        messagebox.showerror("Ошибка", "Неверный формат архива.")

# Создаем главное окно
root = tk.Tk()
root.title("Настройка")
root.geometry("400x500")
root.resizable(width=False, height=False)

# Фрейм для выбора пути
frame_download = ttk.Frame(root)
frame_download.pack(padx=10, pady=10, anchor="w")
frame_btn_download = ttk.Frame(frame_download)

path_var = tk.StringVar()
path_label = ttk.Label(frame_download, text="Выберите путь для установки:")
path_label.pack(pady=10, anchor="w")
path_entry = ttk.Entry(frame_download, textvariable=path_var, width=50)
path_entry.pack(pady=5, anchor="w")

select_button = ttk.Button(frame_btn_download, text="Выбрать путь", command=select_path)
select_button.pack(side="left")

download_button = ttk.Button(frame_btn_download, text="Скачать", command=download_repo)
download_button.pack(side="left", padx=5)
frame_btn_download.pack(anchor="w")

# Фрейм для ввода значений API, DEVICE и ADMIN
frame_config = ttk.Frame(root)
frame_config.pack_forget()  # Изначально скрываем frame_config

# Поле для API
api_var = tk.StringVar()
api_label = ttk.Label(frame_config, text="API:")
api_label.grid(row=0, column=0, pady=5, sticky="w")
api_entry = ttk.Entry(frame_config, textvariable=api_var, width=30)
api_entry.grid(row=0, column=1, pady=5, sticky="w")

# Поле для DEVICE
device_var = tk.StringVar()
device_label = ttk.Label(frame_config, text="DEVICE:")
device_label.grid(row=1, column=0, pady=5, sticky="w")
device_entry = ttk.Entry(frame_config, textvariable=device_var, width=30)
device_entry.grid(row=1, column=1, pady=5, sticky="w")

# Поле для ADMIN
admin_var = tk.StringVar()
admin_label = ttk.Label(frame_config, text="ADMIN:")
admin_label.grid(row=2, column=0, pady=5, sticky="w")
admin_entry = ttk.Entry(frame_config, textvariable=admin_var, width=30)
admin_entry.grid(row=2, column=1, pady=5, sticky="w")

# Кнопка для сохранения настроек
save_button = ttk.Button(frame_config, text="Сохранить", command=lambda: save_config_file(path_var.get()))
save_button.grid(row=3, column=0, columnspan=2, pady=10)

# Запуск главного цикла
root.mainloop()
