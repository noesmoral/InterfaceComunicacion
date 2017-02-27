import RPi.GPIO as GPIO
import time
import threading

#configuramos los pines
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIGD = 6 
ECHOD = 12
TRIGI = 19
ECHOI = 16
#TRIGC = 19
#ECHOC = 16
GPIO.setup(TRIGD,GPIO.OUT)
GPIO.setup(ECHOD,GPIO.IN)
GPIO.setup(TRIGI,GPIO.OUT)
GPIO.setup(ECHOI,GPIO.IN)
#GPIO.setup(TRIGC,GPIO.OUT)
#GPIO.setup(ECHOC,GPIO.IN)
GPIO.output(TRIGD, False)
GPIO.output(TRIGI, False)
#GPIO.output(TRIGIC, False)

def sensor(posicion, stop_event):
	if posicion=="Derecha":
		distanciaAnteriorD=0	
		while (not stop_event.is_set()):
			#Derecha
			#Realizamos un pulso de duracion 10microsegundos para lanzar el ultrasonido
			GPIO.output(TRIGD, True)
			time.sleep(0.00001)
			GPIO.output(TRIGD, False)

			#Detectamos cuando pasa de 0 a 1 osea cuando empieza a recibir la informacion del rebote
			while GPIO.input(ECHOD)==0:
				pulse_start = time.time()
			#Detectamos cuando para de recibir el pulso
			while GPIO.input(ECHOD)==1:
				pulse_end = time.time()

			#Realizamos los calculos para estimar la distancia
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance, 2)
			
			#Suavizamos la distancia tomando la media de dos distancias consecutivas
			distance= (distanciaAnteriorD+distance)/2

			#Mostramos almacenamos distancia para proxima pasada y esperamos un minimo de 30+10 mili segundos
			print "Distancia Derecha:",distance,"cm"
			distanciaAnteriorD=distance
			time.sleep(0.2)
	elif posicion=="Izquierda":
		distanciaAnteriorI=0
		while (not stop_event.is_set()):
			#Izquierda
			#Realizamos un pulso de duracion 10microsegundos para lanzar el ultrasonido
			GPIO.output(TRIGI, True)
			time.sleep(0.00001)
			GPIO.output(TRIGI, False)

	                #Detectamos cuando pasa de 0 a 1 osea cuando empieza a recibir la informacion del rebote
			while GPIO.input(ECHOI)==0:
				pulse_start = time.time()
	                #Detectamos cuando para de recibir el pulso
			while GPIO.input(ECHOI)==1:
				pulse_end = time.time()

	                #Realizamos los calculos para estimar la distancia
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance, 2)

	                #Suavizamos la distancia tomando la media de dos distancias consecutivas
			distance= (distanciaAnteriorI+distance)/2

			#Mostramos almacenamos distancia para proxima pasada y esperamos un minimo de 30+10 mili segundos
			print "Distancia Izquierda:",distance,"cm"
			distanciaAnteriorI=distance
			time.sleep(0.2)
	else:
		"""distanciaAnteriorC=0
		while (not stop_event.is_set()):
		#Central
	        #Realizamos un pulso de duracion 10microsegundos para lanzar el ultrasonido
			GPIO.output(TRIGC, True)
			time.sleep(0.00001)
			GPIO.output(TRIGC, False)

			#Detectamos cuando pasa de 0 a 1 osea cuando empieza a recibir la informacion del rebote
			while GPIO.input(ECHOC)==0:
				pulse_start = time.time()
	                #Detectamos cuando para de recibir el pulso
			while GPIO.input(ECHOC)==1:
				pulse_end = time.time()

			#Realizamos los calculos para estimar la distancia
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance, 2)

			#Suavizamos la distancia tomando la media de dos distancias consecutivas
			distance= (distanciaAnteriorC+distance)/2

			#Mostramos almacenamos distancia para proxima pasada y esperamos un minimo de 30+10 mili segundos
			print "Distancia Central:",distance,"cm"
			distanciaAnteriorC=distance
			time.sleep(0.2)"""

#Realizamos una espera para que se estabilize y evitar cruce con otras medidas
print "Waiting For Sensor To Settle"
time.sleep(2)

#loop principal
try:
	print("Pulse q y enter para terminar")
	t1_stop= threading.Event()
	tx = threading.Thread(target=sensor, args=("Derecha",t1_stop))
	tx.start()
	t2_stop = threading.Event()
	ty = threading.Thread(target=sensor, args=("Izquierda",t2_stop))
	ty.start()
	#t3_stop = threading.Event()
	#tz = threading.Thread(target=sensor, args=("Centro",t3_stop))
	#tz.start()
	while True:
		tecla= raw_input()
		if tecla=="q":
			t1_stop.set()
			t2_stop.set()
			#t3_stop.set()
		  	tx.join()
			ty.join()
			#tz.join()
			GPIO.cleanup()
			break

except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
