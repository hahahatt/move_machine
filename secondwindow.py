import time

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

f1 = open('speed.txt', "a", encoding="UTF-8")
f2 = open('movement.txt', "a", encoding="UTF-8")
f3 = open('time.txt', "a", encoding="UTF-8")
f4 = open('default_movement.txt',"a",encoding="UTF-8")


class SecondWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.Speed_Select_Button()
        self.Move_Select_Button()
        self.Select_Video_time()
        self.select_default_time()
        self.set_check()
        self.show()

    def initUI(self):
        #self.resize(640,480)

        self.setWindowTitle('Second window')
        btn_back=QPushButton("back",self)
        btn_back.move(100,440)
        btn_back.clicked.connect(self.btn_Back)

        self.setGeometry(300, 300, 640, 480)

        btn_save=QPushButton("save",self)
        btn_save.move(400,440)
        btn_save.clicked.connect(self.btn_save)
        self.save_msg=0


    def btn_save(self):
        try:

            self.save_msg = 1
            print("save")
            if self.radio1.isChecked() | self.radio1.isChecked() | self.radio2.isChecked() | self.radio3.isChecked() | self.radio4.isChecked() and \
                    self.time1.isChecked() | self.time2.isChecked() | self.time3.isChecked() | self.time4.isChecked() and \
                    self.radio5.isChecked() | self.radio6.isChecked() | self.radio7.isChecked() and \
                    self.default_time_1.isChecked() | self.default_time_2.isChecked() | self.default_time_3.isChecked() | self.default_time_4.isChecked():
                QtWidgets.QMessageBox.about(self, "Good", "saved")



                #time.sleep(3)
                self.close()
            else:
                QtWidgets.QMessageBox.about(self, "Error", "세 값을 선택하세여")
        except Exception as e:
            print(e)



    def Speed_Select_Button(self):
        groupbox=QGroupBox('Speed',self)
        groupbox.resize(200, 150)

        self.radio1=QRadioButton('lv 1',self)
        self.radio1.move(10,10)
        #self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.Speed_Button_select)
        #self.radio1.clicked.connect(self.btn_save)

        self.radio2=QRadioButton('lv 2',self)
        self.radio2.move(10, 40)
        #self.radio2.setChecked(True)
        self.radio2.clicked.connect(self.Speed_Button_select)
        #self.radio2.clicked.connect(self.btn_save)

        self.radio3=QRadioButton('lv 3',self)
        self.radio3.move(10, 70)
        #self.radio3.setChecked(True)
        self.radio3.clicked.connect(self.Speed_Button_select)
        #self.radio3.clicked.connect(self.btn_save)

        self.radio4 = QRadioButton('lv 4', self)
        self.radio4.move(10, 100)
        # self.radio3.setChecked(True)
        self.radio4.clicked.connect(self.Speed_Button_select)
        #self.radio4.clicked.connect(self.btn_save)

        vbox=QVBoxLayout()
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        vbox.addWidget(self.radio3)
        vbox.addWidget(self.radio4)
        groupbox.setLayout(vbox)



    def Move_Select_Button(self):
        groupbox = QGroupBox('샘플 수/움직이는 시간', self)
        groupbox.move(0, 170)
        groupbox.resize(290, 150)

        self.radio5 = QRadioButton('10개 [시간 3초: 30초/ 5: 50/ 10: 100]', self)
        self.radio5.move(10, 200)
        #self.radio4.setChecked(True)
        self.radio5.clicked.connect(self.Move_Button_select)
        #self.radio5.clicked.connect(self.btn_save)

        self.radio6 = QRadioButton('30개 [시간 3초: 90초/ 5: 150/ 10: 300]', self)
        self.radio6.move(10, 230)
        #self.radio5.setChecked(True)
        self.radio6.clicked.connect(self.Move_Button_select)
        #self.radio6.clicked.connect(self.btn_save)

        self.radio7 = QRadioButton('50개 [시간 3초: 150초/ 5: 250/ 10: 500]', self)
        self.radio7.move(10, 260)
        #self.radio6.setChecked(True)
        self.radio7.clicked.connect(self.Move_Button_select)
        #self.radio7.clicked.connect(self.btn_save)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio5)
        vbox.addWidget(self.radio6)
        vbox.addWidget(self.radio7)
        groupbox.setLayout(vbox)


    def Select_Video_time(self):
        groupbox = QGroupBox('Taking picture time', self)
        groupbox.move(220, 0)
        groupbox.resize(200, 150)

        self.time1=QRadioButton('3초',self)
        self.time1.move(230,30)
        self.time1.clicked.connect(self.Video_time_select)
        #self.time1.clicked.connect(self.btn_save)

        self.time2=QRadioButton('5초',self)
        self.time2.move(230,60)
        self.time2.clicked.connect(self.Video_time_select)
        #self.time2.clicked.connect(self.btn_save)

        self.time3=QRadioButton('10초',self)
        self.time3.move(230, 90)
        self.time3.clicked.connect(self.Video_time_select)
        #self.time3.clicked.connect(self.btn_save)

        self.time4=QRadioButton('15초',self)
        self.time4.move(230, 120)
        self.time4.clicked.connect(self.Video_time_select)
        #self.time4.clicked.connect(self.btn_save)


        vbox=QVBoxLayout()
        vbox.addWidget(self.time1)
        vbox.addWidget(self.time2)
        vbox.addWidget(self.time3)
        vbox.addWidget(self.time4)
        groupbox.setLayout(vbox)

    def select_default_time(self):
        groupbox = QGroupBox('기본 좌우 움직임 시간', self)
        groupbox.move(430, 0)
        groupbox.resize(170, 150)

        self.default_time_1=QRadioButton('1분',self)
        self.default_time_1.move(300,180)
        self.default_time_1.clicked.connect(self.Default_movement_select)

        self.default_time_2 = QRadioButton('3분', self)
        self.default_time_2.move(300, 180)
        self.default_time_2.clicked.connect(self.Default_movement_select)

        self.default_time_3 = QRadioButton('5분', self)
        self.default_time_3.move(300, 180)
        self.default_time_3.clicked.connect(self.Default_movement_select)

        self.default_time_4 = QRadioButton('10분', self)
        self.default_time_4.move(300, 180)
        self.default_time_4.clicked.connect(self.Default_movement_select)


        vbox = QVBoxLayout()
        vbox.addWidget(self.default_time_1)
        vbox.addWidget(self.default_time_2)
        vbox.addWidget(self.default_time_3)
        vbox.addWidget(self.default_time_4)
        groupbox.setLayout(vbox)

    def Speed_Button_select(self):
        self.msg_speed=""
        if self.radio1.isChecked():
            self.msg_speed="1"
        elif self.radio2.isChecked():
            self.msg_speed='2'
        elif self.radio3.isChecked():
            self.msg_speed='3'
        else:
            self.msg_speed='4'

        self.msg_spd=self.msg_speed+'\n'
        f1.write(self.msg_spd)


        print(self.msg_speed+' is selected')

    def Move_Button_select(self):
        self.msg_move=""
        if self.radio5.isChecked():
            self.msg_move="10"
        elif self.radio6.isChecked():
            self.msg_move='30'
        else:
            self.msg_move='50'

        self.msg_mov=self.msg_move+'\n'
        f2.write(self.msg_mov)
        print(self.msg_move+' is selected')

    def Video_time_select(self):
        self.msg_time=""
        if self.time1.isChecked():
            self.msg_time='3'
        elif self.time2.isChecked():
            self.msg_time='5'
        elif self.time3.isChecked():
            self.msg_time='10'
        else:
            self.msg_time='15'

        self.msg_tm=self.msg_time+'\n'
        f3.write(self.msg_tm)
        # try:
        #     if self.time1.isChecked() | self.time2.isChecked() | self.time3.isChecked() | self.time4.isChecked():
        #
        #         print(self.msg_time + ' sec is selected')
        #         # time = int(self.msg)
        #         # angle = mp.SaveData()
        #         # t = Thread(target=angle.infrun)
        #         # t.daemon = True
        #         # t = Thread(target=angle.infrun, daemon=True)
        #         # angle.get_data_from_time(time)
        #
        #         #t.start()
        #
        # except Exception as e:
        #     print(e)

    def Default_movement_select(self):
        self.msg_default_time=''

        if self.default_time_1.isChecked():
            self.msg_default_time='1'
        elif self.default_time_2.isChecked():
            self.msg_default_time='3'
        elif self.default_time_3.isChecked():
            self.msg_default_time='5'
        elif self.default_time_4.isChecked():
            self.msg_default_time='10'

        self.msg_def_time=self.msg_default_time+'\n'
        f4.write(self.msg_def_time)


    def set_check(self):
        try:
            with open('speed.txt', 'r') as f:
                for line1 in f:
                    pass
                last_line1 = line1
                print("last line : ", last_line1)
            print(type(last_line1))
            if last_line1 == "1\n":
                self.radio1.setChecked(True)
                self.msg_speed="1"
            elif last_line1=="2\n":
                self.radio2.setChecked(True)
                self.msg_speed = "2"
            elif last_line1=="3\n":
                self.radio3.setChecked(True)
                self.msg_speed = "3"
            elif last_line1=="4\n":
                self.radio4.setChecked(True)
                self.msg_speed = "4"

            with open('movement.txt','r') as g:
                for line2 in g:
                    pass
                last_line2=line2

            if last_line2=="10\n":
                self.radio5.setChecked(True)
                self.msg_move="10"

            elif last_line2=="30\n":
                self.radio6.setChecked(True)
                self.msg_move="30"
            elif last_line2=="50\n":
                self.radio7.setChecked(True)
                self.msg_move="50"

            with open('time.txt','r') as h:
                for line3 in h:
                    pass
                last_line3=line3
                if last_line3=="3\n":
                    self.time1.setChecked(True)
                    self.msg_time="3"
                elif last_line3=="5\n":
                    self.time2.setChecked(True)
                    self.msg_time="5"
                elif last_line3=="10\n":
                    self.time3.setChecked(True)
                    self.msg_time="10"
                elif last_line3=="15\n":
                    self.time4.setChecked(True)
                    self.msg_time="15"

            with open('default_movement.txt','r') as j:
                for line4 in j:
                    pass
                last_line4=line4
                if last_line4=="1\n":
                    self.default_time_1.setChecked(True)
                    self.msg_default_time="1"
                elif last_line4=="3\n":
                    self.default_time_2.setChecked(True)
                    self.msg_default_time = "3"
                elif last_line4=="5\n":
                    self.default_time_3.setChecked(True)
                    self.msg_default_time = "5"
                elif last_line4=="10\n":
                    self.default_time_4.setChecked(True)
                    self.msg_default_time = "10"

        except Exception as e:
            print(e)



    def btn_Back(self):
        try:

            self.close()
        except Exception as e:
            print(e)