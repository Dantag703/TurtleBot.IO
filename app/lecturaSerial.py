import serial
import time
import numpy as np
import json

def mapear(numero_original, min_original=-150, max_original=150, min_deseado=0, max_deseado=1023):
    numero_original = max(min_original, min(numero_original, max_original))
    numero_mapeado = (numero_original - min_original) * (max_deseado - min_deseado) / (max_original - min_original) + min_deseado
    return int(np.round(numero_mapeado, 0))

def enviar_comando(dev, motor, posicion):
        cad = f"dxl {motor} {posicion}\n"
        dev.write(cad.encode("ascii"))

def moveArm(armstring, timeout=30):
    with serial.Serial("COM3", 57600, timeout=1000) as dev_read:
        dev_read.flushInput()
        dev_read.write("read".encode("ascii"))
        time.sleep(1)
        serRead = dev_read.readline()
        innitPos = list(map(int, serRead.decode('utf-8').strip().split()))
        dev_read.close()

    iniciales = np.array(innitPos)
    finales = np.array([mapear(int(valor)) for valor in armstring['data'].split()])

    print(" ".join(map(str, iniciales)))
    
    start_time = time.time()

    while not np.array_equal(iniciales, finales):
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
                print("Timeout alcanzado. Saliendo del bucle.")
                break
        with serial.Serial("COM3", 57600, timeout=1000) as dev:
            print(str(finales)+" "+str(iniciales))

            for i in range(6):
                if iniciales[i] != finales[i]:
                    iniciales[i] += 1 if finales[i] > iniciales[i] else -1
                    enviar_comando(dev, i + 2, iniciales[i])
            time.sleep(0.05)
            dev.close()
    print(" ".join(map(str, finales)))

