# импорт пакетов
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QListView, QPushButton, QMainWindow
from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QButtonGroup, QLabel, QTableView, QRadioButton
from PyQt5.QtWidgets import QTabWidget, QTextEdit, QInputDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
import sqlite3
import sys
import os
import subprocess
# конец импорта пакетов

# класс главного окна
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # вызываем метод __init__ родительского виджета
        self.settings()  # настраиваем пользовательский интерфейс

    def settings(self):  # настраиваем пользовательский интерфейс
        self.setGeometry(100, 100, 1150, 600) # задаём расположение главного окна
        self.setWindowTitle("Графическая пользовательская БИБЛИОТЕКА.") # как зовут окно?

        self.LinE = QLineEdit(self)  # создаём строку поиска
        self.LinE.setGeometry(20, 20, 800, 30) # задаём расположение строки поиска
        self.LinE.textChanged.connect(self.poisk)  # при изменении текста будет
                                                   # вызываться функция poisk

        self.list_mandatory_filters = ["author", "title"] # список обязательных фильтров
        self.list_additional_filters = ["paper", "volume", "cover", "content",
                                        "year", "publishingHome", "publishingPlace",
                                        "addition"]  # список дополнительных фильтров
        self.tabs_who_not_delete = self.list_mandatory_filters + \
            self.list_additional_filters  # названия фильтров, которые нельзя удалять

        self.BoX = QWidget(self)  # родительский виджет для QVBoxLayout
        self.BoX.setGeometry(820, 20, 150, 500) # расположение родительского виджета для QVBoxLayout

        self.FilterS = QVBoxLayout(self.BoX)  # все фильтры в QVBoxLayout
        self._FILTERS_ = [] # список фильтров (QCheckBox)

        self.FilterS.addWidget(QLabel(self, text="mandatory:")) # заголовок для обязательных фильтров

        for i in range(len(self.list_mandatory_filters)): # перебираем обязательные фильтры
            check_box = QCheckBox(self.list_mandatory_filters[i], self) # создаём для каждого
                                                                        # фильтра отдельный QCheckBox
            self._FILTERS_.append(check_box) # добавляем фильтры в список фильтров
            check_box.stateChanged.connect(self.poisk) # при изменении фильтра вызывается функция poisk
            self.FilterS.addWidget(check_box) # добавляем QCheckBox в QVBoxLayout

        self.FilterS.addWidget(QLabel(self, text="additional:")) # заголовок для дополнительных фильтров

        for i in range(len(self.list_additional_filters)): # перебираем пользовательские фильтры
            check_box = QCheckBox(self.list_additional_filters[i], self) # создаём для каждого
                                                                         # фильтра отдельный QCheckBox
            self._FILTERS_.append(check_box)
            check_box.stateChanged.connect(self.poisk) # при изменении фильтра вызывается функция poisk
            self.FilterS.addWidget(check_box) # добавляем QCheckBox в QVBoxLayout

        self.ButtoN_PluS = QPushButton(self, text="+") # кнопка для добавления новой книги
        self.ButtoN_PluS.setGeometry(830, 560, 140, 30) # расположение кнопки для добавления новой книги
        self.ButtoN_PluS.clicked.connect(self.add_book) # при нажатии на кноку + вызывается функция add_book

        self.ButtoN_SettingS = QPushButton(self, text="menu") # кнопка для открытия меню
        self.ButtoN_SettingS.setGeometry(980, 560, 140, 30) # расположение кнопки для открытия меню
        self.ButtoN_SettingS.clicked.connect(self.polz_settings) # при нажатии на кноку для открытия меню вызывается polz_settings

        self.MainTableBook = QTableView(
            parent=self)  # создаём таблицу с книгами
        self.model = QStandardItemModel()  # модель для создания заголовков таблицы
        
        self.btn0000 = []
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        self.up_date(list(cursor.execute(f"""select * from book""").fetchall())) # обновляем таблицу

        self.BOX1 = QWidget(self) # родительский виджет для QVBoxLayout
        self.BOX1.setGeometry(970, 440, 160, 80) # расположение родительского виджета для QVBoxLayout
        self.SORT_IROVKA = QVBoxLayout(self.BOX1) # сортировка (либо по возрастанию, либо по убыванию)
        radio_button = QRadioButton("alphabetically (/\)") # создаём QRadioButton
        self.control_rev_btn = radio_button
        radio_button.toggled.connect(lambda radio_btn, name="alphabetically (/\)", btn=radio_button: self.sortirovka2(name, btn)) 
        # привязываем к изменению QRadioButton функцию sortirovka2
        self.SORT_IROVKA.addWidget(radio_button) # сортировка по убыванию
        radio_button = QRadioButton("alphabetically (\/)") # создаём QRadioButton
        radio_button.setChecked(True) # включаем кнопку
        radio_button.toggled.connect(lambda radio_btn, name="alphabetically (\/)", btn=radio_button: self.sortirovka2(name, btn)) 
        # привязываем к изменению QRadioButton функцию sortirovka2
        self.SORT_IROVKA.addWidget(radio_button) # сортировка по возрастанию
        self.BOX2 = QWidget(self) # родительский виджет для QVBoxLayout
        self.BOX2.setGeometry(970, 40, 160, 400) # расположение родительского виджета для QVBoxLayout
        self.SORT_IROVKA1 = QVBoxLayout(self.BOX2) # параметры для сортировки
        self.SORT_IROVKA1.addWidget(QLabel(self, text="filters for sorting:")) # заголовок для сортировочных параметров
        radio_button = QRadioButton("id") # создаём QRadioButton
        radio_button.setChecked(True) # включаем кнопку
        radio_button.toggled.connect(lambda radio_btn, name="id", btn=radio_button: self.sortirovka1(name, btn))
        self.btn0000.append(radio_button) 
        # привязываем к изменению QRadioButton функцию sortirovka1
        self.SORT_IROVKA1.addWidget(radio_button) # добавляем QRadioButton в QVBoxLayout
        for i in self.list_mandatory_filters + self.list_additional_filters: # перебираем все параметры
            radio_button = QRadioButton(i) # создаём QRadioButton
            radio_button.toggled.connect(lambda radio_btn, name=i, btn=radio_button: self.sortirovka1(name, btn)) 
            # привязываем к изменению QRadioButton функцию sortirovka1
            self.SORT_IROVKA1.addWidget(radio_button) # добавляем QRadioButton в QVBoxLayout
            self.btn0000.append(radio_button)
        SettingS(self).temm(cursor.execute(f"""select color from settings where id = 1""").fetchall()[0][0])
        connection.close()  # закрываем базу данных Base_of_booK
    
    def up_date(self, base): # функция для обновления таблицы
        self.model.clear() # очистить главную таблицу для новых записей

        self.model.setHorizontalHeaderLabels(
            ["id", "author", "title", "change", "open"]) # добавление заголовков в модель
        self.MainTableBook.setModel(self.model) # модель для таблицы (заголовки добавляем)
        self.MainTableBook.setGeometry(
            20, 60, 800, 500)  # размер таблицы с книгами
        self.MainTableBook.horizontalHeader().resizeSection(
            0, 160)  # размер заголовка с индексом 0
        self.MainTableBook.horizontalHeader().resizeSection(
            1, 160)  # размер заголовка с индексом 1
        self.MainTableBook.horizontalHeader().resizeSection(
            2, 160)  # размер заголовка с индексом 2
        self.MainTableBook.horizontalHeader().resizeSection(
            3, 160)  # размер заголовка с индексом 3
        self.MainTableBook.horizontalHeader().resizeSection(
            4, 160)  # размер заголовка с индексом 4

        for g, i in enumerate(base): # проходим по всем книгам в таблице book
            # добавляем в модель главной таблицы каждую книгу
            self.model.setItem(g, 0, QStandardItem(QIcon(), str(i[0]))) # добавляем id
            self.model.setItem(g, 1, QStandardItem(QIcon(), str(i[1]))) # добавляем author
            self.model.setItem(g, 2, QStandardItem(QIcon(), str(i[2]))) # добавляем title
            BTN_for_table_change_book = QPushButton("Change") # создаём кнопку для редактирования книги
            BTN_for_table_change_book.clicked.connect(lambda btn, id=str(i[0]): self.change(id)) # привязываем кнопку для
                                                                                                 # редактирования книги к
                                                                                                 # функции change
            self.MainTableBook.setIndexWidget(self.model.index(g, 3), BTN_for_table_change_book) # добавляем кнопку
                                                                                                 # редактирования книги
            BTN_for_table_open_book = QPushButton("Open") # создаём кнопку для открытия книги
            BTN_for_table_open_book.clicked.connect(lambda btn, id=str(i[0]): self.open_book(id)) # привязываем кнопку для
                                                                                               # открытия книги к
                                                                                               # функции open
            self.MainTableBook.setIndexWidget(self.model.index(g, 4), BTN_for_table_open_book) # добавляем кнопку для
                                                                                               # открытия книги
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        SettingS(self).temm(cursor.execute(f"""select color from settings where id = 1""").fetchall()[0][0])
        connection.close()  # закрываем базу данных Base_of_booK

    def change(self, id): # функция редактирования книги
        self.MainWindow2 = BookWindow(id, self) # создаём окно для редактирования книги
        self.MainWindow2.show() # показываем окно для редактирования книги

    def open_book(self, id): # функция для открытия новой книги
        try:
            connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
            cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK

            filepath = cursor.execute(f"""select path from book_path_to_file
                                    where id = {id}""").fetchall()[0][0] # путь к файлу с книгой
            
            f = open(filepath) # открываем файл (проверка, на то, что такой файл существует)
            f.close() # закрываем файл

            if sys.platform.startswith('darwin'):
                subprocess.call(('open', filepath))
            elif os.name == 'nt': # For Windows
                os.startfile(filepath)
            elif os.name == 'posix': # For Linux, Mac, etc.
                subprocess.call(('xdg-open', filepath))
            
            connection.close()  # закрываем базу данных Base_of_booK
        except Exception:
            msgBox = QMessageBox()  # создаём QMessageBox
            msgBox.setText("The file does not exist") # выводим сообщение о том, что книга не существует
            msgBox.exec()  # показываем окно

    def poisk(self):  # функция поиска
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        
        if self.LinE.text() != "": # если поисковая строка НЕ пустая
            active_filters = [] # список активных фильтров
            for i in self._FILTERS_: # перебираем фильтры (QCheckBox)
                if i.isChecked(): # если фильтр активен
                    active_filters.append(i.text()) # добавляем его название в список активных фильтров
            list_of_all_suit_filters = [] # список отфильтрованных книг
            for i in active_filters: # перебираем имена фильтров
                _l_ = cursor.execute(f"""select * from book where {i.lower()}
                                        like '%{self.LinE.text().lower()}%'""").fetchall() # список отфильтрованных книг
                                                                                           # (по 1 параметру)
                if _l_ != 0: # если список с фильтрованными книгами не пустой
                    list_of_all_suit_filters += _l_ # пополняем основной список отфильтрованных книг
            list_of_all_suit_filters = list(set(list_of_all_suit_filters)) # убираем повторяющиеся книги
            self.up_date(list_of_all_suit_filters) # обновляем основную таблицу с книгами
        else: # если поисковая строка пустая, выводим список всех книг
            self.up_date(list(cursor.execute(f"""select * from book""").fetchall())) # обновляем главное окно
        
        connection.close()  # закрываем базу данных Base_of_booK
        self.f()
    
    def polz_settings(self):
        self.seTTings = SettingS(self)
        self.seTTings.show()

    def add_book(self):  # функция добавления новой книги
        self.MainWindow2 = BookWindow(self.model.rowCount() + 1, self) # создаём окно для создания новой книги
        self.MainWindow2.show() # показываем окно для создания новой книги
    
    def f(self):
        for i in self.btn0000:
            if i.isChecked():
                self.sortirovka1(i.text(), i)

    def sortirovka1(self, name, btn):  # функция для сортировки, отображающихся книг (1)
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        all_el = ["id"] + self.list_mandatory_filters + self.list_additional_filters # список имён всех фильтров
        new_list_base = [] # список для новых элементов
        for i in range(self.model.rowCount()): # перебираем элементы в таблице
            new_list_base += cursor.execute(f"""select * from book where id =
                            {str(self.model.item(i, 0).text())}""").fetchall() # ищем элементы с id из таблицы
        rever = self.control_rev_btn.isChecked()

        if name != "-":
            self.up_date(list(sorted(new_list_base, key=lambda x: x[all_el.index(name)]
                                     if name == "id" else str(x[all_el.index(name)]), reverse=rever)))  # обновляем таблицу
        else:
            self.up_date(new_list_base[::-1]) # обновляем таблицу

        connection.close()  # закрываем базу данных Base_of_booK
    
    def sortirovka2(self, name, btn):  # функция для сортировки, отображающихся книг (2)
        if btn.isChecked():
            self.sortirovka1("-", btn)
