import re
import webbrowser
from RandomWordGenerator import RandomWord as rw
import tkinter as tk
from tkinter import ttk, messagebox
from database.sql import edit_defaults, get_defaults


def settings():
    def confirm_settings():
        token_value = token_entry.get()
        admin_id_value = admin_id_entry.get()
        secret_word_value = secret_word_entry.get()

        if not token_value or not is_valid_token(token_value):
            messagebox.showerror("Ошибка", 
                                 "Поле токена не заполнено или не соответствует формату.")
            return
        elif get_defaults('TOKEN') is not None and get_defaults('TOKEN') != token_value: 
            messagebox.showwarning("Предупреждение", 'Кажется вы изменили токен бота, необходим перезапуск.\
            \nНажмите "Выход" в выпадающем меню иконки системного трея и запустите бота снова.')

        if not token_value or not admin_id_value or not secret_word_value:
            messagebox.showwarning("Предупреждение", 
                                 "Все поля должны быть заполнены.")
            return
        
        edit_defaults('TOKEN', token_value)
        edit_defaults('ADMIN', admin_id_value)
        edit_defaults('KEY', secret_word_value)

        settings_window.destroy()
        settings_window.quit()

    def cancel_settings():
        settings_window.destroy()
        settings_window.quit()

    def validate_input(char):
        return char.isdigit() or char == ''
    
    def is_valid_token(token):
        # Проверка формата токена бота
        if not token.startswith(""):
            return False

        parts = token.split(":")
        # Проверка наличия ":" и количества цифр после ":"
        return len(parts) == 2 and parts[0].isdigit() and len(parts[1]) > 0
    
    def hiden():
        if show_hiden_var.get():
            token_entry.config(show="")
            secret_word_entry.config(show="")
        else:
            token_entry.config(show="\u2022")
            secret_word_entry.config(show="\u2022")

    def randomword(event):
        secret_word_entry.delete(0, tk.END)
        secret_word_entry.insert(0, rw(5).generate())

    def github(event):
        webbrowser.open('https://github.com/yaroslavyakovkin')

    def botfather(event):
        webbrowser.open('https://t.me/BotFather')

    def getmyid(event):
        webbrowser.open('https://t.me/getmyid_bot')

    def infohelp(event):
        messagebox.showinfo("Помощь",
'Токен:\
\nДля получения токена, воспользуйтесь ботом @BotFather. \
Создайте своего бота и добавьте его токен в поле "Токен". \
Остальной внешний вид, можно настроить на своё усмотрение.\n\
\nАдмин:\
\nЧтобы узнать свой ID, можно воспользоваться ботом @getmyid_bot. \
Выберите ответственного за управление верификацией и принтером, \
узнайте и впишите его ID в поле "Админ"\n\
\nКлюч:\
\nПридумайте короткий пароль для упрощения верификации, любой кто знает этот ключ, \
может верифицироваться самостоятельно, не ожидая одобрения заявки от админа.\n\
\nВсе упомянутые боты, доступны по клику на текст "Токен" и "Админ" в главном меню. \
При клике на "Ключ", сгенерируется случайный вариант.\n\
\nЕсли по какой то причине бот не работает, проверьте правильность написания токена \
и перезапустите приложение. В крайнем случае обращайтесь к создателю бота @yrkdaysnf')

    # Получаем значения из базы данных
    default_token = get_defaults('TOKEN')
    default_admin = get_defaults('ADMIN')
    default_key = get_defaults('KEY')

    # Проверка на значение None и присвоение пустого значения
    default_token = '' if default_token is None else default_token
    default_admin = '' if default_admin is None else default_admin
    default_key = '' if default_key is None else default_key

    # Создаем всплывающее окно
    settings_window = tk.Tk()
    settings_window.title("Настройки бота")

    # Глобальная переменная для отслеживания видимости символов пароля
    show_hiden_var = tk.IntVar()

    # Копирайт
    author = tk.Label(settings_window, 
                    text='© Y.V.Yakovkin, Office Printer, 2024', 
                    cursor="heart",
                    foreground="gray")
    author.grid(row=0, column=0, padx=5, sticky="sw", columnspan=3)
    author.bind("<Button-2>", github)

    # Инфо
    info = tk.Label(settings_window, text='🛈 Помощь', cursor="question_arrow")
    info.grid(row=0, column=3, padx=5, sticky="se")
    info.bind("<Button-1>", infohelp)

    # Поле ввода для токена бота
    token_label = tk.Label(settings_window, text="Токен:", cursor="star")
    token_label.grid(row=1, column=0, pady=5, padx= 5, sticky="sw")
    token_entry = ttk.Entry(settings_window, show="\u2022", width = 55)
    token_entry.grid(row=1, column=1, pady=5, columnspan=3, padx=(0,5), sticky='nsew')
    token_entry.insert(0, default_token)
    token_label.bind("<Button-1>", botfather)

    # Поле ввода для ID админа
    admin_id_label = tk.Label(settings_window, text="Админ:", cursor="star")
    admin_id_label.grid(row=2, column=0, pady=5, padx=5, sticky="sw")
    admin_id_entry = ttk.Entry(settings_window, 
                               validate="key", 
                               validatecommand=(settings_window.register(validate_input), '%S'),
                               width=20)
    admin_id_entry.grid(row=2, column=1, pady=5, sticky='nsew')
    admin_id_entry.insert(0, default_admin)
    admin_id_label.bind("<Button-1>", getmyid)

    # Поле ввода для секретного слова
    secret_word_label = tk.Label(settings_window, text="Ключ:", cursor="pencil")
    secret_word_label.grid(row=2, column=2, pady=5, padx=5, sticky="se")
    secret_word_entry = ttk.Entry(settings_window, show="\u2022", width=20)
    secret_word_entry.grid(row=2, column=3, pady=5, padx=(0,5), sticky='nsew')
    secret_word_entry.insert(0, default_key)
    secret_word_label.bind("<Button-1>", randomword)

    # Кнопка отмены
    cancel_button = ttk.Button(settings_window, text="Отменить", command=cancel_settings)
    cancel_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky="w")

    # Чекбокс для показа/скрытия символов пароля
    show_password_checkbox = tk.Checkbutton(settings_window, 
                                            text="Показать скрытое", 
                                            variable=show_hiden_var, 
                                            command=hiden)
    show_password_checkbox.grid(row=3, column=0, columnspan=4)

    # Кнопка подтверждения
    confirm_button = ttk.Button(settings_window, text="Подтвердить", command=confirm_settings)
    confirm_button.grid(row=3, column=2, columnspan=2, pady=5, padx=5, sticky="e")

    settings_window.attributes('-topmost', True)
    settings_window.eval('tk::PlaceWindow . center')
    settings_window.iconbitmap('assets\\alpha.ico')
    windowsize = re.findall(r'\d+', settings_window.geometry())
    w = windowsize[0]
    h = windowsize[1]
    settings_window.maxsize(w,h)
    settings_window.minsize(w,h)
    settings_window.mainloop()