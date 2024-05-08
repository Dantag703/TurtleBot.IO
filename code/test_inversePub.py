# Importing Libraries
from paho.mqtt import client as mqtt_client
import time
import random
# Raspberry PI IP address
broker = 'ze5a0a21.emqx.cloud'
port = 1883
topic = '/turtlebot/inverse/posX/get/'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'mqttpy'
password = 'public'

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

# Object to capture the frames


# Phao-MQTT Clinet

def run():
    client = connect_mqtt()
    client.loop_start()
    while True :
        randomV = random.randint(0, 10) 
        client.publish(topic, randomV, qos=1)
        print("publish " + topic + " " + str(randomV))


if __name__ == '__main__':
    run()
