#!/usr/bin/python

from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()
sleep(2)
camera.capture('/home/pi/Desktop/Capturas/imagen.jpg',resize=(1024,768))
camera.stop_preview
camera.close()
