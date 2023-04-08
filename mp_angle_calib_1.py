import cv2
import mediapipe as mp
import numpy as np
import scipy.stats as erf
import time
import threading
import matplotlib.pyplot as plt
import DB as d
import sPort as s

base = d.DataBase()
port = s.SPort()


class SaveData:
    def __init__(self):
        # 여기 img 블랙으로 초기화
        self.image = np.zeros((1280, 720, 3), np.uint8)
        self.last_image = np.zeros((1280, 720, 3), np.uint8)
        self.sample_buffH = []
        self.sample_buffV = []
        self.data_sample = []
        self.sampleH = 0
        self.sampleV = 0
        self.x1 = []
        self.y1 = []

        # 얼굴 고정 위치 count를 위한 리스트
        self.face_x = [0] * 11
        self.movement_time = 5

        # 이동 범위를 위한 최대 최소
        self.max_range_x = 10
        self.min_range_x = -10
        self.range = self.max_range_x - self.min_range_x
        self.far_range = 0

        # 이동 범위 계산을 위한 최소 index 찾지
        self.min_index_x = 0

        self.sample_time = 0
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.mp_drawing = mp.solutions.drawing_utils

        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.face_landmark = ''

        self.cap = cv2.VideoCapture(0)
        # 화면 크기를 구한다
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.positionV, self.positionH = 0, 0

        self.angleH, self.angleV = 0, 0
        self.offsetH, self.offsetV = 0, 0
        self.calcH = 0
        self.dist = 0
        # 카메라 별 시야 각이 달라 보정 값을 변경 해야 함
        self.angleError = 50

        # 평균을 이용하여 값 보정
        self.MOVAVG_SIZE = 32
        self.movavg_i = 0
        self.movavg_buffH = []
        self.movavg_buffV = []
        for i in range(0, self.MOVAVG_SIZE):
            self.movavg_buffH.append(0)
            self.movavg_buffV.append(0)

        self.hideImage = False
        self.process = False
    def ret_cap(self):
        return self.cap

    def dosampling(self):
        if self.sample_time== 0:
            self.sample_time = 5
        print("Sampled values in ", self.sample_time, "seconds!")
        if len(self.sample_buffH) > 0:
            self.sampleH = np.round(np.mean(self.sample_buffH), 2)
            self.sampleV = np.round(np.mean(self.sample_buffV), 2)
            print(self.sampleH, self.sampleV)
            base.insert_data(self.sampleH, self.sampleV)
            print("COUNT:", len(self.sample_buffH), "H:", self.sampleH, "V:", self.sampleV)
        else:
            print("No face has been detected")
        self.sample_buffH = []
        self.sample_buffV = []
        self.create_figure()

        threading.Timer(self.sample_time, self.dosampling).start()

    def angle_calib(self):
        self.process = True
        if self.cap.isOpened():

            success, self.image = self.cap.read()

            start = time.time()

            # Flip the image horizontally for a later selfie-view display
            # Also convert the color space from BGR to RGB

            # To improve performance
            self.image.flags.writeable = False
            self.image = cv2.cvtColor(cv2.flip(self.image, 1), cv2.COLOR_BGR2RGB)
            # Get the result
            results = self.face_mesh.process(self.image)

            # Draw the face mesh annotations on the image
            # To improve performance
            self.image.flags.writeable = True
            # Convert the color space from RGB to BGR
            self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

            # initialize the values
            img_h, img_w, img_c = self.image.shape
            face_3d = []
            face_2d = []

            p1 = np.array([0, 0, 0])
            p2 = np.array([0, 0, 0])

            # hide image
            if self.hideImage:
                self.image = np.zeros((img_h, img_w, 3), np.uint8)

            if results.multi_face_landmarks:
                for self.face_landmarks in results.multi_face_landmarks:
                    for idx, lm in enumerate(self.face_landmarks.landmark):
                        # 234/454 is the left/right point of the face
                        if idx == 234:
                            # print(lm.x,lm.y,lm.z)
                            p1 = np.array([lm.x * img_w, lm.y * img_h, lm.z * img_w])
                        if idx == 454:
                            # print(lm.x, lm.y, lm.z)
                            p2 = np.array([lm.x * img_w, lm.y * img_h, lm.z * img_w])

                        if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                            if idx == 1:
                                nose_2d = (lm.x * img_w, lm.y * img_h)
                                nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                            x, y = int(lm.x * img_w), int(lm.y * img_h)

                            # Get the 2D Coordinates
                            face_2d.append([x, y])

                            # Get the 3D Coordinates
                            face_3d.append([x, y, lm.z])

                            # Convert it to the NumPy array
                    face_2d = np.array(face_2d, dtype=np.float64)

                    # Convert it to the NumPy array
                    face_3d = np.array(face_3d, dtype=np.float64)

                    # The camera matrix
                    focal_length = 1 * img_w

                    cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                           [0, focal_length, img_w / 2],
                                           [0, 0, 1]])

                    # The distortion parameters
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)

                    # Solve PnP
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                    # Get rotational matrix
                    rmat, jac = cv2.Rodrigues(rot_vec)

                    # Get angles
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                    # Get the y rotation degree
                    self.angleV = angles[0] * self.width * 1.2 + self.offsetV
                    self.angleH = angles[1] * self.width * 1.2 + self.offsetH
                    # z = angles[2] * 1800

                    # get distance of the face
                    squared_dist = np.sum((p1 - p2) ** 2, axis=0)
                    self.dist = np.sqrt(squared_dist)
                    # print(dist)

                    # See where the user's head tilting
                    """
                    if y < -10:
                        text = "Looking Left"
                    elif y > 10:
                        text = "Looking Right"
                    elif x < -10:
                        text = "Looking Down"
                    elif x > 10:
                        text = "Looking Up"
                    else:
                        text = "Forward"
                    """
                    text = ""
                    # Display the nose direction
                    nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix,
                                                                     dist_matrix)

                    p1 = (int(nose_2d[0]), int(nose_2d[1]))
                    # p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

                    self.positionH, self.positionV = nose_2d[0], nose_2d[1]

                    # print(positionW,positionH)
                    cv2.line(self.image, (0, int(nose_2d[1])), (int(self.width), int(nose_2d[1])), (0, 255, 0), 2)
                    cv2.line(self.image, (int(nose_2d[0]), 0), (int(nose_2d[0]), int(self.height)), (0, 255, 0), 2)

                    # macbook 카메라는 좌/우 최대 25도 정도 오차 발생
                    # 카메라는 고정된 위치기 때문에 각도 보정을 한다

                    # 우선 상하좌우 최대값을 +1 -1로 변경
                    self.positionH = (self.positionH / self.width * 2) - 1
                    self.positionV = (self.positionV / self.height * 2) - 1

                    # y=50x^3
                    self.calcH = -self.angleError \
                            * (self.positionH * self.positionH) \
                            * (self.positionH / abs(self.positionH)) \
                            + self.angleH

                    # 값 보정
                    # 원형 큐의 원리를 통해
                    # 최근 MOVAVG_SIZE개만큼 각도값의 평균을 구한다
                    # 이 과정을 할 경우 값에 약간의 딜레이가 발생한다

                    self.movavg_buffH[self.movavg_i] = np.round(self.calcH, 2)
                    self.movavg_buffV[self.movavg_i] = np.round(self.angleV, 2)
                    self.movavg_i = (self.movavg_i + 1) % self.MOVAVG_SIZE

                    # print(np.round(np.mean(movavg_buffH), 1),np.round(np.mean(movavg_buffV), 1))

                    # print(np.mean(movavg_buff))
                    # Add the text on the image
                    cv2.putText(self.image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                    # H = Yaw
                    cv2.putText(self.image,
                                "H: " + str(np.round(np.mean(self.movavg_buffH), 1)) + "," + str(
                                    np.round(self.calcH, 2)) + "(" + str(
                                    np.round(self.angleH, 2)) + ")", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                                2)
                    # V = Pit
                    cv2.putText(self.image, "V: " + str(np.round(np.mean(self.movavg_buffV), 1)) + "," + str(
                        np.round(self.angleV, 2)),
                                (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    # D = pixel
                    cv2.putText(self.image, "D: " + str(np.round(self.dist, 2)) + "px", (0, 150), cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 0, 255),
                                2)
                    # cv2.putText(image, "z: " + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                self.sample_buffH.append(np.round(np.mean(self.calcH), 2))
                self.sample_buffV.append(np.round(np.mean(self.angleV), 2))

                end = time.time()
                totalTime = end - start

                fps = 1 / totalTime
                # print("FPS: ", fps)

                # cv2.putText(image, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

                self.mp_drawing.draw_landmarks(
                    image=self.image,
                    landmark_list=self.face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=self.drawing_spec,
                    connection_drawing_spec=self.drawing_spec)
            # Full screen mode
            # cv2.namedWindow('Head Pose Estimation', cv2.WND_PROP_FULLSCREEN)
            # cv2.setWindowProperty('Head Pose Estimation', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            # cv2.namedWindow('Head Pose Estimation', cv2.WINDOW_NORMAL | cv2.WINDOW_FULLSCREEN);

            # cv2.imshow('Head Pose Estimation', image)
            # print("H", np.round(np.mean(self.sample_buffH), 2), "V", np.round(np.mean(self.sample_buffV), 2))

            # if cv2.waitKey(5) & 0xFF == 27:
            #    break

        # self.cap.release()
        self.last_image = self.image
        self.process = False
    def ret_landmark(self):
        return self.face_landmarks

    def img_return(self):
        if self.process == True:
            return self.last_image
        else:
            return self.image

    def get_movement_time(self,move_time):
        self.movement_time=move_time

    def get_sample_data(self):
        self.data_sample = base.select_data()
        print("Data sample:", self.data_sample)
        print("Data sample length:", len(self.data_sample))
        if len(self.data_sample) >= self.movement_time:
            for i in range(0, len(self.data_sample)):
                self.x1.append(self.data_sample[i][0])
                self.y1.append(self.data_sample[i][1])
            print("x1:", self.x1)
            print("y1:", self.y1)
            base.delete_data()
            self.data_sample = []
            return self.x1, self.y1
        else:
            print("Not enough data")
            return -1, -1

    def infrun(self):
        threading.Timer(self.sample_time, self.dosampling).start()
        while True:
            # self.img_return()
            self.angle_calib()

    def getSampleAngle(self):
        return self.sampleH, self.sampleV
    def get_data_from_time(self, time):
        self.sample_time = time

    def get_data_offset(self,setH,setV):
        self.offsetH=self.offsetH-setH
        self.offsetV=self.offsetV-setV
        print(self.offsetH,'  ',self.offsetV)

    def create_figure(self):
        # db로 부터 데이터를 받아오는 함수를 통해서 데이터를 저장하고 범위내의 최대 최소 거리를 계산
        x, y = self.get_sample_data()
        print("data:", x, y)

        if x != -1 and y != -1:
            for j in x:
                if self.max_range_x < j:
                    self.max_range_x = j
                if self.min_range_x > j:
                    self.min_range_x = j
            self.range = self.max_range_x - self.min_range_x
            print("최대:", self.max_range_x, "최소:", self.min_range_x, "범위:", self.range)

            print("범위[", end="")
            for k in range(0, 11):
                print(np.round((self.range / 10 * k) + self.min_range_x, 2), end=" ")
            print("]")

            for i in x:
                print("i:", int(i))
                if -4 < int(i) < 4:
                    i = 0
                    temp = int(i / (self.range / 11))
                else:
                    temp = int(i / (self.range / 11))
                print("temp:", temp, end=" ")
                if temp < -5:
                    temp = -5
                elif temp > 5:
                    temp = 5
                self.face_x[temp + 5] += 1

            print()
            print("x: ", self.face_x)
            # 가장 많이 본 얼굴의 index를 기준으로 이동 거리 index를 구한다.
            print("index:", self.face_x.index(max(self.face_x)))
            if self.face_x.index(max(self.face_x)) == 5:
                self.far_range = 50
                print("far_range: ", self.far_range)
                port.move(self.far_range)
                #print(port.get_value())
            elif self.face_x.index(max(self.face_x)) < 5:
                for i in range(6, 11):
                    for j in range(i+1, 11):
                        if self.face_x[i] > self.face_x[j]:
                            self.far_range = j
                        elif self.face_x[i] < self.face_x[j]:
                            self.far_range = i
                        else:
                            self.far_range = j
                print("far_range:", self.far_range)
                port.move(self.far_range)
                #print(port.get_value())
            elif self.face_x.index(max(self.face_x)) > 5:
                for i in range(0, 5):
                    for j in range(1, 5):
                        if self.face_x[i] > self.face_x[j]:
                            self.far_range = j
                        elif self.face_x[i] < self.face_x[j]:
                            self.far_range = i
                        else:
                            self.far_range = i
                print("far_range:", self.far_range)
                port.move(self.far_range)
                #print(port.get_value())

            fig = plt.figure()
            axis = fig.add_subplot(1, 1, 1)
            axis.scatter(x, y, s=1, color='red')
            # axis.plot(tempW, tempH)
            axis.set_xlim([-90, 90])
            axis.set_ylim([-50, 50])
            axis.set_xlabel('Head angle H')
            axis.set_ylabel('Head angle V')
            axis.grid(True)
            plt.savefig('savefig.png')
            x = []
            y = []
            self.face_x = [0] * 11

    def ret_movavg_buffH(self):
        return self.movavg_buffH

    def ret_calcH(self):
        return self.calcH

    def ret_angleH(self):
        return self.angleH

    def ret_movavg_buffV(self):
        return self.movavg_buffV

    def ret_angleV(self):
        return self.angleV

    def ret_dist(self):
        return self.dist
mySave = SaveData()
if __name__ == '__main__':
    base.delete_data()
    t = threading.Thread(target=mySave.infrun)
    t.start()
    # mySave.infrun()
    while True:
        cv2.imshow('Head Pose Estimation', mySave.img_return())
        if cv2.waitKey(1) & 0xFF == 27:
            break
