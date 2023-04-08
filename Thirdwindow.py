from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import sys

from PyQt5.QtWidgets import *

class ThirdWindow(QDialog):
    def __init__(self):
        try:
            super().__init__()
            self.initUI()
            self.show()
        except Exception as e:
            print(e)
    def initUI(self):
        try:
            self.setWindowTitle('Third window')
            self.label = QLabel(self)
            self.setGeometry(300, 300, 640, 480)

            btn_back = QPushButton("back", self)
            btn_back.clicked.connect(self.btn_Back)

            hbox=QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(btn_back)

            vbox=QVBoxLayout()
            vbox.addStretch(1)
            vbox.addLayout(hbox)
            self.setLayout(vbox)

            btn_set_coordinate = QPushButton("분포도 보기", self)
            btn_set_coordinate.move(100, 10)
            btn_set_coordinate.clicked.connect(self.btn_fig_show)

            # btn_repaint = QPushButton("새로고침", self)
            # btn_repaint.move(180, 10)
            # btn_repaint.clicked.connect(self.btn_repaint)


        except Exception as e:
            print(e)

    # def btn_repaint(self):
    #     self.label.repaint()

    def btn_fig_show(self):
        try:
            print('분포도 보기.. : ')
            self.label.resize(640, 480)

            pixmap = QPixmap('savefig.png')
            self.label.setPixmap(pixmap)
            self.label.move(10, 50)

            self.resize(700, 550)

        except Exception as e:
            print(e)

    def btn_Back(self):
        self.close()