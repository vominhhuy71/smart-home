from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from time import sleep
from gpiozero import MotionSensor, Button, TonalBuzzer
import requests
import json
import os.path
from mfrc522 import SimpleMFRC522


pir = MotionSensor(23)
camera = PiCamera()
reader = SimpleMFRC522()
btn = Button(16)  
bz = TonalBuzzer(17)
notify = False #Notify that the door is unlocked

def pressed():
    lock1_response = requests.put('http://localhost:5000/info/security/haveKey',data=None)
    lock1_response = requests.put('http://localhost:5000/info/security/haveMotion',data=None)
    bz.play("A4")
    time.sleep(1)
    bz.stop()
    notify = False
    print("The house is protected!")
    
def authenticate():
    get_keys= requests.get('http://localhost:5000/info/security/keys')
    keys=get_keys.json()
    id, text = reader.read_no_block()
    for member in keys:
         if member['key'] == id:
             print("Welcome home!")
             return True
    return False

while True:
    bz.stop()
    get_response = requests.get('http://localhost:5000/info/security')
    security=get_response.json()
    haveKey = None
    haveMotion = None
    for member in security:
        if member['name'] == 'haveKey':
            haveKey = member['value']
        if member['name'] == 'haveMotion':
            haveMotion = member['value']
    print("Have key: ",haveKey)
    print("Have motion: ",haveMotion)
    #Security mode
    if ((haveKey == False) and (haveMotion == False)):
        #Make have Motion true
        if pir.motion_detected:
            put_motion = requests.put('http://localhost:5000/info/security/haveMotion',data=None)
            print("Motion detected!")
            notify = False
    elif ((haveMotion==True) and (haveKey == False)):
        print("Motion detected!")
        bz.play("C4")
        filename = "/home/pi/Desktop/SmartHome/images/" + (time.strftime("%y%b%d_%H:%M:%S")) + ".jpg"
        camera.capture(filename)
        #result = authenticate()
        get_keys= requests.get('http://localhost:5000/info/security/keys')
        keys=get_keys.json()
        
        status, TagType = reader.read_no_block()
        if status == None:
            continue
        else:
            id, text = reader.read()
            bz.play("A4")
            for member in keys:
                if member['key'] == id:                   
                    key_response = requests.put('http://localhost:5000/info/security/haveKey',data=None)
                    bz.stop()

    elif ((haveKey == True) and (haveMotion == True)):
        if notify == False:
            print("Welcome home!")
            bz.play("A4")
            sleep(1)
            bz.stop()
            notify = True
            
        #btn.when_pressed=pressed
        if btn.is_pressed:
            lock1_response = requests.put('http://localhost:5000/info/security/haveKey',data=None)
            lock1_response = requests.put('http://localhost:5000/info/security/haveMotion',data=None)
            bz.play("A4")
            sleep(1)
            bz.stop()
            notify = False
            print("The house is protected!")
            sleep(10)
    elif ((haveKey == True) and (haveMotion == False)):
        response = requests.put('http://localhost:5000/info/security/haveMotion',data=None)  
    sleep(5)
            
        
        
    