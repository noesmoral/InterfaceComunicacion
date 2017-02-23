#otros import
import RPi.GPIO as GPIO
import time
#importamos la opcion de lanzar otros programas para realizar las capturas
import commands
# importamos la libreria smtplib (no es necesario instalarlo)
import smtplib 
# importamos librerias  para construir el mensaje
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
#importamos librerias para adjuntar
from email.MIMEImage import MIMEImage 
from email import encoders 

GPIO.setmode(GPIO.BCM)
boton = 21
pulsado=False
iteraciones=0
GPIO.setwarnings(False)
GPIO.setup(boton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def pulso(boton):
	global pulsado
	pulsado=True

def estaPulsado():
	global iteraciones
	iteraciones=0
	while GPIO.input(boton):
		iteraciones=iteraciones+1
		time.sleep(0.5)
	return iteraciones

GPIO.add_event_detect(boton, GPIO.RISING, callback=pulso, bouncetime=400)

#funciones envio de mensajes
def mensajeConImagen():
	# definimos los correo de remitente y receptor
	##se envia un mail a
	addr_to   = 'pedro.barquin@gmail.com'
	##el mail sale desde el correo
	addr_from = 'pruebasraspberry@gmail.com'

	# Define SMTP email server details
	smtp_server = 'smtp.gmail.com:587'
	smtp_user   = 'pruebasraspberry@gmail.com'
	smtp_pass   = 'Pruebas16'
	 
	# Construimos el mail
	msg = MIMEMultipart() 
	msg['To'] = addr_to
	msg['From'] = addr_from
	msg['Subject'] = 'Prueba Cabecera'
	#cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
	msg.attach(MIMEText('Cuerpo del mensaje'))

	#hacemos la captura antes de enviar el mensaje nuevo
	result=commands.getoutput('/usr/bin/python /home/pi/Desktop/camara.py')

	#adjuntamos fichero de texto pero puede ser cualquer tipo de archivo
	##cargamos el archivo a adjuntar de la ruta definida por el programa
	fp = open('/home/pi/Desktop/Capturas/imagen.jpg','rb')
	#adjunto = MIMEBase('multipart', 'encrypted')
	adjunto = MIMEImage(fp.read())
	#lo insertamos en una variable
	#adjunto.set_payload(fp.read()) 
	#fp.close()  
	#lo encriptamos en base64 para enviarlo
	#encoders.encode_base64(adjunto) 
	#agregamos una cabecera y le damos un nombre al archivo que adjuntamos puede ser el mismo u otro
	adjunto.add_header('Content-Disposition', 'attachment', filename='captura.jpg')
	#adjuntamos al mensaje
	msg.attach(adjunto) 

	# inicializamos el stmp para hacer el envio
	server = smtplib.SMTP(smtp_server)
	server.starttls() 
	#logeamos con los datos ya seteamos en la parte superior
	server.login(smtp_user,smtp_pass)
	#el envio
	server.sendmail(addr_from, addr_to, msg.as_string())
	#apagamos conexion stmp
	server.quit()

def mensajeSimple():
	# definimos los correo de remitente y receptor
	##se envia un mail a
	addr_to   = 'pedro.barquin@gmail.com'
	##el mail sale desde el correo
	addr_from = 'pruebasraspberry@gmail.com'

	# Define SMTP email server details
	smtp_server = 'smtp.gmail.com:587'
	smtp_user   = 'pruebasraspberry@gmail.com'
	smtp_pass   = 'Pruebas16'
	 
	# Construimos el mail
	msg = MIMEMultipart() 
	msg['To'] = addr_to
	msg['From'] = addr_from
	msg['Subject'] = 'Prueba Titulo'
	#cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
	msg.attach(MIMEText('Mensaje principal'))

	# inicializamos el stmp para hacer el envio
	server = smtplib.SMTP(smtp_server)
	server.starttls()
	#logeamos con los datos ya seteamos en la parte superior
	server.login(smtp_user,smtp_pass)
	#el envio
	server.sendmail(addr_from, addr_to, msg.as_string())
	#apagamos conexion stmp
	server.quit()

try:
	while True:
		time.sleep(0.5)
		if (pulsado):
			veces=estaPulsado()
			if(veces>4):
				mensajeConImagen()
				pulsado=False
				iteraciones=0
			else:
				mensajeSimple()
				pulsado=False
				iteraciones=0
except KeyboardInterrupt:  
	GPIO.cleanup()     
GPIO.cleanup()
