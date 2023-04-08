import threading

import cv2
import numpy
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import mediapipe as mpi

from time import time,sleep
import time
import math

#from mp_angle_calib import base
#from secondwindow import SecondWindow
from second_win import SecondWindow
from Thirdwindow import ThirdWindow
import DB
import mp_angle_calib_1 as mp

import ex_arduuu as ex
import ex_ardu_01 as ex01

db= DB.DataBase()
running = False
angle=mp.SaveData()
rm=ex01.runMotor()

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        try:
            super().__init__()

            self.initUI()

            db.delete_data2()
            db.delete_data3()

        except Exception as e:
            print(e)


    def initUI(self):
        try:
            self.setWindowTitle('Video page')
            self.setGeometry(300, 300, 650, 540)

            self.cpt = angle.ret_cap()
            if self.cpt.isOpened():
                self.fps = 24
                self.sens = 300
                _, self.img_o = self.cpt.read()

                self.img_o = cv2.cvtColor(self.img_o, cv2.COLOR_RGB2GRAY)

                cv2.imwrite("img_o.jpg", self.img_o)

                self.cnt = 0

                self.frame = QLabel(self)
                self.frame.resize(640, 480)
                self.frame.setScaledContents(True)
                self.frame.move(5, 5)

                self.btn_on = QPushButton("On", self)
                self.btn_on.resize(100, 25)
                self.btn_on.move(5, 490)
                self.btn_on.clicked.connect(self.start)

                self.btn_off = QPushButton("Off", self)
                self.btn_off.resize(100, 25)
                self.btn_off.move(5 + 100 + 5, 490)
                self.btn_off.clicked.connect(self.stop)

                self.prt = QLabel(self)
                self.prt.resize(200, 25)
                self.prt.move(5 + 105 + 105, 490)

                self.sldr = QSlider(Qt.Horizontal, self)
                self.sldr.resize(100, 25)
                self.sldr.move(5 + 105 + 105 + 200, 490)
                self.sldr.setMinimum(1)
                self.sldr.setMaximum(30)
                self.sldr.setValue(24)
                self.sldr.valueChanged.connect(self.setFps)

                self.sldr1 = QSlider(Qt.Horizontal, self)
                self.sldr1.resize(100, 25)
                self.sldr1.move(5 + 105 + 105 + 200 + 105, 490)
                self.sldr1.setMinimum(50)
                self.sldr1.setMaximum(500)
                self.sldr1.setValue(300)
                self.sldr1.valueChanged.connect(self.setSens)
            else:
                QtWidgets.QMessageBox.about(self, "Error", "카메라를 연결해주세여.")





            # btn_video_start = QPushButton('Video', self)
            # btn_video_start.move(100, 0)
            # btn_video_start.clicked.connect(self.btn_video_start)



            btn_second = QPushButton("설정", self)
            #btn_second.move(200, 0)
            btn_second.clicked.connect(self.btn_Second)



            btn_apply= QPushButton("적용", self)
            btn_apply.move(100, 0)
            btn_apply.clicked.connect(self.btn_apply)

            btn_cali=QPushButton("카메라 맞추기",self)
            btn_cali.move(200,0)
            btn_cali.clicked.connect(self.btn_cali_func)

            btn_third = QPushButton("분포도창", self)
            btn_third.move(300, 0)
            btn_third.clicked.connect(self.btn_Third)

            self.mp_face_mesh = mpi.solutions.face_mesh
            self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

            self.mp_drawing = mpi.solutions.drawing_utils

            self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        except Exception as e:
            print(e)



    def btn_video_start(self):
        try:
            global running
            running = True
            # while True:
            #     cv2.imshow('Head Pose Estimation(ESC, want to stop)', angle.img_return())
            #     if cv2.waitKey(1) & 0xFF == 27:
            #         break
            while running:
                cv2.imshow('Head Pose Estimation(ESC, want to stop)', angle.img_return())
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        except Exception as e:
            print(e)



    def btn_Second(self):
        try:
            self.hide()

            self.second = SecondWindow()
            self.second.exec()
            print(self.second.save_msg," 메인화면으로 값 이동했음ㅋㄹㅇㄹㄷ")
            if self.second.save_msg == 1:
                #print(self.second.msg_time," 초")
                print(self.second.msg_speed," 단")
                #print(self.second.msg_move, " 개")
            else:
                print("취소됨")
            self.show()
        except Exception as e:
            print(e)

    def btn_apply(self):
        try:
            #time = int(self.second.msg_time)
            #print(time)
            speed=str(self.second.msg_speed)
            print(type(speed))
            default_time=str(self.second.msg_default_time)
            movement=int(self.second.msg_move)

            angle.get_movement_time(movement)
            #angle.get_data_from_time(time)

            db.insert_data2(speed)
            db.insert_data4(default_time)
            #db.insert_data5(time)
            db.insert_data6(movement)

            QtWidgets.QMessageBox.about(self, "Success", "적용.")
            print('time : ',time,' speed : ',speed,' movement : ',movement,' default time : ',default_time)
        except Exception as e:
            print(e)

    def btn_cali_func(self):
        try:
            start = int(math.floor(time.time()))
            print("버튼 누름 ",start)
            sleep(3)
            end = int(math.floor(time.time()))
            print("end 시간 : ",end)
            if end - start == 3:
                print("3초 지남")
                print(angle.getSampleAngle())
                setH=angle.getSampleAngle()[0]
                setV=angle.getSampleAngle()[1]
                print(setH," ",setV)
                angle.get_data_offset(setH,setV)
                print("오프셋값 보냄")
        except Exception as e:
            print(e)

    def btn_Third(self):

        try:
            self.hide()

            self.third = ThirdWindow()
            self.third.exec()
            self.show()
        except Exception as e:
            print(e)

    def setFps(self):
        self.fps = self.sldr.value()
        self.prt.setText("FPS" + str(self.fps) + "로 조정")
        self.timer.stop()
        self.timer.start(1000 / self.fps)

    def setSens(self):
        self.sens = self.sldr.value()
        self.prt.setText("감도" + str(self.sens) + "로 조정")

    def start(self):

        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 / self.fps)

    def nextFrameSlot(self):
        try:
            _, cam = self.cpt.read()
            cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
            cam=cv2.flip(cam,1)
            # cv2.putText(cam, str, (10, 100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))
            text = ""
            cv2.putText(cam, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            # H = Yaw
            cv2.putText(cam,
                        "H: " + str(np.round(np.mean(angle.ret_movavg_buffH()), 1)) + "," + str(
                            np.round(angle.ret_calcH(), 2)) + "(" + str(
                            np.round(angle.ret_angleH(), 2)) + ")", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        2)
            #V = Pit
            cv2.putText(cam, "V: " + str(np.round(np.mean(angle.ret_movavg_buffV()), 1)) + "," + str(
                np.round(angle.ret_angleV(), 2)),
                        (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # D = pixel
            cv2.putText(cam, "D: " + str(np.round(angle.ret_dist(), 2)) + "px", (0, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2)


            self.mp_drawing.draw_landmarks(
                image=cam,
                landmark_list=angle.ret_landmark(),
                connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.drawing_spec)

            self.img_p = cv2.cvtColor(cam, cv2.COLOR_RGB2GRAY)
            cv2.imwrite('img_p.jpg', self.img_p)
            self.compare(self.img_o, self.img_p)
            self.img_o = self.img_p.copy()
            img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            self.frame.setPixmap(pix)
        except Exception as e:
            print(e)
    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))
        self.timer.stop()

    def compare(self, img_o, img_p):
        err = numpy.sum((img_o.astype("float") - img_p.astype("float")) ** 2)
        err /= float(img_o.shape[0] * img_p.shape[1])
        if (err >= self.sens):
            t = time.localtime()
            self.prt.setText(
                "{}-{}-{} {}:{}:{} 움직임 감지".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))

    def get_movavg(self):
        self.movavg_buff[self.movavg_i]

if __name__=="__main__":

    try:
        app = QApplication(sys.argv)

        window = MyWindow()

        window.show()

        db.delete_data()
        t = threading.Thread(target=angle.infrun)
        t.daemon = True
        t = threading.Thread(target=angle.infrun, daemon=True)
        t.start()

        t2=threading.Thread(target=rm.command_motor)
        t2.daemon = True
        t2=threading.Thread(target=rm.command_motor, daemon=True)
        t2.start()

        sys.exit(app.exec_())
    except Exception as e:
        print(e)