# конец класса главного окна


# класс окна редактирования и удаления книги
class BookWindow(QWidget):
    def __init__(self, id, main):
        self.main = main
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        self.id = id  # id книги
        self.new_tabs = []  # именя новых фильтров
        super().__init__()  # вызываем метод __init__ родительского виджета
        self.settings()  # настраиваем пользовательский интерфейс
        self.PatH = QLabel(self) # создаём поле отображения пути к файлу книги
        self.PatH.setGeometry(630, 350, 160, 100) # задаём расположение поля отображения пути к файлу книги
        self.PatH.setWordWrap(True) # устанавливаем автоматический перенос строк
        if len(cursor.execute(f"SELECT * FROM book WHERE id = {self.id}").fetchall()) != 0: # если книга
                                                                                            # уже есть в базе
                                                                                            #  (т.е. мы её редактируем)
            cursor.executescript(
                f"""INSERT OR IGNORE INTO book_filters_keys(id) VALUES({self.id})""")  # создаём место для новых полей
                                                                                       # в таблице book_filters_keys
            cursor.executescript(
                f"""INSERT OR IGNORE INTO book_filters_values(id) VALUES({self.id})""")  # создаём место для новых полей
                                                                                         # в таблице book_filters_values
            self.PatH.setText(cursor.execute(f"""select path from book_path_to_file
             where id = {self.id}""").fetchall()[0][0]) # выводим на QLabel путь к файлу
        if len(cursor.execute(f"select * from book_filters_keys where id = {self.id}").fetchall()) != 0: # если кнга есть в
                                                                                                         # таблице book
            self.new_tabs += cursor.execute(
                f"select * from book_filters_keys where id = {self.id}").fetchall()[0][1:] # в new_tabs добавляем названия
                                                                                           # пользовательских фильтров
        self.new_tabs = list(
            filter(lambda x: x != "NULL" and x != "None" and x != None, self.new_tabs)) # убираем фильтры, которых нет
                                                                                        # у данной книги
        for i in list(self.new_tabs):  # перебираем все пользовательские параметры
            if i != "NULL" and i != "None": # если фиьтр существует для этой книги
                self.TaBBooKFilterS.addTab(QTextEdit(), QIcon(), i) # создаём вкладку для каждого пользовательского параметра

        if len(cursor.execute(f"select * from book where id = {self.id}").fetchall()) != 0: # если книги нет в таблице book
            for i in range(self.TaBBooKFilterS.count()):  # проходим по всем TAB-ам
                if i < len(MainWindow().tabs_who_not_delete): # проверяем не является ли фильтр пользовательским
                    self.TaBBooKFilterS.widget(i).setPlainText(str(cursor.execute(f"""
                    select {MainWindow().tabs_who_not_delete[i]} from book where id = {self.id}""").fetchall()[0][0]))  
                    # помещаем сохранённые данные на виджет в TAB
                else:
                    if str(self.TaBBooKFilterS.tabText(i)) != "NULL" or str(self.TaBBooKFilterS.tabText(i)) != "None":
                        # если поле не пустое
                        self.TaBBooKFilterS.widget(i).setPlainText(str(cursor.execute(f"""
                            select {self.new_tabs[i - len(MainWindow().tabs_who_not_delete)]} 
                            from book_filters_values where id = {self.id}""").fetchall()[0][0]))  
                            # помещаем сохранённые данные на виджет в TAB

        connection.close()  # закрываем базу данных Base_of_booK

    def settings(self):  # настраиваем пользовательский интерфейс
        self.setGeometry(200, 100, 800, 500) # задаём расположение окна добавления книги
        self.setWindowTitle("Добавьте книгу.")  # как зовут окно?

        self.TaBBooKFilterS = QTabWidget(self) # TaB, в котором можно редактировать параметры книги
        self.TaBBooKFilterS.setGeometry(20, 20, 600, 450) # задаём расположение TaB с параметрами книги
        for i in list(MainWindow().list_mandatory_filters + MainWindow().list_additional_filters):
            # перебираем все пареметры (не включая id)
            self.TaBBooKFilterS.addTab(QTextEdit(), QIcon(), i) # создаём вкладку для каждого параметра

        self.Button_add_filteR = QPushButton(self, text="Add filter") # создаём кнопку добавления пользовательского фильтра
        self.Button_add_filteR.setGeometry(630, 20, 160, 40) # задаёи расположене кнопки добавления пользовательского фильтра
        self.Button_add_filteR.clicked.connect(
            self.add_filter)  # при нажатии на кнопку
                              # добавления пользовательского
                              #  фильтра вызывается функция add_filter

        self.Button_delete_filteR = QPushButton(self, text="Delete filter") # создаём кнопку удаления пользовательского фильтра
        self.Button_delete_filteR.setGeometry(630, 70, 160, 40) # задаёи расположене кнопки удаления пользовательского фильтра
        self.Button_delete_filteR.clicked.connect(
            self.delete_filter)  # при нажатии на кнопку
                                 # удаления пользовательского
                                 # фильтра вызывается функция delete_filter

        self.Button_save_book_filterS = QPushButton(
            self, text="Save")  # создание кнопки сохранения
        self.Button_save_book_filterS.setGeometry(
            630, 120, 160, 40)  # задаёи расположене кнопки сохранения
        self.Button_save_book_filterS.clicked.connect(
            self.save)  # при нажатии на кнопку
                        # сохранения книги вызывается функция save

        self.Button_delete_booK = QPushButton(
            self, text="Delete this BOOK")  # создание кнопки удаления книги
        self.Button_delete_booK.setGeometry(630, 170, 160, 40) # задаёи расположене кнопки удаления книги
        self.Button_delete_booK.clicked.connect(
            self.delete)  # при нажатии на кнопку
                          # удаления книги вызывается функция delete
        
        self.Button_add_patH = QPushButton(
            self, text="Add path")  # создание кнопки для добавления или изменения пути к файлу
        self.Button_add_patH.setGeometry(
            630, 300, 160, 40)  # задаёи расположене кнопки для добавления или изменения пути к файлу
        self.Button_add_patH.clicked.connect(
            self.add_path)  # при нажатии на кнопку
                            # для добавления или изменения пути к файлу вызывается функция add_path

    def add_filter(self):  # функция для добавления нового пользовательского фильтра
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        name_of_filter = QInputDialog.getText(self, 'Name of filter', 'Input:')[
            0]  # получаем название фильтра
        if name_of_filter in self.new_tabs: # если фильтр в списке пользовательских фильтров 
            msgBox = QMessageBox()  # создаём QMessageBox
            msgBox.setText("Such a filter already exists.") # выводим сообщение о том, что такой фильтр уже имеется
            msgBox.exec()  # показываем окно
        else:
            if name_of_filter in list(map(lambda x: x[1], cursor.execute(f"pragma table_info(book_filters_keys)"))):
                # если фильтр уже существует в таблице
                cursor.executescript(str(f"""UPDATE book_filters_keys SET
                                    {name_of_filter} = '{name_of_filter}'
                                     WHERE id = {self.id}"""))  # сохранием имя колонки в таблице book_filters_keys
                self.TaBBooKFilterS.addTab(QTextEdit(), QIcon(
                ), name_of_filter)  # создаём новый пустой фильтр в QTabWidget
                self.new_tabs.append(name_of_filter) # добавляем фильтр в список пользовательских фильтров для этой книги
            else:
                self.new_tabs.append(name_of_filter) # добавляем имя фильтра в список имён новых фильтров
                cursor.executescript(str(
                    f"""ALTER TABLE book_filters_keys ADD COLUMN {name_of_filter}
                     VARCHAR (1000)"""))  # добавляем фильтр в базу book_filters_keys
                cursor.executescript(str(
                    f"""ALTER TABLE book_filters_values ADD COLUMN {name_of_filter}
                     VARCHAR (1000)"""))  # добавляем фильтр в базу book_filters_values
                cursor.executescript(str(f"""UPDATE book_filters_keys SET 
                                    {name_of_filter} = '{name_of_filter}'
                                     WHERE id = {self.id}"""))  # сохранием имя колонки в таблице book_filters_keys
                self.TaBBooKFilterS.addTab(QTextEdit(), QIcon(
                ), name_of_filter)  # создаём новый пустой фильтр в QTabWidget
        connection.close()  # закрываем базу данных Base_of_booK

    def delete_filter(self):  # функция для удаления пользовательского фильтра
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        if not(self.TaBBooKFilterS.tabText(self.TaBBooKFilterS.currentIndex()) in MainWindow().tabs_who_not_delete):
            # проверка на то, что текущий фильтр можно удалить
            cursor.executescript(
                f"""UPDATE book_filters_keys SET {self.TaBBooKFilterS.tabText(self.TaBBooKFilterS.currentIndex())}
                 = 'NULL' WHERE id = {self.id}""")  # удаляем значение из таблицы значений фильтров
            cursor.executescript(
                f"""UPDATE book_filters_values SET {self.TaBBooKFilterS.tabText(self.TaBBooKFilterS.currentIndex())}
                 = 'NULL' WHERE id = {self.id}""")  # удаляем значение из таблицы названий фильтров
            self.TaBBooKFilterS.removeTab(
                self.TaBBooKFilterS.currentIndex())  # удаление текущего фильтра из TabWindow
        else:  # если фильтр удалить нельзя
            msgBox = QMessageBox()  # создаём QMessageBox
            msgBox.setText("This filter cannot be removed") # выводим сообщение о том, что фильтр удалять нельзя
            msgBox.exec()  # показываем окно

        connection.close()  # закрываем базу данных Base_of_booK

    def save(self):  # функция для сохранения изменений
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        if len(cursor.execute(f"SELECT * FROM book WHERE id = {self.id}").fetchall()) == 0: # если книги нет в базе
                                                                                            # (т.е. мы её не редактируем,
                                                                                            #  а добавляем)
            cursor.executescript(
                f"""INSERT OR IGNORE INTO book_filters_keys(id) VALUES({self.id})""")  # создаём место для новых полей
                                                                                       # в таблице book_filters_keys
            cursor.executescript(
                f"""INSERT OR IGNORE INTO book_filters_values(id) VALUES({self.id})""")  # создаём место для новых полей
                                                                                         # в таблице book_filters_values
            cursor.executescript(
                f"""INSERT OR IGNORE INTO book_path_to_file(id) VALUES({self.id})""")  # создаём место для новых полей
                                                                                       # в таблице book_path_to_file
        if len(cursor.execute(f"SELECT * FROM book WHERE id = {self.id}").fetchall()) != 0:  # если элемент с таким id
                                                                                             # уже есть в таблице book
            for i in range(self.TaBBooKFilterS.count()):  # прохлдим по всем TaB-ам
                if i < len(MainWindow().tabs_who_not_delete): # проверяем является ли фильтр пользовательским
                    cursor.executescript(str(f"""UPDATE book SET 
                                {MainWindow().tabs_who_not_delete[i]} = '{self.TaBBooKFilterS.widget(i).toPlainText()}'
                                WHERE id = {self.id}"""))  # сохраняем значение основного фильтра
                else:
                    cursor.executescript(str(f"""UPDATE book_filters_values SET 
                                {self.new_tabs[i - len(MainWindow().tabs_who_not_delete)]}
                                = '{self.TaBBooKFilterS.widget(i).toPlainText()}'
                                WHERE id = {self.id}"""))  # сохраняем значение пользовательского фильтра
            cursor.executescript(str(f"""UPDATE book_path_to_file SET 
                        path = '{self.PatH.text()}' WHERE id = {self.id}"""))  # сохраняем путь к файлу
        else:
            names_of_filters = list(
                MainWindow().tabs_who_not_delete + self.new_tabs) # имена всех фильтров (название колонок)
            values_of_filters = []  # значения фильтров (значения клеточек)
            for i in range(self.TaBBooKFilterS.count()):  # прохлдим по всем TaB-ам
                values_of_filters.append(
                    self.TaBBooKFilterS.widget(i).toPlainText()) # сохраняем их значения в списке значений фильров
            cursor.executescript(f"""INSERT INTO book
                    ({names_of_filters[0]}) VALUES('{values_of_filters[0]}')""")  # создаём в базе книгу с записанным
                                                                                  # первым фильром
            connection.commit() # подтверждаем все действия
            for i in range(1, len(names_of_filters)): # проходимся по именам фильтров
                if i < len(MainWindow().tabs_who_not_delete): # проверяем является ли фильтр пользовательским
                    cursor.executescript(f"""UPDATE book
                            SET {names_of_filters[i]} = '{values_of_filters[i]}'
                            WHERE id = {self.id}""")  # сохраняем значение основного фильтра
                else:
                    cursor.executescript(str(f"""UPDATE book_filters_keys SET 
                                {self.new_tabs[i - len(MainWindow().tabs_who_not_delete)]}
                                = '{self.new_tabs[i - len(MainWindow().tabs_who_not_delete)]}'
                                WHERE id = {self.id}"""))  # сохраняем название пользовательского фильтра
                    cursor.executescript(str(f"""UPDATE book_filters_values SET 
                                {self.new_tabs[i - len(MainWindow().tabs_who_not_delete)]}
                                = '{self.TaBBooKFilterS.widget(i).toPlainText()}'
                                WHERE id = {self.id}"""))  # сохраняем значение пользовательского фильтра
                connection.commit()  # подтверждаем операции
            cursor.executescript(str(f"""UPDATE book_path_to_file SET 
                        path = '{self.PatH.text()}' WHERE id = {self.id}"""))  # сохраняем путь к файлу
        self.main.up_date(list(cursor.execute(f"""select * from book""").fetchall())) # обновляем главное окно
        cursor.close()  # закрываем cursor
        connection.close()  # закрываем базу данных Base_of_booK
        self.close()  # закрываем окно редактирования

    def delete(self):  # функция для удаления книги
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        cursor.executescript(
            f"""DELETE from book where id = {self.id}""")  # удаляем из book
        cursor.executescript(
            f"""DELETE from book_filters_keys where id = {self.id}""")  # удаляем из book_filters_keys
        cursor.executescript(
            f"""DELETE from book_filters_values where id = {self.id}""")  # удаляем из book_filters_values
        cursor.executescript(
            f"""DELETE from book_path_to_file where id = {self.id}""")  # удаляем из book_path_to_file

        for i, g in enumerate(list(cursor.execute(f"""select * from book""").fetchall())): # проходим по всем книгам в таблице book
            cursor.executescript(str(f"""UPDATE book SET id
                                = '{i + 1}' where id = {str(g[0])}"""))  # обновляем id книг в таблице book
            cursor.executescript(str(f"""UPDATE book_filters_keys SET id
                                = '{i + 1}' where id = {str(g[0])}"""))  # обновляем id книг в таблице book_filters_keys
            cursor.executescript(str(f"""UPDATE book_filters_values SET id
                                = '{i + 1}' where id = {str(g[0])}"""))  # обновляем id книг в таблице book_filters_values
            cursor.executescript(str(f"""UPDATE book_path_to_file SET id
                                = '{i + 1}' where id = {str(g[0])}"""))  # обновляем id книг в таблице book_path_to_file
        
        self.main.up_date(list(cursor.execute(f"""select * from book""").fetchall())) # обновляем главное окно
        connection.close()  # закрываем базу данных Base_of_booK
        self.close()  # закрываем окно редактирования
    
    def add_path(self):
        file_name = QFileDialog.getOpenFileName(self)[0] # получение пути к файлу
        self.PatH.setText(file_name) # выводим путь к файлу на поле QLabel
    
    def closeEvent(self, *k):
        super().closeEvent(*k)
        self.main.f()
