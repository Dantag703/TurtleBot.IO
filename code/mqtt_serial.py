import numpy as np
import serial
import time
from paho.mqtt import client as mqtt_client
import random

# MQTT Broker configuration
broker = 't6b406cc.ala.dedicated.aws.emqxcloud.com'
port = 1883
topics_set = ['/turtlebot/set/#', '/turtlebot/get/arm/1']
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'mqttpy'
password = 'public'
com = 'COM3'

# Function to connect to the MQTT broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Function to map a value from one range to another
def mapear(numero_original, min_deseado, max_deseado):
    min_original = 0
    max_original = 100
    numero_original = max(min_original, min(numero_original, max_original))
    numero_mapeado = (numero_original - min_original) * (max_deseado - min_deseado) / (max_original - min_original) + min_deseado
    return numero_mapeado

# function to decode mqtt message, get actual position of the arm and 
# create a soft trayectory to reach the final point
def arm_trayectory(msg):
    fdxl = msg.payload.decode()
    fdxl = [np.deg2rad(float(x)) for x in fdxl]
    print('final '+fdxl)
    dev = serial.Serial(com, 57600, timeout=1000)
    dev.flushInput()   
    cad2="read"
    dev.write(cad2.encode("ascii"))
    time.sleep(1)
    print("reading")
    serRead = dev.readline()
    print(serRead)
    decodeRead = serRead.decode('utf-8').strip()
    innitPos = decodeRead.split()
    idxl = [int(pos) for pos in innitPos[:6]]
    print('init '+idxl)
    fdxl = msg.payload.decode()
    fdxl = [np.deg2rad(float(x)) for x in fdxl]
    fdxl = list(map(lambda x: np.deg2rad(float(x)), fdxl))

    while any([idxl[i] != fdxl[i] for i in range(6)]):
        print("entro al while")
        for i, id_motor in enumerate(idxl, start=2):
            if idxl[i-2] != fdxl[i-2]:
                if fdxl[i-2] > idxl[i-2]:
                    idxl[i-2] += 1
                else:
                    idxl[i-2] -= 1

                dev = serial.Serial(com, 57600)
                dev.flushInput()
                cad = f"dxl {id_motor} {idxl[i-2]}\n"
                dev.write(cad.encode("ascii"))
                dev.close()
                time.sleep(0.1)

# Function to subscribe to MQTT topics and define actions upon receiving messages
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == '/turtlebot/set/arm':
           arm_trayectory(msg)
        elif msg.topic == '/turtlebot/set/wheels':
            speed = msg.payload.decode()
            speed = [int(x) for x in speed]
            dev = serial.Serial(com, 57600)
            dev.flushInput()
            cad = f"dxl 0 {speed[0]}\n"
            dev.write(cad.encode("ascii"))
            dev.close()
            dev = serial.Serial(com, 57600)
            dev.flushInput()
            cad = f"dxl 1 {speed[1]}\n"
            dev.write(cad.encode("ascii"))
            dev.close()
        elif msg.topic == '/turtlebot/get/arm/1':
            dev = serial.Serial(com, 57600, timeout=1000)
            dev.flushInput()   
            cad2="read"
            dev.write(cad2.encode("ascii"))
            time.sleep(1)
            print("reading")
            serRead = dev.readline()
            print(serRead)
        elif msg.topic == '/turtlebot/set/stab':
            pos = int(msg.payload.decode())
            dev = serial.Serial(com, 57600)
            dev.flushInput()
            cad = f"p 0 {pos}\n"
            dev.write(cad.encode("ascii"))
            dev.close()
    # part where it subscribes to mqtt topics                    
    for topic in topics_set:
        client.subscribe(topic, qos=0)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    

if __name__ == '__main__':
    run()