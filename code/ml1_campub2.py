# Importing Libraries
from paho.mqtt import client as mqtt_client
import base64
import time
import random
import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt 
from torchvision import transforms
global last_frame, start_time, start_time2, frame_count

last_frame = None
start_time = time.time()
start_time2 = time.time()
frame_count = 0
# MQTT Broker configuration
broker = 't6b406cc.ala.dedicated.aws.emqxcloud.com'
port = 1883
topic_sub = '/turtlebot/camera/3'
topic_pub = '/turtlebot/camera/4'
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

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
# import ML model
midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
midas.to(device)
midas.eval()
# import ML transforms
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform 
print('modelos cargados')

# setup the frames to export to the mqtt
def send_frame_to_mqtt(frame,client,topic):
    _, buffer = cv2.imencode('.jpeg', frame)
    frame_bytes = buffer.tobytes()
    client.publish(topic, frame_bytes, qos=1)

# decode mqtt frame, transform, predict and publish frame with ML
def generate_ml_frames(client,topic):
    if last_frame is not None:
        img = cv2.imdecode(np.frombuffer(last_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgbatch = transform(img).to(device)

        # Make a prediction
        with torch.no_grad(): 
            prediction = midas(imgbatch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size = img.shape[:2], 
                mode='bicubic', 
                align_corners=False
            ).squeeze()

            output = prediction.cpu().numpy()
        # Escalar y convertir a RGB
        output_rgb = (output - np.min(output)) / (np.max(output) - np.min(output))
        frame = np.uint8(plt.cm.magma(output_rgb) * 255)

        send_frame_to_mqtt(frame,client,topic)
        print

# Function to subscribe to MQTT topics and define actions upon receiving messages
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if msg.topic == '/turtlebot/camera3/':
            global last_frame, frame_count, start_time2
            start_time = time.time()
            last_frame = msg.payload
            generate_ml_frames(client,topic_pub)
            # Calcular el tiempo de espera para mantener la tasa de fps
            end_time = time.time()
            frame_time = end_time - start_time
            if frame_time < 1/10:
                time.sleep(1/10 - frame_time)
                generate_ml_frames(client,topic_pub)
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
    # part where it subscribes to mqtt topics                    
    client.subscribe(topic_sub, qos=1)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
