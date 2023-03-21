import sys
import datetime as dt
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtWebEngineWidgets
import psycopg2
import plotly.graph_objects as go
import plotly.io as pio
from charts import *

class Dashboard(QMainWindow):
    def __init__(self):

        super().__init__()

        ag = QGuiApplication.primaryScreen().availableGeometry()
        mainWindowWidth = ag.width()
        mainWindowHeight = ag.height()
        mainWindowLeft = 0
        mainWindowTop = 0
        self.setGeometry(mainWindowLeft, mainWindowTop, mainWindowWidth, mainWindowHeight)
        self.setWindowTitle("PLedger_Dashboard v1.0")

        self.setupUI()

    def setupUI(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)

        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        # Components 1

        today = dt.date.today()
        self.label1 = QLabel(today.strftime("%Y년 %m월") + " 가계부")
        # fontDB = QFontDatabase()
        # fontDB.addApplicationFont('')
        self.label1.setFont(QFont('고딕체', 20))

        month_first = dt.date(today.year, today.month, 1).strftime('%Y-%m-%d')
        # query = f"""SELECT TYPE, SUM(AMOUNTS) AS AMOUNT_SUM FROM LEDGER.TRANSACTION WHERE TRANS_DATE > '{month_first}' AND TYPE = 2 GROUP BY TYPE;"""
        query1 = """SELECT TYPE, SUM(AMOUNTS) AS AMOUNT_SUM FROM LEDGER.TRANSACTION WHERE TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE) AND TYPE = 2 GROUP BY TYPE;"""
        cursor.execute(query1)
        test = cursor.fetchall()
        self.label2 = QLabel("소비 합계: ", self)
        self.payments_per_month = QLabel(str(test[0][1]) + "원")
        self.label3 = QLabel("일별 소비: ", self)
        query2 = """
                SELECT 
                    SUM(AMOUNTS) / EXTRACT(DAY FROM NOW()) AS AVERAGE_PAY, EXTRACT(DAY FROM NOW()) 
                FROM 
                    LEDGER.TRANSACTION 
                WHERE 
                    TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE) AND TYPE = 2;"""
        cursor.execute(query2)
        results2 = cursor.fetchall()
        self.income_per_month = QLabel(str(int(results2[0][0])) +"원")
        self.label4 = QLabel("남은 금액: ", self)
        self.left = QLabel("!!!!!!!원", self)
        # 주중 소비, 주말 소비 구하기

        # bullet_graph = bulletChart()
        # self.browser3 = QtWebEngineWidgets.QWebEngineView()
        # self.browser3.setHtml(bullet_graph.html)
        # self.browser3.setMaximumHeight(100)

        components1 = QVBoxLayout()
        components1_1 = QHBoxLayout()
        components1_1.addWidget(self.label1)
        components1_2 = QHBoxLayout()
        components1_2.addWidget(self.label2)
        components1_2.addWidget(self.payments_per_month)
        components1_3 = QHBoxLayout()
        components1_3.addWidget(self.label3)
        components1_3.addWidget(self.income_per_month)
        components1_4 = QHBoxLayout()
        components1_4.addWidget(self.label4)
        components1_4.addWidget(self.left)

        components1.addLayout(components1_1)
        components1.addLayout(components1_2)
        components1.addLayout(components1_3)
        components1.addLayout(components1_4)
        # components1.addWidget(self.browser3)

        # Components2

        graph1 = compareChart()
        self.browser1 = QtWebEngineWidgets.QWebEngineView()
        self.browser1.setHtml(graph1.html)

        graph2 = donutChart()
        self.browser2 = QtWebEngineWidgets.QWebEngineView()
        self.browser2.setHtml(graph2.html)

        components2 = QHBoxLayout()
        components2.addWidget(self.browser1)
        components2.addWidget(self.browser2)

        vbox = QVBoxLayout()
        vbox.addLayout(components1)
        vbox.addLayout(components2)

        cursor.close()
        wid.setLayout(vbox)

app = QApplication(sys.argv)
window = Dashboard()
window.show()
app.exec()