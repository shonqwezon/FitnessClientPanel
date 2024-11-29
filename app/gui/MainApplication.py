import tkinter as tk
from tkinter import messagebox
from app.gui.LoginScreen import LoginScreen
from app.gui.labels import EXIT_CONFIRM_TITLE, EXIT_CONFIRM_MESSAGE


class MainApplication(tk.Tk):
    """Главное окно приложения, обеспечивающее навигацию между экранами."""

    def __init__(self):
        super().__init__()
        self.title("Fitness Client Panel")
        self.geometry("800x600")  # Устанавливаем начальный размер
        self.resizable(True, True)  # Делаем окно растягиваемым

        self.user_data = {}  # Для хранения данных, например, логина пользователя

        self.current_frame = None
        self.show_frame(LoginScreen)  # Открываем экран логина по умолчанию

        # Обработка закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_frame(self, frame_class):
        """Переключение между экранами."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)

    def on_close(self):
        """Обработка закрытия окна."""
        if messagebox.askokcancel(EXIT_CONFIRM_TITLE, EXIT_CONFIRM_MESSAGE):
            self.destroy()
