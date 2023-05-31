from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
import time
import numpy as np

rear_wheels_enable  = True
front_wheels_enable = True
FW_ANGLE_MAX    = 180
FW_ANGLE_MIN    = 0

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
fw.offset = 0

motor_speed = 70

bw.speed = motor_speed

