#include <DynamixelSDK.h>
#include <Servo.h>
Servo myservo1;  // create servo object to control a servo
Servo myservo2;
#include <DynamixelWorkbench.h>
#define DEVICE_NAME "1"
#define STRING_BUF_NUM 64
#define BAUDRATE 1000000
String cmd[STRING_BUF_NUM];
DynamixelWorkbench dxl_wb;
void split(String data, char separator, String* temp);
bool result = false;            // Communication result
uint8_t error = 0;                          // Dynamixel error
int16_t present_position = 0;               // Present position
int16_t present_velocity = 0;               // Present position

void setup() {
  const char *log = NULL;
  bool result = false;
  uint16_t model_number = 0;
  myservo1.attach(3);
  myservo2.attach(2);
  Serial.begin(57600);
  Serial.println("Start..");
  dynamixel::PortHandler *portHandler = dynamixel::PortHandler::getPortHandler("COM3");
  // Initialize Packethandler1 instance
  dynamixel::PacketHandler *packetHandler = dynamixel::PacketHandler::getPacketHandler(1.0);
  if (portHandler->openPort())
  {
    Serial.print("Succeeded to open the port!\n");
  }
  else
  {
    Serial.print("Failed to open the port!\n");
    Serial.print("Press any key to terminate...\n");
    return;
  }
  if (portHandler->setBaudRate(BAUDRATE))
  {
    Serial.print("Succeeded to change the baudrate!\n");
  }
  else
  {
    Serial.print("Failed to change the baudrate!\n");
    Serial.print("Press any key to terminate...\n");
    return;
  }
  result = dxl_wb.init(DEVICE_NAME, BAUDRATE, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to init WB");
  }
  else
  {
    Serial.print("Succeeded to init WB: ");
    Serial.println(BAUDRATE);  
  }

  int16_t dxl_present_position2 = 0;
  int16_t dxl_present_position3 = 0;
  int16_t dxl_present_position4 = 0;
  int16_t dxl_present_position5 = 0;
  int16_t dxl_present_position6 = 0;
  int16_t dxl_present_position7 = 0;

    uint8_t goal2 = 513;
    uint8_t goal3 = 513;
    uint8_t goal4 = 513;
    uint8_t goal5 = 513;
    uint8_t goal6 = 513;
    uint8_t goal7 = 810;
  while(1){
    if (Serial.available() > 0) {
      String read_string = Serial.readStringUntil('\n');
     
      read_string.trim();
      split(read_string, ' ', cmd);
      if (cmd[0] == "read"){
        packetHandler->read2ByteTxRx(portHandler, 2, 36, (uint16_t*)&dxl_present_position2);
        packetHandler->read2ByteTxRx(portHandler, 3, 36, (uint16_t*)&dxl_present_position3);
        packetHandler->read2ByteTxRx(portHandler, 4, 36, (uint16_t*)&dxl_present_position4);
        packetHandler->read2ByteTxRx(portHandler, 5, 36, (uint16_t*)&dxl_present_position5);
        packetHandler->read2ByteTxRx(portHandler, 6, 36, (uint16_t*)&dxl_present_position6);
        packetHandler->read2ByteTxRx(portHandler, 7, 36, (uint16_t*)&dxl_present_position7);

        String sapo = String(dxl_present_position2)+" "+String(dxl_present_position3)+" "+String(dxl_present_position4)+" "+String(dxl_present_position5)+" "+String(dxl_present_position6)+" "+String(dxl_present_position7);

        Serial.println(sapo);
      }
      if (cmd[0] == "dxl"){
        uint8_t id = cmd[1].toInt();
        if (id > 1 && id < 8){
          Serial.println(cmd[0]);
          uint16_t goal = cmd[2].toInt();
          result = packetHandler->write2ByteTxRx(portHandler, id, 30, goal, &error);
        }
        if (id >= 0 && id < 2){
          result = dxl_wb.ping(id, &model_number, &log);
          if (result == false)
          {
            Serial.println(log);
            Serial.println("Failed to ping");
          }
          else
          {
            Serial.println("Succeeded to ping");
            Serial.print("id : ");
            Serial.print(id);
            Serial.print(" model_number : ");
            Serial.println(model_number);
          }
          int32_t goal = cmd[2].toInt();
          result = dxl_wb.wheelMode(id, 0, &log);
          if (result == false)
          {
            Serial.println(log);
            Serial.println("Failed to change wheel mode");
          }
          else
          {
            Serial.println("Succeed to change wheel mode");
            Serial.println("Dynamixel is moving...");
            dxl_wb.goalVelocity(id, goal);
          }
        }
      }
      if (cmd[0] == "p"){
        uint8_t id = cmd[1].toInt();
        if (id == 1){
          myservo1.write(cmd[2].toInt());
        }
        if (id == 2){
          myservo2.write(cmd[2].toInt());
        }
        if (id == 0){
          uint8_t mode = cmd[2].toInt();
          if (mode == 0){
            myservo1.write(15);
            myservo2.write(175);
          }
          if (mode == 1){
            myservo1.write(105);
            myservo2.write(80);
          }
          if (mode == 2){
            myservo1.write(125);
            myservo2.write(60);
          }
          if (mode == 3){
            myservo1.write(145);
            myservo2.write(40);
          }
          if (mode == 4){
            myservo1.write(165);
            myservo2.write(20);
          }
          if (mode == 5){
            myservo1.write(180);
            myservo2.write(0);
          }
        }
      }
    }
  }
}

void loop() {
  Serial.print("cualquier maricada");
}

void split(String data, char separator, String* temp)
{
  int cnt = 0;
  int get_index = 0;

  String copy = data;
  
  while(true)
  {
    get_index = copy.indexOf(separator);

    if(-1 != get_index)
    {
      temp[cnt] = copy.substring(0, get_index);

      copy = copy.substring(get_index + 1);
    }
    else
    {
      temp[cnt] = copy.substring(0, copy.length());
      break;
    }
    ++cnt;
  }
}
