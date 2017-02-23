#!/bin/sh
sudo apt-get install espeak
sudo apt-get install python-picamera -y

mv Si.mp3 No.mp3 PreguntasRespuestas.csv EnvioCorreo.py Demo7.py camara.py lanzar.sh lanzar1.sh /home/pi/Desktop/
sudo mv script/detector-init script/detector-init1  /etc/init.d/
sudo chmod 775 /etc/init.d/detector-init
sudo chmod 7777 /etc/init.d/detector-init1
sudo sudo update-rc.d detector-init defaults
sudo sudo update-rc.d detector-init1 defaults
cd /home/pi/Desktop/
mkdir Capturas PreguntasMP3 RespuestasMP3