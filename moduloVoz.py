#!/usr/bin/python
import os,signal
import subprocess, time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) ## GPIO 17 como salida

class VOZ():

	def __init__(self):
		try:
			os.system("rm /home/pi/Desktop/registro.txt")

			subprocess.Popen('sudo pocketsphinx_continuous -lm /home/pi/Diccionario/9586.lm -dict /home/pi/Diccionario/9586.dic > /home/pi/Desktop/registro.txt -adcdev sysdefault -inmic yes',stdout=subprocess.PIPE,shell=True)
			time.sleep(1)

		except Exception as e:
			print(e)

	def close(self):
                os.system("sudo pkill pocketsphinx_co")
