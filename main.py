import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, \
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Students Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "MOBILE"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")
        edit_button.clicked.connect(self.edit)
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)



    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add a new student")
        self.setFixedSize(300, 300)

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        self.student_course = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.student_course.addItems(courses)
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile")
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)

        layout = QVBoxLayout()
        layout.addWidget(self.student_name)
        layout.addWidget(self.student_course)
        layout.addWidget(self.student_mobile)
        layout.addWidget(add_button)
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.student_course.itemText(self.student_course.currentIndex())
        mobile = self.student_mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search")
        self.setFixedSize(300,300)
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("enter the name")
        button_search = QPushButton("Find")
        button_search.clicked.connect(self.find_name)

        layout = QVBoxLayout()
        layout.addWidget(self.search_name)
        layout.addWidget(button_search)
        self.setLayout(layout)

    def find_name(self):
        target_name = self.search_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (target_name,))
        rows = list(result)
        items = main_window.table.findItems(target_name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()
        self.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()

sys.exit(app.exec())