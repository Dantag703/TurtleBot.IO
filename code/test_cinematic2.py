# We will do the imports required for this notebook here
# numpy provides import array and linear algebra utilities
import numpy as np
# the robotics toolbox provides robotics specific functionality
import roboticstoolbox as rtb
# spatial math provides objects for representing transformations
from scipy.spatial.transform import Rotation
import spatialmath as sm
# paho mqtt for mqtt broker conection
# from paho.mqtt import client as mqtt_client
# import random
# import json
broker = 'ze5a0a21.emqx.cloud'
port = 1883
topics_claw = '/turtlebot/arm/claw/set/'

# import serial


# topics_fkine = ['/turtlebot/arm/base/set/','/turtlebot/arm/shoulder/set/',
#                 '/turtlebot/arm/elbow1/set/','/turtlebot/arm/elbow/set/',
#                 '/turtlebot/arm/wrist/set/']

# topics_ikine = ['turtlebot/inverse/sliX/set','turtlebot/inverse/sliY/set',
#               'turtlebot/inverse/sliZ/set','turtlebot/inverse/sliR/set',
#               'turtlebot/inverse/sliP/set','turtlebot/inverse/sliYaw/set']

# topics_claw = ['/turtlebot/arm/claw/set/']

# client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'mqttpy'
# password = 'public'

# def connect_mqtt():
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT Broker!")
#         else:
#             print("Failed to connect, return code %d\n", rc)
#     # Set Connecting Client ID
#     client = mqtt_client.Client(client_id)
#     client.username_pw_set(username, password)
#     client.on_connect = on_connect
#     client.connect(broker, port)
#     return client

def mapear(numero_original):
    min_original = -150
    max_original = 150
    min_deseado =0
    max_deseado = 1023
    # Asegúrate de que el número original esté dentro del rango original
    numero_original = max(min_original, min(numero_original, max_original))
    # Calcula el número mapeado utilizando una regla de tres
    numero_mapeado = (numero_original - min_original) * (max_deseado - min_deseado) / (max_original - min_original) + min_deseado
    
    return int(np.round(numero_mapeado,0))

# def writedxl(qdxl):
#     dev = serial.Serial("COM3",57600)   
#     dev.flushInput()
#     for i in range(5):
#         print(qdxl[i])
#         cad = "dxl "+str(i+2)+" "+str(mapear(np.rad2deg(qdxl[i])))+"\n"
#         print(cad)
#         dev.write(cad.encode("ascii"))
#     dev.close() 
# # arm ET
E1 = rtb.ET.Rz()
E2 = rtb.ET.tz(0.085)
E3 = rtb.ET.Rx(-np.pi/2)
E4 = rtb.ET.Rz()
E41 = rtb.ET.Rz(np.pi/2)
E5 = rtb.ET.tx(-0.095)
E6 = rtb.ET.Rz()
E7 = rtb.ET.tx(-0.095)
E8 = rtb.ET.Rz()
E81 = rtb.ET.Rz(-np.pi/2)
E9 = rtb.ET.tx(-0.025)
E10 = rtb.ET.Rx(np.pi/2)
E11 = rtb.ET.Rz()
E12 = rtb.ET.tz(0.175)

arm = rtb.ETS([E1, E2, E3, E4, E41, E5, E6, E7, E8, E81, E9, E10, E11, E12])
arm.qlim = [[np.deg2rad(-150), np.deg2rad(-124), np.deg2rad(-138), np.deg2rad(-103), np.deg2rad(-150)],
 [ np.deg2rad(150),  np.deg2rad(128),  np.deg2rad(149),  np.deg2rad(101),  np.deg2rad(150)]]

dxl2,dxl3,dxl4,dxl5,dxl6 = 0,0,0,0,0
q0 = np.array([0, 0, 0, 0, 0])
q = np.array([np.deg2rad(150), np.deg2rad(90), 0, 0, 0])
qdxl = np.array([np.deg2rad(dxl2), np.deg2rad(dxl3), np.deg2rad(dxl4), np.deg2rad(dxl5), np.deg2rad(dxl6)])
# writedxl(qdxl)
Tep = arm.fkine(qdxl)

x = np.round(Tep.t[0]*100,2)
y = np.round(Tep.t[1]*100,2)
z = np.round(Tep.t[2]*100,2)
print(f"The fkine method: \n{Tep}")
print(f"X: {x} cm")
print(f"Y: {y} cm")
print(f"Z: {z} cm")
R = Tep.R
r = Rotation.from_matrix(R)
# Extract the roll, pitch, and yaw angles
roll, pitch, yaw = np.round(r.as_euler('zyx', degrees=True),4) # 'zyx' specifies the order of rotations
print(f"Roll: {roll} degrees")
print(f"Pitch: {pitch} degrees")
print(f"Yaw: {yaw} degrees")

Etz = rtb.ET.tz(z/100).A()
Ety = rtb.ET.ty(y/100).A()
Etx = rtb.ET.tx(x/100).A()
Erz = rtb.ET.Rx(np.deg2rad(roll)).A()
Ery = rtb.ET.Ry(np.deg2rad(pitch)).A()
Erx = rtb.ET.Rz(np.deg2rad(yaw)).A()


