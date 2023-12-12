import tkinter as tk
from datetime import datetime
from tkinter import ttk, simpledialog, messagebox
import mysql.connector

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        # Подключение к базе данных MySQL
        self.connection_params = {
            "host": "localhost",
            "user": "root",
            "password": "1234",
            "database": "kursovaya",
            "auth_plugin" : "mysql_native_password"
        }
        self.connection = mysql.connector.connect(**self.connection_params)
        self.cursor = self.connection.cursor()

        # Создание GUI
        self.create_widgets()

        self.last_search = None

    def create_widgets(self):
        # Создание главного фрейма
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Фрейм для вкладок с таблицами
        tabs_frame = tk.Frame(main_frame)
        tabs_frame.pack(side=tk.LEFT, fill="both", expand=True)

        # Создание вкладок
        self.tab_control = ttk.Notebook(tabs_frame)
        tab1 = ttk.Frame(self.tab_control)
        tab2 = ttk.Frame(self.tab_control)
        tab3 = ttk.Frame(self.tab_control)
        tab4 = ttk.Frame(self.tab_control)
        tab5 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab1, text='Dostavka')
        self.tab_control.add(tab2, text='Klient')
        self.tab_control.add(tab3, text='Mebel')
        self.tab_control.add(tab4, text='Prodavec')
        self.tab_control.add(tab5, text='Zakaz')
        self.tab_control.pack(expand=1, fill="both")

        # Стиль для Treeview
        treeview_style = ttk.Style()
        treeview_style.theme_use("default")
        treeview_style.configure("Treeview", background="#545454", fieldbackground="#ffffff", foreground="white")
        treeview_style.map("Treeview", background=[('selected', 'black')])

        # Стиль для рамок ячеек
        treeview_style.layout("Treeview.Item", [('Treeitem.padding',
                                                 {'sticky': 'nswe',
                                                  'children': [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                                                                ('Treeitem.text', {'sticky': 'we'})]})])
        treeview_style.configure("Treeview.Item", borderwidth=1, relief="solid", bordercolor="black")

        # Таблица 1
        self.create_table(tab1, "dostavka",
                          ["ID", "VremyaDostavki", "Nomertelefona", "TipDostavki"])

        # Таблица 2
        self.create_table(tab2, "klient", ["ID", "FIOZakazchika", "Nomertelefona", "Adres"])

        # Таблица 3
        self.create_table(tab3, "mebel", ["ID","Gabariti", "Color", "Materialy", "Ves"])

        # Таблица4
        self.create_table(tab4, "prodavec", ["ID", "FIOProdavca", "Nomertelefona", "Adres"])

        # Таблица5
        self.create_table(tab5, "zakaz", ["ID", "VremyaZakaza", "GabaritiMebeli", "Material"])

        # Фрейм с кнопками
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки для каждой таблицы
        button_width = 15  # Ширина кнопок
        update_button = tk.Button(buttons_frame, text="Обновить", width=button_width, command=self.update_table)
        update_button.pack(side=tk.TOP, pady=5)
        add_button = tk.Button(buttons_frame, text="Добавить запись", width=button_width, command=self.add_record)
        add_button.pack(side=tk.TOP, pady=5)
        edit_button = tk.Button(buttons_frame, text="Редактировать запись", width=button_width,
                                command=self.edit_record)
        edit_button.pack(side=tk.TOP, pady=5)
        delete_button = tk.Button(buttons_frame, text="Удалить запись", width=button_width, command=self.delete_record)
        delete_button.pack(side=tk.TOP, pady=5)
        report_button = tk.Button(buttons_frame, text="Сгенерировать отчет", width=button_width,
                                  command=self.generate_report)
        report_button.pack(side=tk.TOP, pady=5)

        # Фрейм для поиска и сортировки
        search_sort_frame = tk.Frame(main_frame)
        search_sort_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Поле для ввода текста поиска
        self.search_entry = tk.Entry(search_sort_frame)
        self.search_entry.pack(side=tk.TOP, padx=5, pady=5)

        # Кнопка для выполнения поиска
        search_button = tk.Button(search_sort_frame, text="Поиск", command=self.search_data)
        search_button.pack(side=tk.TOP, padx=5, pady=5)

        # Кнопки для сортировки
        asc_button = tk.Button(search_sort_frame, text="Сортировать ASC", command=lambda: self.sort_data("ASC"))
        asc_button.pack(side=tk.TOP, padx=5, pady=5)
        desc_button = tk.Button(search_sort_frame, text="Сортировать DESC", command=lambda: self.sort_data("DESC"))
        desc_button.pack(side=tk.TOP, padx=5, pady=5)
    def create_table(self, tab, table_name, columns):
        tree = ttk.Treeview(tab, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Получение данных из базы данных
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Вставка данных в таблицу
        for row in rows:
            tree.insert("", "end", values=row)

        # Добавление treeview в окно
        tree.pack(fill="both", expand=True)

    def update_table(self):
        # Получение текущей вкладки
        current_tab = self.tab_control.select()
        current_tab_index = self.tab_control.index(current_tab)

        # Получение названия таблицы для текущей вкладки
        table_names = ["dostavka", "klient", "mebel", "prodavec", "zakaz"]
        table_name = table_names[current_tab_index]

        # Очистка существующих данных в Treeview
        tree = self.tab_control.winfo_children()[current_tab_index].winfo_children()[0]
        tree.delete(*tree.get_children())

        # Получение данных из базы данных
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Вставка данных в таблицу
        for row in rows:
            tree.insert("", "end", values=row)

    def add_record(self):
        # Диалог для выбора таблицы
        table_name = simpledialog.askstring("Выбор таблицы", "Введите название таблицы (dostavka, klient, mebel):")
        if table_name not in ["dostavka", "klient", "mebel", "prodavec", "zakaz"]:
            messagebox.showerror("Ошибка", "Неверное название таблицы")
            return

        # Диалог для ввода данных
        input_data = simpledialog.askstring("Ввод записи", "Введите значения записи через запятую:")
        if not input_data:
            return

        # Разделение введенных данных на список значений
        values = input_data.split(",")

        # Вставка данных в выбранную таблицу
        columns = ["ID", "VremyaDostavki", "Nomertelefona", "TipDostavki"]
        if table_name == "klient":
            columns = ["ID", "FIOZakazchika", "Nomertelefona", "Adres"]
        elif table_name == "mebel":
            columns = ["ID","Gabariti", "Color", "Materialy", "Ves"]
        elif table_name == "prodavec":
            columns = ["ID", "FIOProdavca", "Nomertelefona", "Adres"]
        elif table_name == "zakaz":
            columns = ["ID", "VremyaZakaza", "GabaritiMebeli", "Material"]

        # Подготовка SQL-запроса
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})"
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            rows = self.cursor.fetchall()
            # Обновление представления таблицы
            self.update_table_view(table_name, rows)
            messagebox.showinfo("Успех", "Запись успешно добавлена")
        except mysql.connector.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить запись. Ошибка: {e}")

    def update_table_view(self, table_name):
        # Обновление представления таблицы после добавления, редактирования или удаления записей
        # Очистка существующих данных в Treeview
        for child in self.tab_control.winfo_children():
            if child.winfo_children():
                child.winfo_children()[0].delete(*child.winfo_children()[0].get_children())

        # Получение данных из базы данных и обновление Treeview
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        tree = self.tab_control.winfo_children()[self.tab_control.index("current")].winfo_children()[0]
        for row in rows:
            tree.insert("", "end", values=row)

    def edit_record(self):
        # Диалог для выбора таблицы
        table_name = simpledialog.askstring("Выбор таблицы", "Введите название таблицы (dostavka, klient, mebel, prodavec, zakaz):")
        if table_name not in ["dostavka", "klient", "mebel","prodavec","zakaz"]:
            messagebox.showerror("Ошибка", "Неверное название таблицы")
            return

        # Получение данных из выбранной таблицы для отображения
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Создание диалогового окна для выбора записи
        record_selection_dialog = simpledialog.askstring("Выбор записи",
                                                         "Введите ID записи, которую вы хотите редактировать:")
        if not record_selection_dialog:
            return

        try:
            record_id = int(record_selection_dialog)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат ID записи")
            return

        # Проверка наличия записи с указанным ID
        if any(record_id in row for row in rows):
            # Определение имен столбцов для каждой таблицы
            if table_name == "klient":
                columns = ["ID", "FIOZakazchika", "Nomertelefona", "Adres"]
            elif table_name == "mebel":
                columns = ["ID","Gabariti", "Color", "Materialy", "Ves"]
            elif table_name == "prodavec":
                columns = ["ID", "FIOProdavca", "Nomertelefona", "Adres"]
            elif table_name == "zakaz":
                columns = ["ID", "VremyaZakaza", "GabaritiMebeli", "Material"]

            # Диалог для ввода новых данных
            new_data = simpledialog.askstring("Редактирование записи", "Введите новые значения записи через запятую:")
            if not new_data:
                return

            # Разделение введенных данных на список значений
            new_values = new_data.split(",")

            # Подготовка SQL-запроса для обновления записи
            update_query = f"UPDATE {table_name} SET "
            update_query += ", ".join([f"{col} = %s" for col in columns])
            update_query += f" WHERE id = {record_id}"

            try:
                self.cursor.execute(update_query, new_values)
                self.connection.commit()
                rows = self.cursor.fetchall()
                # Обновление представления таблицы
                self.update_table_view(table_name, rows)
                messagebox.showinfo("Успех", "Запись успешно отредактирована")
            except mysql.connector.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось отредактировать запись. Ошибка: {e}")
        else:
            messagebox.showerror("Ошибка", f"Запись с ID {record_id} не найдена в таблице {table_name}")

    def delete_record(self):
        # Диалог для выбора таблицы
        table_name = simpledialog.askstring("Выбор таблицы", "Введите название таблицы (dostavka, klient, mebel, prodavec, zakaz):")
        if table_name not in ["Dostavka", "Klient", "Mebel", "Prodavec", "Zakaz"]:
            messagebox.showerror("Ошибка", "Неверное название таблицы")
            return

        # Получение данных из выбранной таблицы для отображения
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Создание диалогового окна для выбора записи
        record_selection_dialog = simpledialog.askstring("Выбор записи", "Введите ID записи, которую вы хотите удалить:")
        if not record_selection_dialog:
            return

        try:
            record_id = int(record_selection_dialog)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат ID записи")
            return

        # Проверка наличия записи с указанным ID
        if any(record_id in row for row in rows):
            # Подготовка SQL-запроса для удаления записи
            delete_query = f"DELETE FROM {table_name} WHERE id = %s"

            try:
                self.cursor.execute(delete_query, (record_id,))
                self.connection.commit()
                rows = self.cursor.fetchall()
                # Обновление представления таблицы
                self.update_table_view(table_name, rows)
                messagebox.showinfo("Успех", "Запись успешно удалена")
            except mysql.connector.Error as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить запись. Ошибка: {e}")
        else:
            messagebox.showerror("Ошибка", f"Запись с ID {record_id} не найдена в таблице {table_name}")

    def search_data(self):
        search_text = self.search_entry.get()

        if not search_text:
            messagebox.showinfo("Пустой запрос", "Введите текст для поиска.")
            return

        try:
            tables = ["dostavka", "klient", "mebel", "prodavec", "zakaz"]  # Замените на фактические имена ваших таблиц
            columns = [
                ["ID", "VremyaDostavki", "Nomertelefona", "TipDostavki"],
                ["ID", "FIOZakazchika", "Nomertelefona", "Adres"],
                ["ID","Gabariti", "Color", "Materialy", "Ves"],
                ["ID", "FIOProdavca", "Nomertelefona", "Adres"],
                ["ID", "VremyaZakaza", "GabaritiMebeli", "Material"]
            ]  # Замените на фактические столбцы в ваших таблицах

            # Создаем пустое множество для результатов поиска
            search_results_set = set()

            # Проходим по всем таблицам
            for i, table in enumerate(tables):
                # Проходим по всем столбцам таблицы
                for column in columns[i]:
                    # Формируем запрос для поиска по конкретному столбцу
                    query = f"SELECT * FROM {table} WHERE {column} LIKE '%{search_text}%'"
                    self.cursor.execute(query)
                    rows = self.cursor.fetchall()

                    # Добавляем найденные строки в множество результатов
                    search_results_set.update(rows)
            app.last_search = search_text
            # Преобразуем множество обратно в список
            search_results = list(search_results_set)

            if not search_results:
                messagebox.showinfo("Результаты поиска", "По вашему запросу ничего не найдено.")
                return

            # Создаем новое окно для отображения результатов поиска
            search_results_window = tk.Toplevel(self.root)
            search_results_window.title("Результаты поиска")

            # Отображаем найденные строки в окне
            text_widget = tk.Text(search_results_window)
            text_widget.pack(fill="both", expand=True)

            # Вставка данных в текстовый виджет
            for row in search_results:
                text_widget.insert("end", f"{row}\n")

        except mysql.connector.Error as err:
            messagebox.showerror("Ошибка запроса", f"Ошибка при выполнении запроса: {err}")

    def sort_data(self, order):
        # Получение текущей вкладки и названия таблицы
        current_tab = self.tab_control.select()
        current_tab_index = self.tab_control.index(current_tab)
        table_names = ["dostavka", "klient", "mebel", "prodavec", "zakaz"]
        table_name = table_names[current_tab_index]

        # Получение данных из базы данных и сортировка
        query = f"SELECT * FROM {table_name} ORDER BY ID {order}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Обновление представления таблицы после выполнения сортировки
        self.update_table_view(table_name, rows)

    def update_table_view(self, table_name, rows):
        # Очистка существующих данных в Treeview
        tree = self.tab_control.winfo_children()[self.tab_control.index("current")].winfo_children()[0]
        tree.delete(*tree.get_children())

        # Вставка данных в таблицу
        for row in rows:
            tree.insert("", "end", values=row)

    def get_columns(self, table_name):
        # Возвращает список столбцов для указанной таблицы
        columns = ["ID", "VremyaDostavki", "Nomertelefona", "TipDostavki"]
        if table_name == "klient":
            columns = ["ID", "FIOZakazchika", "Nomertelefona", "Adres"]
        elif table_name == "mebel":
            columns = ["ID","Gabariti", "Color", "Materialy", "Ves"],
        elif table_name == "prodavec":
            columns = ["ID", "FIOProdavca", "Nomertelefona", "Adres"],
        elif table_name == "zakaz":
            column = ["ID", "VremyaZakaza", "GabaritiMebeli", "Material"]

    def generate_report(self):
        # Получаем текущее время
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Формируем отчет
        report_text = f"Отчет:\nВремя: {self.current_time}\n"

        # Получаем информацию о структуре всех таблиц
        table_info = self.get_table_info()

        # Вставляем информацию о структуре и содержании каждой таблицы в отчет
        for table_name, data in table_info.items():
            report_text += f"\nТаблица: {table_name}\n"
            columns = data['columns']
            rows = data['rows']

            # Вставляем заголовки столбцов
            for col in columns:
                report_text += f"{col:<30}"

            report_text += "\n"

            # Вставляем содержимое таблицы
            for row in rows:
                for cell in row:
                    report_text += f"{str(cell):<30}"
                report_text += "\n"

        # Если есть результат последнего поиска, добавляем его в отчет
        if self.last_search:
            report_text += f"\nПоследний поиск: {self.last_search}\n"

        # Создаем новое диалоговое окно для отчета
        report_dialog = tk.Toplevel(self.root)
        report_dialog.title("Отчет")

        # Создаем Text для отображения отчета
        report_textbox = tk.Text(report_dialog, wrap="none", width=160, height=35)
        report_textbox.insert("1.0", report_text)

        # Размещаем Text в окне
        report_textbox.pack(fill="both", expand=True)

        # Добавляем кнопку для закрытия окна отчета
        close_button = tk.Button(report_dialog, text="Закрыть", command=report_dialog.destroy)
        close_button.pack()

    def get_table_info(self):
        # Получаем информацию о структуре и содержании всех таблиц
        table_info = {}
        query = "SHOW TABLES"
        self.cursor.execute(query)
        table_names = [row[0] for row in self.cursor.fetchall()]

        for table_name in table_names:
            # Получаем структуру таблицы
            columns_query = f"SHOW COLUMNS FROM {table_name}"
            self.cursor.execute(columns_query)
            columns = [row[0] for row in self.cursor.fetchall()]

            # Получаем содержимое таблицы
            data_query = f"SELECT * FROM {table_name}"
            self.cursor.execute(data_query)
            rows = self.cursor.fetchall()

            table_info[table_name] = {'columns': columns, 'rows': rows}

        return table_info

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
