# Autonomous vehicle
### By: NoisyScope

## 1. Introduction
The main objective of this project is the creation of a 4 wheel, back thrust device which is able to detect a specific track and move forward while keeping itself in the center of the surface mentioned above. As well as knowing the basic funcionality of the device, we also have some limitations which involve a '*base*' platform in which we will be developing the project. We are using a Raspberry **Pi 4b 8GB model**, along with a pre-build kit from Sunfounder.

## 2. Parts list
-SunFounder PiCar V kit
-Raspberry Pi 4b 8gb

## 3. Code
As we know, Raspberry Pi boards support **Python** natively, that's why we will be using it to develop the project. You can find the code in this repository as: `code.py`. 

## 3.1 Code explanation
The first section of the code imports all the libraries needed for the code to work, keep in mind that there are several libraries that are specific for the raspberry as well as the 'SunFounder PicarV kit'.
```
import cv2 as cv
import numpy as np
import os
import time
import picar
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
```
The code will secondly declare all the variables needed for the servo, as well as the motors at the same time it initializes the webcam. You should't be modifying all the values declared in the code. The only values of interest you should be changing in order to test the code are:
`motor_speed` = Car speed (0-100)
`kp` = Proportional controller (it is a multiplier, so be careful entering a value higher than 1)

### 3.1.1 Function definition
In the code we define 2 functions: `find_centroid`, `movement`
`find_centroid` will read the image from the webcam, then it will create a colour mask, as well as a binarization in order to have a plain image with black and white spots along all the image. Secondly, it will use `cv.moments` in order to find the centroid of all the figures that appear to be on the image. Then, we will have to filter the biggest contour and detect the centroid of it. This is because we will want to detect the biggest blob on the image, which should be the black color of the track.

`movement` is the function in charge of moving the car forward as well as turning it through the servo by receiving an input value of the error (expected point along 'x' axis - actual 'x' axis value of the previously calculated centroid)

