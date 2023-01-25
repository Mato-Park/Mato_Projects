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

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)

        wid.setLayout(vbox)


app = QApplication(sys.argv)
window = InsertWindow()
window.show()
app.exec()