Tep2 = Etx @ Ety @ Etz @ Erz @ Ery @ Erx
print(f"The fkine method: \n{np.round(Tep2,4)}")
print("inverse")
inv = arm.ik_NR(Tep2,q0)
if inv[1] == 1:
    print(inv)
    qdxl = inv[0]
    dxl2 = np.round(np.rad2deg(qdxl[0]),3)
    dxl3 = np.round(np.rad2deg(qdxl[1]),3)
    dxl4 = np.round(np.rad2deg(qdxl[2]),3)
    dxl5 = np.round(np.rad2deg(qdxl[3]),3)
    dxl6 = np.round(np.rad2deg(qdxl[4]),3)
    print(f"The ikine method NR: \n q0:{dxl2} q1:{dxl3} q2:{dxl4} q3:{dxl5} q4:{dxl6}")
else:
    inv = arm.ik_GN(Tep2,q0)
    if inv[1] == 1:
        print(inv)
        qdxl = inv[0]
        dxl2 = np.round(np.rad2deg(qdxl[0][0]),3)
        dxl3 = np.round(np.rad2deg(qdxl[0][1]),3)
        dxl4 = np.round(np.rad2deg(qdxl[0][2]),3)
        dxl5 = np.round(np.rad2deg(qdxl[0][3]),3)
        dxl6 = np.round(np.rad2deg(qdxl[0][4]),3)
        print(f"The ikine method GN: \n q0:{dxl2} q1:{dxl3} q2:{dxl4} q3:{dxl5} q4:{dxl6}")
    else:
        inv = arm.ik_LM(Tep2,q0)
        if inv[1] == 1:
            print(inv)
            qdxl = inv[0]
            dxl2 = np.round(np.rad2deg(qdxl[0][0]),3)
            dxl3 = np.round(np.rad2deg(qdxl[0][1]),3)
            dxl4 = np.round(np.rad2deg(qdxl[0][2]),3)
            dxl5 = np.round(np.rad2deg(qdxl[0][3]),3)
            dxl6 = np.round(np.rad2deg(qdxl[0][4]),3)
            print(f"The ikine method LM: \n q0:{dxl2} q1:{dxl3} q2:{dxl4} q3:{dxl5} q4:{dxl6}")
        else:
            print("cant solve")




# def subscribe(client: mqtt_client):
#     def on_message(client, userdata, msg):
#         print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
#         if msg.topic in topics_fkine:
#             pos = topics_fkine.index(msg.topic)
#             qdxl[pos] = np.deg2rad(float(msg.payload.decode()))
#             Tep = arm.fkine(qdxl)
#             x = np.round(Tep.t[0]*100,2)
#             y = np.round(Tep.t[1]*100,2)
#             z = np.round(Tep.t[2]*100,2)
#             client.publish('/turtlebot/inverse/posX/get/',x ,qos=1)
#             client.publish('/turtlebot/inverse/posY/get/',y ,qos=1)
#             client.publish('/turtlebot/inverse/posZ/get/',z ,qos=1)
#             R = Tep.R
#             r = Rotation.from_matrix(R)
#             # Extract the roll, pitch, and yaw angles
#             roll, pitch, yaw = np.round(r.as_euler('zyx', degrees=True),2)  # 'zyx' specifies the order of rotations
#             client.publish('/turtlebot/inverse/posR/get/',roll ,qos=1)
#             client.publish('/turtlebot/inverse/posP/get0/',pitch ,qos=1)
            
#             client.publish('/turtlebot/inverse/posYaw/get/',yaw ,qos=1)
#             writedxl(qdxl)
#             goal = mapear(int(msg.payload.decode()))
#             qdxl_json = qdxl.tobytes()
#             # Publica el array en el tema MQTT
#             client.publish('/turtlebot/arm/array', qdxl_json ,qos=1)  
#             print(qdxl)
#             print(f"The fkine method: \n{Tep}")
#             print(f"X: {x} cm")
#             print(f"Y: {y} cm")
#             print(f"Z: {z} cm")
#             print(f"Roll: {roll} degrees")
#             print(f"Pitch: {pitch} degrees")
#             print(f"Yaw: {yaw} degrees")
#             print(f"The ikine method: \n q0:{qdxl[0]} q1:{qdxl[1]} q2:{qdxl[2]} q3:{qdxl[3]} q4:{qdxl[4]}")
#         if msg.topic in topics_ikine:
#             pos = topics_ikine.index(msg.topic)
#             qdxl[pos] = float(msg.payload.decode())
#             Tep = arm.fkine(qdxl)
#             goal = mapear(int(msg.payload.decode()))
#         if msg.topic in topics_claw:
#             dev = serial.Serial("COM3",57600)   
#             dev.flushInput()
#             cad = "dxl "+str(7)+" "+str(mapear(int(msg.payload.decode())))+"\n"
#             print(cad)
#             dev.write(cad.encode("ascii"))
#             dev.close() 
            
        

#     for topic in topics_fkine:
#         client.subscribe(topic, qos=1)
#     for topic in topics_ikine:
#         client.subscribe(topic, qos=1)
#     for topic in topics_claw:
#         client.subscribe(topic, qos=1)
#     client.on_message = on_message


# def run():
#     client = connect_mqtt()
#     subscribe(client)
#     client.loop_forever()
    

# if __name__ == '__main__':
#     run()
      