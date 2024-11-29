import tkinter as tk


class AdminMenuScreen(tk.Frame):
    """Меню администратора."""

    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Добро пожаловать в меню администратора!").pack(pady=20)
        # Добавьте другие элементы для меню администратора
