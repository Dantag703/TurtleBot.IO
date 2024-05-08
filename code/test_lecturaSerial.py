import pandas as pd
import numpy as np
import serial
import time

dev = serial.Serial("COM3", 57600, timeout=1000)
dev.flushInput()

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

# try:
# Recorre el DataFrame con un bucle for y un retraso de 100 milisegundos
#     cad="p 0 1"
# # t=40

#     dev.write(cad.encode("ascii"))

cad2="read"
dev.write(cad2.encode("ascii"))
time.sleep(1)
print("reading")
serRead = dev.readline()
print(serRead)
decodeRead = serRead.decode('utf-8').strip()
# print(decodeRead, end='')
innitPos = decodeRead.split()
dxl2 = int(innitPos[0])
dxl3 = int(innitPos[1])
dxl4 = int(innitPos[2])
dxl5 = int(innitPos[3])
dxl6 = int(innitPos[4])
dxl7 = int(innitPos[5])
print(str(dxl2)+" "+str(dxl3)+" "+str(dxl4)+" "+str(dxl5)+" "+str(dxl6)+" "+str(dxl7))
dev.close()
# topics_fkine = ['/turtlebot/arm/base/set/','/turtlebot/arm/shoulder/set/',
#             '/turtlebot/arm/elbow1/set/','/turtlebot/arm/elbow/set/',
#             '/turtlebot/arm/wrist/set/']

# topics_claw = ['/turtlebot/arm/claw/set/']

dxl2f = mapear(150)
dxl3f = mapear(100)
dxl4f = mapear(-100)
dxl5f = mapear(0)
dxl6f = mapear(0)
dxl7f = mapear(0)

dlxStr = str(dxl2f)+" "+str(dxl3f)+" "+str(dxl4f)+" "+str(dxl5f)+" "+str(dxl6f)+" "+str(dxl7f)


while dxl2!=dxl2f or dxl3!=dxl3f or dxl4!=dxl4f or dxl5!=dxl5f or dxl6!=dxl6f or dxl7!=dxl7f :
    print("entro al while")
    if  dxl2!=dxl2f:
        if dxl2f > dxl2:
            dxl2 += 1
        else: 
            dxl2 -=1
    if  dxl3!=dxl3f:
        if dxl3f > dxl3:
            dxl3 += 1
        else: 
            dxl3 -=1
    if  dxl4!=dxl4f:
        if dxl4f > dxl4:
            dxl4 += 1
        else: 
            dxl4 -=1
    if  dxl5!=dxl5f:
        if dxl5f > dxl5:
            dxl5 += 1
        else: 
            dxl5 -=1
    if  dxl6!=dxl6f:
        if dxl6f > dxl6:
            dxl6 += 1
        else: 
            dxl6 -=1
    if  dxl7!=dxl7f:
        if dxl7f > dxl7:
            dxl7 += 1
        else: 
            dxl7 -=1

    qdxl = np.array([dxl2,dxl3,dxl4,dxl5,dxl6,dxl7])
    dev = serial.Serial("COM3",57600)   
    dev.flushInput()
    for i in range(6):
        print(qdxl[i])
        cad = "dxl "+str(i+2)+" "+str(qdxl[i])+"\n"
        print(cad)
        dev.write(cad.encode("ascii"))
    dev.close()
    time.sleep(0.1)
print(dlxStr)

# ecept KeyboardInterrupt:
