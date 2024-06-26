import unittest
from flask import request, make_response, redirect, render_template, session, send_from_directory, jsonify, Response, stream_with_context
from flask_login import login_required, current_user
from app import create_app
from flask_mqtt import Mqtt
import numpy as np
import matplotlib.pyplot as plt 
global omega,lV ,w1,w2,fps, fps2, fps3, fps4, start_time, start_time2, start_time3, start_time4, frame_count, frame_count2, frame_count3, frame_count4, last_frame, last_frame2, last_frame3, last_frame4, posX, posY, posZ, posR, posP, posYaw, q1, q2, q3, q4, q5, q6
import threading
import time
import requests
from app.cinematicLocal import fkine, ikine, fwkine
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
omega= 0
lV = 0
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
fps = 0
fps2 = 0
fps3 = 0
fps4 = 0
start_time = time.time()
start_time2 = time.time()
start_time3 = time.time()
start_time4 = time.time()

# Create app
app = create_app()
topics = ['/turtlebot/camera/#']
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
        global start_time, start_time2, start_time3, start_time4, frame_count, frame_count2, frame_count3, frame_count4, last_frame, last_frame2, last_frame3, last_frame4, fps, fps2, fps3, fps4
        if message.topic == '/turtlebot/camera/1':
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
        elif message.topic == '/turtlebot/camera/2':
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
        elif message.topic == '/turtlebot/camera/3':
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
        elif message.topic == '/turtlebot/camera/4':
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


@app.route('/publishF', methods=['POST'])
def publishF_message():
    global posX,posY,posZ,posR,posP,posYaw
    global q1,q2,q3,q4,q5,q6
    request_data = request.get_json()
    msg = request_data['msg']
    qdxl = msg.split()
    print(qdxl)
    q1,q2,q3,q4,q5,q6 = [float(x) for x in qdxl]
    
    print(request_data)
    # moveArm(request_data)
    posX,posY,posZ,posR,posP,posYaw = fkine(request_data)
    print (posX,posY,posZ,posR,posP,posYaw)
    response = make_response(redirect('/get_label_value'))
    publish_result = mqtt_client.publish(
    request_data['topic'], request_data['msg'])
    print(jsonify({'code': request_data}))

    return response

@app.route('/publishFW', methods=['POST'])
def publishFW_message():
    global omega,lV,w1,w2
    request_data = request.get_json()
    msg = request_data['msg']
    wdxl = msg.split()
    print(f'wdxl: {wdxl}')
    w1,w2 = [float(x) for x in wdxl]
    omega,V = fwkine(w1,w2)
    print(f'iwdxl: {omega,lV}')
    response = make_response(redirect('/get_label_value'))
    publish_result = mqtt_client.publish(
    request_data['topic'], request_data['msg'])
    print(jsonify({'code': request_data}))
    return response

@app.route('/publishI', methods=['POST'])
def publishI_message():
    global posX,posY,posZ,posR,posP,posYaw
    global q1,q2,q3,q4,q5,q6
    request_data = request.get_json()
    msg = request_data['msg']
    inv = msg.split()
    print()
    inv = [float(x) for x in inv]
    print(request_data)
    q1,q2,q3,q4,q5,q6 = ikine(request_data,q1,q2,q3,q4,q5,q6)
    print (q1,q2,q3,q4,q5,q6)
    msg = str(q1)+' '+str(q2)+' '+str(q3)+' '+str(q4)+' '+str(q5)+' '+str(q6)
    response = make_response(redirect('/get_label_value'))
    publish_result = mqtt_client.publish(
    request_data['topic'], msg)
    print(jsonify({'code': request_data}))
    return response

@app.route('/publish', methods=['POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(
    request_data['topic'], request_data['msg'])
    return jsonify({'code': request_data})

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
        'q6': q6,
        'w1':w1,
        'w2':w2,
        'omega':omega,
        'lV':lV
    })

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    username = current_user.id
    label_url = request.url_root + 'get_label_value'
    label_response = requests.get(label_url)
    label_values = label_response.json()
    context = {
        'username': username,
        'posX': label_values['posX'],
        'posY': label_values['posY'],
        'posZ': label_values['posZ'],
        'posR': label_values['posR'],
        'posP': label_values['posP'],
        'posYaw': label_values['posYaw'],
        'q1': label_values['q1'],
        'q2': label_values['q2'],
        'q3': label_values['q3'],
        'q4': label_values['q4'],
        'q5': label_values['q5'],
        'q6': label_values['q6'],
        'w1': label_values['w1'],
        'w2': label_values['w2'],
        'omega': label_values['omega'],
        'lV': label_values['lV']
    }

    return render_template('home.html', **context)


@app.route('/simulation', methods=['GET', 'POST'])
@login_required
def simulation():
    username = current_user.id
    label_url = request.url_root + 'get_label_value'
    label_response = requests.get(label_url)
    label_values = label_response.json()
    context = {
        'username': username,
        'posX': label_values['posX'],
        'posY': label_values['posY'],
        'posZ': label_values['posZ'],
        'posR': label_values['posR'],
        'posP': label_values['posP'],
        'posYaw': label_values['posYaw'],
        'q1': label_values['q1'],
        'q2': label_values['q2'],
        'q3': label_values['q3'],
        'q4': label_values['q4'],
        'q5': label_values['q5'],
        'q6': label_values['q6'],
        'w1': label_values['w1'],
        'w2': label_values['w2'],
        'omega': label_values['omega'],
        'lV': label_values['lV']
    }

    return render_template('simulation.html', **context)

@app.route('/machine-learning', methods=['GET', 'POST'])
@login_required
def machine_learning():
    username = current_user.id

    context = {
        'username': username,
        'fps': fps,
        'fps2': fps2,
        'fps3': fps3,
        'fps4': fps4,
    }

    return render_template('machine-learning.html', **context)

if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=subscribe_to_topics_and_handle_messages)
    mqtt_thread.start()
    app.run(port=8080, debug=True)
