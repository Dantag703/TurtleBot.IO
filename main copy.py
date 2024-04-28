import unittest
from flask import request, make_response, redirect, render_template, session, send_from_directory, jsonify, Response, stream_with_context
from flask_login import login_required, current_user
from app import create_app
from flask_mqtt import Mqtt
import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt 
from torchvision import transforms
global last_frame, last_frame2, last_frame3, last_frame4, posX, posY, posZ, posR, posP, posYaw, q1, q2, q3, q4, q5, q6,w1,w2

midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
midas.to('cpu')
midas.eval()
# Input transformation pipeline
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform 
print('modelos cargados')
# inverse data variables
posX = 0
posY = 0
posZ = 0
posR = 0
posP = 0
posYaw = 0
# limbs data variables
q1 = 0
q2 = 0
q3 = 0
q4 = 0
q5 = 0
q6 = 0
#wheels data variables
w1 = 0
w2 = 0

app = create_app()
topics = ['/turtlebot/camera/', '/turtlebot/camera2/', '/turtlebot/camera3/','/turtlebot/camera4/']
mqtt_client = Mqtt(app)
last_frame = None


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully to mqtt')
        for topic in topics:
            mqtt_client.subscribe(topic, qos=1)  # subscribe topic

    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global last_frame, last_frame2, last_frame3, last_frame4
    if message.topic == '/turtlebot/camera/':
        last_frame = message.payload
    elif message.topic == '/turtlebot/camera2/':
        last_frame2 = message.payload
    elif message.topic == '/turtlebot/camera3/':
        last_frame3 = message.payload
    elif message.topic == '/turtlebot/camera4/':
        last_frame4 = message.payload
    else:
        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )
        print(
            'Received message on topic: {topic} with payload: {payload}'.format(**data))


@app.route('/publish', methods=['POST'])
def publish_message():
    request_data = request.get_json()
    print(request_data)
    publish_result = mqtt_client.publish(
        request_data['topic'], request_data['msg'])
    return jsonify({'code': publish_result[0]})

# Ruta para recibir el valor del slider y publicarlo en MQTT


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

@app.route('/get_fbx/<filename>')
def get_fbx(filename):
    return send_from_directory('static/models', filename)




@app.route("/")
@login_required
def index():
    user_ip = request.remote_addr

    response = make_response(redirect("/home"))
    session['user_ip'] = user_ip
    return response


def generate_frames():
    while True:
        if last_frame is not None:
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + last_frame + b'\r\n')

def generate_ml_frames():
    while True:
        if last_frame is not None:
            img = cv2.imdecode(np.frombuffer(last_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgbatch = transform(img).to('cpu')

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
            output_rgb = np.uint8(plt.cm.magma(output_rgb) * 255)
            _, buffer = cv2.imencode('.jpeg', output_rgb)
            frame_bytes = buffer.tobytes()
            last_ml_frame = frame_bytes
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + last_ml_frame + b'\r\n')


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_ml_feed')
def video_ml_feed():
    return Response(generate_ml_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    username = current_user.id
    
    context = {
        'username': username,
        'posX': posX,
        'posY': posY,
        'posZ': posZ,
        'posR': posR,
        'posP': posP,
        'posYaw': posYaw,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'q4': q4,
        'q5': q5,
        'q6': q6,
        'w1': w1,
        'w2': w2
    }

    return render_template('home.html', **context)

from flask import jsonify

@app.route('/get_label_value')
def get_label_value():
    return jsonify({ 
        'posX': posX,
        'posY': posY,
        'posZ': posZ,
        'posR': posR,
        'posP': posP,
        'posYaw': posYaw,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'q4': q4,
        'q5': q5,
        'q6': q6
    })


@app.route('/simulation', methods=['GET', 'POST'])
@login_required
def simulation():
    username = current_user.id

    context = {
        'username': username,
        'posX': posX,
        'posY': posY,
        'posZ': posZ,
        'posR': posR,
        'posP': posP,
        'posYaw': posYaw
    }

    return render_template('simulation.html', **context)




@app.route('/SLAM', methods=['GET', 'POST'])
@login_required
def SLAM():
    username = current_user.id

    context = {
        'username': username
    }

    return render_template('SLAM.html', **context)




@app.route('/machine-learning', methods=['GET', 'POST'])
@login_required
def machine_learning():
    username = current_user.id

    context = {
        'username': username
    }

    return render_template('machine-learning.html', **context)



if __name__ == "__main__":
    app.run(port=8080, debug=True)
