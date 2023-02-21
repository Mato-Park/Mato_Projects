import sys
import datetime as dt
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtWebEngineWidgets
import psycopg2
import plotly.graph_objects as go

class components2():

    def chart1(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        query = """
        SELECT A.DATE, SUM(A.AMOUNTS_SUM) OVER(ORDER BY A.DATE) AS OVER_SUM
        FROM (
            SELECT TO_CHAR(TRANS_DATE, 'YYYY-MM-DD') AS DATE, SUM(AMOUNTS) AS AMOUNTS_SUM 
            FROM LEDGER.TRANSACTION
            WHERE TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE - INTERVAL '1' MONTH)
            AND TRANS_DATE < DATE_TRUNC('MONTH', CURRENT_DATE)
            AND TYPE = 2
            GROUP BY TRANS_DATE
            ORDER BY TRANS_DATE ASC
        ) AS A
        ;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        accum_consumption = pd.DataFrame(results, columns = ['date1', 'amounts'])

        query = """
        SELECT A.DATE, SUM(A.AMOUNTS_SUM) OVER(ORDER BY A.DATE) AS OVER_SUM 
        FROM (SELECT TO_CHAR(TRANS_DATE, 'YYYY-MM-DD') AS DATE, SUM(AMOUNTS) AS AMOUNTS_SUM
            FROM LEDGER.TRANSACTION
            WHERE TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE)
            AND TYPE = 2
            GROUP BY TRANS_DATE
            ORDER BY TRANS_DATE ASC
        ) AS A
        ;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        accum_consumption = pd.merge(accum_consumption, pd.DataFrame(results, columns = ['date2', 'amounts2']), left_index=True, right_index = True, how = 'left')

        fig = go.Figure()
        fig.add_trace(go.Scatter(y = accum_consumption['amounts'], mode = 'lines', name = 'previous'))
        fig.add_trace(go.Scatter(y = accum_consumption['amounts2'], mode = 'lines', name = 'current'))
        fig.update_layout(title = 'Compare Consumption b/w previous and current months')

        return fig

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
        query = f"""SELECT TYPE, SUM(AMOUNTS) AS AMOUNT_SUM FROM LEDGER.TRANSACTION WHERE TRANS_DATE > '{month_first}' AND TYPE = 2 GROUP BY TYPE;"""
        cursor.execute(query)
        test = cursor.fetchall()
        self.label2 = QLabel("소비 합계: ", self)
        self.payments_per_month = QLabel(str(test[0][1]) + "원")
        self.label3 = QLabel("소득 합계: ", self)
        self.income_per_month = QLabel("!!!!!원")
        self.label4 = QLabel("남은 금액: ", self)
        self.left = QLabel("!!!!!!!원", self)

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

        # Components2

        query = """
        SELECT A.DATE, SUM(A.AMOUNTS_SUM) OVER(ORDER BY A.DATE) AS OVER_SUM
        FROM (
            SELECT TO_CHAR(TRANS_DATE, 'YYYY-MM-DD') AS DATE, SUM(AMOUNTS) AS AMOUNTS_SUM 
            FROM LEDGER.TRANSACTION
            WHERE TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE - INTERVAL '1' MONTH)
            AND TRANS_DATE < DATE_TRUNC('MONTH', CURRENT_DATE)
            AND TYPE = 2
            GROUP BY TRANS_DATE
            ORDER BY TRANS_DATE ASC
        ) AS A
        ;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        accum_consumption = pd.DataFrame(results, columns = ['date1', 'amounts'])

        query = """
        SELECT A.DATE, SUM(A.AMOUNTS_SUM) OVER(ORDER BY A.DATE) AS OVER_SUM 
        FROM (SELECT TO_CHAR(TRANS_DATE, 'YYYY-MM-DD') AS DATE, SUM(AMOUNTS) AS AMOUNTS_SUM
            FROM LEDGER.TRANSACTION
            WHERE TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE)
            AND TYPE = 2
            GROUP BY TRANS_DATE
            ORDER BY TRANS_DATE ASC
        ) AS A
        ;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        accum_consumption = pd.merge(accum_consumption, pd.DataFrame(results, columns = ['date2', 'amounts2']), left_index=True, right_index = True, how = 'left')

        fig = go.Figure()
        fig.add_trace(go.Scatter(y = accum_consumption['amounts'], mode = 'markers+lines', marker = dict(size = 5, color = 'black'), name = 'previous'))
        fig.add_trace(go.Scatter(y = accum_consumption['amounts2'], mode = 'markers+lines', marker = dict(size = 5, color = 'red'), name = 'current'))
        fig.update_layout(
            go.Layout(
                title = {'text': 'Compare Consumption b/w previous and current months',
                         'font': {'color': 'black', 'size': 20}},
                plot_bgcolor= 'white'
            ))
        fig.update_xaxes(showgrid = True, gridwidth = 0.1, gridcolor = '#eee')
        fig.update_yaxes(showgrid = True, gridwidth = 0.1, gridcolor = '#eee')

        self.browser1 = QtWebEngineWidgets.QWebEngineView()
        self.browser1.setHtml(fig.to_html(include_plotlyjs = 'cdn'))
        # Y축 label 수정, text message 추가, dashboard 배경색과 어울리지 않음
        components2 = QVBoxLayout()
        components2.addWidget(self.browser1)

        vbox = QVBoxLayout()
        vbox.addLayout(components1)
        vbox.addLayout(components2)

        cursor.close()
        wid.setLayout(vbox)

app = QApplication(sys.argv)
window = Dashboard()
window.show()
app.exec()