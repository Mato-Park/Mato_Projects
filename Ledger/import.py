import sys
import datetime as dt
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import psycopg2
from insert_dialog import InsertWindow

class importText(QDialog):
    def __init__(self, mainWindowLeft, mainWindowTop):
        super().__init__()

        dialogWidth = 800
        dialogHeight = 700
        dialogLeft = mainWindowLeft + 100
        dialogTop = mainWindowTop + 15
        
        self.setGeometry(dialogLeft, dialogTop, dialogWidth, dialogHeight)
        self.setWindowTitle("text로부터 가져오기")
        self.setModal(True)

        self.setupUI()
    
    def setupUI(self):
        # db 연결
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        # 미저장 데이터 가져오기
        self.getButton1 = QPushButton("가져오기", self)
        self.getButton1.clicked.connect(self.getButtonClicked)
        
        self.table1 = QTableWidget(self)
        self.table1.setRowCount(1)
        self.table1.setColumnCount(5)
        self.table1.setColumnWidth(0, 40)
        self.table1.setHorizontalHeaderLabels(('No', 'Date', 'Time', 'Ammounts', 'Place'))
        self.table1.setMinimumWidth(600)
        self.table1.setSortingEnabled(True)
        self.table1.setEditTriggers(QAbstractItemView.EditTrigger(0)) # 수정 못하게 막기
        self.table1.doubleClicked.connect(self.tableDoubleClicked)
        
        self.exitButton = QPushButton("나가기", self)
        self.exitButton.clicked.connect(self.exitButtonClicked)

        self.label1 = QLabel("Date: ", self)
        self.dateEdit1 = QDateEdit(self)
        self.dateEdit1.setDisplayFormat('yyyy-MM-dd')
        self.dateEdit1.setDate(QDate.currentDate())
        self.dateEdit1.setCalendarPopup(True)

        self.label2 = QLabel("Time: ", self)
        self.timeEdit1 = QTimeEdit(self)
        self.timeEdit1.setDisplayFormat('hh:mm')
        self.timeEdit1.setTime(QTime.currentTime())

        self.label3 = QLabel("Payments: ", self)
        self.paymentsCombo = QComboBox(self)
        query = """SELECT DISTINCT PAYMENTS_NAME, PAYMENTS_ID FROM LEDGER.PAYMENTS ORDER BY PAYMENTS_ID ASC;"""
        cursor.execute(query)
        category = [i[0] for i in cursor.fetchall()]
        self.paymentsCombo.addItems(category)

        self.label4 = QLabel("Category: ", self)
        self.categoryCombo = QComboBox(self)
        query = """SELECT * FROM LEDGER.CATEGORY;"""
        cursor.execute(query)
        type_tup = cursor.fetchall()
        type_list = [i[1] for i in type_tup]
        self.categoryCombo.addItems(type_list)

        self.label5 = QLabel("Place: ", self)
        self.lineEdit1 = QLineEdit(self)
        # self.lineEdit1.setMaximumWidth(300)

        self.label6 = QLabel("memo: ", self)
        self.memoEdit = QTextEdit()
        self.memoEdit.setAcceptRichText(False)
        # self.memoEdit.setMaximumWidth(300)

        self.label7 = QLabel("Ammounts: ", self)
        self.ammountsInput = QLineEdit()
        self.ammountsInput.setMaxLength(10)
        # self.ammountsInput.setMaximumWidth(200)
        self.label8 = QLabel("원(￦)", self)

        self.insertButton = QPushButton('Insert!', self)
        self.insertButton.clicked.connect(self.insertButtonClicked)

        layout = QHBoxLayout()
        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.getButton1)
        layout_1.addWidget(self.table1)
        layout_1.addWidget(self.exitButton)

        layout_2 = QVBoxLayout()
        layout_2_1 = QHBoxLayout()
        layout_2_1.addWidget(self.label1)
        layout_2_1.addWidget(self.dateEdit1)
        layout_2_2 = QHBoxLayout()
        layout_2_2.addWidget(self.label2)
        layout_2_2.addWidget(self.timeEdit1)
        layout_2_3 = QHBoxLayout()
        layout_2_3.addWidget(self.label3)
        layout_2_3.addWidget(self.paymentsCombo)
        layout_2_4 = QHBoxLayout()
        layout_2_4.addWidget(self.label4)
        layout_2_4.addWidget(self.categoryCombo)
        layout_2_5 = QVBoxLayout()
        layout_2_5.addWidget(self.label5)
        layout_2_5.addWidget(self.lineEdit1)
        layout_2_5.addWidget(self.label6)
        layout_2_5.addWidget(self.memoEdit)
        layout_2_6 = QHBoxLayout()
        layout_2_6.addWidget(self.label7)
        layout_2_6.addWidget(self.ammountsInput)
        layout_2_6.addWidget(self.label8)
        layout_2.addLayout(layout_2_1)
        layout_2.addLayout(layout_2_2)
        layout_2.addLayout(layout_2_3)
        layout_2.addLayout(layout_2_4)
        layout_2.addLayout(layout_2_5)
        layout_2.addLayout(layout_2_6)
        layout_2.addWidget(self.insertButton)

        layout.addLayout(layout_1)
        layout.addLayout(layout_2)
        self.setLayout(layout)

        cursor.close()

    def getButtonClicked(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()
        query = """SELECT id, date, time, ammounts, place FROM message.text_message WHERE SAVE_CHECK = FALSE;"""
        cursor.execute(query)
        self.getResults = cursor.fetchall()
        self.table1.setRowCount(len(self.getResults))
        
        i = 0 
        for row in self.getResults:
            j = 0
            for col in row:
                item = QTableWidgetItem(str(col))
                # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignVCenter)
                self.table1.setItem(i, j, item)
                j += 1
            i += 1
    
    def tableDoubleClicked(self):
        global message_id
        global row_number

        row = self.table1.currentIndex().row()
        date_format = "%Y-%m-%d"
        date = dt.datetime.strptime(self.table1.item(row, 1).text(), date_format)
        time_format = "hh:mm:ss"
        time = QTime.fromString(self.table1.item(row, 2).text(), time_format)
        self.dateEdit1.setDate(date)
        self.timeEdit1.setTime(time)

        ammounts = self.table1.item(row, 3).text()
        self.ammountsInput.setText(ammounts)
        place = self.table1.item(row, 4).text()
        self.lineEdit1.setText(place)
        message_id = int(self.table1.item(row, 0).text())
        row_number = self.table1.currentRow()
    
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
        ammounts = int(self.ammountsInput.text())
        place = self.lineEdit1.text()
        memo = self.memoEdit.toPlainText()
        payments = self.paymentsCombo.currentText()
        category = self.categoryCombo.currentText()

        insert_query = f"""INSERT INTO LEDGER.TRANSACTION (trans_date, trans_time, day, type, category, amounts, memo, place, payments) 
                        VALUES('{date}', '{time}', '{day[date2.weekday()]}', 2, '{category_dict[category]}', {ammounts}, '{memo}', '{place}',
                         '{payments_dict[payments]}');"""
        cursor.execute(insert_query)
        cursor.execute("COMMIT")

        insert_query2 = f"""UPDATE MESSAGE.TEXT_MESSAGE SET SAVE_CHECK = TRUE WHERE  ID = {message_id};"""
        cursor.execute(insert_query2)
        cursor.execute("COMMIT")
        cursor.close()

        self.table1.removeRow(row_number)


    def exitButtonClicked(self):
        self.close()


class importDashboard(QMainWindow):
    def __init__(self):

        super().__init__()

        ag = QGuiApplication.primaryScreen().availableGeometry()
        mainWindowWidth = 800
        mainWindowHeigt = 700
        mainWindowLeft = (ag.width() - mainWindowWidth) / 2
        mainWindowTop = (ag.height() - mainWindowHeigt) / 2
        self.setGeometry(mainWindowLeft, mainWindowTop, mainWindowWidth, mainWindowHeigt)
        self.setWindowTitle("PImport_Dashboard v1.0")
    
        self.setupUI()
    
    def setupUI(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # 제목
        self.label1 = QLabel("Ledger Table", self)
        font1 = self.label1.font()
        font1.setPointSize(50)
        self.label1.setFont(font1)
        # self.button1 = QPushButton("조  회", self)
        # self.button1.setMaximumWidth(150)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label1)
        # hbox1.addWidget(self.button1)

        # 테이블 생성
        self.selectTable1 = QTableWidget(self)
        # self.selectTable1.setRowCount(1)
        self.selectTable1.setColumnCount(6)
        self.selectTable1.setColumnWidth(0, 40)
        self.selectTable1.setHorizontalHeaderLabels(('No', 'Date', 'Time', 'Category', 'Ammounts', 'Place'))

        # 버튼 생성
        self.selectButton = QPushButton("조회하기", self)
        self.getfromtextButton = QPushButton("가져오기", self)
        self.inputButton = QPushButton("입력하기", self)
        self.exitButton = QPushButton("나가기", self)

        self.selectButton.clicked.connect(self.selectButtonClicked)
        self.exitButton.clicked.connect(self.exitButtonClicked)
        self.getfromtextButton.clicked.connect(self.textButtonClicked)
        self.inputButton.clicked.connect(self.inputButtonClicked)

        hbox2 = QHBoxLayout()
        hbox2_1 = QVBoxLayout()
        hbox2_1.addWidget(self.selectTable1)
        hbox2_2 = QVBoxLayout()
        hbox2_2.addWidget(self.selectButton)
        hbox2_2.addWidget(self.getfromtextButton)
        hbox2_2.addWidget(self.inputButton)
        hbox2_2.addWidget(self.exitButton)
        hbox2.addLayout(hbox2_1)
        hbox2.addLayout(hbox2_2)


        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        wid.setLayout(vbox)

    def selectButtonClicked(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        query = """
                SELECT A.TRANS_ID,
                        A.TRANS_DATE,
                        A.TRANS_TIME,
                        B.CATEGORY_NAME,
                        A.AMOUNTS,
                        A.PLACE
                FROM
                        LEDGER.TRANSACTION AS A
                        JOIN
                            LEDGER.CATEGORY AS B
                            ON A.CATEGORY = B.CATEGORY_ID
                ORDER BY A.TRANS_ID DESC;
                """
        cursor.execute(query)
        self.results = cursor.fetchall()
        self.selectTable1.setRowCount(len(self.results))

        i = 0 
        for row in self.results:
            j = 0
            for col in row:
                item = QTableWidgetItem(str(col))
                # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignVCenter)
                self.selectTable1.setItem(i, j, item)
                j += 1
            i += 1

        cursor.close()


    def inputButtonClicked(self):
        sg = self.geometry()
        inputwindow = InsertWindow(sg.left(), sg.top(), 500, 400)
        inputwindow.exec()

    def textButtonClicked(self):
        sg = self.geometry()
        textdialog = importText(sg.left(), sg.top())
        textdialog.exec()
    
    def exitButtonClicked(self):
        self.close()

app = QApplication(sys.argv)
window = importDashboard()
window.show()
app.exec()