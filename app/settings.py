import tkinter as tk
from tkinter import ttk, messagebox
from database.sql import edit_defaults, get_defaults


def settings():
    def confirm_settings():
        # Получаем значения из полей ввода
        token_value = token_entry.get()
        admin_id_value = admin_id_entry.get()
        secret_word_value = secret_word_entry.get()

        # Проверка, что поле токена не пусто и соответствует формату токена бота
        if not token_value or not is_valid_token(token_value):
            messagebox.showerror("Ошибка", "Поле токена не заполнено или имеет некорректный формат.")
            return

        # Сохраняем значения в базу данных (вместо вывода)
        edit_defaults('TOKEN', token_value)
        edit_defaults('ADMIN', admin_id_value)
        edit_defaults('KEY', secret_word_value)

        # Закрываем всплывающее окно
        settings_window.quit()

    def cancel_settings():
        settings_window.quit()

    # Функция для ограничения ввода только цифр
    def validate_input(char):
        return char.isdigit() or char == ''
    
    def is_valid_token(token):
        # Проверка формата токена бота
        if not token.startswith(""):
            return False

        parts = token.split(":")
        # Проверка наличия ":" и количества цифр после ":"
        return len(parts) == 2 and parts[0].isdigit() and len(parts[1]) > 0

    # Получаем значения из базы данных
    default_token = get_defaults('TOKEN')
    default_admin = get_defaults('ADMIN')
    default_key = get_defaults('KEY')

    # # Создаем главное окно и скрываем его
    # root = tk.Tk()
    # root.withdraw()

    # Создаем всплывающее окно
    settings_window = tk.Tk()
    settings_window.title("Настройки бота")

    # Поле ввода для токена бота
    token_label = ttk.Label(settings_window, text="Токен:")
    token_label.grid(row=0, column=0, pady=5, padx= 2, sticky="sw")
    token_entry = ttk.Entry(settings_window, show="*", width = 40)
    token_entry.grid(row=0, column=1, pady=5, columnspan=3, sticky='nsew')
    token_entry.insert(0, default_token)

    # Поле ввода для ID админа
    admin_id_label = ttk.Label(settings_window, text="Админ:")
    admin_id_label.grid(row=1, column=0, pady=5, padx=2, sticky="sw")
    admin_id_entry = ttk.Entry(settings_window, 
                               validate="key", 
                               validatecommand=(settings_window.register(validate_input), '%S'),
                               width=20)
    admin_id_entry.grid(row=1, column=1, pady=5, padx=(0, 5), sticky='nsew')
    admin_id_entry.insert(0, default_admin)

    # Поле ввода для секретного слова
    secret_word_label = ttk.Label(settings_window, text="Ключ:")
    secret_word_label.grid(row=1, column=2, pady=5, sticky="sw")
    secret_word_entry = ttk.Entry(settings_window, width=20)
    secret_word_entry.grid(row=1, column=3, pady=5, sticky='nsew')
    secret_word_entry.insert(0, default_key)

    # Кнопка подтверждения
    confirm_button = ttk.Button(settings_window, text="Подтвердить", command=confirm_settings)
    confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Кнопка отмены
    cancel_button = ttk.Button(settings_window, text="Отменить", command=cancel_settings)
    cancel_button.grid(row=2, column=2, columnspan=2, pady=10)
    settings_window.geometry("350x100")
    settings_window.minsize(350,100)
    #settings_window.overrideredirect(True)
    settings_window.attributes('-topmost', True)
    settings_window.eval('tk::PlaceWindow . center')
    settings_window.mainloop()