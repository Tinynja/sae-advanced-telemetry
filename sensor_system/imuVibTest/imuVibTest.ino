// Most receivers require an inverter on the sport line to work with the hardware serial of an Arduino
// Known receivers that DON'T need an inverter:
//		Jumper R8
//		*any that is directly compatible with Pixhawk
// Connect any S.Port pin on your receiver to the RX pin of the Arduino
// Put a 10K resistor between TX and RX of the Arduino

#include <SPort.h>                  //Include the SPort library
#include "Wire.h"
#include <MPU6050_light.h>

// Enregtistrement de Capteurs - I2C
MPU6050 imu(Wire);

void imu_acc_X(SPortSensor* sensor);
void imu_acc_Y(SPortSensor* sensor);
void imu_acc_Z(SPortSensor* sensor);
void imu_ang_X(SPortSensor* sensor);
void imu_ang_Y(SPortSensor* sensor);
void imu_ang_Z(SPortSensor* sensor);

// Enregristrement de capteurs - SPort
SPortHub hub(0xFF); // Physical ID 
// IMU
SPortSensor sRoll(0x310, imu_ang_X);
SPortSensor sPitch(0x320, imu_ang_Y);
SPortSensor sYaw(0x330, imu_ang_Z);
SPortSensor sAccX(SPORT_SENSOR_ACCX, imu_acc_X);
SPortSensor sAccY(SPORT_SENSOR_ACCY, imu_acc_Y);
SPortSensor sAccZ(SPORT_SENSOR_ACCZ, imu_acc_Z);

void setup() {
  // Initialisation SPort
  // IMU
  hub.registerSensor(sRoll);
  hub.registerSensor(sRoll);
  hub.registerSensor(sPitch);
  hub.registerSensor(sYaw);
  hub.registerSensor(sAccY);
  hub.registerSensor(sAccX);
  hub.registerSensor(sAccZ);
  hub.begin();                  //Begin the serial interface for S.Port

  // Intialisation du IMU (initialisé en dernier pour minimiser le temps entre imu.begin() et le premier imu.update()
  byte statusIMU = imu.begin();
  while (statusIMU != 0) { } // Tout arrêter si problème de connection
  imu.writeData(MPU6050_CONFIG_REGISTER, 0x06); // Activer le low pass filter built-in du MPU6050
  imu.calcOffsets(true, true); // Gyro et Accelero

 
}

void loop() {
  imu.update();
  hub.handle();
}

void imu_acc_X(SPortSensor* sensor) { sensor->setValue(imu.getAccX()); }
void imu_acc_Y(SPortSensor* sensor) { sensor->setValue(imu.getAccY()); }
void imu_acc_Z(SPortSensor* sensor) { sensor->setValue(imu.getAccZ()); }
void imu_ang_X(SPortSensor* sensor) { sensor->setValue(imu.getAngleX()); }
void imu_ang_Y(SPortSensor* sensor) { sensor->setValue(imu.getAngleY()); }
void imu_ang_Z(SPortSensor* sensor) { sensor->setValue(imu.getAngleZ()); }
