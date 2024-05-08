import unittest
from flask import request, make_response, redirect, render_template, session, send_from_directory, jsonify, Response, stream_with_context, url_for, request
from flask_login import login_required, current_user
from app import create_app
from app.lecturaSerial import moveArm
import cv2 as cv
import numpy as np
global omega,lV ,w1,w2,fps, fps2, fps3, fps4, start_time, start_time2, start_time3, start_time4, frame_count, frame_count2, frame_count3, frame_count4, last_frame, last_frame2, last_frame3, last_frame4, posX, posY, posZ, posR, posP, posYaw, q1, q2, q3, q4, q5, q6
from app.cinematicLocal import fkine, ikine, fwkine
import requests
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
last_frame = None

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
    video = cv.VideoCapture(0)
    while True:
        try:
            ret, frame = video.read()
            if not ret:
                last_frame = None
            _, buffer = cv.imencode('.jpeg', frame)
            frame_bytes = buffer.tobytes()
            last_frame = frame_bytes
        except:
            video.release()
            last_frame = None
        if last_frame is not None:
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + last_frame + b'\r\n')


@app.route('/publishF', methods=['POST'])
def publish_message():
    global posX,posY,posZ,posR,posP,posYaw
    global q1,q2,q3,q4,q5,q6
    request_data = request.get_json()
    # msg = request_data['msg']
    # qdxl = msg.split()
    # print(qdxl)
    # q1,q2,q3,q4,q5,q6 = [float(x) for x in qdxl]
    
    print(request_data)
    # moveArm(request_data)
    posX,posY,posZ,posR,posP,posYaw = fkine(request_data)
    print (posX,posY,posZ,posR,posP,posYaw)
    response = make_response(redirect('/get_label_value'))
    return response

@app.route('/publishFW', methods=['POST'])
def publishFW_message():
    global omega,lV,w1,w2
    request_data = request.get_json()
    msg = request_data['data']
    wdxl = msg.split()
    print(f'wdxl: {wdxl}')
    w1,w2 = [float(x) for x in wdxl]
    omega,V = fwkine(w1,w2)
    print(f'iwdxl: {omega,lV}')
    response = make_response(redirect('/get_label_value'))
    return response

@app.route('/publishI', methods=['POST'])
def publishI_message():
    global posX,posY,posZ,posR,posP,posYaw
    global q1,q2,q3,q4,q5,q6
    request_data = request.get_json()
    msg = request_data['data']
    inv = msg.split()
    print()
    inv = [float(x) for x in inv]
    print(request_data)
    q1,q2,q3,q4,q5,q6 = ikine(request_data,q1,q2,q3,q4,q5,q6)
    print (q1,q2,q3,q4,q5,q6)
    msg = str(q1)+' '+str(q2)+' '+str(q3)+' '+str(q4)+' '+str(q5)+' '+str(q6)
    response = make_response(redirect('/get_label_value'))
    return response

@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
    app.run(port=8080, debug=True)
