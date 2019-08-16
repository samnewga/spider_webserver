from picamera import PiCamera
from picamera.array import PiRGBArray
from imutils.video import VideoStream
from multiprocessing import Process,Queue,Pipe
from time import sleep
import math
import argparse
import datetime
import warnings
import imutils
import time
import cv2
import json
#import threading
#import thread
import sys
import random
import RPi.GPIO as GPIO
import numpy as np
import sys

Motor1A = 22
Motor1B = 23
Motor1E = 25
Motor2A = 19
Motor2B = 26
Motor2E = 13
GPIO.setmode(GPIO.BCM) 
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)
pwm = GPIO.PWM(13, 100)
test = 5 
GPIO.setmode(GPIO.BCM)
TRIG = 4
ECHO = 18
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
def forward():
    print("Forward")
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    sleep(5)
    GPIO.output(Motor1E, GPIO.LOW)

def turn():
    print("Turning")
    pwm.start(45)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)
    sleep(2)
    pwm.stop()
    GPIO.output(Motor2E, GPIO.LOW)

def backward():
    print("Backwards")
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    sleep(5)
    GPIO.output(Motor1E, GPIO.LOW)
def turn2():
    print("Turning 2")
    pwm.start(45)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)
    GPIO.output(Motor2E, GPIO.HIGH)
    sleep(2)
    pwm.stop()
    GPIO.output(Motor2E, GPIO.LOW)
def end():
    print("Turning 2")
    GPIO.cleanup()
def measure(GPIO,ECHO,TRIG):
    end = 0
    start = 0
    loop = True
    GPIO.output(TRIG,True)
    time.sleep(0.0001)
    GPIO.output(TRIG,False)
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    while loop == True:
        if GPIO.input(ECHO) == False:
            print("Time started")
            start = time.time()
            print(start)
        if GPIO.input(ECHO) == True:
            print("Time ended")
            end = time.time()
            print(end)
            loop = False
    sig_time = ((end-start)*34300)/2
    #less than 5
    if sig_time > 5:
        return True
    if sig_time < 5:
        return False
    print(sig_time)
def MachineLearning(camera,left,right,test):
    t = 1
    w1 = .8
    mf = w1 * int(camera[0]) * t
    #mt = w2 *EchoDist * t
    if mf <= left:
        turn()
    elif mf >= right:
        turn2()
    else:
        forward()
    return 0
def MachineLearning2(camera,left,right):
    f = 1
    w2 = .5
    mt = w2 *EchoDist * f
    #if mf <= left:
        #print('left')
    #elif mf >= right:
        #print('right')
    #else:
        #print('forward')
def photo():
    test = 5 
    GPIO.setmode(GPIO.BCM)
    TRIG = 4
    ECHO = 18
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    holder = []
    # Warms up camera and grabs reference to raw camera capture
    vs = PiCamera()
    vs.resolution = tuple([640,480])
    vs.framerate = 30
    raw = PiRGBArray(vs,size = tuple([640,480]))
    time.sleep(2.5)
    for f in vs.capture_continuous(raw, format = "bgr", use_video_port = True):
        end = 0
        while True:
            end = end + 1
        #Store each frame
            frame = f.array
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(5,5),0)
            thresh = cv2.threshold(gray,45,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
            thresh = cv2.medianBlur(thresh,5)
            erode = cv2.erode(thresh,(15,15),iterations =1)
            dilate = cv2.dilate(erode,(15,15),iterations = 1)
            edges = cv2.Canny(dilate,50,150,apertureSize = 3)
            raw.truncate(0)
            contours,hierarchy = cv2.findContours(edges.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            #print(contours)
            try:
                c = max(contours,key = cv2.contourArea)
                furthest = tuple(c[c[:,:,1].argmin()][0])
            except:
                cv2.waitKey(1) & 0xFF
            raw.truncate(0)
            mid_x = int((frame.shape[1])/2)
            left = int(mid_x - 100)
            right = int(mid_x + 100)
            toclose = measure(GPIO,ECHO,TRIG)
            if toclose == False:
                test = MachineLearning(furthest,left,right,test)
                cv2.drawContours(frame,contours,-1,(0,255,0),3)
            else:
                turn()
                forward()
            cv2.imshow('test',frame)
            key = cv2.waitKey(1) & 0xFF
            if end == 5:
                sys.exit()
            
while True:            
    photo()
