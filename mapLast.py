import pylab as pl
import numpy
import cv2
import RPi.GPIO as GPIO                    
import time
from matplotlib import collections  as mc
import math
from Adafruit_IO import Client


aio = Client('2847f3e0b36f4f308a5582fdc58211ab')




GPIO.setmode(GPIO.BCM)                      
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

q=0
GPIO.setup(12,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)                  
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(25,GPIO.OUT)

pwm=GPIO.PWM(25,50)
pwm.start(5)
DutyCycle = 1/18* (q) + 2
pwm.ChangeDutyCycle(DutyCycle)
lines = [[(0, 1), (3, 3)], [(0, 1), (7, 9)], [(0, 1), (8, 7)]]

for i in range (0, 36):

    GPIO.output(TRIG, False)                 
    print ("Waitng For Sensor To Settle")
    time.sleep(1)

    print ("Distance measurement in progress")

    GPIO.output(TRIG, True)                  
    time.sleep(0.00001)                      
    GPIO.output(TRIG, False)                 

    while GPIO.input(ECHO)==0:               
        pulse_start = time.time()            
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()               

    pulse_duration = pulse_end - pulse_start 

    distance = pulse_duration * 17150        
    distance = round(distance, 2)            

    if distance > 2 and distance < 400:      
        print ("Distance:",distance - 0.5,"cm")
    else:
        print ("Out Of Range")
    a=math.cos(math.radians(q))*distance
    b=math.sin(math.radians(q))*distance
    q=q+.8
    if (q>180):
        q=0

    lines.append([(0, 1),(a,b)])
    c = [1, 0, 0, 1]
    i=i+1
    
print(lines)
aio.send('line segment', lines)
lc = mc.LineCollection(lines, colors=c, linewidths=0.5)


fig, ax = pl.subplots()


ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
fig.savefig('foo1.png')
time.sleep(1)
r=cv2.imread('foo1.png')
cv2.imshow('Mapped image',r)
    

Attachments 