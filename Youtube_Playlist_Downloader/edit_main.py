import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import eyed3

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

        self.button1 = QPushButton('나가기', self)
        self.button1.setMaximumWidth(200)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.button1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        
        wid.setLayout(vbox)

class MainContent(MainWindow):
    def __init__(self):
        super().__init__()

        path = '/Users/mato/Desktop/Study/Python/Youtube_Playlists_Downloader/download'
        files = os.listdir(path)
        self.file_list.addItems(files)

        self.file_list.itemDoubleClicked.connect(self.double_clicked_event)

    def double_clicked_event(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

class EditDialog(QDialog):
    def __init__(self):

        dialogleft = 1200
        dialogTop = 120
        dialogWidth = 600
        dialogHeight = 450
        self.setGeometry(dialogleft, dialogTop, dialogWidth, dialogHeight)
        self.setWindowTitle('Edit Mp3 file Metadata')
        self.setModal(True)

        self.setupUI()

    def setupUI(self):
        self.label1 = QLabel('Title')
        

app = QApplication(sys.argv)
window = MainContent()
window.show()
app.exec()