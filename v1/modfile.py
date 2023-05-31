#Librerías necesarias, más información en documento “Guía de instalación y uso del AGV.
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os
from threading import Thread

#variables de apoyo.
max_speed = 50
turn_angle = 30 #max 30
alfa = 57  #diferencial resultante de una vuelta que requiera el ángulo máximo de giro a la izq.

m = turn_angle/alfa

#variables control
kp = 8

# Estas variables se crearon durante la competencia en Tampico para encontrar los valores del filtro de imagen de manera más rápida.
#blue_min = 10
#blue_max = 25
#green_min = 100
#red_min = 50

#configuración ángulos de giro.
fw_angle_straight = 100.6
fw_angle_max = fw_angle_straight + turn_angle #giro a la izq
fw_angle_min = fw_angle_straight - turn_angle #giro a la der

#configurar componentes.
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
picar.setup()

def nothing():
    pass

def main():
    #CV
    img = scan()
    img.start()

    #crear figura de sliders, los trackbar se usaron para controlar la velocidad de los motores durante las pruebas “max_speed”, así como el valor del control proporcional “kp”.
    cv2.namedWindow('Trackbar')
    cv2.createTrackbar('kp', 'Trackbar', 20, 100, nothing)
    cv2.createTrackbar('max_speed', 'Trackbar', 30, 100, nothing)
    #cv2.createTrackbar('green_min', 'Trackbar', 100, 255, nothing)
    #cv2.createTrackbar('red_min', 'Trackbar', 50, 255, nothing)

    #Iniciar Componentes.
    bw.speed = 0
    bw.forward()
    fw.turn(fw_angle_straight)
    sleep(0.01)

    while True:
        #Trackbars update. Se obtienen los valores del trackbar
        kp = cv2.getTrackbarPos('kp', 'Trackbar')/10
        max_speed = cv2.getTrackbarPos('max_speed', 'Trackbar')
        #blue_max = cv2.getTrackbarPos('green_min', 'Trackbar')
        #blue_max = cv2.getTrackbarPos('red_min', 'Trackbar')
        turn_speed = int(0.7* max_speed)
        

        #Función de giro
        bw.speed = max_speed
        fw_angle = m*kp*((img.dif+img.dif_a+img.dif_aa)/3) + fw_angle_straight #Con esta función se consigue el ángulo de giro.
        if fw_angle < fw_angle_min:
            fw_angle = fw_angle_min
        if fw_angle > fw_angle_max:
            fw_angle = fw_angle_max
        fw.turn(fw_angle)
        sleep(0.001)
        
def destroy():
    bw.stop()
    cam.release()
    cv2.destroyAllWindows()

#Con la siguiente clase se mantiene la obtención de la imagen de manera paralela y así no se espera a que algo previo pase.
class scan(Thread):
    def _init_(self):
        Thread._init_(self)
        self.kernel = np.ones((5, 5), np.uint8)
        self.cam = cv2.VideoCapture(0)
        self.dif = 0
        self.dif_a = 0
        self.dif_aa = 0

#Mostrar la imagen de la cámara  
 if not self.cam.isOpened:
            print('ERROR: Failed to open camera')

        #configuración display
        self.screen_width = 160
        self.screen_height = 120
        self.cam.set(3, self.screen_width)
        self.cam.set(4, self.screen_height)
        self.center_x = int(self.screen_width / 2)

        #configuración filtro
        self.orange_min = np.array([20, 100, 20]) #10, 100, 50 naranja
        self.orange_max = np.array([40, 255, 255])#25, 255, 255 naranja
        self.blur_level = 5 #número entero e impar

    def run(self):
        while True:
            #actualizar dif_a
            self.dif_aa = self.dif_a
            self.dif_a = self.dif

            #captura de imagen, obtiene un frame de la cámara para saber si se sigue obteniendo imagen de la cámara (fuente)
            self.ret, self.bgr_image = self.cam.read()

            if self.ret == False:
                print('ERROR: Failed to read image')
                
            #temporal
            cv2.namedWindow("Original", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("Original", self.bgr_image)

            #procesado inicial
            self.bgr_image = cv2.medianBlur(self.bgr_image, self.blur_level)
            self.hsv_image = cv2.cvtColor(self.bgr_image, cv2.COLOR_BGR2HSV)

            self.mask_orange = cv2.inRange(self.hsv_image, self.orange_min, self.orange_max)
            self.mask_orange = cv2.GaussianBlur(self.mask_orange, (self.blur_level, self.blur_level), 0)

            self.proc_image = cv2.bitwise_and(self.bgr_image, self.bgr_image, mask=self.mask_orange)

            #posición promedio areas filtradas (255)
            self.pos_sum = 0
            self.n = 0
            
            #Algo que hace la línea
            for self.y in range(self.screen_height):
                self.fin = 0 #variable de linea de fin
                for self.x in range(self.screen_width):
                    if self.mask_orange[self.y,self.x] == 255:
                        self.pos_sum += self.x
                        self.n += 1
                        self.fin += 1 #variable de linea de fin
                #detector de línea final
                if self.fin == self.screen_width:
                    sleep(2)
                    self.cam.release()
                    destroy()
            #robot perdido
            if self.n == 0:
                self.pos_x = self.center_x
                self.dif = self.dif_a
            else:
                self.pos_x = int(self.pos_sum / self.n)
                self.dif = self.pos_x - self.center_x

            #líneas visuales de centro y pos_x
            cv2.line(self.proc_image, (self.pos_x, 0), (self.pos_x, self.screen_height), (255, 0, 0), 1)
            cv2.line(self.proc_image, (self.center_x, 0), (self.center_x, self.screen_height), (0, 0, 255), 1)

            #Mostrar imágenes
            cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("Image", self.proc_image)

            if cv2.waitKey(1) & 0xFF == ord('q'): #Cerrar el programa con la tecla “q”.
                break
                self.cam.release()
                destroy()

if _name_ == '_main_': #Sirve para correr el programa.
    try:
        main()
    except KeyboardInterrupt:
        destroy()
