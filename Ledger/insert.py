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
        mainWindowWidth = 500
        mainWindowHeigt = 400
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

        # db 연결 - 데이터 가져오기
        db = psycopg2.connect(host = 'localhost', dbname = 'test', user = 'mato', port = 5432)
        cursor = db.cursor()

        # 지불방식 선택
        self.label3 = QLabel("지불방식 선택: ", self) # 수입/지출 선택에 따라 다른 화면이 표시되게 선택
        self.paymentsCombo = QComboBox(self)
        query = """SELECT DISTINCT PAYMENTS_TYPE FROM PAYMENTS;""" # 지불방식 가져오기
        cursor.execute(query)
        category = [i[0] for i in cursor.fetchall()]
        category.append('기타')
        self.paymentsCombo.addItems(category)
        
        # Category 선택
        self.label4 = QLabel("카테고리 설정: ", self)
        self.categoryCombo = QComboBox(self)
        query = """SELECT * FROM CATEGORY;"""
        cursor.execute(query)
        type_tup = cursor.fetchall()
        type_list = [i[1] for i in type_tup]
        self.categoryCombo.addItems(type_list)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.label3)
        hbox2.addWidget(self.paymentsCombo)
        hbox2.addWidget(self.label4)
        hbox2.addWidget(self.categoryCombo)

        # 사용처 입력
        self.label5 = QLabel("사용처 입력: ", self)
        self.lineEdit1 = QLineEdit(self)

        # 금액 입력
        self.label6 = QLabel("금액 입력: ", self)
        self.priceInput = QLineEdit(self)
        self.priceInput.setMaxLength(10)
        # self.priceInput.setMaximumWidth(250)
        self.label7 = QLabel("원(￦)", self)
        # self.label5.setMaximumWidth(50)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.label5)
        hbox3.addWidget(self.lineEdit1)
        hbox3.addWidget(self.label6)
        hbox3.addWidget(self.priceInput)
        hbox3.addWidget(self.label7)

        # 메모 입력
        self.label8 = QLabel("메  모", self)
        self.memoEdit = QTextEdit()
        self.memoEdit.setAcceptRichText(False)

        # 입력/나가기 버튼 생성
        self.inputButton = QPushButton("입력", self)
        self.exitButton = QPushButton("나가기", self)
        self.exitButton.clicked.connect(self.exitButtonClicked)

        hbox4 = QHBoxLayout()
        hbox4_1 = QVBoxLayout()
        hbox4_1.addWidget(self.label8)
        hbox4_1.addWidget(self.memoEdit)
        hbox4_2 = QVBoxLayout()
        hbox4_2.addWidget(self.inputButton)
        hbox4_2.addWidget(self.exitButton)
        hbox4.addLayout(hbox4_1)
        hbox4.addLayout(hbox4_2)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        wid.setLayout(vbox)

    def exitButtonClicked(self):
        self.close()
        

app = QApplication(sys.argv)
window = InsertWindow()
window.show()
app.exec()