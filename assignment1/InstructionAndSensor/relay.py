import serial
import time
import string
# reading and writing data from and to arduino serially.
# rfcomm0 -> this could be different
ser = serial.Serial("/dev/rfcomm0", 9600)


import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    print("Connection returned result: " + str(rc) )
    client.subscribe("instruction")

def on_message(client, userdata, msg): # Func for Sending msg
    # print(msg.topic+" "+str(msg.payload))
    print(f"Instruction {msg.payload.decode('UTF-8')} is being sent to teensy!")
    if(msg.payload.decode('UTF-8') == 'LED_ON'):
        print('Turning on')
        ser.write(str.encode('LED_ON'))
    elif(msg.payload.decode('UTF-8') == 'LED_OFF'):
        print('Turning off')
        ser.write(str.encode('LED_OFF'))
    elif(msg.payload.decode('UTF-8') == 'BUZZ'):
        print('Buzzing')
        ser.write(str.encode('BUZZ'))
        
def createclient(port):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("ec2-3-25-144-105.ap-southeast-2.compute.amazonaws.com", 1883, 60)
    client.loop_forever()

import paho.mqtt.publish as publish

def lookfordata(port):
    ser.write(str.encode('Start\r\n'))
    while True:
        if ser.in_waiting > 0:
            rawserial = ser.readline()
            cookedserial = rawserial.decode('utf-8').strip('\r\n')
            humidity, temp, hic, moisture = cookedserial.split(';')

            publish.single("Temperature", rawserial, hostname="ec2-3-25-144-105.ap-southeast-2.compute.amazonaws.com")
            publish.single("Humidity", humidity, hostname="ec2-3-25-144-105.ap-southeast-2.compute.amazonaws.com")
            publish.single("Moisture", moisture, hostname="ec2-3-25-144-105.ap-southeast-2.compute.amazonaws.com")


import threading

t1 = threading.Thread(target = lookfordata, args = [ser])
t2 = threading.Thread(target = createclient, args = [ser])
t1.start()
t2.start()