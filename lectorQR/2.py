import sys
import os
import time


os.system('sudo modprobe bcm2835-v4l2')
time.sleep(1)
os.system('v4l2-ctl --overlay=1')
time.sleep(1)
p = os.popen('/usr/bin/zbarcam -v --nodisplay --prescale=640x480')

def start_scan():
    global p
    while True:
	#time.sleep(0.5)
        print('Scanning')
        data = p.readline()
        qrcode = str(data)[8:]
        if(qrcode):
            print(qrcode)

try:
    start_scan()
except KeyboardInterrupt:
    print('Stop scanning')
finally:
    p.close()
