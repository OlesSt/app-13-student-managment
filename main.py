import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, \
    QLabel, \
    QWidget, \
    QGridLayout, \
    QLineEdit, \
    QPushButton, \
    QMainWindow, QTableWidget
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Students Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "MOBILE"))
        self.setCentralWidget(self.table)

    def load_data(self):
        pass



app = QApplication(sys.argv)
StudentManagementSystem = MainWindow()
StudentManagementSystem.show()

sys.exit(app.exec())