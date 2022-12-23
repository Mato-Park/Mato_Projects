import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import eyed3
from eyed3 import id3
from eyed3 import load
import urllib
from urllib import request

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ag = QGuiApplication.primaryScreen().availableGeometry()
        mainWindowWidth = 1000
        mainWindowHeight = 700
        mainWindowLeft = (ag.width() - mainWindowWidth) / 2
        mainWindowTop = (ag.height() - mainWindowHeight) / 2
        self.setGeometry(mainWindowLeft, mainWindowTop, mainWindowWidth, mainWindowHeight)

        self.setWindowTitle('edit_mp3_metadata_v1.0')

        self.setupUI()
    
    def setupUI(self):

        wid = QWidget(self)
        self.setCentralWidget(wid)

        self.label1 = QLabel('Mp3 File List')
        self.label1.setFont(QFont('굴림체', 20))

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label1)

        self.file_list = QListWidget(self)
        # self.file_list.addItems(['a', 'b'])
        # self.file_list.addItems
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.file_list)

        self.edit_button = QPushButton('편집하기', self)
        self.edit_button.setMaximumWidth(200)
        self.button1 = QPushButton('나가기', self)
        self.button1.setMaximumWidth(200)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.edit_button)
        hbox3.addWidget(self.button1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        
        wid.setLayout(vbox)

class MainContent(MainWindow):
    def __init__(self):
        super().__init__()

        global path
        path = '/Users/mato/Desktop/Study/Python/Youtube_Playlists_Downloader/download'
        files = os.listdir(path)
        self.file_list.addItems(files)

        self.file_list.itemDoubleClicked.connect(self.double_clicked_event)
        self.file_list.itemClicked.connect(self.clicked_event)

        self.edit_button.clicked.connect(self.pushbuttonClicked)

    def double_clicked_event(self):
        # edit_file = self.file_list.currentItem().text()
        edit_dialog = EditDialog()
        edit_dialog.exec()

    def clicked_event(self):
        global edit_file
        edit_file = self.file_list.currentItem().text() # list widget에서 현재 선택한 아이템 텍스트 가져오기
    
    def pushbuttonClicked(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        dialogleft = 700
        dialogTop = 200
        dialogWidth = 600
        dialogHeight = 450
        self.setGeometry(dialogleft, dialogTop, dialogWidth, dialogHeight)
        self.setWindowTitle('Edit Mp3 file Metadata')
        self.setModal(True)

        self.setupUI()

    def setupUI(self):
        wid = QWidget(self)

        ### ---------------------------------
        self.label1 = QLabel('File Name: ')
        # self.file_name = QLineEdit(self)
        self.file_name = QLabel(edit_file)
        self.button1 = QPushButton('Edit', self)

        self.button1.clicked.connect(self.editbuttonClicked)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.file_name)
        hbox1.addWidget(self.button1)

        ### ------------------
        self.label2 = QLabel('음원 속성 편집하기')
        self.label2.setFont(QFont('굴림체', 20))

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.label2)

        file = path + '/' + edit_file
        tag = id3.Tag()
        tag.parse(file)

        ### Artist
        self.artist_label = QLabel('Artist: ')
        self.artist_edit = QLineEdit(tag.artist)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.artist_label)
        hbox3.addWidget(self.artist_edit)

        ### Title
        self.title_label = QLabel('Title: ')
        self.title_edit = QLineEdit(tag.title)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.title_label)
        hbox4.addWidget(self.title_edit)

        ### Album
        self.album_label = QLabel('Album: ')
        self.album_edit = QLineEdit(tag.album)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.album_label)
        hbox5.addWidget(self.album_edit)

        ### Genre
        self.genre_label = QLabel('Genre: ')
        # self.genre_edit = QLineEdit(tag.genre.name)

        if tag.genre == None:
            self.genre_edit = QLineEdit()
        else:
            self.genre_edit = QLineEdit(tag.genre.name)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.genre_label)
        hbox6.addWidget(self.genre_edit)

        ### Album jacket 가져오기 ===============================
        self.label3 = QLabel('Album Jacket 편집하기')
        self.label3.setFont(QFont('굴림체', 20))
        hbox7 = QHBoxLayout()
        hbox7.addWidget(self.label3)

        self.image_url = QLabel('Image URL: ')
        self.image_edit = QLineEdit()
        self.image_button = QPushButton('가져오기', self)
        self.image_save_button = QPushButton('저장하기', self)

        self.image_button.clicked.connect(self.image_get_button)
        self.image_save_button.clicked.connect(self.image_save_clicked)

        self.image = QLabel( self)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(self.image_url)
        hbox8.addWidget(self.image_edit)
        hbox8.addWidget(self.image_button)
        hbox8.addWidget(self.image_save_button)
        hbox8_2 = QHBoxLayout()
        hbox8_2.addWidget(self.image)
        # hbox8_v1 = QVBoxLayout()
        # hbox8_v1_h1 = QHBoxLayout()
        # hbox8_v1_h2 = QHBoxLayout()
        # hbox8_v2 = QVBoxLayout()
        # hbox8_v1_h1.addWidget(self.image_url)
        # hbox8_v1_h1.addWidget(self.image_edit)
        # hbox8_v1_h2.addWidget(self.image_button)
        # hbox8_v1_h2.addWidget(self.image_save_button)
        # hbox8_v1.addLayout(hbox8_v1_h1)
        # hbox8_v1.addLayout(hbox8_v1_h2)
        # hbox8_v2.addWidget(self.image)
        # hbox8.addLayout(hbox8_v1)
        # hbox8.addLayout(hbox8_v2)

        ### 저장 & 나가기 버튼 생성
        self.save_button = QPushButton('Save', self)
        self.exit_button = QPushButton('Exit', self)

        self.save_button.clicked.connect(self.save_button_clicked)
        self.exit_button.clicked.connect(self.exit_button_clicked)

        hbox9 = QHBoxLayout()
        hbox9.addWidget(self.save_button)
        hbox9.addWidget(self.exit_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)
        vbox.addLayout(hbox8_2)
        vbox.addLayout(hbox9)

        wid.setLayout(vbox)

    def save_button_clicked(self):
        tag = eyed3.load(path + '/' + edit_file)
        tag.tag.artist = self.artist_edit.text()
        tag.tag.title = self.title_edit.text()
        tag.tag.album = self.album_edit.text()
        tag.tag.genre = self.genre_edit.text()
        tag.tag.images.set(3, image_web, "image/jpeg", u"None")

        tag.tag.save()

    def image_get_button(self):
        image_path = self.image_edit.text()
        global image_web
        image_web = urllib.request.urlopen(image_path).read()

        self.qpixel = QPixmap()
        self.qpixel.loadFromData(image_web)
        self.image.setPixmap(self.qpixel)
        self.image.resize(self.qpixel.width(), self.qpixel.height())
        self.image.repaint()
        self.image.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.update()

    def image_save_clicked(self):
        image_path = self.image_edit.text()
        save_path = '/Users/mato/Desktop/Study/Python/Youtube_Playlists_Downloader/image/' + self.artist_edit.text() + '_' + self.album_edit.text()
        urllib.request.urlretrieve(image_path, save_path + '.jpg')

    def exit_button_clicked(self):
        self.close()

    def editbuttonClicked(self):
        name_edit = Name_edit()
        name_edit.exec()

class Name_edit(QDialog):
    def __init__(self):
        super().__init__()

        dialogleft = 800
        dialogTop = 500
        dialogWidth = 600
        dialogHeight = 80
        self.setGeometry(dialogleft, dialogTop, dialogWidth, dialogHeight)
        self.setWindowTitle('Change File Name')
        self.setModal(True)

        self.setupUI()
    
    def setupUI(self):
        wid = QWidget(self)

        self.label1 = QLabel('파일명 :')
        self.name_edit = QLineEdit(edit_file)
        self.name_edit.setMinimumWidth(500)

        self.change_button = QPushButton('Change!')
        self.change_button.clicked.connect(self.name_change_clicked)

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.name_edit)
        hbox2.addWidget(self.change_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        wid.setLayout(vbox)
    
    def name_change_clicked(self):
        path = '/Users/mato/Desktop/Study/Python/Youtube_Playlists_Downloader/download/'
        new_name = self.name_edit.text()
        print(new_name)
        os.rename(path + edit_file, path + new_name)
        self.close()



app = QApplication(sys.argv)
window = MainContent()
window.show()
app.exec()