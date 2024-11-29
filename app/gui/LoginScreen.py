import tkinter as tk
from tkinter import messagebox
from gui.admin.AdminMenuScreen import AdminMenuScreen
from gui.manager.ManagerMenuScreen import ManagerMenuScreen
from labels import (
    LOGIN_SCREEN_TITLE,
    LOGIN_LABEL,
    PASSWORD_LABEL,
    LOGIN_BUTTON,
    LOGIN_ERROR,
    LOGIN_ADMIN_WELCOME,
    LOGIN_MANAGER_WELCOME,
)


class LoginScreen(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.master = master
        self.on_success = on_success
        self.master.title(LOGIN_SCREEN_TITLE)

        # Создание верхнего отступа для смещения элементов вниз
        self.configure(pady=50)

        # Логин
        self.login_label = tk.Label(self, text=LOGIN_LABEL, font=("Arial", 14))
        self.login_label.pack(pady=(10, 5))

        self.login_entry = tk.Entry(self, width=30)
        self.login_entry.pack(pady=5)

        # Пароль
        self.password_label = tk.Label(self, text=PASSWORD_LABEL, font=("Arial", 14))
        self.password_label.pack(pady=(20, 5))

        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)

        # Кнопка входа
        self.login_button = tk.Button(self, text=LOGIN_BUTTON, command=self.handle_login, width=15)
        self.login_button.pack(pady=30)

        self.pack(fill="both", expand=True)

    def handle_login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Пример валидации данных
        if login == "admin" and password == "admin":
            messagebox.showinfo(LOGIN_ADMIN_WELCOME, "Добро пожаловать, администратор!")
            self.on_success(role="admin")
        elif login == "manager" and password == "1":
            messagebox.showinfo(LOGIN_MANAGER_WELCOME, "Добро пожаловать, менеджер!")
            self.on_success(role="manager")
        else:
            messagebox.showerror(LOGIN_ERROR, "Неверные логин или пароль")
