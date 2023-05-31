import cv2 # Import the OpenCV library to enable computer vision
import numpy as np # Import the NumPy scientific computing library
import edge_detection as edge # Handles the detection of lane lines
import matplotlib.pyplot as plt # Used for plotting and error checking
import picar
import os
from threading import Thread
import time
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo

# Car initialization settings
picar.setup()
# Initial parameter configuration
show_image_enable = False
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
motor_speed = 20
kp=1 # Proportional controller
MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 150
TILT_ANGLE_MIN  = 70
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30
FW_STRAIGHT     = 90


def car_movement(self):
  center_offset = self.center_offset
  print(center_offset)
  bw.forward()
  if float(center_offset)>2:
      fw_angle=FW_STRAIGHT-(30*kp) #giro izquierda
      bw.speed = motor_speed
      fw.turn(fw_angle)
  # Corrección de ángulo en caso de sobrepasar los límites
      if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
          fw_angle = ((180 - fw_angle) - 90)/2 + 90
          fw.turn(fw_angle)

  elif float(center_offset)<-2:
      fw_angle=FW_STRAIGHT+(30*kp) #giro derecha
      bw.speed = motor_speed
      fw.turn(fw_angle)
  # Corrección de ángulo en caso de sobrepasar los límites
      if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
          fw_angle = ((180 - fw_angle) - 90)/2 + 90
          fw.turn(fw_angle)
  else:
      
      bw.speed = motor_speed
      fw.turn(FW_STRAIGHT)