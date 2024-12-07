import hashlib
import tkinter as tk
from tkinter import messagebox, ttk

from app import setup_logger
from app.db import database, exceptions
from app.db.config import DbTable
from datetime import date

logger = setup_logger(__name__)


class MainApplication(tk.Tk):
    """Главное окно приложения, обеспечивающее навигацию между экранами."""

    def __init__(self):
        super().__init__()
        self.title("Fitness Client Panel")
        self.geometry("800x600")  # Устанавливаем начальный размер
        self.user_data = {
            "username": None,
            "role": None,
            "sportcenter_id": None,
        }  # Хранение данных пользователя

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Отображаем экран логина по умолчанию
        self.show_login_screen()

    def clear_screen(self):
        """
        Удаляет все виджеты с текущего экрана.
        """
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """
        Отображает экран логина.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Вход в систему", font=("Arial", 24)).pack(pady=20)

        # Поля для ввода логина и пароля
        login_var = tk.StringVar()
        password_var = tk.StringVar()

        tk.Label(self, text="Логин:").pack(pady=5)
        tk.Entry(self, textvariable=login_var).pack(pady=5)

        tk.Label(self, text="Пароль:").pack(pady=5)
        tk.Entry(self, textvariable=password_var, show="*").pack(pady=5)

        # Ошибка авторизации
        error_label = tk.Label(self, text="", fg="red")
        error_label.pack()

        def hash_string_sha256(input_string):
            # Преобразуем строку в байты
            input_bytes = input_string.encode("utf-8")
            # Хешируем строку
            hash_object = hashlib.sha256(input_bytes)
            # Преобразуем хеш в шестнадцатеричный формат
            return hash_object.hexdigest()

        # Кнопка входа
        def login():
            login = login_var.get()
            password = password_var.get()

            if database.is_admin(login, password):
                self.user_data["username"] = "Администратор"
                self.user_data["role"] = "admin"
                self.show_admin_menu()
            elif database.is_correct_manager(login, hash_string_sha256(password)):
                self.user_data["username"] = login
                self.user_data["role"] = "manager"
                self.user_data["sportcenter_id"] = database.get_table(DbTable.MANAGER)[0][3]
                self.show_manager_menu()
            else:
                error_label.config(text="Неверный логин или пароль")

        tk.Button(self, text="Войти", command=login).pack(pady=20)

    #
    # ---
    #

    # админская часть

    def show_admin_menu(self):
        """
        Отображает меню администратора.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Меню администратора", font=("Arial", 24)).pack(pady=20)

        # Отображение имени пользователя
        tk.Label(self, text=f"Добро пожаловать, {self.user_data['username']}").pack(pady=10)

        # Кнопки
        tk.Button(
            self, text="Управление менеджерами", width=30, command=self.admin_managers_menu
        ).pack(pady=5)
        tk.Button(self, text="Управление залами", width=30, command=self.admin_offices_menu).pack(
            pady=5
        )
        tk.Button(self, text="Услуги", width=30, command=self.admin_services_menu).pack(pady=5)
        tk.Button(self, text="Настройка тарифов", width=30, command=self.admin_plans_menu).pack(
            pady=5
        )
        tk.Button(self, text="Просмотр", width=30, command=self.admin_view_menu).pack(pady=5)
        tk.Button(self, text="Удаление", width=30, command=self.admin_delete_menu).pack(pady=5)

        tk.Button(self, text="Выйти", width=30, command=self.show_login_screen).pack(pady=20)

    # Управление менеджерами

    def admin_managers_menu(self):
        self.clear_screen()

        tk.Label(self, text="Менеджеры", font=("Arial", 24)).pack(pady=20)

        tk.Button(self, text="Добавить", width=30, command=self.admin_managers_choose_office).pack(
            pady=5
        )
        tk.Button(self, text="Удалить", width=30, command=self.admin_managers_delete).pack(pady=5)
        tk.Button(self, text="назад", command=self.show_admin_menu, width=30).pack(pady=5)

    def admin_managers_choose_office(self):
        """
        Экран выбора спортзала.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Выбор спортзала для менеджера", font=("Arial", 24)).pack(pady=20)

        # Массив залов
        halls = database.get_table(DbTable.SPORTCENTER)
        logger.debug(halls)

        hall_names = [hall[1] for hall in halls]

        # Список с залами
        hall_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=hall_names), height=len(hall_names)
        )
        hall_list.pack(pady=10)

        # Кнопка "Подтвердить"
        def confirm_hall():
            try:
                index = hall_list.curselection()[0]

                selected_id = halls[index][0]
                self.admin_managers_input_name(halls[index][1], selected_id)
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите спортзал.")

        tk.Button(self, text="Подтвердить", width=30, command=confirm_hall).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_managers_menu).pack(pady=10)

    def admin_managers_input_name(self, hall_name, hall_id):
        """
        Экран ввода имени менеджера.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text=f"Добавление менеджера для {hall_name}", font=("Arial", 24)).pack(
            pady=20
        )

        # Поле для ввода имени
        tk.Label(self, text="Введите имя менеджера:").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(self, textvariable=name_var).pack(pady=10)

        # Поле для ввода email
        tk.Label(self, text="Введите email менеджера:").pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(self, textvariable=email_var).pack(pady=10)

        # Поле для ввода пароля
        tk.Label(self, text="Введите пароль менеджера:").pack(pady=5)
        password_var = tk.StringVar()
        tk.Entry(self, textvariable=password_var).pack(pady=10)

        def hash_string_sha256(input_string):
            # Преобразуем строку в байты
            input_bytes = input_string.encode("utf-8")
            # Хешируем строку
            hash_object = hashlib.sha256(input_bytes)
            # Преобразуем хеш в шестнадцатеричный формат
            return hash_object.hexdigest()

        # Кнопка "Подтвердить"
        def confirm_name():
            manager_name = name_var.get().strip()
            email = email_var.get().strip()
            password = password_var.get().strip()
            if manager_name and email and password:
                database.add_manager(
                    manager_name, email, hash_string_sha256(password), int(hall_id)
                )
                messagebox.showinfo("Успех", f"Менеджер '{manager_name}' добавлен в {hall_name}.")
                self.admin_managers_menu()
            else:
                messagebox.showwarning("Ошибка", "Введите имя менеджера.")

        tk.Button(self, text="Подтвердить", width=30, command=confirm_name).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_managers_choose_office).pack(
            pady=10
        )

    def admin_managers_delete(self):
        """
        Экран удаления менеджера.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Удаление менеджера", font=("Arial", 24)).pack(pady=20)

        # Поле для ввода имени менеджера
        tk.Label(self, text="Введите имя менеджера:").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(self, textvariable=name_var).pack(pady=10)

        # Кнопка "Удалить"
        def delete_manager():
            manager_name = name_var.get().strip()
            try:
                if manager_name:
                    database.delete_manager(manager_name)
                    messagebox.showinfo("Успех", f"Менеджер '{manager_name}' удален.")
                    self.admin_managers_menu()
                else:
                    messagebox.showwarning("Ошибка", "Введите имя менеджера.")
            except exceptions.DbError as ex:
                messagebox.showwarning("Ошибка", ex)

        tk.Button(self, text="Удалить", width=30, command=delete_manager).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_managers_menu).pack(pady=10)

    # Управление залами

    def admin_offices_menu(self):
        self.clear_screen()

        tk.Label(self, text="Залы", font=("Arial", 24)).pack(pady=20)

        tk.Button(self, text="Добавить", width=30, command=self.admin_offices_add).pack(pady=5)
        tk.Button(self, text="Удалить", width=30, command=self.admin_offices_delete).pack(pady=5)
        tk.Button(self, text="назад", command=self.show_admin_menu, width=30).pack(pady=5)

    def admin_offices_add(self):
        self.clear_screen()

        # Поле для названия зала
        tk.Label(self, text="Введите название зала:").pack(pady=5)
        office_name = tk.StringVar()
        tk.Entry(self, textvariable=office_name).pack(pady=10)

        # Поле для адреса зала
        tk.Label(self, text="Введите адрес зала:").pack(pady=5)
        office_address = tk.StringVar()
        tk.Entry(self, textvariable=office_address).pack(pady=10)

        # Поле для времени открытия зала
        tk.Label(self, text="Введите время открытия зала (чч:мм):").pack(pady=5)
        office_open_time = tk.StringVar()
        tk.Entry(self, textvariable=office_open_time).pack(pady=10)

        # Поле для времени открытия зала
        tk.Label(self, text="Введите время закрытия зала (чч:мм):").pack(pady=5)
        office_close_time = tk.StringVar()
        tk.Entry(self, textvariable=office_close_time).pack(pady=10)

        # Поле для коэффицента стоимости зала
        tk.Label(self, text="Введите коэффицент стоимости зала:").pack(pady=5)
        office_cost_ratio = tk.StringVar()
        tk.Entry(self, textvariable=office_cost_ratio).pack(pady=10)

        def admin_offices_add_confirm():
            try:
                name = office_name.get()
                address = office_address.get()
                open_time = office_open_time.get()
                close_time = office_close_time.get()
                cost_ratio = office_cost_ratio.get()

                database.add_sportcenter(name, address, open_time, close_time, cost_ratio)
                messagebox.showinfo("Успех", f"Зал {name} добавлен")
                self.admin_offices_menu()

            except exceptions.DbError as ex:
                messagebox.showwarning(title="Ошибка", message=str(ex))
            except Exception as ex:
                messagebox.showwarning(title="Ошибка", message=str(ex))

        tk.Button(self, text="Добавить", width=30, command=admin_offices_add_confirm).pack(pady=5)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_offices_menu).pack(pady=10)

    def admin_offices_delete(self):
        self.clear_screen()

        tk.Label(self, text="Удаление зала", font=("Arial", 24)).pack(pady=20)

        # Массив залов

        halls = database.get_table(DbTable.SPORTCENTER)
        logger.debug(halls)

        hall_names = [hall[1] for hall in halls]

        # Список с залами
        tk.Label(self, text="Выберите спортзал:").pack(pady=5)
        hall_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=hall_names), height=len(hall_names)
        )
        hall_list.pack(pady=10)

        def confirm_delete_office():
            try:
                index = hall_list.curselection()[0]

                # Находим ID выбранного спортзала
                selected_id = halls[index][0]

                # Удаляем спортзал по ID
                database.delete_sportcenter(selected_id)
                messagebox.showinfo("Спортцентр удален")
                self.admin_offices_menu()
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите спортзал.")

        tk.Button(self, text="Удалить", width=30, command=confirm_delete_office).pack(pady=5)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_managers_menu).pack(pady=10)

    # Управление услугами

    def admin_services_menu(self):
        self.clear_screen()

        tk.Label(self, text="Услуги", font=("Arial", 24)).pack(pady=20)

        tk.Button(self, text="Добавить", width=30, command=self.admin_services_add).pack(pady=5)
        tk.Button(self, text="Удалить", width=30, command=self.admin_services_delete).pack(pady=5)
        tk.Button(self, text="назад", command=self.show_admin_menu, width=30).pack(pady=5)

    def admin_services_add(self):
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Добавление услуги", font=("Arial", 24)).pack(pady=20)

        # Поле для ввода имени
        tk.Label(self, text="Введите название услуги:").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(self, textvariable=name_var).pack(pady=10)

        # Поле для ввода cost
        tk.Label(self, text="Введите стоимость услуги:").pack(pady=5)
        cost_var = tk.StringVar()
        tk.Entry(self, textvariable=cost_var).pack(pady=10)

        # Кнопка "Подтвердить"
        def confirm_service():
            service = name_var.get().strip()
            cost = cost_var.get()
            try:
                if service and cost.isdigit():
                    messagebox.showinfo("Успех", f"Услуга '{service}' добавлена.")

                    database.add_service(service, int(cost))

                    self.admin_services_menu()
                else:
                    messagebox.showwarning("Ошибка", "Введите название услуги.")
            except exceptions.DbError as ex:
                messagebox.showwarning("Oшибка", ex)

        tk.Button(self, text="Подтвердить", width=30, command=confirm_service).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_services_menu).pack(pady=10)

    def admin_services_delete(self):
        self.clear_screen()

        tk.Label(self, text="Удаление услуг", font=("Arial", 24)).pack(pady=20)

        services = database.get_table(DbTable.SERVICE)
        logger.debug(services)
        services_names = [service[1] for service in services]

        tk.Label(self, text="Выберите услугу:").pack(pady=5)
        services_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=services_names), height=len(services_names)
        )
        services_list.pack(pady=10)

        def confirm_delete_service():
            try:
                index = services_list.curselection()[0]

                selected_id = services[index][0]
                database.delete_service(int(selected_id))
                messagebox.showinfo("Услуга удалена")

                self.admin_services_menu()
            except exceptions.DbError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите услугу.")

        tk.Button(self, text="Удалить", width=30, command=confirm_delete_service).pack(pady=5)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_services_menu).pack(pady=10)

    # Управление тарифами

    def admin_plans_menu(self):
        """
        Меню управления тарифами.
        """
        self.clear_screen()

        tk.Label(self, text="Тарифы", font=("Arial", 24)).pack(pady=20)

        tk.Button(self, text="Добавить", width=30, command=self.admin_plans_choose_office).pack(
            pady=5
        )
        tk.Button(self, text="Удалить", width=30, command=self.admin_plans_delete).pack(pady=5)
        tk.Button(self, text="Назад", command=self.show_admin_menu, width=30).pack(pady=5)

    def admin_plans_choose_office(self):
        """
        Выбор зала для тарифа.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Выберите зал для тарифа", font=("Arial", 24)).pack(pady=20)

        # Массив залов
        halls = database.get_table(DbTable.SPORTCENTER)
        halls_names = [hall[1] for hall in halls]

        # Список залов
        hall_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=halls_names), height=len(halls_names)
        )
        hall_list.pack(pady=10)

        # Кнопка "Выбрать"
        def confirm_hall():
            try:
                index = hall_list.curselection()[0]
                hall_id = halls[index][0]
                self.admin_plans_choose_services(halls[index][1], hall_id)
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите зал.")
            except exceptions.DbError as ex:
                messagebox.showwarning(ex)

        tk.Button(self, text="Выбрать", width=30, command=confirm_hall).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_plans_menu).pack(pady=10)

    def admin_plans_choose_services(self, hall_name, hall_id):
        """
        Выбор услуг для тарифа.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text=f"Услуги для тарифа в {hall_name}", font=("Arial", 24)).pack(pady=20)

        # Массив услуг
        services = database.get_table(DbTable.SERVICE)
        services_names = [service[1] for service in services]

        # Список услуг с множественным выбором
        selected_services = []
        service_list = tk.Listbox(
            self,
            selectmode=tk.MULTIPLE,
            listvariable=tk.StringVar(value=services_names),
            height=len(services_names),
        )
        service_list.pack(pady=10)

        # Кнопка "Выбрать"
        def confirm_services():
            selected_indices = service_list.curselection()
            if selected_indices:
                for index in selected_indices:
                    selected_services.append(services[index][0])
                self.admin_plans_add_details(hall_name, hall_id, selected_services)
            else:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите хотя бы одну услугу.")

        tk.Button(self, text="Выбрать", width=30, command=confirm_services).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(
            self, text="Назад", width=30, command=lambda: self.admin_plans_choose_office()
        ).pack(pady=10)

    def admin_plans_add_details(self, hall_name, hall_id, selected_services):
        """
        Ввод параметров тарифа.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text=f"Параметры тарифа для {hall_name}", font=("Arial", 24)).pack(pady=20)

        # tk.Label(self, text=f"Выбранные услуги: {', '.join(selected_services)}").pack(pady=10)

        # Поля для ввода параметров
        tk.Label(self, text="Базовая цена:").pack(pady=5)
        base_price_var = tk.StringVar()
        tk.Entry(self, textvariable=base_price_var).pack(pady=5)

        tk.Label(self, text="Время начала (чч:мм):").pack(pady=5)
        start_time_var = tk.StringVar()
        tk.Entry(self, textvariable=start_time_var).pack(pady=5)

        tk.Label(self, text="Время окончания (чч:мм):").pack(pady=5)
        end_time_var = tk.StringVar()
        tk.Entry(self, textvariable=end_time_var).pack(pady=5)

        # Кнопка "Добавить"
        def confirm_details():
            base_price = base_price_var.get().strip()
            start_time = start_time_var.get().strip()
            end_time = end_time_var.get().strip()

            if not base_price or not start_time or not end_time:
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")
                return

            try:
                database.add_plan(
                    int(base_price), start_time, end_time, hall_id, selected_services
                )
                messagebox.showinfo(
                    "Успех",
                    f"Тариф добавлен:\nЗал: {hall_name}\nВремя: {start_time} - {end_time}",
                )
                self.admin_plans_menu()
            except exceptions.DbError as ex:
                messagebox.showwarning(ex)
                self.admin_plans_menu()
                return

        tk.Button(self, text="Добавить", width=30, command=confirm_details).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(
            self,
            text="Назад",
            width=30,
            command=lambda: self.admin_plans_choose_services(hall_name),
        ).pack(pady=10)

    def admin_plans_delete(self):
        """
        Меню удаления тарифов.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Удаление тарифа", font=("Arial", 24)).pack(pady=20)

        # Массив залов
        halls = database.get_table(DbTable.SPORTCENTER)
        halls_names = [hall[1] for hall in halls]

        # Список залов
        hall_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=halls_names), height=len(halls_names)
        )
        hall_list.pack(pady=10)

        # Кнопка "Выбрать"
        def confirm_hall():
            try:
                index = hall_list.curselection()[0]
                hall_id = halls[index][0]
                self.admin_plans_delete_choose_tariff(halls[index][1], hall_id)
            except exceptions.DbError as ex:
                messagebox.showwarning(ex)
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите зал.")

        tk.Button(self, text="Выбрать", width=30, command=confirm_hall).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_plans_menu).pack(pady=10)

    def admin_plans_delete_choose_tariff(self, hall_name, hall_id):
        """
        Выбор тарифа для удаления.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text=f"Удаление тарифа из {hall_name}", font=("Arial", 24)).pack(pady=20)

        # Массив тарифов
        try:
            tariffs = database.get_table(DbTable.PLAN, hall_id)
        except exceptions.DbError as ex:
            messagebox.showwarning(message=ex)
            self.admin_plans_menu()
            return
        # Список тарифов
        tariff_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=tariffs), height=len(tariffs), width=50
        )
        tariff_list.pack(pady=10)

        # Кнопка "Удалить"
        def confirm_delete():
            try:
                index = tariff_list.curselection()[0]
                selected_tariff_id = tariffs[index][0]
                tariff_name = tariffs[index][1]
                database.delete_plan(selected_tariff_id)
                messagebox.showinfo("Успех", f"Тариф '{tariff_name}' из {hall_name} удален.")
                self.admin_plans_menu()
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите тариф для удаления.")

        tk.Button(self, text="Удалить", width=30, command=confirm_delete).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_plans_delete).pack(pady=10)

    # Просмотр

    def admin_view_menu(self):
        """Меню просмотра данных."""
        self.clear_screen()

        tk.Label(self, text="Просмотр", font=("Arial", 24)).pack(pady=20)

        tk.Button(self, text="Менеджеры", width=30, command=self.admin_view_managers).pack(pady=5)
        tk.Button(self, text="Залы", width=30, command=self.admin_view_halls).pack(pady=5)
        tk.Button(self, text="Услуги", width=30, command=self.admin_view_services).pack(pady=5)
        tk.Button(self, text="Клиенты", width=30, command=self.admin_view_clients).pack(pady=5)

        tk.Button(self, text="Назад", width=30, command=self.show_admin_menu).pack(pady=5)

    def create_table(self, columns, data):
        """
        Создает таблицу Treeview с прокруткой.

        :param columns: Список столбцов таблицы.
        :param data: Данные для заполнения таблицы (список словарей).
        :return: Объект Treeview.
        """
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, pady=10)

        # Создаем Treeview
        tree = ttk.Treeview(container, columns=columns, show="headings", height=15)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Прокрутка
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        # Настраиваем столбцы
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor=tk.W)

        # Заполняем таблицу
        for row in data:
            tree.insert("", tk.END, values=[row[col] for col in columns])

        return tree

    def admin_view_managers(self):
        """Просмотр списка менеджеров."""
        self.clear_screen()

        tk.Label(self, text="Менеджеры", font=("Arial", 24)).pack(pady=20)

        # Пример данных
        try:
            managers_db = database.get_table(DbTable.MANAGER)
        except exceptions.DbError as ex:
            messagebox.showwarning(message=ex)
            self.admin_view_menu()
            return
        logger.debug(managers_db)
        managers = []
        for manager in managers_db:
            managers.append({"ФИО": manager[0], "Email": manager[2], "Зал": manager[4]})

        logger.debug(managers)

        # Создаем таблицу
        columns = ["ФИО", "Email", "Зал"]
        self.create_table(columns, managers)

        def delete_table_from_db():
            database.drop_table(DbTable.MANAGER)
            messagebox.showinfo("Удаление", "Таблица менеджеров успешно удалена.")
            self.quit()

        # Кнопка "Удалить таблицу"
        tk.Button(
            self,
            text="Удалить таблицу",
            width=30,
            command=delete_table_from_db,
        ).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_view_menu).pack(pady=10)

    def admin_view_halls(self):
        """Просмотр списка залов."""
        self.clear_screen()

        tk.Label(self, text="Залы", font=("Arial", 24)).pack(pady=20)

        # Пример данных
        try:
            halls_db = database.get_table(DbTable.SPORTCENTER)
        except exceptions.DbError as ex:
            messagebox.showwarning(message=ex)
            self.admin_view_menu()
            return
        logger.debug(halls_db)
        halls = []

        for hall in halls_db:
            halls.append(
                {
                    "Назваиние": hall[1],
                    "Адрес": hall[2],
                    # "Открытие": hall[2],
                    # "Закртыие": hall[3],
                    # "Коэфф. стоимости": hall[4],
                }
            )

        # Создаем таблицу
        columns = ["Назваиние", "Адрес"]  # "Открытие", "Закртыие", "Коэфф. стоимости"]
        self.create_table(columns, halls)

        def delete_table_from_db():
            database.drop_table(DbTable.SPORTCENTER)
            messagebox.showinfo("Удаление", "Таблица залов успешно удалена.")
            self.quit()

        # Кнопка "Удалить таблицу"
        tk.Button(
            self,
            text="Удалить таблицу",
            width=30,
            command=delete_table_from_db,
        ).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_view_menu).pack(pady=10)

    def admin_view_services(self):
        """Просмотр списка услуг."""
        self.clear_screen()

        tk.Label(self, text="Услуги", font=("Arial", 24)).pack(pady=20)

        # Пример данных
        try:
            services_db = database.get_table(DbTable.SERVICE)
        except exceptions.DbError as ex:
            messagebox.showwarning(message=ex)
            self.admin_view_menu()
            return
        logger.debug(services_db)
        services = [{"Услуга": service[1], "Стоимость": service[2]} for service in services_db]

        # Создаем таблицу
        columns = ["Услуга", "Стоимость"]
        self.create_table(columns, services)

        def delete_table_from_db():
            database.drop_table(DbTable.SPORTCENTER)
            messagebox.showinfo("Удаление", "Таблица услуг успешно удалена.")
            self.quit()

        # Кнопка "Удалить таблицу"
        tk.Button(
            self,
            text="Удалить таблицу",
            width=30,
            command=delete_table_from_db,
        ).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_view_menu).pack(pady=10)

    def admin_view_clients(self):
        """Просмотр списка клиентов."""
        self.clear_screen()

        tk.Label(self, text="Клиенты", font=("Arial", 24)).pack(pady=20)

        # Пример данных
        try:
            clients_db = database.get_table(DbTable.CLIENT)
        except exceptions.DbError as ex:
            messagebox.showwarning(message=ex)
            self.admin_view_menu()
            return
        logger.debug(clients_db)
        clients = [
            {"ФИО": client[1], "Баланс": client[2], "Дата регистрации": client[3]}
            for client in clients_db
        ]

        # Создаем таблицу
        columns = ["ФИО", "Баланс", "Дата регистрации"]
        self.create_table(columns, clients)

        def delete_table_from_db():
            database.drop_table(DbTable.SPORTCENTER)
            messagebox.showinfo("Удаление", "Таблица клиентов успешно удалена.")
            self.quit()

        # Кнопка "Удалить таблицу"
        tk.Button(
            self,
            text="Удалить таблицу",
            width=30,
            command=delete_table_from_db,
        ).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_view_menu).pack(pady=10)

    # удаление всего

    def admin_delete_menu(self):
        self.clear_screen()

        tk.Label(self, text="Удаление", font=("Arial", 24)).pack(pady=20)

        def delete_all_tables():
            database.drop_table()
            messagebox.showinfo("Удаление", "Все таблицы удалены")
            database.close()
            self.quit()

        tk.Button(self, text="Удалить все таблицы", width=30, command=delete_all_tables).pack(
            pady=5
        )

        def delete_db():
            database.drop_db()
            messagebox.showinfo("Удаление", "Всё...")
            database.close()
            self.quit()

        tk.Button(self, text="Удалить БД", width=30, command=delete_db).pack(pady=5)

        tk.Button(self, text="Назад", width=30, command=self.show_admin_menu).pack(pady=5)

    #
    # ---
    #

    # менеджерская часть

    def show_manager_menu(self):
        """
        Отображает меню менеджера.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Меню менеджера", font=("Arial", 24)).pack(pady=20)

        # Отображение имени пользователя
        tk.Label(self, text=f"Добро пожаловать, {self.user_data['username']}").pack(pady=10)

        # Кнопки
        tk.Button(self, text="Тарифы", width=30, command=self.manager_plan_services).pack(pady=5)
        tk.Button(self, text="Услуги", width=30, command=self.manager_services).pack(pady=5)
        tk.Button(self, text="Залы", width=30, command=self.manager_offices).pack(pady=5)
        tk.Button(self, text="Клиенты", width=30, command=self.manager_clients_menu).pack(pady=5)
        tk.Button(self, text="Выйти", width=30, command=self.show_login_screen).pack(pady=20)

    # просмотр услуг
    def manager_services(self):
        self.clear_screen()

        tk.Label(self, text="Услуги", font=("Arial", 24)).pack(pady=20)

        # Пример данных
        try:
            services_db = database.get_table(DbTable.SERVICE)
        except exceptions.DbError as ex:
            messagebox.showwarning(message=ex)
            self.show_manager_menu()
            return
        logger.debug(services_db)
        services = [{"Услуга": service[1], "Стоимость": service[2]} for service in services_db]

        # Создаем таблицу
        columns = ["Услуга", "Стоимость"]
        self.create_table(columns, services)

        tk.Button(self, text="Назад", width=30, command=self.show_manager_menu).pack(pady=5)

    # выбор услуг для подбора тарифа
    def manager_plan_services(self):
        self.clear_screen()

        # Заголовок
        tk.Label(self, text="Услуги для побдора тарифа", font=("Arial", 24)).pack(pady=20)

        # Массив услуг
        services = database.get_table(DbTable.SERVICE)
        services_names = [service[1] for service in services]

        # Список услуг с множественным выбором
        selected_services = []
        service_list = tk.Listbox(
            self,
            selectmode=tk.MULTIPLE,
            listvariable=tk.StringVar(value=services_names),
            height=len(services_names),
        )
        service_list.pack(pady=10)

        # Кнопка "Выбрать"
        def confirm_services():
            selected_indices = service_list.curselection()
            if selected_indices:
                for index in selected_indices:
                    selected_services.append(services[index][0])
                self.manager_plan_get(selected_services)
            else:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите хотя бы одну услугу.")

        tk.Button(self, text="Выбрать", width=30, command=confirm_services).pack(pady=10)

    def manager_plan_get(self, services):
        self.clear_screen()
        logger.debug(services)

        tk.Label(self, text="Тарифы с выбранными услугами", font=("Arial", 24)).pack(pady=20)

        try:
            plans_db = database.get_table(DbTable.PLAN, services)
        except exceptions.DbError as ex:
            messagebox.showwarning(ex)
            self.show_manager_menu()
            return
        except Exception as ex:
            messagebox.showwarning(ex)
            self.show_manager_menu()
            return

        logger.debug(plans_db)
        plans = [
            {
                "Стоимость": service[1],
                "Начало": service[2],
                "Окончание": service[3],
                "Услуги": service[4],
                "Зал": service[5],
                "Адрес": service[6],
            }
            for service in plans_db
        ]

        # Создаем таблицу
        columns = ["Стоимость", "Начало", "Окончание", "Услуги", "Зал", "Адрес"]
        self.create_table(columns, plans)

        tk.Button(self, text="Назад", width=30, command=self.show_manager_menu).pack(pady=10)

    def manager_offices(self):
        self.clear_screen()

        tk.Label(self, text="Выьерите зал для просмотра тарифов", font=("Arial", 24)).pack(pady=20)

        # Массив залов
        halls = database.get_table(DbTable.SPORTCENTER)
        logger.debug(halls)

        hall_names = [hall[1] for hall in halls]

        # Список с залами
        tk.Label(self, text="Выберите спортзал:").pack(pady=5)
        hall_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=hall_names), height=len(hall_names)
        )
        hall_list.pack(pady=10)

        def choose_office():
            try:
                index = hall_list.curselection()[0]

                # Находим ID выбранного спортзала
                selected_id = halls[index][0]

                self.manager_plans_for_office(selected_id)
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите спортзал.")

        tk.Button(self, text="Выбрать", width=30, command=choose_office).pack(pady=10)

    def manager_plans_for_office(self, office_id):
        self.clear_screen()
        tk.Label(self, text="Зал и его тарифы", font=("Arial", 24)).pack(pady=20)

        try:
            office = database.get_table(DbTable.SPORTCENTER, office_id)[0]
            tk.Label(self, text=str(office)).pack(pady=5)

            tk.Label(self, text="Тарифы с выбранными услугами", font=("Arial", 24)).pack(pady=20)
            plans_db = database.get_table(DbTable.PLAN, office_id)
            logger.debug(plans_db)
        except exceptions.DbError as ex:
            messagebox.showwarning(ex)
            self.show_manager_menu()
        except Exception as ex:
            messagebox.showwarning(ex)
            self.show_manager_menu()

        logger.debug(plans_db)
        plans = [
            {
                "Стоимость": plan[1],
                "Начало": plan[2],
                "Окончание": plan[3],
                "Услуги": plan[4],
            }
            for plan in plans_db
        ]

        # Создаем таблицу
        columns = ["Стоимость", "Начало", "Окончание", "Услуги"]
        self.create_table(columns, plans)

        tk.Button(self, text="Назад", width=30, command=self.show_manager_menu).pack(pady=10)

    # Клиенты

    def manager_clients_menu(self):
        self.clear_screen()
        database.get_table(DbTable.CLIENT, "")

        # Заголовок
        tk.Label(self, text="Клиенты", font=("Arial", 24)).pack(pady=20)

        # Кнопки
        tk.Button(
            self, text="Добавить клиента в базу", width=30, command=self.manager_clients_add_client
        ).pack(pady=5)
        tk.Button(
            self,
            text="Добавить тариф для клиента",
            width=30,
            command=self.manager_clients_add_plan_for_client,
        ).pack(pady=5)
        tk.Button(
            self, text="Найти по ФИО", width=30, command=self.manager_clients_find_name
        ).pack(pady=5)
        tk.Button(
            self,
            text="Изменить тариф у клиента",
            width=30,
            command=self.manager_clietns_change_plane,
        ).pack(pady=5)
        tk.Button(self, text="Передать тариф", width=30).pack(pady=5)
        tk.Button(self, text="Назад", width=30, command=self.show_manager_menu).pack(pady=20)

    def manager_clients_add_plan_for_client(self):
        self.clear_screen()

        tk.Label(self, text="Добавление тариф для клиента", font=("Arial", 24)).pack(pady=20)

        tk.Label(self, text="ФИО").pack(pady=5)
        fullname_var = tk.StringVar()
        tk.Entry(self, textvariable=fullname_var).pack(pady=5)

        tk.Label(self, text="Дата окончания").pack(pady=5)
        date_var = tk.StringVar()
        tk.Entry(self, textvariable=date_var).pack(pady=5)

        # Массив залов
        plans = database.get_table(DbTable.PLAN, self.user_data["sportcenter_id"])
        plans_names = [plan[1] for plan in plans]

        # Список залов
        plan_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=plans_names), height=len(plans_names)
        )
        plan_list.pack(pady=10)

        def change_plan():
            try:
                index = plan_list.curselection()[0]
                plan_id = int(plans[index][0])
                fullname = fullname_var.get().strip()
                day, month, year = date_var.get().split(".")
                end_date = date(int(year), int(month), int(day))

                client = database.get_table(DbTable.CLIENT, fullname)[0]
                logger.debug(client)
                database.set_client_plan(client[0], plan_id, end_date)
                messagebox.showinfo(message="Тариф добавлен")
            except exceptions.DbError as ex:
                messagebox.showwarning(message=ex)
            except Exception as ex:
                messagebox.showwarning(message=ex)

        tk.Button(self, text="Добавить", width=30, command=change_plan).pack(pady=10)

        tk.Button(self, text="Назад", width=30, command=self.manager_clients_menu).pack(pady=20)

    def manager_clients_find_name(self):
        self.clear_screen()

        tk.Label(self, text="Найти по ФИО", font=("Arial", 24)).pack(pady=20)

        tk.Label(self, text="ФИО").pack(pady=5)
        fullname_var = tk.StringVar()
        tk.Entry(self, textvariable=fullname_var).pack(pady=5)

        def find():
            fullname = fullname_var.get().strip()
            self.manager_clients_client_info(fullname)

        tk.Button(self, text="Найти", width=30, command=find).pack(pady=10)
        tk.Button(self, text="Назад", width=30, command=self.manager_clients_menu).pack(pady=20)

    def manager_clients_client_info(self, fullname):
        self.clear_screen()

        try:
            client = database.get_table(DbTable.CLIENT, fullname)[0]
            logger.debug(client)
        except exceptions.DbError as ex:
            messagebox.showwarning(message=ex)
            self.manager_clients_menu()
            return

        tk.Label(self, text="Информация о клиенте", font=("Arial", 24)).pack(pady=20)

        text = ""
        for i in range(1, len(client)):
            text += str(client[i]) + "  "

        tk.Label(self, text=text).pack(pady=5)

        tk.Label(self, text="Сумма для изменения баланса").pack(pady=5)
        edit_balance_var = tk.StringVar()
        tk.Entry(self, textvariable=edit_balance_var).pack(pady=5)

        def increase_balance():
            edit_balance = edit_balance_var.get()

            try:
                database.update_balance(client[0], int(client[2]) + int(edit_balance))
                messagebox.showinfo(message="Баланс изменен")
                self.manager_clients_client_info(fullname)
                return
            except exceptions.DbError as ex:
                messagebox.showwarning(message=ex)
                self.manager_clients_menu()
                return
            except Exception as ex:
                messagebox.showwarning(message=ex)
                self.manager_clients_menu()
                return

        tk.Button(self, text="Начислить", width=30, command=increase_balance).pack(pady=10)

        def decrease_balance():
            edit_balance = edit_balance_var.get()

            try:
                database.update_balance(client[0], int(client[2]) - int(edit_balance))
                messagebox.showinfo(message="Баланс изменен")
                self.manager_clients_client_info(fullname)
                return
            except exceptions.DbError as ex:
                messagebox.showwarning(message=ex)
                self.manager_clients_menu()
                return

        tk.Button(self, text="Снять", width=30, command=decrease_balance).pack(pady=10)

        tk.Button(self, text="Назад", width=30, command=self.manager_clients_menu).pack(pady=20)

    def manager_clietns_change_plane(self):
        self.clear_screen()

        tk.Label(self, text="Изменение тарифа у клиента", font=("Arial", 24)).pack(pady=20)

        tk.Label(self, text="ФИО").pack(pady=5)
        fullname_var = tk.StringVar()
        tk.Entry(self, textvariable=fullname_var).pack(pady=5)

        tk.Label(self, text="Дата окончания").pack(pady=5)
        date_var = tk.StringVar()
        tk.Entry(self, textvariable=date_var).pack(pady=5)

        # Массив залов
        plans = database.get_table(DbTable.PLAN, self.user_data["sportcenter_id"])
        plans_names = [plan[1] for plan in plans]

        # Список залов
        plan_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=plans_names), height=len(plans_names)
        )
        plan_list.pack(pady=10)

        def change_plan():
            try:
                index = plan_list.curselection()[0]
                plan_id = int(plans[index][0])
                fullname = fullname_var.get().strip()
                day, month, year = date_var.get().split(".")
                end_date = date(int(year), int(month), int(day))

                client = database.get_table(DbTable.CLIENT, fullname)[0]
                logger.debug(client)
                database.delete_client_plan(client[0], plan_id)
                database.set_client_plan(client[0], plan_id, end_date)
                messagebox.showinfo(message="Тариф изменен")
            except exceptions.DbError as ex:
                messagebox.showwarning(message=ex)
            except Exception as ex:
                messagebox.showwarning(message=ex)

        tk.Button(self, text="Изменить", width=30, command=change_plan).pack(pady=10)

        tk.Button(self, text="Назад", width=30, command=self.manager_clients_menu).pack(pady=20)

    def manager_clients_add_client(self):
        self.clear_screen()

        tk.Label(self, text="Добавление клиента в базу", font=("Arial", 24)).pack(pady=20)

        tk.Label(self, text="ФИО").pack(pady=5)
        fullname_var = tk.StringVar()
        tk.Entry(self, textvariable=fullname_var).pack(pady=5)

        tk.Label(self, text="Баланс").pack(pady=5)
        balance_var = tk.StringVar()
        tk.Entry(self, textvariable=balance_var).pack(pady=5)

        def add_client():
            fullname = fullname_var.get().strip()
            balance = balance_var.get().strip()

            try:
                database.add_client(fullname)
                client_id = database.get_table(DbTable.CLIENT, fullname)[0][0]
                database.update_balance(client_id, int(balance))

            except exceptions.DbError as ex:
                messagebox.showwarning(message=ex)
            except Exception as ex:
                messagebox.showwarning(message=ex)

        tk.Button(self, text="Добавить", width=30, command=add_client).pack(pady=10)

        tk.Button(self, text="Назад", width=30, command=self.manager_clients_menu).pack(pady=20)

    # закртыть приложение
    def on_close(self):
        """
        Обработчик закрытия приложения.
        """
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти из приложения?"):
            # Здесь можно сохранить данные или выполнить другие действия перед выходом
            database.close()
            self.destroy()
