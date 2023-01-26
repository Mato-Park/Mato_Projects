import sys
import datetime as dt
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import psycopg2


class InsertWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ag = QGuiApplication.primaryScreen().availableGeometry()
        mainWindowWidth = 800
        mainWindowHeigt = 700
        mainWindowLeft = (ag.width() - mainWindowWidth) / 2
        mainWindowTop = (ag.height() - mainWindowHeigt) / 2
        self.setGeometry(mainWindowLeft, mainWindowTop, mainWindowWidth, mainWindowHeigt)
        self.setWindowTitle("PLedger_Insert v1.0")
    
        self.setupUI()
    
    def setupUI(self):

        wid = QWidget(self)
        self.setCentralWidget(wid)

        # 일자 선택
        self.label1 = QLabel("일   자: ", self)
        self.dateEdit1 = QDateEdit(self)
        self.dateEdit1.setDisplayFormat('yyyy-MM-dd')
        self.dateEdit1.setDate(QDate.currentDate())
        self.dateEdit1.setCalendarPopup(True)

        # 시간 선택
        self.label2 = QLabel("시   간: ", self)
        self.timeEdit1 = QTimeEdit(self)
        self.timeEdit1.setDisplayFormat('AP hh:mm')
        self.timeEdit1.setTime(QTime.currentTime())

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.dateEdit1)
        hbox1.addWidget(self.label2)
        hbox1.addWidget(self.timeEdit1)

        # Category 선택
        self.label3 = QLabel("카테고리 설정: ", self)
        self.categoryCombo = QComboBox(self)

        db = psycopg2.connect(host = 'localhost', dbname = 'test', user = 'mato', port = 5432)
        cursor = db.cursor()
        query = """SELECT * FROM CATEGORY"""
        cursor.execute(query)
        type_tup = cursor.fetchall()
        type_list = [i[1] for i in type_tup]
        self.categoryCombo.addItems(type_list)

        # 금액 입력
        self.label4 = QLabel("금액 입력: ", self)
        self.priceInput = QLineEdit(self)
        self.priceInput.setMaxLength(10)
        self.priceInput.setMaximumWidth(250)
        self.label5 = QLabel("원(￦)", self)
        self.label5.setMaximumWidth(50)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.label3)
        hbox2.addWidget(self.categoryCombo)
        hbox2.addWidget(self.label4)
        hbox2.addWidget(self.priceInput)
        hbox2.addWidget(self.label5)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        wid.setLayout(vbox)


app = QApplication(sys.argv)
window = InsertWindow()
window.show()
app.exec()