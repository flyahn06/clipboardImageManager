from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QThread
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PIL import ImageGrab
import configparser
import win32clipboard
import sys
import re

blacklist = re.compile(r'.*[\/:*?"<>|].*', re.DOTALL)

class RemoveStatusBar(QThread):
    remove = pyqtSignal()
    time = 2000
    queue = []

    # 여러 작업이 동시에 시행되었을 때 마지막 이벤트를 기준으로 2 초를 기다리기 위함입니다.
    def run(self):
        print("run called, queue", self.queue)
        self.queue.append("task")
        self.msleep(self.time)
        self.queue.pop()
        print("run end, queue", self.queue)
        if len(self.queue) == 0:
            self.remove.emit()

class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked = pyqtSignal()  # 클릭이벤트 시그널

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        try:
            self.config.read("config.ini")
            print(self.config["DEFAULT"]["last_save_dir"])
            print(self.config["DEFAULT"]["last_load_file"])
            print(self.config["DEFAULT"]["last_filename"])
            print(self.config["DEFAULT"]["last_n"])
        except:
            self.initConfig()
            QMessageBox.information(self, '정보', "config.ini 를 찾을 수 없어 생성했습니다.\n프로그램을 다시 시작해 주세요",
                                 QMessageBox.Yes, QMessageBox.Yes)
            sys.exit(0)

        self.setupUi()

    def setupUi(self):
        self.resize(878, 254)
        self.setMinimumSize(QtCore.QSize(878, 254))
        self.setMaximumSize(QtCore.QSize(878, 254))

        self.setWindowIcon(QtGui.QIcon("clipboard.jpg"))

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.info_imgsave_lb = QtWidgets.QLabel(self.centralwidget)
        self.info_imgsave_lb.setObjectName("info_imgsave_lb")
        self.horizontalLayout_3.addWidget(self.info_imgsave_lb)

        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.info_save_imagepath_lb = QtWidgets.QLabel(self.centralwidget)
        self.info_save_imagepath_lb.setObjectName("info_save_imagepath_lb")
        self.gridLayout.addWidget(self.info_save_imagepath_lb, 0, 0, 1, 1)

        self.save_imagepath_input = ClickableLineEdit(self.centralwidget)
        self.save_imagepath_input.setObjectName("save_imagepath_input")
        self.save_imagepath_input.clicked.connect(self.saveImagePath)
        self.save_imagepath_input.setText(self.config['DEFAULT']['last_save_dir'])
        self.save_imagepath_input.setStatusTip("클릭하여 이미지의 저장 경로를 선택합니다.")
        self.gridLayout.addWidget(self.save_imagepath_input, 0, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_9.addLayout(self.verticalLayout)

        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.save_n_input = QtWidgets.QLineEdit(self.centralwidget)
        self.save_n_input.setMaximumSize(QtCore.QSize(50, 100))
        self.save_n_input.setObjectName("save_n_input")
        self.save_n_input.setStatusTip("정수인 파일의 번호를 입력하세요. 파일 이름의 {n}이 이것으로 대체됩니다.")
        self.save_n_input.setText(self.config['DEFAULT']["last_n"])

        self.gridLayout_2.addWidget(self.save_n_input, 0, 1, 1, 1)
        self.info_save_filename_lb = QtWidgets.QLabel(self.centralwidget)
        self.info_save_filename_lb.setObjectName("info_save_filename_lb")

        self.gridLayout_2.addWidget(self.info_save_filename_lb, 0, 2, 1, 1)
        self.info_save_n_lb = QtWidgets.QLabel(self.centralwidget)
        self.info_save_n_lb.setObjectName("info_save_n_lb")
        self.gridLayout_2.addWidget(self.info_save_n_lb, 0, 0, 1, 1)

        self.save_filename_input = QtWidgets.QLineEdit(self.centralwidget)
        self.save_filename_input.setObjectName("save_filename_input")
        self.save_filename_input.setStatusTip("파일의 이름을 입력하세요. {n} 은 n 에 입력한 값으로 대체됩니다. 형식은 항상 .png 형식입니다.")
        self.save_filename_input.setText(self.config['DEFAULT']['last_filename'])

        self.gridLayout_2.addWidget(self.save_filename_input, 0, 3, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_2)
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setObjectName("save_btn")
        self.save_btn.setStatusTip("이미지 저장을 수행합니다.")
        self.save_btn.clicked.connect(self.saveImage)

        self.verticalLayout_9.addWidget(self.save_btn)
        self.horizontalLayout_3.addLayout(self.verticalLayout_9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.info_imageload_lb = QtWidgets.QLabel(self.centralwidget)
        self.info_imageload_lb.setObjectName("info_imageload_lb")

        self.horizontalLayout_4.addWidget(self.info_imageload_lb)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.info_load_imagepath_lb = QtWidgets.QLabel(self.centralwidget)
        self.info_load_imagepath_lb.setObjectName("info_load_imagepath_lb")

        self.gridLayout_3.addWidget(self.info_load_imagepath_lb, 0, 0, 1, 1)
        self.load_imagepath_input = ClickableLineEdit(self.centralwidget)
        self.load_imagepath_input.setObjectName("load_imagepath_input")
        self.load_imagepath_input.setText(self.config['DEFAULT']['last_load_file'])
        self.load_imagepath_input.setStatusTip("클릭하여 클립보드로 복사할 이미지의 위치를 선택합니다.")
        self.load_imagepath_input.clicked.connect(self.loadImagePath)

        self.gridLayout_3.addWidget(self.load_imagepath_input, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_3)

        self.load_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_btn.setObjectName("load_btn")
        self.load_btn.setStatusTip("이미지 불러오기를 수행합니다.")
        self.load_btn.clicked.connect(self.loadImage)

        self.verticalLayout_5.addWidget(self.load_btn)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("config.ini 로딩에 성공했습니다!", 5000)

        self.succeed = QtWidgets.QLabel(self)
        self.statusbar.addPermanentWidget(self.succeed)

        self.retranslateUi()
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "클립보드 이미지 메니저"))
        self.info_imgsave_lb.setText(_translate("MainWindow", "    이미지 저장   "))
        self.info_save_imagepath_lb.setText(_translate("MainWindow", "파일 경로"))
        self.info_save_filename_lb.setText(_translate("MainWindow", "파일 이름"))
        self.info_save_n_lb.setText(_translate("MainWindow", "n"))
        self.save_btn.setText(_translate("MainWindow", "저장"))
        self.info_imageload_lb.setText(_translate("MainWindow", " 이미지 불러오기"))
        self.info_load_imagepath_lb.setText(_translate("MainWindow", "이미지 경로"))
        self.load_btn.setText(_translate("MainWindow", "불러오기"))

    def initConfig(self):
        with open("config.ini", 'w') as f:
            w = """[DEFAULT]
last_save_dir = C:\\ 
last_load_file = C:\\
last_filename = 
last_n = 1"""
            f.write(w)

    def clearStatusLabel(self):
        self.succeed.setText("")

    def saveImagePath(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "저장할 경로를 선택하세요", self.save_imagepath_input.text())

        if not filepath:
            return

        self.save_imagepath_input.setText(filepath)

    def loadImagePath(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, '파일 열기', self.load_imagepath_input.text(), "모든 이미지 파일 (*.jpg *.png *.jpeg *.gif)")
        filepath = fname[0]
        if not filepath:
            return
        self.load_imagepath_input.setText(filepath)

    def saveImage(self):
        img = ImageGrab.grabclipboard()

        if not img:
            QMessageBox.critical(self, '오류', "클립보드의 내용물이 이미지가 아닙니다.\n이미지 복사 후 다시 시도해 주세요",
                                 QMessageBox.Yes, QMessageBox.Yes)
            return

        if not self.save_n_input.text().isdigit():
            QMessageBox.critical(self, '오류', "n의 값이 정수가 아닙니다." + "\n" + "n의 값을 다시 입력해 주세요",
                                 QMessageBox.Yes, QMessageBox.Yes)
            return

        imgname = self.save_filename_input.text() if self.save_filename_input.text().endswith(".png") else self.save_filename_input.text() + ".png"
        imgname = imgname.replace("{n}", self.save_n_input.text())

        if blacklist.match(imgname):
            QMessageBox.critical(self, '오류', "파일 이름에는 다음의 문자를 사용할 수 없습니다." + "\n" + "\\ / : * ? \" < > |",
                                 QMessageBox.Yes, QMessageBox.Yes)
            return

        filepath = self.save_imagepath_input.text() + "/" + imgname
        img.save(filepath, 'PNG')

        self.save_n_input.setText(str(int(self.save_n_input.text()) + 1))
        self.succeed.setText(imgname + "  저장 성공")
        self.removeRegister = RemoveStatusBar()
        self.removeRegister.remove.connect(self.clearStatusLabel)
        self.removeRegister.start()

    def loadImage(self):
        pass

    def closeEvent(self, QCloseEvent):
        last_save_dir = self.save_imagepath_input.text()
        last_load_file = self.load_imagepath_input.text()
        last_filename = self.save_filename_input.text()
        last_n = self.save_n_input.text()

        self.config["DEFAULT"] = {
            'last_save_dir': last_save_dir,
            'last_load_file': last_load_file,
            'last_filename': last_filename,
            'last_n': last_n
        }

        with open("config.ini", 'w') as f:
            self.config.write(f)


app = QApplication(sys.argv)
w = Mainwindow()
sys.exit(app.exec_())
