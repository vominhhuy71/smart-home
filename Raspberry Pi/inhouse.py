import requests
import json
import time
import i2clcd
import I2C_LCD_driver
from time import sleep
from gpiozero import Button, LED
import os

#bedLight
led1 = LED(17)
btn1 = Button(16)
#livingRoomLight
led2 = LED(27)
btn2 = Button(20)

lcd = I2C_LCD_driver.lcd()
#my_lcd = i2clcd.i2clcd(i2c_bus=1,i2c_addr=0x27,lcd_width=16)
    

def toggle_bedLight():
    requests.put('http://46.101.183.30:5000/info/lights/bedLight',data = None)
def toggle_lvLight():
    requests.put('http://46.101.183.30:5000/info/lights/lvLight',data = None)

ds18b20 = ''

def setup():
    global ds18b20
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
setup()


while True:
    #Get temperature
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    data = {"temp":round(temperature,2)}
    put_data = json.dumps(data)
    headers = {'content-type': 'application/json'}
    print(put_data)
    put_temp = requests.put('http://46.101.183.30:5000/info/thermistor',data = put_data,headers = headers)
    #Display temperature
    get_temp = requests.get('http://46.101.183.30:5000/info/thermistor')
    temp=get_temp.json()
    output = str(temp['value'])+' Celsius.'
    lcd.lcd_display_string('Temperature:',1,0)
    lcd.lcd_display_string(output,2,0)
    #my_lcd.print_line('Indoor:',line=0)
    #my_lcd.print_line(output,line=1)
    get_response = requests.get('http://46.101.183.30:5000/info/lights')
    lights = get_response.json()
    bedLight = None
    lvLight = None
    for light in lights:
        if light['name'] == 'bedLight':
            bedLight = light['value']
            #print(light['name'])
            #print(light['value'])
        if light['name'] == 'lvLight':
            lvLight = light['value']
            #print(light['name'])
            #print(light['value'])
    if lvLight == True:
        led2.on()
    else:
        led2.off()
    if bedLight == True:
        led1.on()
    else:
        led1.off()
    
    btn1.when_pressed=toggle_bedLight
    btn2.when_pressed=toggle_lvLight
    sleep(5)