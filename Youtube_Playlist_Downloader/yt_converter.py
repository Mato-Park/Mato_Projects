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
import time
import shutil
import glob

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

        self.status_label = QLabel("", self)

        vbox = QVBoxLayout()
        # vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addWidget(self.status_label)
        wid.setLayout(vbox)


# class test(QThread):
#     proc = pyqtSignal(str)

#     def __init__(self):
#         super().__init__()
    
#     def run(self):
#         count = 0
#         for i in range(0, 10):
#             count += 1
#             self.proc.emit('count')
#             time.sleep(1)

class MainContent(MainWindow):
    # add_sec_signal = pyqtSignal()
    # send_instance_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super().__init__()

        self.search_button.clicked.connect(self.search) # 검색 버튼 불르면 search 매소드를 호출하고 searcher 클래스 실행!
        self.download_button.clicked.connect(self.download)

        self.search_url.textChanged[str].connect(self.title_update) # 플레이리스트 url입력하면 그것을 가져오는 매소드 호출

        self.th_search = searcher(parent = self) # searcher 클래스 호출하기
        self.th_search.updated_list.connect(self.list_update) # 시그널 보내기!
        self.th_search.updated_label.connect(self.status_update)

        self.th_download = downloader(parent = self)
        self.th_download.updated_label.connect(self.status_update)

        self.show()

    def title_update(self, input):
        global target_url
        target_url = input
        print(target_url)

    # @pyqtSlot()
    def search(self):
        # self.video_list.insertItem(0, 'test')
        self.video_list.clear()
        self.th_search.start()

    def download(self):
        self.th_download.start()

    @pyqtSlot(str)
    def list_update(self, msg):
        self.video_list.addItem(msg)
        # self.video_list.insertItem(0, msg)
        self.video_list.selectAll()

    @pyqtSlot(str)
    def status_update(self, msg):
        self.status_label.setText(msg)

"""
썸네일 다운받는 것도 추가함
"""

class searcher(QThread):
    updated_list = pyqtSignal(str)
    updated_label = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__()
        self.main = parent

    def __del__(self): # 소멸자 생성
        self.wait()

    def run(self):
        print("Success!!!!!!")
        global target_url
        global down_url_list
        global down_title_list
        global down_image_list
        
        down_url_list = []
        down_title_list = []
        down_image_list = []
        
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
                        down_image_list.append(info_dict['entries'][i]['thumbnail'])
                        
                else:
                    video_title = info_dict.get('title', None)
                    self.updated_list.emit(video_title)

                    down_url_list.append(target_url)
                    down_title_list.append(video_title)
            
            self.updated_label.emit('Load Complete!')
        
        else:
            self.updated_label.emit('Please Insert Playlist url')

class downloader(QThread):
    updated_label = pyqtSignal(str)

    def __init__(self, parent = None):
        super().__init__()
        self.main = parent
    
    def __del__(self):
        self.wait()
    
    """
    원작자는 플레이리스트의 비디오들의 타이틀을 가져온 다음 선택한 것만 다운로드 하는 것으로 기능을 구현했지만,
    난 다운받고 싶은 것만 저장시킨 것이므로 타이틀을 확인후 바로 다운로드 하는 것으로 기능을 구현함
    그리고 난 영상을 다운받을 필요 없으므로 음원만 다운받는 것만 구현하고 끝!
    썸네일은 다운받을 순 있지만 쓸만한 게 있을까? 굳이 없어도 될듯 한데 일단 기능을 살려놓자
    """

    def run(self):
        global down_url_list
        global down_title_list
        global down_image_list
        # global selected_title

        # titles = []

        cnt = 0

        for i, url in enumerate(down_url_list):
            self.updated_label.emit("{}/{} Downloading video files...".format(i, len(down_title_list)))

            video_output_dir = os.path.join('./download/', '%(title)s.%(ext)s')
            # image_output_dir = os.path.join('./image/', '%(title)s.%(ext)s')

            ydl_opt_audio = {
                'outtmpl': video_output_dir,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opt_audio) as ydl:
                ydl.download([url])

            image_url = down_image_list[i]
            urllib.request.urlretrieve(image_url, '/image/{}_picture.jpg'.format(i))

        
        self.updated_label.emit("Download Complete")


app = QApplication(sys.argv)
window = MainContent()
window.show()
app.exec()
