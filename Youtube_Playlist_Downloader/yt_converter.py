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

"""
    MainWindow 클래스에 화면 구성을 설정하고
    MainContent 클래스에 안에 내용을 채우는 식으로 구조를 변경함
"""

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


class MainContent(MainWindow):
    add_sec_signal = pyqtSignal()
    send_instance_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super().__init__()

        self.search_button.clicked.connect(self.search)

        self.th_search = searcher(parent = self)
        self.th_search.updated_list.connect(self.list_update)
        self.th_search.updated_label.connect(self.status_update)

        self.show()

    @pyqtSignal()
    def search(self):
        # self.video_list.insertItem(0, 'test')
        self.video_list.clear()
        self.th_search.start

    @pyqtSignal(str)
    def list_update(self, msg):
        self.video_list.addItem(msg)
        self.video_list.selectAll()

    @pyqtSignal(str)
    def status_update(self, msg):
        self.status_label.setText(msg)

class searcher(QThread):
    updated_list = pyqtSignal(str)
    updated_label = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__()
        self.main = parent

    def __del__(self): # 소멸자 생성
        self.wait()

    def run(self):

        global target_url
        global down_url_list
        global down_title_list

        down_url_list = []
        down_title_list = []

        if target_url != "":
            self.updated_label.emit("Reading Playlist lists...")

            ydl_opts = {'format': 'bestaudio/best'}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(target_url, download = False)

                if 'entries' in info_dict:
                    video = info_dict['entries']

                    for i, _ in enumerate(video):
                        video = info_dict['entries'][i]
                        self.updated_list.emit(info_dict['entries'][i]['title'])

                        down_url_list.append(info_dict['entries'][i]['webpage_url'])
                        down_title_list.append(info_dict['entries'][i]['title'])
                else:
                    video_title = info_dict.get('title', None)
                    self.updated_list.emit(video_title)

                    down_url_list.append(target_url)
                    down_title_list.append(video_title)
            
            self.updated_label.emit('Load Complete!')
        
        else:
            self.updated_label.emit('Please Insert Playlist url')



app = QApplication(sys.argv)
window = MainContent()
window.show()
app.exec()
