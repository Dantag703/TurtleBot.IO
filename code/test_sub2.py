from paho.mqtt import client as mqtt_client
import random

broker = 't6b406cc.ala.dedicated.aws.emqxcloud.com'
port = 1883
topics_set = ['/turtlebot/set/#', '/turtlebot/get/arm/1']

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

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    for topic in topics_set:
        client.subscribe(topic, qos=0)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    

if __name__ == '__main__':
    run()