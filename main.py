
from flask import request, make_response, redirect, render_template, session, send_from_directory, jsonify, Response, stream_with_context
from flask_login import login_required, current_user
from app import create_app
from flask_mqtt import Mqtt
import numpy as np
import matplotlib.pyplot as plt 
global start_time, start_time2, start_time3, start_time4, frame_count, frame_count2, frame_count3, frame_count4, last_frame, last_frame2, last_frame3, last_frame4, posX, posY, posZ, posR, posP, posYaw, q1, q2, q3, q4, q5, q6,w1,w2
import threading
import time
# cinematic variables
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
# wheels data variables
w1 = 0
w2 = 0
# Initialize Frames
lock = threading.Lock()
last_frame = None
last_frame2 = None
last_frame3 = None
last_frame4 = None
frame_count = 0
frame_count2 = 0
frame_count3 = 0
frame_count4 = 0
start_time = time.time()
start_time2 = time.time()
start_time3 = time.time()
start_time4 = time.time()
# Create app
app = create_app()
topics = ['/turtlebot/camera/', '/turtlebot/camera2/', '/turtlebot/camera3/','/turtlebot/camera4/']
mqtt_client = Mqtt(app)
last_frame = None

# Route to subscribe and conect to MQTT broker
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully to mqtt')
        for topic in topics:
            mqtt_client.subscribe(topic, qos=1)  # subscribe topic

    else:
        print('Bad connection. Code:', rc)

# Route read MQTT Topics
def subscribe_to_topics_and_handle_messages():
    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        global start_time, start_time2, start_time3, start_time4, frame_count, frame_count2, frame_count3, frame_count4, last_frame, last_frame2, last_frame3, last_frame4
        if message.topic == '/turtlebot/camera/':
            last_frame = message.payload
            frame_count += 1 
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                fps = frame_count / elapsed_time
                print("Frames per second:", fps)
                print("Frames:", frame_count)
                # Reset counters
                frame_count = 0
                start_time = time.time()
        elif message.topic == '/turtlebot/camera2/':
            last_frame2 = message.payload
            frame_count2 += 1 
            elapsed_time2 = time.time() - start_time2
            if elapsed_time2 >= 1:
                fps2 = frame_count2 / elapsed_time2
                print("Frames per second:", fps2)
                print("Frames:", frame_count2)
                # Reset counters
                frame_count2 = 0
                start_time2 = time.time()
        elif message.topic == '/turtlebot/camera3/':
            last_frame3 = message.payload
            frame_count3 += 1 
            elapsed_time3 = time.time() - start_time3
            if elapsed_time3 >= 1:
                fps3 = frame_count3 / elapsed_time3
                print("Frames per second:", fps3)
                print("Frames:", frame_count3)
                # Reset counters
                frame_count3 = 0
                start_time3 = time.time()
        elif message.topic == '/turtlebot/camera4/':
            last_frame4 = message.payload
            frame_count4 += 1 
            elapsed_time4 = time.time() - start_time4
            if elapsed_time4 >= 1:
                fps4 = frame_count4 / elapsed_time4
                print("Frames per second:", fps4)
                print("Frames:", frame_count4)
                # Reset counters
                frame_count4 = 0
                start_time4 = time.time()
        else:
            data = dict(
                topic=message.topic,
                payload=message.payload.decode()
            )
            print(
                'Received message on topic: {topic} with payload: {payload}'.format(**data))

# route tu publish MQTT Topics
@app.route('/publish', methods=['POST'])
def publish_message():
    request_data = request.get_json()
    print(request_data)
    publish_result = mqtt_client.publish(
        request_data['topic'], request_data['msg'])
    return jsonify({'code': publish_result[0]})

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

def generate_frames2():
    while True:
        if last_frame is not None:
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + last_frame2 + b'\r\n')
    
def generate_frames3():
    while True:
        if last_frame is not None:
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + last_frame3 + b'\r\n')

def generate_frames4():
    while True:
        if last_frame is not None:
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + last_frame4 + b'\r\n')

@app.route('/video_feed')
def video_feed():
    with lock:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    with lock:
        return Response(generate_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed3')
def video_feed3():
    with lock:
        return Response(generate_frames3(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed4')
def video_feed4():
    with lock:
        return Response(generate_frames4(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
    mqtt_thread = threading.Thread(target=subscribe_to_topics_and_handle_messages)
    mqtt_thread.start()
    app.run(port=8080, debug=True)
