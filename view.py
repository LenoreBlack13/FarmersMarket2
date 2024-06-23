import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import scrolledtext
from tkinter import messagebox


class MarketsView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Markets")
        self.root.geometry("1000x800")  # Устанавливаем размер окна 1200x800
        self.controller = None
        self.page_number = 0
        self.page_size = 30
        self.total_pages = 0
        self.create_frame()
        self.create_grid()
        self.create_widgets()

    def set_controller(self, controller):
        self.controller = controller

    def create_widgets(self):
        self.create_widgets_for_search()
        self.create_widgets_for_tables()
        self.create_widgets_for_details()
        self.create_widgets_for_reviews()

    def create_grid(self):
        self.root.rowconfigure(0, weight=2)  # Строка для поиска
        self.root.rowconfigure(1, weight=3)  # Строка для таблицы
        self.root.rowconfigure(2, weight=3)  # Строка для таблицы
        self.root.rowconfigure(3, weight=2)  # Строка для обзора
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)

    def create_frame(self):
        self.search_frame = ttk.LabelFrame(self.root, text="Поиск рынков")
        self.search_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.table_frame = ttk.LabelFrame(self.root, text="Таблица рынков")
        self.table_frame.grid(row=1, column=0, columnspan=2, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Настройка поведения сетки для рамки с таблицей
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.columnconfigure(1, weight=0)
        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.rowconfigure(1, weight=0)

        self.details_frame = ttk.LabelFrame(self.root, text="Подробнее")
        self.details_frame.grid(row=0, column=2, columnspan=2, rowspan=3, padx=10, pady=10, sticky="nsew")

        self.review_frame = ttk.LabelFrame(self.root, text="Оставить отзыв")
        self.review_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Отключаем автоматическую пропагацию размеров
        self.search_frame.grid_propagate(False)
        self.table_frame.grid_propagate(False)
        self.details_frame.grid_propagate(False)
        self.review_frame.grid_propagate(False)

    def create_widgets_for_search(self):
        ttk.Label(self.search_frame, text="Город:").grid(row=0, column=0, padx=5, pady=5)
        self.search_city_entry = ttk.Entry(self.search_frame)
        self.search_city_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.search_frame, text="Штат:").grid(row=0, column=2, padx=5, pady=5)
        self.search_state_entry = ttk.Entry(self.search_frame)
        self.search_state_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.search_frame, text="Индекс:").grid(row=1, column=0, padx=5, pady=5)
        self.search_zip_entry = ttk.Entry(self.search_frame)
        self.search_zip_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.search_frame, text="Расстояние:").grid(row=1, column=2, padx=5, pady=5)
        self.search_distance_entry = ttk.Entry(self.search_frame)
        self.search_distance_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка для выполнения поиска
        self.search_button = ttk.Button(self.search_frame, text="Поиск", command=self.search)
        self.search_button.grid(row=2, column=3, padx=5, pady=5, sticky="e")

    def search(self):
        city = self.search_city_entry.get()
        state = self.search_state_entry.get()
        zip_code = self.search_zip_entry.get()
        self.controller.search_markets(city, state, zip_code)

    def create_widgets_for_tables(self):
        # Настройка поведения сетки для рамки с таблицей
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.columnconfigure(1, weight=0)
        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.rowconfigure(1, weight=0)

        # Создаем виджет Treeview для отображения данных в рамке
        self.tree = ttk.Treeview(self.table_frame, columns=("Market", "Rating"), show='headings')
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Создаем скроллбар и привязываем его к Treeview
        self.scrollbar_table = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar_table.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.scrollbar_table.set)

        # Двойной клик по строке в таблице
        self.tree.bind("<Double-1>", self.on_tree_select)

        # Привязка события ButtonRelease-1 к Treeview
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        # Кнопки для навигации
        self.nav_frame = tk.Frame(self.table_frame)
        self.nav_frame.grid(row=1, column=0, columnspan=2, pady=5)
        self.nav_frame.columnconfigure(0, weight=1)
        self.nav_frame.columnconfigure(1, weight=1)

        self.prev_button = ttk.Button(self.nav_frame, text="<<<", command=self.prev_page)
        self.prev_button.grid(row=0, column=0, sticky='w')

        self.next_button = ttk.Button(self.nav_frame, text=">>>", command=self.next_page)

        # Кнопки для навигации
        self.nav_frame = tk.Frame(self.table_frame)
        self.nav_frame.grid(row=1, column=0, columnspan=2, pady=5)
        self.nav_frame.columnconfigure(0, weight=1)
        self.nav_frame.columnconfigure(1, weight=1)

        self.prev_button = ttk.Button(self.nav_frame, text="<<<", command=self.prev_page)
        self.prev_button.grid(row=0, column=0, sticky='w')

        self.next_button = ttk.Button(self.nav_frame, text=">>>", command=self.next_page)
        self.next_button.grid(row=0, column=1, sticky='e')

        self.page_label = ttk.Label(self.nav_frame, text="Page 1")
        self.page_label.grid(row=0, column=2, sticky='e')

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        market_name = self.tree.item(selected_item)["values"][0]
        details = self.controller.get_market_details(market_name)
        self.update_details(details)

    def get_replacements(self):
        return {
            "marketname": "Market Name",
            "season1date": "First season date",
            "season1time": "First season time",
            "season2date": "Second season date",
            "season2time": "Second season time",
            "season3date": "Third season date",
            "season3time": "Third season time",
            "season4date": "Fourth season date",
            "season4time": "Fourth season time",
            "wiccash": "WIC cash",
            "wic": "WIC",
            "sfmnp": "SFMNP",
            "bakedgoods": "baked goods",
        }

    def format_details_name(self, col_name):
        replacements = self.get_replacements()
        return replacements.get(col_name, col_name)

    def update_details(self, details):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        details_text = ""  # Собираем строку с нужной информацией из details
        if not details.empty:
            for column in details.columns:
                formatted_column = self.format_details_name(column)
                details_text += f"{formatted_column}: {details[column].values[0]}\n"
        else:
            details_text = "Детали не найдены"

        # Создаем Text виджет и Скроллбар
        text_widget = tk.Text(self.details_frame, wrap='word', height=15)
        scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        # Размещаем Text виджет и Скроллбар в сетке
        text_widget.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Заполняем Text виджет текстом
        text_widget.insert("1.0", details_text)

        text_widget.config(state=tk.DISABLED)  # Делаем Text виджет только для чтения

        # Настройка расширения виджета при изменении размера окна
        self.details_frame.grid_rowconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(0, weight=1)

    def update_table(self, data):
        self.tree.delete(*self.tree.get_children())

        # Установка заголовков столбцов
        columns = ["Market", "Rating"]
        self.tree["columns"] = columns

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        # Заполнение Treeview данными
        for index, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Автонастройка ширины столбцов
        self.autosize_columns()
        self.update_nav_buttons()

    def autosize_columns(self):
        # Получаем шрифт, используемый в Treeview через стиль
        style = ttk.Style()
        font = tkFont.Font(font=style.lookup("Treeview", "font"))

        for col in self.tree["columns"]:
            # Начальное значение ширины - ширина заголовка столбца
            max_width = font.measure(col)

            for item in self.tree.get_children():
                cell_value = self.tree.set(item, col)
                cell_width = font.measure(cell_value)
                max_width = max(max_width, cell_width)

            # Добавляем отступ
            self.tree.column(col, width=max_width + 10, anchor='w')

    def update_nav_buttons(self):
        self.total_pages = self.controller.get_total_pages(self.page_size)
        self.page_label.config(text=f"Page {self.page_number + 1} of {self.total_pages}")

        if self.page_number == 0:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")

        if self.page_number >= self.total_pages - 1:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")

    def prev_page(self):
        if self.page_number > 0:
            self.page_number -= 1
            self.controller.update_table(page_number=self.page_number)

    def next_page(self):
        if self.page_number < self.total_pages - 1:
            self.page_number += 1
            self.controller.update_table(page_number=self.page_number)

    def create_widgets_for_details(self):
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.rowconfigure(0, weight=1)

        info_label = ttk.Label(self.details_frame, text="Нажмите на рынок, чтобы увидеть подробности")
        info_label.grid(row=0, column=0, padx=10, pady=10)

    def create_widgets_for_reviews(self):
        ttk.Label(self.review_frame, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.name_user_entry = ttk.Entry(self.review_frame)
        self.name_user_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.review_frame, text="Фамилия:").grid(row=1, column=0, padx=5, pady=5)
        self.lastname_user_entry = ttk.Entry(self.review_frame)
        self.lastname_user_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.review_frame, text="Оценка:").grid(row=2, column=0, padx=5, pady=5)
        self.rating_combobox = ttk.Combobox(self.review_frame, values=["1", "2", "3", "4", "5"])
        self.rating_combobox.grid(row=2, column=1, padx=5, pady=5)

        self.review_entry = tk.Text(self.review_frame, width=50, height=6)
        self.review_entry.grid(row=0, column=2, columnspan=3, rowspan=3, padx=50, pady=5, sticky='nsew')

        # Кнопка для отправки отзыва
        self.review_button = ttk.Button(self.review_frame, text="Отправить", command=self.on_submit_review)
        self.review_button.grid(row=2, column=5, padx=5, pady=5, sticky="e")

    def get_selected_market_name(self):
        selected_item = self.tree.selection()[0]
        market_name = self.tree.item(selected_item)["values"][0]
        return market_name

    def on_submit_review(self):
        first_name = self.name_user_entry.get()
        last_name = self.lastname_user_entry.get()
        rating = self.rating_combobox.get()
        review_text = self.review_entry.get("1.0", tk.END)
        self.controller.submit_review(first_name, last_name, rating, review_text)

        # Очищаем поля после отправки отзыва (если необходимо)
        self.name_user_entry.delete(0, tk.END)
        self.lastname_user_entry.delete(0, tk.END)
        self.rating_combobox.set('')
        self.review_entry.delete("1.0", tk.END)

        # Показать уведомление об успешной отправке
        messagebox.showinfo("Успех", "Отзыв был успешно отправлен!")

    def show(self):
        self.root.mainloop()
