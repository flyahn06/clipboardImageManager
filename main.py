from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import configparser
import sys
import PIL


class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked = pyqtSignal()  # signal when the text entry is left clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        try:
            print(self.config["DEFAULT"]["last_save_dir"])
            print(self.config["DEFAULT"]["last_load_file"])
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

        self.centralwidget = QtWidgets.QWidget()
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

        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.info_save_imagepath_lb = QtWidgets.QLabel(self.centralwidget)
        self.info_save_imagepath_lb.setObjectName("info_save_imagepath_lb")

        self.gridLayout_2.addWidget(self.info_save_imagepath_lb, 0, 0, 1, 1)
        self.info_save_n_lb = QtWidgets.QLabel(self.centralwidget)
        self.info_save_n_lb.setObjectName("info_save_n_lb")

        self.gridLayout_2.addWidget(self.info_save_n_lb, 1, 0, 1, 1)
        self.save_imagepath_input = ClickableLineEdit(self.centralwidget)
        self.save_imagepath_input.setObjectName("save_imagepath_input")
        self.save_imagepath_input.clicked.connect(self.saveImage)

        self.gridLayout_2.addWidget(self.save_imagepath_input, 0, 1, 1, 1)
        self.save_n_input = QtWidgets.QLineEdit(self.centralwidget)
        self.save_n_input.setObjectName("save_n_input")
        self.save_n_input.setText("1")

        self.gridLayout_2.addWidget(self.save_n_input, 1, 1, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_2)
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setObjectName("save_btn")

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
        self.load_imagepath_input.clicked.connect(self.loadImage)

        self.gridLayout_3.addWidget(self.load_imagepath_input, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_3)
        self.load_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_btn.setObjectName("load_btn")

        self.verticalLayout_5.addWidget(self.load_btn)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "클립보드 이미지 메니저"))
        self.info_imgsave_lb.setText(_translate("MainWindow", "    이미지 저장   "))
        self.info_save_imagepath_lb.setText(_translate("MainWindow", "이미지 경로"))
        self.info_save_n_lb.setText(_translate("MainWindow", "n(숫자값)"))
        self.save_btn.setText(_translate("MainWindow", "저장"))
        self.info_imageload_lb.setText(_translate("MainWindow", " 이미지 불러오기"))
        self.info_load_imagepath_lb.setText(_translate("MainWindow", "이미지 경로"))
        self.load_btn.setText(_translate("MainWindow", "불러오기"))

    def initConfig(self):
        with open("config.ini", 'w') as f:
            w = """[DEFAULT]
last_save_dir = 
last_load_file = """
            f.write(w)

    def saveImage(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "저장할 경로를 선택하세요")
        print(filepath)
        self.save_imagepath_input.setText(filepath)



    def loadImage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, '파일 열기', 'c:\\', "모든 이미지 파일 (*.jpg *.png *.jpeg *.gif)")
        filepath = fname[0]
        print(filepath)

app = QApplication(sys.argv)
w = Mainwindow()
sys.exit(app.exec_())