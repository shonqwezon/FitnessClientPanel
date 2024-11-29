import tkinter as tk


class ManagerMenuScreen(tk.Frame):
    """Меню менеджера."""

    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Добро пожаловать в меню менеджера!").pack(pady=20)
        # Добавьте другие элементы для меню менеджера
