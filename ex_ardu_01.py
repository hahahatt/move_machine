import math
import threading

import serial
import time
import DB as db

try:
    d = db.DataBase()
    ready = 'READY!'
    standby = 'standby'
    py_serial = serial.Serial(port='COM7', baudrate=115200)

except Exception as e:
    print(e)

class runMotor:

    def __init__(self):
        try:
            #self.py_serial = serial.Serial(port='COM7', baudrate=115200)
            self.str1 = 'move '
            self.last_speed_data='4'
            self.last_range_data=''
            self.range=0
            self.i=0
            self.last_time=1



        except Exception as e:
            print(e)



    def get_speed_data(self):
        try:
            print('스피드 데이터 가져오는 곳')
            if len(d.select_data2()) != 0:
                self.speed_data = d.select_data2()
                self.last_speed_data = self.speed_data[len(self.speed_data) - 1][0]
                self.last_speed_data = str(self.last_speed_data)
                # print('self.last_range_data Type : ', type(self.last_range_data))
        except Exception as e:
            print(e)



    def get_range_data(self):
        try:
            print('범위 나온거 가져옴')
            if len(d.select_data3()) != 0:
                self.range_data = d.select_data3()
                self.last_range_data = self.range_data[len(self.range_data) - 1][0]
                self.last_range_data = str(self.last_range_data)
                self.range = int(self.last_range_data)
                # print('self.last_range_data Value : ', self.last_range_data)
        except Exception as e:
            print(e)

    def get_default_time_data(self):
        if len(d.select_data4()) != 0:
            self.default_time=d.select_data4()
            self.last_time_data=self.default_time[len(self.default_time) - 1][0]
            self.last_time_data=int(self.last_time_data)
            print('디폴트 시간 값 : ',self.last_time_data)
            print('타입 : ',type(self.last_time_data))
            return self.last_time_data


    def right_move(self):

        if py_serial.readable():
            right_str = 'move 280 '
            right_str=right_str+self.last_speed_data
            right_str = right_str.encode('utf-8')
            py_serial.write(right_str)

            print('휴식시간..1')
            time.sleep(50)


    def left_move(self):
        if py_serial.readable():
            # if data == standby:
            left_str = 'move 10 '
            left_str = left_str + self.last_speed_data
            left_str = left_str.encode('utf-8')
            py_serial.write(left_str)

            print('휴식시간..2')
            time.sleep(50)

    def center_move(self):
        if py_serial.readable():
        #if data == standby:
            center_str = 'move 145 '
            center_str=center_str+self.last_speed_data
            center_str = center_str.encode('utf-8')
            py_serial.write(center_str)

            print('휴식시간..3')
            time.sleep(50)


    def command_motor(self):
        try:

            if py_serial.readable():
                str1='move 145 4'
                str1=str1.encode('utf-8')
                py_serial.write(str1)
                print('초기값 전달')
                i=0
                time.sleep(10)
                print('와일문 시작')


            while True:


                if py_serial.readable():
                    py_serial.timeout=10
                    response = py_serial.readline()
                    # response = self.py_serial.readline()
                    data = response[:len(response) - 1].decode()
                    print(response[:len(response) - 1].decode())
                    data = bytes(data, 'utf-8')
                    data = data[:len(data) - 1].decode()
                    print('맨처음 data : ',data)
                    if data=='':
                        data='standby'


                if data == ready or data==standby:
                    print('여기 들어감')
                    self.get_range_data()
                    self.get_speed_data()
                    self.last_time=self.get_default_time_data()

                    if self.last_time==30:
                        wait_time=30
                    elif self.last_time == 1:
                        wait_time = 60
                    elif self.last_time==5:
                        wait_time=300
                    elif self.last_time==10:
                        wait_time=600


                    print(self.range)

                    if self.range>50:
                        print('1')
                        self.left_move()
                        self.right_move()
                        time.sleep(50)
                        self.center_move()
                        time.sleep(wait_time)
                        #왼쪽부터 시작하는 코드
                    if self.range==50:
                        i=i+1
                        if i%2==0:
                            print('2-1')
                            self.right_move()
                            self.left_move()
                            time.sleep(50)
                            self.center_move()
                            time.sleep(wait_time)
                        elif i%2==1:
                            print('2-2')
                            self.left_move()
                            self.right_move()
                            time.sleep(50)
                            self.center_move()
                            time.sleep(wait_time)

                        if i>=10:
                            i=0

                        #왼쪽 또는 오른쪽부터 시작하는 코드
                    if self.range<50 and self.range!=0:
                        print('3')
                        self.right_move()
                        self.left_move()
                        time.sleep(50)
                        self.center_move()
                        time.sleep(wait_time)
                        #오른쪽부터 시작하는 코드









        except Exception as e:
            print(e)

rm=runMotor()

if __name__=="__main__":
    t=threading.Thread(target=rm.command_motor)
    t.start()