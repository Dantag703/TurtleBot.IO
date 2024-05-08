# We will do the imports required for this notebook here
# numpy provides import array and linear algebra utilities
import numpy as np
# the robotics toolbox provides robotics specific functionality
import roboticstoolbox as rtb
# spatial math provides objects for representing transformations
from scipy.spatial.transform import Rotation
import spatialmath as sm
# paho mqtt for mqtt broker conection
import math
import random
import json

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

def dinamic():# arm ET
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
    return arm

def fkine(request_data):
    msg = request_data['data']
    qdxl = msg.split()
    print(qdxl)
    qdxl = [np.deg2rad(float(x)) for x in qdxl]
    print(qdxl)
    arm = dinamic()
    # qdxl = np.array([np.deg2rad(float(dxl2)), np.deg2rad(float(dxl3)), np.deg2rad(dxl4), np.deg2rad(dxl5), np.deg2rad(dxl6)])
    Tep = arm.fkine(qdxl)
    posX = np.round(Tep.t[0]*100,0)
    posY = np.round(Tep.t[1]*100,0)
    posZ = np.round(Tep.t[2]*100,0)
    print(f"The fkine method: \n{Tep}")
    print(f"X: {posX} cm")
    print(f"Y: {posY} cm")
    print(f"Z: {posZ} cm")
    R = Tep.R
    r = Rotation.from_matrix(R)
    # Extract the roll, pitch, and yaw angles
    posR, posP, posYaw = np.round(r.as_euler('zyx', degrees=True),0) # 'zyx' specifies the order of rotations
    print(f"Roll: {posR} degrees")
    print(f"Pitch: {posP} degrees")
    print(f"Yaw: {posYaw} degrees")

    return posX,posY,posZ,posR,posP,posYaw

def invCalc(arm,Tep,q0):
    # Cartesion DoF priority matrix
    we = np.array([1.0, 1.0, 1.0, 0, 0, 0])
    # Maximum iterations allowed in a search
    ilimit = 30
    # Maximum searches allowed per problem
    slimit = 100
    # Solution tolerance
    tol = 1e-2
    methods = ['Newton Raphson (pinv=True):','Gauss Newton (pinv=True):','LM Wampler 1e-4:','LM Chan 0.1:','LM Sugihara 0.0001:']
    inv1 = arm.ik_NR(
            Tep=Tep,q0=q0,
            ilimit=ilimit,
            slimit=slimit,
            tol=tol,
            mask=we,
            pinv=True,
            joint_limits=True
        )
    print(methods[0])
    print(inv1)
    inv2 = arm.ik_GN(
            Tep=Tep,q0=q0,
            ilimit=ilimit,
            slimit=slimit,
            tol=tol,
            mask=we,
            pinv=True,
            joint_limits=True
        )
    print(methods[1])
    print(inv2)
    inv3 = arm.ik_LM(
            Tep=Tep,q0=q0,
            ilimit=ilimit,
            slimit=slimit,
            tol=tol,
            mask=we,
            k=1e-4,
            joint_limits=True,
            method="wampler"
        )
    print(methods[2])
    print(inv3)
    inv4 = arm.ik_LM(
            Tep=Tep,q0=q0,
            ilimit=ilimit,
            slimit=slimit,
            tol=tol,
            mask=we,
            k=0.1,
            joint_limits=True,
            method="chan"
        )
    print(methods[3])
    print(inv4)
    inv5 = arm.ik_LM(
            Tep=Tep,q0=q0,
            ilimit=ilimit,
            slimit=slimit,
            tol=tol,
            mask=we,
            k=0.0001,
            joint_limits=True,
            method="sugihara"
        )
    print(methods[4])
    print(inv5)
    valores = [inv1, inv2, inv3, inv4, inv5]
    valores_filtrados = [tupla for tupla in valores if tupla[1] == 1]
    if valores_filtrados:  # Verificar si hay tuplas que cumplan con la condición
        # Obtener el array con el mayor valor en la última posición
        mayor_valor = max(valores_filtrados, key=lambda x: x[-1])[0]
        # Asignar el array con el mayor valor en la última posición a la variable 'inv'
        inv = mayor_valor
        for i, tupla in enumerate(valores):
            if np.array_equal(tupla[0], mayor_valor):
                indice_original = i
                break
        # Imprimir el array con el mayor valor en la última posición
        print("la inversa es:", methods[indice_original])
    else:
        print("cant solve.")
        inv = q0
    return inv
    
def ikine(request_data,q1,q2,q3,q4,q5,q6):
    msg = request_data['data']
    posInv = msg.split()
    print(posInv)
    posInv = [float(x) for x in posInv]
    arm = dinamic()
    q0 = np.array([q1, q2,  q3, q4, q5])

    Etz = rtb.ET.tz(posInv[0]/100).A()
    Ety = rtb.ET.ty(posInv[1]/100).A()
    Etx = rtb.ET.tx(posInv[2]/100).A()
    Erz = rtb.ET.Rx(np.deg2rad(posInv[3])).A()
    Ery = rtb.ET.Ry(np.deg2rad(posInv[4])).A()
    Erx = rtb.ET.Rz(np.deg2rad(posInv[5])).A()
    Tep2 = Etx @ Ety @ Etz @ Erz @ Ery @ Erx
    print(f"The fkine method: \n{np.round(Tep2,4)}")
    print("inverse")
    qdxl = invCalc(arm,Tep2,q0)
    dxl2 = np.round(np.rad2deg(qdxl[0]),0)
    dxl3 = np.round(np.rad2deg(qdxl[1]),0)
    dxl4 = np.round(np.rad2deg(qdxl[2]),0)
    dxl5 = np.round(np.rad2deg(qdxl[3]),0)
    dxl6 = np.round(np.rad2deg(qdxl[4]),0)
    print(f"q0:{dxl2} q1:{dxl3} q2:{dxl4} q3:{dxl5} q4:{dxl6}")
    return dxl2,dxl3,dxl4,dxl5,dxl6,q6
            
def fwkine(w1,w2):
    fc = 0.299 * (2 * math.pi / 60)
    w1 = fc*w1
    w2 = -fc*w2

    R = 0.0325
    L = 0.16

    lV = R * (w1 + w2)/2
    omega = R * (w1 - w2)/L
    return np.round(lV,2), np.round(omega,2)
