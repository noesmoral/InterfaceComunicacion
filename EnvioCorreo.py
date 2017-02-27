#!/usr/bin/env python
# -*- coding: utf-8 -*-
#otros import
import RPi.GPIO as GPIO
import time
import sys
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

addr_to='pedro.barquin@gmail.com'
mensaje="Cuerpo del mensaje de pruebas de raspberry, para el envio de correos"

#funciones envio de mensajes
def mensajeConImagen():
	# definimos los correo de remitente y receptor
	##se envia un mail a
	global addr_to
        global mensaje
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
	msg['Subject'] = 'Correo notificacion Pruebas Raspberry'
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
	global addr_to
	global mensaje
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
	msg['Subject'] = 'Correo notificacion Pruebas Raspberry'
	#cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
	msg.attach(MIMEText(mensaje))

	# inicializamos el stmp para hacer el envio
	server = smtplib.SMTP(smtp_server)
	server.starttls()
	#logeamos con los datos ya seteamos en la parte superior
	server.login(smtp_user,smtp_pass)
	#el envio
	server.sendmail(addr_from, addr_to, msg.as_string())
	#apagamos conexion stmp
	server.quit()

if len(sys.argv)==1:
	mensajeSimple()
elif len(sys.argv)>1 and len(sys.argv)<4:
	print "Se ha olvidado añadir algun elemento o poner Default"
	print "El orden es:"
	print "Mensaje con imagen: Imagen o Default"
	print "Cuerpo del mensaje: xxx o Default"
	print "Correo: xxx@gmail.com o Default"
else:
	if sys.argv[2]!="Default":
		mensaje=sys.argv[2]
	if sys.argv[3]!="Default":
		addr_to= sys.argv[3]
		if addr_to.endswith(('@gmail.com','@hotmail.com')):
			pass
		else:
			print "el correo (tercer parametro) no es valido"
			sys.exit()
	if sys.argv[1]=="Imagen":
		mensajeConImagen()
	elif sys.argv[1]=="Default":
		mensajeSimple()
	else:
		print "El primer parametro no es valido"
