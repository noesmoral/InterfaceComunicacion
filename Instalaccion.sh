#!/bin/sh
sudo apt-get install espeak -y
sudo apt-get install python-picamera -y
sudo apt-get install python-opencv -y
sudo apt-get install python-scipy -y
sudo apt-get install ipython -y
sudo apt-get install qrencode -y
sudo apt-get install python-zbar -y 
sudo apt-get install alsa-utils -y
sudo apt-get install mpg321 -y
sudo apt-get install lame -y

sudo mv Si.mp3 No.mp3 PreguntasRespuestas.csv EnvioCorreo.py Demo7.py camara.py lanzar.sh lanzar1.sh /home/pi/Desktop/
sudo mv pictogramas/ /home/pi/Desktop/
sudo mv script/detector-init script/detector-init1  /etc/init.d/
sudo chmod 775 /etc/init.d/detector-init
sudo chmod 775 /etc/init.d/detector-init1
sudo update-rc.d detector-init defaults
sudo update-rc.d detector-init1 defaults
cd /home/pi/Desktop/
mkdir Capturas PreguntasMP3 RespuestasMP3
