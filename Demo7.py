#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from subprocess import call
import pygame
import time
import commands
import sys
import os
import csv
import pygame.mixer
from pygame.locals import *

GPIO.setmode(GPIO.BCM)  #configuramos el formato en este caso segun la posicion en la placa

#variables y declaracciones
ledV = 25
ledR = 22
boton_si = 23
boton_no = 24
boton_apagar=20
pulsadoSi=False
pulsadoNo=False
iteraciones=0

listaRespuestas=[]
listaRespuestasImagenes=[]
listaPreguntas=[]
listaPreguntasImagenes=[]

tamanio=0

#graficos
pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode((800, 480))
WHITE = (255, 255, 255)
screen.fill(WHITE)
myfont = pygame.font.SysFont("monospace", 55)

#configuramos los pines gpio para los pulsadores y leds
GPIO.setwarnings(False)
GPIO.setup(boton_si, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(boton_no, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(boton_apagar, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledV, GPIO.OUT, initial=False)
GPIO.setup(ledR, GPIO.OUT, initial=False)

def no(boton_no):
	global pulsadoNo
	pulsadoNo=True

def si(boton_si):
	global pulsadoSi
	pulsadoSi=True

def importarFrases():
	global listaRespuestas
	global listaPreguntas
	global tamanio
	archivo=csv.reader(open('/home/pi/Desktop/PreguntasRespuestas.csv'), delimiter=';')
	for index,PreRes in enumerate(archivo):
		if (index!=0):
			listaPreguntas.append(PreRes[0])	
			listaRespuestas.append(PreRes[1])	
			listaPreguntasImagenes.append(PreRes[2])
			listaRespuestasImagenes.append(PreRes[3])
	tamanio=len(listaPreguntas)

def apagar(boton_apagar):
	GPIO.cleanup()
	pygame.quit()
	sys.exit(0)
	

GPIO.add_event_detect(boton_si, GPIO.RISING, callback=si, bouncetime=400)
GPIO.add_event_detect(boton_no, GPIO.RISING, callback=no, bouncetime=400)
GPIO.add_event_detect(boton_apagar, GPIO.RISING, callback=apagar, bouncetime=400)


def respuestaSiMensaje(mensaje):
	global listaRespuestas	
	global listaRespuestasImagenes
	separarImagenesPreguntas(listaRespuestasImagenes[mensaje])
	mostrarTexto(listaRespuestas[mensaje])
	GPIO.output(ledV, True)
	os.system('aplay 2>/dev/null /home/pi/Desktop/RespuestasMP3/'+str(mensaje)+'.mp3')
	GPIO.output(ledV, False)
	time.sleep(2)
	screen.fill(WHITE)
	pygame.display.flip()
	

def respuestaSi():
	print("Respuesta: SI")
	GPIO.output(ledV, True) ## Enciendo el 27
	os.system('aplay 2>/dev/null /home/pi/Desktop/Si.mp3')
	GPIO.output(ledV, False)

def respuestaNo():
	print("Respuesta: NO")
	GPIO.output(ledR, True) ## Enciendo el 27
	os.system('aplay 2>/dev/null /home/pi/Desktop/No.mp3')
	GPIO.output(ledR, False)

def estaPulsadoNo():
	global iteraciones
	iteraciones=0
	while GPIO.input(boton_no):
		iteraciones=iteraciones+1
		time.sleep(0.5)
	return iteraciones

def separarImagenesPreguntas(cadenaImagenes):
	listaImagenes=cadenaImagenes.split("-")
	if len(listaImagenes)==1:
		if listaImagenes[0]!="0":
			background_image = load_image(listaImagenes[0])
                        screen.blit(background_image, (300, 100))
	elif len(listaImagenes)==2:
		background_image = load_image(listaImagenes[0])
		screen.blit(background_image, (250, 100))
		background_image = load_image(listaImagenes[1])
		screen.blit(background_image, (450, 100))
	elif  len(listaImagenes)==3:
		background_image = load_image(listaImagenes[0])
		screen.blit(background_image, (200, 100))
		background_image = load_image(listaImagenes[1])
		screen.blit(background_image, (400, 100))
		background_image = load_image(listaImagenes[2])
		screen.blit(background_image, (600, 100))
	elif  len(listaImagenes)==4:
		background_image = load_image(listaImagenes[0])
		screen.blit(background_image, (125, 100))
		background_image = load_image(listaImagenes[1])
		screen.blit(background_image, (285, 100))
		background_image = load_image(listaImagenes[2])
		screen.blit(background_image, (445, 100))
		background_image = load_image(listaImagenes[3])
		screen.blit(background_image, (605, 100))
	elif  len(listaImagenes)==5:
		background_image = load_image(listaImagenes[0])
		screen.blit(background_image, (0, 100))
		background_image = load_image(listaImagenes[1])
		screen.blit(background_image, (155, 100))
		background_image = load_image(listaImagenes[2])
		screen.blit(background_image, (310, 100))
		background_image = load_image(listaImagenes[3])
		screen.blit(background_image, (465, 100))
		background_image = load_image(listaImagenes[4])
		screen.blit(background_image, (620, 100))
	else:
		for i in range(0, len(listaImagenes)):
			background_image = load_image(listaImagenes[i])
			screen.blit(background_image, (i*155, 0))

def preguntas():
	cont=0
	global tamanio
	global pulsadoSi
	global pulsadoNo
	pulsadoNo=False
	pulsadoSi=False
	global listaPreguntas
	global listaPreguntasImagenes
	print(listaPreguntas[cont]+"?")
	separarImagenesPreguntas(listaPreguntasImagenes[cont])
	mostrarTexto(listaPreguntas[cont]+"?")
	os.system('aplay 2>/dev/null /home/pi/Desktop/PreguntasMP3/'+str(cont)+'.mp3')
	while cont<tamanio:
		time.sleep(0.3)
		if (pulsadoSi):
			screen.fill(WHITE)
			pygame.display.flip()
			respuestaSiMensaje(cont)
			pulsadoNo=False
			pulsadoSi=False
			break
		if (pulsadoNo):
			screen.fill(WHITE)
			pygame.display.flip()
			cont=cont+1
			if cont==tamanio:
				cont=0
			pulsadoNo=False
			pulsadoSi=False
			separarImagenesPreguntas(listaPreguntasImagenes[cont])
			mostrarTexto(listaPreguntas[cont]+"?")		
			os.system('aplay 2>/dev/null /home/pi/Desktop/PreguntasMP3/'+str(cont)+'.mp3')

def convertirRespuestas():
	global tamanio
	global listaRespuestas
	cont=0
	while cont<tamanio:
		archi=open('/home/pi/Desktop/RespuestasMP3/datos.txt','w')
		archi.write(listaRespuestas[cont])
		archi.close()
		os.system('espeak -v es -s 150 -f /home/pi/Desktop/RespuestasMP3/datos.txt -w /home/pi/Desktop/RespuestasMP3/'+str(cont)+'.mp3')
		cont=cont+1	

def convertirPreguntas():
	global tamanio
	global listaPreguntas
	cont=0
	while cont<tamanio:
		archi=open('/home/pi/Desktop/PreguntasMP3/datos.txt','w')
		archi.write(listaPreguntas[cont])
		archi.close()
		os.system('espeak -v es -s 150 -f /home/pi/Desktop/PreguntasMP3/datos.txt -w /home/pi/Desktop/PreguntasMP3/'+str(cont)+'.mp3')
		cont=cont+1

def mostrarTexto(mensaje):
        textSurface=myfont.render(mensaje, 1, (0,0,0))
	textRect= textSurface.get_rect()
	textRect.center=(400,350)
	screen.blit(textSurface,textRect)
	pygame.display.update()

def load_image(filename):
	ruta="/home/pi/Desktop/pictogramas/"+filename+".png"
	try: image = pygame.image.load(ruta)
	except pygame.error, message:
		raise SystemExit, message
	return image.convert()
	
try:
	importarFrases()
	convertirRespuestas()
	convertirPreguntas()
	mostrarTexto("Demo")
	time.sleep(5)
	#limpiamos pantalla
	screen.fill(WHITE)
	pygame.display.flip()
	while True:
		time.sleep(0.5)
		if (pulsadoSi):
			respuestaSi()
			pulsadoNo=False
			pulsadoSi=False
		if (pulsadoNo):
			veces=estaPulsadoNo()
			print(veces)
			if(veces>4):
				preguntas()
				pulsadoNo=False
				pulsadoSi=False
				iteraciones=0
			else:
				respuestaNo()
				pulsadoNo=False
				pulsadoSi=False
				iteraciones=0
except KeyboardInterrupt:  
	GPIO.cleanup()    
	pygame.quit() 
	sys.exit(0)	
GPIO.cleanup()       
pygame.quit()
sys.exit(0)    
