import serial
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Connection to serial port
ser = serial.Serial("/dev/rfcomm0", 9600)
# Callback for what to do on connect
def on_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    if(int(rc) == 0):
        print("Connection successful.")
        client.subscribe("instruction")
    else:
        print(f"Connection was not successful. Exit code: {str(rc)}")
# Callback for what to do on message
def on_message(client, userdata, msg):
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
# Method to relay instructions via a thread callback.
def createclient(port):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("3.25.144.105", 1883, 60)
    client.loop_forever()
# Method to deliver data to mqtt on aws via a thread callback
def lookfordata(port):
    ser.write(str.encode('Start\r\n'))
    while True:
        if ser.in_waiting > 0:
            rawserial = ser.readline()
            cookedserial = rawserial.decode('utf-8').strip('\r\n')
            humidity, temp, hic, moisture = cookedserial.split(';')
            
            publish.single("Data", f'Current Temperature is {temp} Celsius \n Humidity is at {humidity} % \n Moisture at sensor is {moisture}', hostname="3.25.144.105")
# Starting 2 threads with lookforadta & createclient
import threading
t1 = threading.Thread(target = lookfordata, args = [ser])
t2 = threading.Thread(target = createclient, args = [ser])
t1.start()
t2.start()

# publish.single("Temperature", temp, hostname="ec2-3-25-144-105.ap-southeast-2.compute.amazonaws.com")
            # publish.single("Humidity", humidity, hostname="ec2-3-25-144-105.ap-southeast-2.compute.amazonaws.com")
            # publish.single("Moisture", moisture, hostname="ec2-3-25-144-105.ap-southeast-2.compute.amazonaws.com")