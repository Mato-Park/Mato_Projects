import sys
import datetime as dt
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import psycopg2
import sqlite3
from os.path import expanduser

def fetch_db_data(db, query):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(query)

        return cursor.fetchall()
    except Exception as e:
        sys.exit("Error reading the database: %s" %e)

class registerNumber(QDialog):
    def __init__(self, mainWindowLeft, mainWindowTop):
        super().__init__()

        dialogWidth = 300
        dialogHeight = 200
        dialogLeft = mainWindowLeft + 50
        dialogTop = mainWindowTop + 50

        self.setGeometry(dialogLeft, dialogTop, dialogWidth, dialogHeight)
        self.setWindowTitle("Register #")
        self.setModal(True)

        self.setupUI()
        
    def setupUI(self):

        self.label1 = QLabel('Number: ')
        self.label1.setMinimumWidth(50)
        self.numberEdit = QLineEdit(self)

        self.label2 = QLabel('Name: ')
        self.label2.setMinimumWidth(50)
        self.nameEdit = QLineEdit(self)
        
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.numberEdit)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.nameEdit)

        self.insertButton = QPushButton('Register!', self)
        self.insertButton.setMaximumWidth(100)
        self.insertButton.clicked.connect(self.insertButtonClicked)
        self.exitButton = QPushButton('Exit', self)
        self.exitButton.setMaximumWidth(100)
        self.exitButton.clicked.connect(self.exitButtonClicked)

        layout3 = QHBoxLayout()
        layout3.addWidget(self.insertButton)
        layout3.addWidget(self.exitButton)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)

        self.setLayout(layout)
    
    def insertButtonClicked(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        number = self.numberEdit.text()
        name = self.nameEdit.text()

        try:
            query = f"""INSERT INTO MESSAGE.MESSAGE_ID (NUMBER, NAME) VALUES('{number}', '{name}');"""
            cursor.execute(query)
            db.commit()
            QMessageBox.about(self, 'commit status', 'Commit Success!')

            self.numberEdit.clear()
            self.nameEdit.clear()
        except (Exception, psycopg2.DatabaseError) as error:
            db.rollback()

            QMessageBox.about(self, 'commit status', f"Error in transaction, '{error}'")

    def exitButtonClicked(self):
        self.close()

class messageDashboard(QMainWindow):
    def __init__(self):

        super().__init__()

        ag = QGuiApplication.primaryScreen().availableGeometry()
        mainWindowWidth = 900
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
        font1.setPointSize(30)
        self.label1.setFont(font1)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label1)

        # Register Number
        self.label2 = QLabel("Registered Number", self)
        font2 = self.label2.font()
        font2.setPointSize(20)
        self.label2.setFont(font2)
        self.label_duration = QLabel("Duration: ", self)
        self.label_duration.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.combo_duration = QComboBox(self)
        combo_list = [str(i) for i in range(1, 10)]
        self.combo_duration.addItems(combo_list)
        self.combo_duration.setCurrentIndex(4)
        self.combo_duration.setMaximumWidth(100)
        # self.combo_duration.set

        self.numberTable = QTableWidget(self)
        self.numberTable.setColumnCount(3)
        self.numberTable.setColumnWidth(0, 40)
        self.numberTable.setHorizontalHeaderLabels(('No', 'Number', 'Name'))
        # self.numberTable.setMaximumHeight(100)
        self.numberTable.setEditTriggers(QAbstractItemView.EditTrigger(0)) # 수정 못하게 막기
        self.numberTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # row 선택
        self.numberTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection) # 한개만 선택

        self.numbershowButton = QPushButton("Show", self)
        self.numbershowButton.setMaximumWidth(100)
        self.numbershowButton.clicked.connect(self.numbershowButtonClicked)
        self.registerButton = QPushButton("Register", self)
        self.registerButton.setMaximumWidth(100)
        self.registerButton.clicked.connect(self.registerButtonClicked)
        self.getButton = QPushButton('Get', self)
        self.getButton.setMaximumWidth(100)
        self.getButton.clicked.connect(self.getButtonClicked)
        
        hbox2 = QVBoxLayout()
        hbox2_0 = QHBoxLayout()
        hbox2_0.addWidget(self.label2)
        hbox2_0.addWidget(self.label_duration)
        hbox2_0.addWidget(self.combo_duration)
        hbox2_1 = QHBoxLayout()
        hbox2_1_1 = QVBoxLayout()
        hbox2_1_1.addWidget(self.numberTable)
        hbox2_1_2 = QVBoxLayout()
        hbox2_1_2.addWidget(self.numbershowButton)
        hbox2_1_2.addWidget(self.registerButton)
        hbox2_1_2.addWidget(self.getButton)
        hbox2_1.addLayout(hbox2_1_1)
        hbox2_1.addLayout(hbox2_1_2)
        hbox2.addLayout(hbox2_0)
        hbox2.addLayout(hbox2_1)

        # 문자 가져오기
        self.label3 = QLabel("Text Message Table", self)
        font3 = self.label3.font()
        font3.setPointSize(20)
        self.label3.setFont(font3)
        # self.numberText = QText
        self.textTable = QTableWidget(self)
        self.textTable.setColumnCount(7)
        self.textTable.setHorizontalHeaderLabels(('Id', 'Number', 'Date', 'Text', 'Ammounts', 'place', 'check'))
        self.textTable.setMinimumHeight(350)
        self.textTable.setEditTriggers(QAbstractItemView.EditTrigger(0)) # 수정 못하게 막기
        # self.textTable.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection) # 다중선택 가능
        self.textTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # row 선택
        self.textTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection) # 한개만 선택
        # self.textTable.doubleClicked.connect(self.textTableDoubleClicked)

        self.textshowButton = QPushButton("Show", self)
        self.textshowButton.setMaximumWidth(100)
        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.setMaximumWidth(100)

        self.textshowButton.clicked.connect(self.textshowButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

        hbox3 = QVBoxLayout()
        hbox3.addWidget(self.label3)
        hbox3_1 = QHBoxLayout()
        hbox3_1.addWidget(self.textTable)
        hbox3_2 = QVBoxLayout()
        hbox3_2.addWidget(self.textshowButton)
        hbox3_2.addWidget(self.deleteButton)
        hbox3_1.addLayout(hbox3_2)
        hbox3.addLayout(hbox3_1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        wid.setLayout(vbox)

    def numbershowButtonClicked(self):
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

    def registerButtonClicked(self):
        sg = self.geometry()
        registerdialog = registerNumber(sg.left(), sg.top())
        registerdialog.exec()

    def getButtonClicked(self):
        if len(self.numberTable.selectedItems()) == 0:
            QMessageBox.about(self, 'Error!', 'Please Select One Row!')
        else:
            text_number = self.numberTable.selectedItems()[1].text()
            duration_day = self.combo_duration.currentText()

            db_path = expanduser("~") + "/Library/Messages/chat.db"
            query = f"""SELECT text, handle.id, datetime((date / 1000000000) + 978307200, 'unixepoch', 'localtime'),
                    handle.service, message.destination_caller_id, message.is_from_me, date((date/1000000000)+978307200, 'unixepoch', 'localtime')
                    FROM message JOIN handle ON message.handle_id = handle.ROWID
                    WHERE handle.id == '{text_number}' and message.is_from_me == 0 and 
                    date((date/1000000000)+978307200, 'unixepoch', 'localtime') >= date('now', 'localtime', '-{duration_day} days')
                    ORDER BY date asc"""

            rval = fetch_db_data(db_path, query)

            db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
            cursor = db.cursor()

            for i in rval:
                try:
                    number = i[1]
                    text_original = i[0]
                    date = i[6]
                    time = i[0].split(" ")[3]
                    ammounts = int(i[0].split(" ")[4][:-1].replace(',', ''))
                    place = i[0].split(" ")[5]
                    query = f"""INSERT INTO message.text_message (number, text_original, date, time, ammounts, place) 
                                VALUES('{number}', '{text_original}', '{date}', '{time}', {ammounts}, '{place}')
                                ON CONFLICT (TEXT_ORIGINAL)
                                DO NOTHING;"""
                    cursor.execute(query)
                    cursor.execute("COMMIT")
                    print("Insert Sucess!! ======================")
                except Exception as e:
                    QMessageBox.about(self, 'Fail!', 'Insert Fail!')

            QMessageBox.about(self, 'Good!', 'Success!!')
    
        # print(len(self.numberTable.selectedItems()))
                
            # print(self.numberTable.selectedItems()) #  아무것도 선택하지 않으면 empty list 반환
            # print(self.numberTable.selectedItems()[1].text())


    def textshowButtonClicked(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        query = """SELECT ID, NUMBER, TEXT_ORIGINAL, DATE, AMMOUNTS, PLACE, SAVE_CHECK FROM MESSAGE.TEXT_MESSAGE
                    WHERE SAVE_CHECK = FALSE
                    ORDER BY ID DESC;"""
        cursor.execute(query)
        self.results = cursor.fetchall()
        self.textTable.setRowCount(len(self.results))

        i = 0
        for row in self.results:
            j = 0
            for col in row:
                item = QTableWidgetItem(str(col))
                # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignVCenter)
                self.textTable.setItem(i, j, item)
                j += 1
            i += 1

        self.textTable.resizeColumnsToContents()
        self.textTable.resizeRowsToContents()

    # def textTableDoubleClicked(self):
    #     print(self.textTable.selectedIndexes()[1].row())
        
    def deleteButtonClicked(self):
        if len(self.textTable.selectedItems()) == 0:
            QMessageBox.about(self, 'Error!', 'Please Select One Row!')
        else:
            message = QMessageBox(self)
            message.setWindowTitle('Warning!')
            message.setText('Are you Sure to Delete!?')
            message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            message.setIcon(QMessageBox.Icon.Question)
            reply = message.exec()

            if reply == QMessageBox.StandardButton.Yes:
                message_id = int(self.textTable.selectedItems()[0].text())
                
                db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
                cursor = db.cursor()
                try:
                    query = f"""DELETE FROM MESSAGE.TEXT_MESSAGE WHERE ID = {message_id};"""
                    cursor.execute(query)
                    cursor.execute('COMMIT;')
                    QMessageBox.about(self, 'Delete!', 'Deleted From Table!')
                except (Exception, psycopg2.DatabaseError) as error:
                    db.rollback()

                    QMessageBox.about(self, 'commit status', f"Error in transaction, '{error}'")
            else:
                print('N')
        
        

        # row = self.textTable.rowCount()
        # print(self.textTable.selectedIndexes()[0].row())
        # for i in range(row):
            # print(self.textTable.indexAt(i, 3))
            # print(self.textTable.item(i, 2).text())
            # print(self.textTable.item(i, 1).text())
            # if self.textTable.item(i, 2).checkState() == 2:
            #     number = self.textTable.item(i, 0).text()
            #     date = self.textTable.item(i, 1).text()
            #     print(number, date)


            


app = QApplication(sys.argv)
window = messageDashboard()
window.show()
app.exec()