# конец класса окна редактирования и удаления книги

# класс для окна с настройками
class SettingS(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setGeometry(300, 300, 500, 300)
        self.main = main
        self.settings()
    
    def settings(self):
        self.BOX_color = QWidget(self) # родительский виджет для QVBoxLayout
        self.BOX_color.setGeometry(20, 20, 100, 280) # расположение родительского виджета для QVBoxLayout
        self.BOX_model = QVBoxLayout(self.BOX_color) # 

        radio_button = QRadioButton("light") # создаём QRadioButton
        radio_button.toggled.connect(lambda radio_btn, name="light": self.temm(name))
        self.BOX_model.addWidget(radio_button)
        radio_button = QRadioButton("dark") # создаём QRadioButton
        radio_button.toggled.connect(lambda radio_btn, name="dark": self.temm(name))
        self.BOX_model.addWidget(radio_button)
        radio_button = QRadioButton("blue") # создаём QRadioButton
        radio_button.toggled.connect(lambda radio_btn, name="blue": self.temm(name))
        self.BOX_model.addWidget(radio_button)
        radio_button = QRadioButton("gray") # создаём QRadioButton
        radio_button.toggled.connect(lambda radio_btn, name="gray": self.temm(name))
        self.BOX_model.addWidget(radio_button)
        radio_button = QRadioButton("yellow") # создаём QRadioButton
        radio_button.toggled.connect(lambda radio_btn, name="yellow": self.temm(name))
        self.BOX_model.addWidget(radio_button)
        radio_button = QRadioButton("rainbow") # создаём QRadioButton
        radio_button.toggled.connect(lambda radio_btn, name="rainbow": self.temm(name))
        self.BOX_model.addWidget(radio_button)
        radio_button = QRadioButton("green") # создаём QRadioButton
        radio_button.toggled.connect(lambda radio_btn, name="green": self.temm(name))
        self.BOX_model.addWidget(radio_button)
    
    def temm(self, name):
        _light_ = [(255, 255, 255, 0, 0, 0)]
        _dark_ = [(0, 0, 0, 255, 255, 255)]
        _blue_ = [(135, 206, 235, 0, 0, 0), (65, 105, 225, 0, 0, 0), (135, 206, 235, 0, 0, 0), (175, 238, 238, 0, 0, 0)]
        _gray_ = [(10, 10, 10, 255, 255, 255), (20, 20, 20, 255, 255, 255), (30, 30, 30, 255, 255, 255)]
        _yellow_ = [(255, 215, 0, 0, 0, 0), (255, 255, 0, 0, 0, 0), (255, 165, 0, 0, 0, 0)]
        _rainbow_ = [(255, 0, 0, 0, 0, 0), (255, 69, 0, 0, 0, 0), (255, 255, 0, 0, 0, 0), (0, 255, 0, 0, 0, 0),
                 (0, 0, 255, 0, 0, 0), (128, 0, 128, 0, 0, 0)][::-1]
        _green_ = [(0, 255, 0, 0, 0, 0), (154, 205, 50, 0, 0, 0), (0, 128, 0, 0, 0, 0)]
        _all_1 = [_light_, _dark_, _blue_, _gray_, _yellow_, _rainbow_, _green_]
        _all_2 = ["light", "dark", "blue", "gray", "yellow", "rainbow", "green"]

        checkboxes = self.main.findChildren(QWidget)
        color = _all_1[_all_2.index(name)]
        self.main.setStyleSheet(f"""background: rgb{color[0][0], color[0][1], color[0][2]}; 
                color: rgb{color[0][3], color[0][4], color[0][5]};""")
        for i, item in enumerate(checkboxes):
            item.setStyleSheet(f"""background: rgb{color[i % len(color)][0], color[i % len(color)][1], color[i % len(color)][2]}; 
                color: rgb{color[i % len(color)][3], color[i % len(color)][4], color[i % len(color)][5]};""")
        self.main.LinE.setStyleSheet(f"""background: rgb{color[-1][0], color[-1][1], color[-1][2]}; 
                color: rgb{color[-1][3], color[-1][4], color[-1][5]};""")
        connection = sqlite3.connect("Base_for_booK.sqlite") # открываем базу данных Base_of_booK
        cursor = connection.cursor()  # создаём cursor базы данных Base_of_booK
        cursor.executescript(f"""update settings set color = '{name}' where id = 1""")
        connection.close()  # закрываем базу данных Base_of_booK
# конец класса окна с настройками

# создание главного окна
app = QApplication(sys.argv)
MainWindow_main = MainWindow()
MainWindow_main.show()
sys.exit(app.exec())