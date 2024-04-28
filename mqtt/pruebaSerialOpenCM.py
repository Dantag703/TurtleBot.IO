import serial
dev = serial.Serial("COM3",57600)
dev.flushInput()
cad = "p 0 1"

dev.write(cad.encode("ascii"))

dev.close()
