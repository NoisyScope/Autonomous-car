#import libraries
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os

picar.setup()
# Initial parameter configuration
show_image_enable   = False
draw_circle_enable  = False
scan_enable         = False
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

# Picar parameter definition
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.offset = 0
motor_speed = 60

# Filter setting (used for tracking a red ball)
hmn = 12
hmx = 37
smn = 96
smx = 255
vmn = 186
vmx = 255

def destroy():
    bw.stop()
    img.release()

def test():
    fw.turn(90)

    if rear_wheels_enable:
        bw.speed = motor_speed
        bw.backward()
    if rear_wheels_enable:
        bw.speed = motor_speed
        bw.forward()


#Example of parameter activation (This currently does not work)
    if show_image_enable:
        cv2.namedWindow("Threshold lower image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Threshold lower image", lower_red_hue_range)
        cv2.namedWindow("Threshold upper image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Threshold upper image", upper_red_hue_range)
        cv2.namedWindow("Combined threshold images", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Combined threshold images", red_hue_image)
        cv2.namedWindow("Detected red circles on the input image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Detected red circles on the input image", orig_image)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
