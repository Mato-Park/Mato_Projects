import sys
import datetime as dt
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import psycopg2

class InsertWindow(QDialog):
    def __init__(self, mainWindowLeft, mainWindowTop, dialogWidth, dialogHeight):
        super().__init__()

        dialogLeft = mainWindowLeft + 200
        dialogTop = mainWindowTop + 80
        self.setGeometry(dialogLeft, dialogTop, dialogWidth, dialogHeight)
        self.setWindowTitle("Insert Dialog v1.0")
    
        self.setupUI()
    
    def setupUI(self):

        vbox = QVBoxLayout()

        # 일자 선택
        self.label1 = QLabel("일   자: ", self)
        self.dateEdit1 = QDateEdit(self)
        self.dateEdit1.setDisplayFormat('yyyy-MM-dd')
        self.dateEdit1.setDate(QDate.currentDate())
        self.dateEdit1.setCalendarPopup(True)

        # 시간 선택
        self.label2 = QLabel("시   간: ", self)
        self.timeEdit1 = QTimeEdit(self)
        self.timeEdit1.setDisplayFormat('hh:mm')
        self.timeEdit1.setTime(QTime.currentTime())

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.dateEdit1)
        hbox1.addWidget(self.label2)
        hbox1.addWidget(self.timeEdit1)

        # db 연결 - 데이터 가져오기
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        # 지불방식 선택
        self.label3 = QLabel("지불방식 선택: ", self) # 수입/지출 선택에 따라 다른 화면이 표시되게 선택
        self.paymentsCombo = QComboBox(self)
        query = """SELECT DISTINCT PAYMENTS_NAME, PAYMENTS_ID FROM LEDGER.PAYMENTS ORDER BY PAYMENTS_ID;""" # 지불방식 가져오기
        cursor.execute(query)
        category = [i[0] for i in cursor.fetchall()]
        category.append('기타')
        self.paymentsCombo.addItems(category)
        
        # Category 선택
        self.label4 = QLabel("카테고리 설정: ", self)
        self.categoryCombo = QComboBox(self)
        query = """SELECT * FROM LEDGER.CATEGORY;"""
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
        self.insertButton = QPushButton("입력", self)
        self.exitButton = QPushButton("나가기", self)
        self.insertButton.clicked.connect(self.insertButtonClicked)
        self.exitButton.clicked.connect(self.exitButtonClicked)

        hbox4 = QHBoxLayout()
        hbox4_1 = QVBoxLayout()
        hbox4_1.addWidget(self.label8)
        hbox4_1.addWidget(self.memoEdit)
        hbox4_2 = QVBoxLayout()
        hbox4_2.addWidget(self.insertButton)
        hbox4_2.addWidget(self.exitButton)
        hbox4.addLayout(hbox4_1)
        hbox4.addLayout(hbox4_2)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

    def insertButtonClicked(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        get_query1 = """SELECT DISTINCT PAYMENTS_ID, PAYMENTS_NAME FROM LEDGER.PAYMENTS;"""
        cursor.execute(get_query1)
        payments_tup = cursor.fetchall()
        payments_dict = dict(map(reversed, payments_tup))
        
        get_query2 = """SELECT * FROM LEDGER.CATEGORY;"""
        cursor.execute(get_query2)
        category = cursor.fetchall()
        category_dict = dict(map(reversed, category))

        day = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
        date = self.dateEdit1.date().toString("yyyy-MM-dd")
        date2 = dt.datetime.strptime(self.dateEdit1.date().toString("yyyy-MM-dd"), "%Y-%m-%d")
        time = self.timeEdit1.time().toString("hh:mm")
        ammounts = int(self.priceInput.text())
        place = self.lineEdit1.text()
        memo = self.memoEdit.toPlainText()
        payments = self.paymentsCombo.currentText()
        category = self.categoryCombo.currentText()

        insert_query = f"""INSERT INTO LEDGER.TRANSACTION (trans_date, trans_time, day, type, category, amounts, memo, place, payments) 
                        VALUES('{date}', '{time}', '{day[date2.weekday()]}', 2, '{category_dict[category]}', {ammounts}, '{memo}', '{place}',
                         '{payments_dict[payments]}');"""
        cursor.execute(insert_query)
        cursor.execute("COMMIT")

    def exitButtonClicked(self):
        self.close()
        

# app = QApplication(sys.argv)
# window = InsertWindow()
# window.show()
# app.exec()