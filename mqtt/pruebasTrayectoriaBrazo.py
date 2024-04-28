import pandas as pd
import numpy as np
import serial
import time

data = pd.read_csv('./nicolas_sapo.txt', delimiter=' ',names=["dxl2","dxl3","dxl4","dxl5","dxl6","dxl7","t"])
print(data.head(5))
# Guarda cada columna en variables individuales
dxl2 = data['dxl2']
dxl3 = data['dxl3']
dxl4 = data['dxl4']
dxl5 = data['dxl5']
dxl6 = data['dxl6']
dxl7 = data['dxl7']
tiempo = data['t']

dev = serial.Serial("COM3", 57600)
dev.flushInput()
# Rcorre el DataFrame con un bucle for y un retraso de 100 milisegundos
cad="p 0 1"
# t40
dev.write(cad.encode("ascii"))

    



for i in range(len(data)-1):
    valordxl2i = dxl2[i]
    valordxl3i = dxl3[i]
    valordxl4i = dxl4[i]
    valordxl5i = dxl5[i]
    valordxl6i = dxl6[i]
    valordxl7i = dxl7[i]
    t= tiempo[i]
    valordxl2f = dxl2[i+1]
    valordxl3f = dxl3[i+1]
    valordxl4f = dxl4[i+1]
    valordxl5f = dxl5[i+1]
    valordxl6f = dxl6[i+1]
    valordxl7f = dxl7[i+1]
    valordxl2 = valordxl2i
    valordxl3 = valordxl3i
    valordxl4 = valordxl4i
    valordxl5 = valordxl5i
    valordxl6 = valordxl6i
    valordxl7 = valordxl7i
    for j in range(t):
        print(str(int(valordxl2))+" "+str(int(valordxl3))+" "+str(int(valordxl4))+" "+str(int(valordxl5))+" "+str(int(valordxl6))+" "+str(int(valordxl7)))
        valordxl2 = (valordxl2 + (valordxl2f-valordxl2i)/t) 
        dev.write(cad.encode("ascii"))
        cad = "dxl 2 "+str(int(valordxl2))+"\n"
        valordxl3 = (valordxl3 + (valordxl3f-valordxl3i)/t)
        dev.write(cad.encode("ascii"))
        cad = "dxl 3 "+str(int(valordxl3))+"\n"
        valordxl4 = (valordxl4 + (valordxl4f-valordxl4i)/t)
        dev.write(cad.encode("ascii"))
        cad = "dxl 4 "+str(int(valordxl4))+"\n"
        valordxl5 = (valordxl5 + (valordxl5f-valordxl5i)/t)
        dev.write(cad.encode("ascii"))
        cad = "dxl 5 "+str(int(valordxl5))+"\n"
        valordxl6 = (valordxl6 + (valordxl6f-valordxl6i)/t)
        dev.write(cad.encode("ascii"))
        cad = "dxl 6 "+str(int(valordxl6))+"\n"
        valordxl7 = (valordxl7 + (valordxl7f-valordxl7i)/t)
        dev.write(cad.encode("ascii"))
        cad = "dxl 7 "+str(int(valordxl7))+"\n"
        time.sleep(0.05)
    print(i)
dev.close()
