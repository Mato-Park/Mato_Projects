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
import plotly.colors as clrs

class bulletChart:
    def __init__(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()

        query = """
                SELECT
                    SUM(AMOUNTS)    AS AMOUNTS
                FROM
                    LEDGER.TRANSACTION
                WHERE
                    TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE) AND
                    TYPE = 2
                ;
                """
        cursor.execute(query)
        results = cursor.fetchall()
        amounts = results[0][0] / 10000

        fig = go.Figure()
        fig['layout'].update(
            dict(shapes = []),
            barmode = 'stack',
            height = 400,
            width = 300,
            showlegend = False,
            annotations = []
        )

        width_axis = 'xaxis'
        length_axis = 'yaxis'

        for key in fig['layout']:
            if 'xaxis' in key or 'yaxis' in key:
                fig['layout'][key]['showgrid'] = False
                fig['layout'][key]['zeroline'] = False
            if length_axis in key:
                fig['layout'][key]['tickwidth'] = 1
            if width_axis in key:
                fig['layout'][key]['showticklabels'] = False
                fig['layout'][key]['range'] = [-0.5, 0.5]
        
        range_colors = ["rgb(76, 175, 80)", "rgb(255, 152, 0)", "rgb(244, 67, 54)"]
        measure_colors = ["rgb(31, 119, 180)", "rgb(176, 196, 221)"]

        range_n = [100, 150, 200]

        for idx in range(len(range_n)):
            # range bars: 배경이되는 range bars
            inter_colors = clrs.n_colors(
                range_colors[0], range_colors[1], len(range_n), 'rgb'
            )

            x = [0]
            y = [sorted(range_n)[-1 -idx]]
            bar = go.Bar(
                x = x,
                y = y,
                # marker = dict(color = inter_colors[-1 - idx]),
                marker = dict(color = range_colors[-1 - idx]),
                orientation = 'v',
                hoverinfo = 'y',
                base = 0,
                width = 1
            )
            fig.add_trace(bar)

        # measure bar: current value
        bar = go.Bar(
            x = x,
            y = [amounts],
            marker = dict(color = "rgb(33, 150, 243)"),
            hoverinfo = 'y',
            width = 0.4,
            base = 0
        )
        fig.add_trace(bar)

        self.html = pio.to_html(fig, full_html = False, include_plotlyjs = 'cdn')

# class bulletChart:
#     def __init__(self):
#         db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
#         cursor = db.cursor()

#         query = """SELECT
#                     SUM(AMOUNTS)      AS  AMOUNTS
#                 FROM
#                     LEDGER.TRANSACTION
#                 WHERE
#                     TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE) AND
#                     TYPE = 2
#                 ;
#                 """
#         cursor.execute(query)
#         results = cursor.fetchall()
#         amounts = results[0][0] / 10000

#         fig = go.Figure(go.Indicator(
#             mode = "number+gauge+delta",
#             gauge = {
#                 'shape': "bullet",
#                 'axis' : {'range': [0, 200]},
#                 'threshold' : {
#                     'line': {'color': "red", 'width': 5},
#                     'thickness': 0.75,
#                     'value': 150
#                 },
#                 'steps': [
#                     {'range': [0, 75], 'color': "lightgray"},
#                     {'range': [75, 150], 'color': "gray"}
#                 ],
#                 'bar': {'color': 'green'}
#                 },
#             value = amounts,
#             delta = {'reference': 200, 'position': "left"},
#             domain = {'x': [0.1, 1], 'y': [0, 1]},
#             title = {'text': "<b>Consume</b><br><span style='color':gray; font-size:0.5em'>Kor. ₩</span>", 'font': {"size": 14}}
#         ))
#         fig.update_layout(height = 250)
#         self.html = pio.to_html(fig, full_html = False, include_plotlyjs = 'cdn')

class donutChart:
    def __init__(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()
        # fig = go.Figure(data = [go.Bar(x=['A', 'B', 'C'], y = [1, 3, 2])])
        # self.html = pio.to_html(fig, full_html = False)
        query = """SELECT
                    B.CATEGORY_NAME,
                    SUM(A.AMOUNTS)      AS  AMOUNTS
                FROM
                    LEDGER.TRANSACTION AS A
                    JOIN
                        LEDGER.CATEGORY AS B
                        ON A.CATEGORY = B.CATEGORY_ID
                WHERE 
                    A.TRANS_DATE >= DATE_TRUNC('MONTH', CURRENT_DATE)
                GROUP BY B.CATEGORY_NAME
                ORDER BY AMOUNTS DESC;
                """
        cursor.execute(query)
        results = cursor.fetchall()
        results_df = pd.DataFrame(results, columns = ['category', 'value'])

        label = list(results_df['category'])
        values = list(results_df['value'])

        fig = go.Figure(data = go.Pie(labels = label, values = values, hole = .3, pull = [0.1]))
        fig.update_traces(hoverinfo = 'label+percent', textinfo = 'label+value', textfont_size = 10, marker= dict(line = dict(color = '#eeeeee', width = 2)))
        fig.update_layout(
            go.Layout(
                title = {'text': 'Expenditure per Categories',
                         'font': {'color': 'black', 'size': 20}},
                plot_bgcolor= 'white'
            ))
        self.html = pio.to_html(fig, full_html = False, include_plotlyjs = 'cdn')

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
    
class compareChart:
    def __init__(self):
        db = psycopg2.connect(host = 'localhost', dbname = 'ledger', user = 'mato', port = 5432)
        cursor = db.cursor()
        
        query1 = """
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
        cursor.execute(query1)
        results = cursor.fetchall()

        accum_consumption = pd.DataFrame(results, columns = ['date1', 'amounts'])

        query2 = """
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
        cursor.execute(query2)
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

        self.html = pio.to_html(fig, full_html = False, include_plotlyjs = 'cdn')
        # Y축 label 수정, text message 추가, dashboard 배경색과 어울리지 않음