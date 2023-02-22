import sys
import datetime as dt
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import psycopg2
import sqlite3
from os.path import expanduser

class messageDashboard(QMainWindow):
    def __init__(self):

        super().__init__()

        ag = QGuiApplication.primaryScreen().availableGeometry()
        mainWindowWidth = 800
        mainWindowHeight = 700
        mainWindowLeft = (ag.width() - mainWindowWidth) / 2
        mainWindowTop = (ag.height() - mainWindowHeight) / 2
        self.setGeometry(mainWindowLeft, mainWindowTop, mainWindowWidth, mainWindowHeight)
        self.setWindowTitle("Message Dashboard v1")

        self.setupUI()

    def setupUI(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Title
        self.label1 = QLabel("Message Dashboard", self)
        font1 = self.label1.font()
        font1.setPointSize(50)
        self.label1.setFont(font1)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label1)

        # Register Number
        self.label2 = QLabel("Registered Number", self)
        font2 = self.label2.font()
        font2.setPointSize(20)
        self.label2.setFont(font2)

        self.numberTable = QTableWidget(self)
        self.numberTable.setColumnCount(3)
        self.numberTable.setColumnWidth(0, 40)
        self.numberTable.setHorizontalHeaderLabels(('No', 'Number', 'Name'))

        self.registerButton = QPushButton("Register", self)

        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        query = """SELECT * FROM MESSAGE.MESSAGE_ID;"""
        cursor.execute(query)
        self.results = cursor.fetchall()
        self.numberTable.setRowCount(len(self.results))

        i = 0
        for row in self.results:
            j = 0
            for col in row:
                item = QTableWidgetItem(str(col))
                self.numberTable.setItem(i, j, item)
                j += 1
            i += 1
        
        hbox2 = QVBoxLayout()
        hbox2.addWidget(self.label2)
        hbox2_1 = QHBoxLayout()
        hbox2_1.addWidget(self.numberTable)
        hbox2_1.addWidget(self.registerButton)
        hbox2.addLayout(hbox2_1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        wid.setLayout(vbox)

app = QApplication(sys.argv)
window = messageDashboard()
window.show()
app.exec()