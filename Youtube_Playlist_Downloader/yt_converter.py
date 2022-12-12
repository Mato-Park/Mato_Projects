import os
import sys
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import yt_dlp
import json
import urllib
from io import BytesIO
from PIL import Image
from urllib import request

target_url = ''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ag = QGuiApplication.primaryScreen().availableGeometry()
        mainWindowWidth = 1000
        mainWindowHeight = 700
        mainWindowLeft = (ag.width() - mainWindowWidth) / 2
        mainWindowTop = (ag.height() - mainWindowHeight) / 2
        self.setGeometry(mainWindowLeft, mainWindowTop, mainWindowWidth, mainWindowHeight)

        self.setWindowTitle('yt_converter_v1.0')

        self.setupUI()

    def setupUI(self):

        wid = QWidget(self)
        self.setCentralWidget(wid)

        self.label = QLabel('플레이리스트 url 입력: ')
        self.label.setFont(QFont('굴림체', 20))
        self.search_url = QLineEdit(self)
        self.search_button = QPushButton("검색", self)
        self.search_button.setMinimumWidth(100)
        # self.status_label = QLabel("", self)
        # self.download_button = QPushButton('다운로드')

        hbox = QHBoxLayout()
        # # hbox.addStretch(0)
        hbox.addWidget(self.label)
        hbox.addWidget(self.search_url)
        hbox.addWidget(self.search_button)
        # # hbox.addStretch(0)

        hbox2 = QHBoxLayout()
        self.label2 = QLabel('Youtube 리스트')
        self.label2.setFont(QFont('굴림체', 30))
        self.label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        hbox2.addWidget(self.label2)

        self.video_list = QListWidget(self)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.video_list)

        self.download_button = QPushButton('다운로드', self)
        self.download_button.setMaximumWidth(200)
        
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.download_button)

        vbox = QVBoxLayout()
        # vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        wid.setLayout(vbox)

        self.show()

        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
