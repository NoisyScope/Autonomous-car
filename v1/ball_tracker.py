from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os

picar.setup()
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking
show_image_enable   = False
draw_circle_enable  = False
scan_enable         = False
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30


bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
picar.setup()

fw.offset = 0

bw.speed = 0
fw.turn(90)

motor_speed = 60

bw.speed = motor_speed
bw.forward()