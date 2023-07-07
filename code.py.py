import cv2 as cv
import numpy as np
import os
import time
import picar
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo


def nothing(x):pass

cap = cv.VideoCapture(0)
cv.namedWindow('videoUI', cv.WINDOW_NORMAL)
T=240
x=0
# Picar parameter definition
picar.setup()
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.offset = 0
motor_speed = 40
kp=0.8 # Proportional controller
MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 150
TILT_ANGLE_MIN  = 70
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30
FW_STRAIGHT     = 90

def find_centroid(frame):
    global x
    global error
    error = 0
    while x < 3:

        contours, _= cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # Calculate the moments of the contour
            M = cv.moments(contour)
            # Calculate the centroid coordinates
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Draw the centroid on the frame
                cv.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
                error=cX-301
                x += 1
        return error

def movement(error):
    global x
    if float(error)>8:
        fw_angle=FW_STRAIGHT-(float(error)*kp) #giro derecha
        bw.speed = motor_speed
        fw.turn(fw_angle)
    # Corrección de ángulo en caso de sobrepasar los límites
        if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
            fw_angle = ((180 - fw_angle) - 90)/2 + 90
            fw.turn(fw_angle)

    elif float(error)<-8:
        fw_angle=FW_STRAIGHT+(float(error)*kp) #giro derecha
        bw.speed = motor_speed
        fw.turn(fw_angle)
    # Corrección de ángulo en caso de sobrepasar los límites
        if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
            fw_angle = ((180 - fw_angle) - 90)/2 + 90
            fw.turn(fw_angle)
    else:
        bw.speed = motor_speed
        fw.turn(FW_STRAIGHT)
    x -= 1
        
while(True):
    ret, frame = cap.read()
    frame=frame[280:480,0:640]
    vid_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    median_blur_image = cv.medianBlur(vid_gray, 11)
    thresh = T
    vid_bw = cv.threshold(vid_gray, thresh, 255, cv.THRESH_BINARY_INV)[1]
    find_centroid(vid_bw)
    error=error
    movement(error)
    cv.imshow('videoUI',cv.flip(vid_bw,1))
    print(error)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()