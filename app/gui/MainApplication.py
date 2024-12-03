import tkinter as tk
from tkinter import messagebox, ttk


class MainApplication(tk.Tk):
    """Главное окно приложения, обеспечивающее навигацию между экранами."""

    def __init__(self):
        super().__init__()
        self.title("Fitness Client Panel")
        self.geometry("800x600")  # Устанавливаем начальный размер
        self.user_data = {"username": None, "role": None}  # Хранение данных пользователя

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

        # Кнопка входа
        def login():
            login = login_var.get()
            password = password_var.get()

            if login == "admin" and password == "admin":
                self.user_data["username"] = "Администратор"
                self.user_data["role"] = "admin"
                self.show_admin_menu()
            elif login == "manager" and password == "manager":
                self.user_data["username"] = "Менеджер"
                self.user_data["role"] = "manager"
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
        tk.Label(self, text="Выбор спортзала", font=("Arial", 24)).pack(pady=20)

        # Массив залов
        halls = ["Зал 1", "Зал 2", "Зал 3", "Зал 4"]

        # Переменная для хранения выбранного зала
        selected_hall = tk.StringVar(value="")

        # Список с залами
        tk.Label(self, text="Выберите спортзал:").pack(pady=5)
        hall_list = tk.Listbox(self, listvariable=tk.StringVar(value=halls), height=len(halls))
        hall_list.pack(pady=10)

        # Кнопка "Подтвердить"
        def confirm_hall():
            try:
                index = hall_list.curselection()[0]
                selected_hall.set(halls[index])
                self.admin_managers_input_name(selected_hall.get())
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите спортзал.")

        tk.Button(self, text="Подтвердить", width=30, command=confirm_hall).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_managers_menu).pack(pady=10)

    def admin_managers_input_name(self, hall_name):
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

        # Кнопка "Подтвердить"
        def confirm_name():
            manager_name = name_var.get().strip()
            if manager_name:
                messagebox.showinfo("Успех", f"Менеджер '{manager_name}' добавлен в {hall_name}.")
                self.show_admin_menu()
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
            if manager_name:
                # Здесь будет логика удаления менеджера
                messagebox.showinfo("Успех", f"Менеджер '{manager_name}' удален.")
                self.show_admin_menu()
            else:
                messagebox.showwarning("Ошибка", "Введите имя менеджера.")

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
        office_adress = tk.StringVar()
        tk.Entry(self, textvariable=office_adress).pack(pady=10)

        # Поле для времени открытия зала
        tk.Label(self, text="Введите время открытия зала:").pack(pady=5)
        office_open_time = tk.StringVar()
        tk.Entry(self, textvariable=office_open_time).pack(pady=10)

        # Поле для времени открытия зала
        tk.Label(self, text="Введите время закрытия зала:").pack(pady=5)
        office_close_time = tk.StringVar()
        tk.Entry(self, textvariable=office_close_time).pack(pady=10)

        # Поле для коэффицента стоимости зала
        tk.Label(self, text="Введите коэффицент стоимости зала:").pack(pady=5)
        office_cost_ratio = tk.StringVar()
        tk.Entry(self, textvariable=office_cost_ratio).pack(pady=10)

        def admin_offices_add_confirm():
            pass

        tk.Button(self, text="Добавить", width=30, command=admin_offices_add_confirm).pack(pady=5)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_offices_menu).pack(pady=10)

    def admin_offices_delete(self):
        self.clear_screen()

        tk.Label(self, text="Удаление зала", font=("Arial", 24)).pack(pady=20)

        # Массив залов
        halls = ["Зал 1", "Зал 2", "Зал 3", "Зал 4"]

        # Переменная для хранения выбранного зала
        selected_hall = tk.StringVar(value="")

        # Список с залами
        tk.Label(self, text="Выберите спортзал:").pack(pady=5)
        hall_list = tk.Listbox(self, listvariable=tk.StringVar(value=halls), height=len(halls))
        hall_list.pack(pady=10)

        def confirm_delete_office():
            try:
                index = hall_list.curselection()[0]
                selected_hall.set(halls[index])
                self.show_admin_menu()
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
        tk.Button(self, text="Удалить", width=30, command=self.admin_offices_delete).pack(pady=5)
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
            if service:
                messagebox.showinfo("Успех", f"Услуга '{service}' добавлена.")
                self.show_admin_menu()
            else:
                messagebox.showwarning("Ошибка", "Введите название услуги.")

        tk.Button(self, text="Подтвердить", width=30, command=confirm_service).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_services_menu).pack(pady=10)

    def admin_services_delete(self):
        self.clear_screen()

        tk.Label(self, text="Удаление услуг", font=("Arial", 24)).pack(pady=20)

        services = [
            "возможность 1",
            "возможность 2",
            "возможность 3",
            "возможность 4",
            "возможность 5",
            "возможность 6",
            "возможность 7",
        ]

        service = tk.StringVar(value="")

        tk.Label(self, text="Выберите услугу:").pack(pady=5)
        hall_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=services), height=len(services)
        )
        hall_list.pack(pady=10)

        def confirm_delete_service():
            try:
                index = hall_list.curselection()[0]
                service.set(services[index])
                self.show_admin_menu()
            except IndexError:
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
        tk.Label(self, text="Выберите зал", font=("Arial", 24)).pack(pady=20)

        # Массив залов
        halls = ["Зал 1", "Зал 2", "Зал 3", "Зал 4"]

        # Список залов
        selected_hall = tk.StringVar(value="")
        hall_list = tk.Listbox(self, listvariable=tk.StringVar(value=halls), height=len(halls))
        hall_list.pack(pady=10)

        # Кнопка "Выбрать"
        def confirm_hall():
            try:
                index = hall_list.curselection()[0]
                selected_hall.set(halls[index])
                self.admin_plans_choose_services(selected_hall.get())
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите зал.")

        tk.Button(self, text="Выбрать", width=30, command=confirm_hall).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_plans_menu).pack(pady=10)

    def admin_plans_choose_services(self, hall_name):
        """
        Выбор услуг для тарифа.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text=f"Услуги для {hall_name}", font=("Arial", 24)).pack(pady=20)

        # Массив услуг
        services = ["Йога", "Тренажерный зал", "Кардио", "Плавание"]

        # Список услуг с множественным выбором
        selected_services = []
        service_list = tk.Listbox(
            self,
            selectmode=tk.MULTIPLE,
            listvariable=tk.StringVar(value=services),
            height=len(services),
        )
        service_list.pack(pady=10)

        # Кнопка "Выбрать"
        def confirm_services():
            selected_indices = service_list.curselection()
            if selected_indices:
                for index in selected_indices:
                    selected_services.append(services[index])
                self.admin_plans_add_details(hall_name, selected_services)
            else:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите хотя бы одну услугу.")

        tk.Button(self, text="Выбрать", width=30, command=confirm_services).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(
            self, text="Назад", width=30, command=lambda: self.admin_plans_choose_office()
        ).pack(pady=10)

    def admin_plans_add_details(self, hall_name, selected_services):
        """
        Ввод параметров тарифа.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text=f"Параметры тарифа для {hall_name}", font=("Arial", 24)).pack(pady=20)

        tk.Label(self, text=f"Выбранные услуги: {', '.join(selected_services)}").pack(pady=10)

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

            messagebox.showinfo(
                "Успех",
                f"Тариф добавлен:\nЗал: {hall_name}\nУслуги: {', '.join(selected_services)}\nЦена:\
 {base_price}\nВремя: {start_time} - {end_time}",
            )
            self.admin_plans_menu()

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
        halls = ["Зал 1", "Зал 2", "Зал 3", "Зал 4"]

        # Список залов
        selected_hall = tk.StringVar(value="")
        hall_list = tk.Listbox(self, listvariable=tk.StringVar(value=halls), height=len(halls))
        hall_list.pack(pady=10)

        # Кнопка "Выбрать"
        def confirm_hall():
            try:
                index = hall_list.curselection()[0]
                selected_hall.set(halls[index])
                self.admin_plans_delete_choose_tariff(selected_hall.get())
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите зал.")

        tk.Button(self, text="Выбрать", width=30, command=confirm_hall).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_plans_menu).pack(pady=10)

    def admin_plans_delete_choose_tariff(self, hall_name):
        """
        Выбор тарифа для удаления.
        """
        self.clear_screen()

        # Заголовок
        tk.Label(self, text=f"Удаление тарифа из {hall_name}", font=("Arial", 24)).pack(pady=20)

        # Массив тарифов (пример)
        tariffs = ["Тариф 1", "Тариф 2", "Тариф 3"]

        # Список тарифов
        selected_tariff = tk.StringVar(value="")
        tariff_list = tk.Listbox(
            self, listvariable=tk.StringVar(value=tariffs), height=len(tariffs)
        )
        tariff_list.pack(pady=10)

        # Кнопка "Удалить"
        def confirm_delete():
            try:
                index = tariff_list.curselection()[0]
                selected_tariff.set(tariffs[index])
                tariff_name = selected_tariff.get()
                # Удаляем тариф (в реальной реализации подключите базу данных или API)
                messagebox.showinfo("Успех", f"Тариф '{tariff_name}' из {hall_name} удален.")
                self.show_admin_menu()
            except IndexError:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите тариф для удаления.")

        tk.Button(self, text="Удалить", width=30, command=confirm_delete).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_plans_delete).pack(pady=10)

    # Просмотр

    def delete_table_from_db(self, table_name):
        """
        Удаляет таблицу из базы данных.
        """
        # Здесь будет логика удаления таблицы из БД
        messagebox.showinfo("Удаление", f"Таблица '{table_name}' успешно удалена.")
        pass

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
        managers = [
            {"ФИО": "Иванов Иван Иванович", "Email": "ivanov@example.com"},
            {"ФИО": "Петров Петр Петрович", "Email": "petrov@example.com"},
        ]

        # Создаем таблицу
        columns = ["ФИО", "Email"]
        self.create_table(columns, managers)

        # Кнопка "Удалить таблицу"
        tk.Button(
            self,
            text="Удалить таблицу",
            width=30,
            command=lambda: self.delete_table_from_db("managers"),
        ).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_view_menu).pack(pady=10)

    def admin_view_halls(self):
        """Просмотр списка залов."""
        self.clear_screen()

        tk.Label(self, text="Залы", font=("Arial", 24)).pack(pady=20)

        # Пример данных
        halls = [
            {"Зал": "Зал 1", "Адрес": "ул. Ленина, 1"},
            {"Зал": "Зал 2", "Адрес": "ул. Советская, 10"},
        ]

        # Создаем таблицу
        columns = ["Зал", "Адрес"]
        self.create_table(columns, halls)

        # Кнопка "Удалить таблицу"
        tk.Button(
            self,
            text="Удалить таблицу",
            width=30,
            command=lambda: self.delete_table_from_db("halls"),
        ).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_view_menu).pack(pady=10)

    def admin_view_services(self):
        """Просмотр списка услуг."""
        self.clear_screen()

        tk.Label(self, text="Услуги", font=("Arial", 24)).pack(pady=20)

        # Пример данных
        services = [
            {"Услуга": "Йога", "Цена": "500 руб"},
            {"Услуга": "Тренажерный зал", "Цена": "1000 руб"},
        ]

        # Создаем таблицу
        columns = ["Услуга", "Цена"]
        self.create_table(columns, services)

        # Кнопка "Удалить таблицу"
        tk.Button(
            self,
            text="Удалить таблицу",
            width=30,
            command=lambda: self.delete_table_from_db("services"),
        ).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_view_menu).pack(pady=10)

    def admin_view_clients(self):
        """Просмотр списка клиентов."""
        self.clear_screen()

        tk.Label(self, text="Клиенты", font=("Arial", 24)).pack(pady=20)

        # Пример данных
        clients = [
            {"ФИО": "Сидоров Сидр Сидорович"},
            {"ФИО": "Александров Александр Александрович"},
        ]

        # Создаем таблицу
        columns = ["ФИО"]
        self.create_table(columns, clients)

        # Кнопка "Удалить таблицу"
        tk.Button(
            self,
            text="Удалить таблицу",
            width=30,
            command=lambda: self.delete_table_from_db("clients"),
        ).pack(pady=10)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", width=30, command=self.admin_view_menu).pack(pady=10)

    # удаление всего

    def admin_delete_menu(self):
        self.clear_screen()

        tk.Label(self, text="Удаление", font=("Arial", 24)).pack(pady=20)

        def delete_all_tables():
            pass

        tk.Button(
            self, text="Удалить все таблицы", width=30, command=self.admin_view_services
        ).pack(pady=5)
        tk.Button(self, text="Удалить БД", width=30, command=self.admin_view_clients).pack(pady=5)

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
        tk.Button(self, text="Добавить клиента", width=30).pack(pady=5)
        tk.Button(self, text="Удалить клиента", width=30).pack(pady=5)
        tk.Button(self, text="Просмотр клиентов", width=30).pack(pady=5)
        tk.Button(self, text="Назад", width=30, command=self.show_admin_menu).pack(pady=20)

    # закртыть приложение
    def on_close(self):
        """
        Обработчик закрытия приложения.
        """
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти из приложения?"):
            # Здесь можно сохранить данные или выполнить другие действия перед выходом
            self.destroy()
