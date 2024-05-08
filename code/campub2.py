# Importing Libraries
import cv2 as cv
from paho.mqtt import client as mqtt_client
import base64
import time
import random
# Raspberry PI IP address
broker = 't6b406cc.ala.dedicated.aws.emqxcloud.com'
port = 1883
topic = "/turtlebot/camera/3"
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

# setup the frames to export to the mqtt
def send_frame_to_mqtt(frame,client,topic):
    _, buffer = cv.imencode('.jpeg', frame)
    frame_bytes = buffer.tobytes()
    client.publish(topic, frame_bytes, qos=1)

# Object to capture the frames
video = cv.VideoCapture(0)

# fuction to conect the camera and send the frames
def capture_and_publish(client):
    start_time2 = time.time()
    frame_count = 0
    while True:
        start_time = time.time()

        # Capturar un frame
        ret, frame = video.read()
        if not ret:
            break

        # Enviar el frame a MQTT
        

        # Calcular el tiempo de espera para mantener la tasa de fps
        end_time = time.time()
        frame_time = end_time - start_time
        if frame_time < 1/10:
            time.sleep(1/10 - frame_time)
            send_frame_to_mqtt(frame, client, topic)
            #print("hola: ",frame_time)
            frame_count += 1 
            elapsed_time = time.time() - start_time2
            if elapsed_time >= 1:
                fps = frame_count / elapsed_time
                print("Frames per second:", fps)
                print("Frames:", frame_count)
                # Reset counters
                frame_count = 0
                start_time2 = time.time()

        
def run():
    client = connect_mqtt()
    client.loop_start()
    capture_and_publish(client)


if __name__ == '__main__':
    run()