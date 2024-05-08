from dynamixel_sdk import *                 # Uses Dynamixel SDK library
from paho.mqtt import client as mqtt_client
import random

broker = 'c1efe023.ala.dedicated.aws.emqxcloud.com'
port = 1883
topics_set = ['/turtlebot/arm/claw/set/','/turtlebot/arm/wrist/set/',
              '/turtlebot/arm/elbow/set/','/turtlebot/arm/elbow1/set/',
              '/turtlebot/arm/shoulder/set/','/turtlebot/arm/base/set/']
topics_status = ['/turtlebot/arm/claw/status/','/turtlebot/arm/wrist/status/',
                 '/turtlebot/arm/elbow/status/','/turtlebot/arm/elbow1/status/',
                 '/turtlebot/arm/shoulder/status/','/turtlebot/arm/base/status/']

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'mqttpy'
password = 'public'

# Protocol version
PROTOCOL_VERSION        = 1.0               # See which protocol version is used in the Dynamixel
# Default setting
BAUDRATE                = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME              = 'COM3'    # Check which port is being used on your controller
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36

DXL_ID = [7,6,5,4,3,2]
DXL_MINIMUM_POSITION = [335,0,177,25,0,0]
DXL_MAXIMUM_POSITION = [810,1023,859,985,1023,1023]

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()

# Enable Dynamixel Torque
def enable_DXL(DXL_ID,ADDR_MX_TORQUE_ENABLE):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, 1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")

# Disable Dynamixel Torque
def disable_DXL(DXL_ID,ADDR_MX_TORQUE_ENABLE):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
def set_DXL(DXL_ID,ADDR_MX_GOAL_POSITION, goal):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler,DXL_ID, ADDR_MX_GOAL_POSITION, goal)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"set DXL_{DXL_ID} to:{goal}%")

def mapear(numero_original, min_deseado, max_deseado):
    min_original = 0
    max_original = 100
    # Asegúrate de que el número original esté dentro del rango original
    numero_original = max(min_original, min(numero_original, max_original))
    # Calcula el número mapeado utilizando una regla de tres
    numero_mapeado = (numero_original - min_original) * (max_deseado - min_deseado) / (max_original - min_original) + min_deseado
    
    return numero_mapeado

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic in topics_set:
            pos = topics_set.index(msg.topic)
            goal = mapear(int(msg.payload.decode()),DXL_MINIMUM_POSITION[pos],DXL_MAXIMUM_POSITION[pos])
            set_DXL(DXL_ID[pos],ADDR_MX_GOAL_POSITION, int(goal))
        elif msg.topic in topics_status:
            pos = topics_status.index(msg.topic)
            if msg.payload.decode() == 'ON':
                enable_DXL(DXL_ID[pos],  ADDR_MX_TORQUE_ENABLE)
            elif msg.payload.decode() == 'OFF':
                disable_DXL(DXL_ID[pos],  ADDR_MX_TORQUE_ENABLE)
    for topic in topics_set:
        client.subscribe(topic, qos=0)
    for topic in topics_status:
        client.subscribe(topic, qos=0)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    

if __name__ == '__main__':
    run()
    portHandler.closePort()