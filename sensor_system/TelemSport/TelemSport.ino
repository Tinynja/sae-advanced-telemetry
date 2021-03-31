// Most receivers require an inverter on the sport line to work with the hardware serial of an Arduino
// Known receivers that DON'T need an inverter:
//		Jumper R8
//		*any that is directly compatible with Pixhawk
// Connect any S.Port pin on your receiver to the RX pin of the Arduino
// Put a 10K resistor between TX and RX of the Arduino

#include <SPort.h>                  //Include the SPort library
#include "Wire.h"
#include <MPU6050_light.h>
#include <Adafruit_BMP085.h>
#include <Adafruit_GPS.h>

// Pitot variables, clean up later
#define PITOT_ADDR 0x28
float pitotBias;

//******* PARAMÈTRE AJUSTABLES ******
#define V1_PIN A1 // Pin d'entrée du capteur de voltage de la batterie principale
#define I1_PIN A2 // Pin d'entrée du capteur de courant de la batterie principale
#define V2_PIN A3 // Pin d'entrée du capteur de voltage de la batterie télémétrie
const float facteur_V1 = 1;
const float facteur_I1 = 1;
const float facteur_V2 = 1;

// Pression au sol, pour altimètre
int32_t pressionSol; // Pression au niveau de la mer, en Pa

// Variables de conversion
const float m2ft = 3.28084;

// Enregtistrement de Capteurs - I2C
MPU6050 imu(Wire);
Adafruit_BMP085 alt;
Adafruit_GPS GPS(&Wire);

// Fonctions de capteur
void gps_lat_long(SPortSensor* sensor);
void gps_time_date(SPortSensor* sensor);

void imu_acc_X(SPortSensor* sensor);
void imu_acc_Y(SPortSensor* sensor);
void imu_acc_Z(SPortSensor* sensor);
void imu_ang_X(SPortSensor* sensor);
void imu_ang_Y(SPortSensor* sensor);
void imu_ang_Z(SPortSensor* sensor);

void anal_cour_1(SPortSensor* sensor);
void anal_volt_1(SPortSensor* sensor);
void anal_volt_2(SPortSensor* sensor);

void pitot_press(SPortSensor* sensor);


// Enregristrement de capteurs - SPort
SPortHub hub(0xFF); // Physical ID 
// Altimètre
SPortSensor sAlt(SPORT_SENSOR_ALT);
// IMU
SPortSensor sRoll(0x310, imu_ang_X);
SPortSensor sPitch(0x320, imu_ang_Y);
SPortSensor sYaw(0x330, imu_ang_Z);
SPortSensor sAccX(SPORT_SENSOR_ACCX, imu_acc_X);
SPortSensor sAccY(SPORT_SENSOR_ACCY, imu_acc_Y);
SPortSensor sAccZ(SPORT_SENSOR_ACCZ, imu_acc_Z);
// GPS
SPortSensor sLatLong(SPORT_SENSOR_GPS_LATI_LONG, gps_lat_long);
// Analog
SPortSensor sCurr1(SPORT_SENSOR_CURR, anal_cour_1);
SPortSensor sVolt1(SPORT_SENSOR_A3,   anal_volt_1);
SPortSensor sVolt2(SPORT_SENSOR_A4,   anal_volt_2);
// Pitot
SPortSensor sPitot(0x340, pitot_press);

void setup() {
  // Initialisation SPort
  // Altimetre
  hub.registerSensor(sAlt);
  // IMU
  hub.registerSensor(sRoll);
  hub.registerSensor(sRoll);
  hub.registerSensor(sPitch);
  hub.registerSensor(sYaw);
  hub.registerSensor(sAccY);
  hub.registerSensor(sAccX);
  hub.registerSensor(sAccZ);
  // GPS
  hub.registerSensor(sLatLong);
  // Pitot
  hub.registerSensor(sPitot);
  // Courant et voltage
  hub.registerSensor(sCurr1);
  hub.registerSensor(sVolt1);
  hub.registerSensor(sVolt2);
  hub.begin();                  //Begin the serial interface for S.Port

  // Initialisation des pins analog
  pinMode(V1_PIN, INPUT);
  pinMode(I1_PIN, INPUT);
  pinMode(V1_PIN, INPUT);

  // Initialisation du GPS
  GPS.begin(0x10);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);

  // Initialisation du Pitot
  Wire.beginTransmission(0x28);
  Wire.write(0x00);
  Wire.endTransmission();
  pitotBias = pitotCalibrate(100);

  // Initialisation de l'altimètre
  byte statusAlt = alt.begin();
  while (statusAlt = 0) { } // Tout arrêter si problème de connection
  pressionSol = alt.readSealevelPressure();
  
  // Intialisation du IMU (initialisé en dernier pour minimiser le temps entre imu.begin() et le premier imu.update()
  byte statusIMU = imu.begin();
  while (statusIMU != 0) { } // Tout arrêter si problème de connection
  imu.writeData(MPU6050_CONFIG_REGISTER, 0x06); // Activer le low pass filter built-in du MPU6050
  imu.calcOffsets(true, true); // Gyro et Accelero

 
}

void loop() {
  imu.update();

  sAlt.setValue(alt.readAltitude(pressionSol));

  GPS.read();
  if(GPS.newNMEAreceived()) {
    GPS.parse(GPS.lastNMEA());    
  }
  
  hub.handle();
}

float pitotCalibrate(int nSamples){

   float sum = 0;
   for (int i = 0; i < nSamples; i++) {
      Wire.requestFrom(PITOT_ADDR,2);

      byte value1 = Wire.read();
      byte value2 = Wire.read();
    
      int16_t dp = value1 << 8 | value2;
      dp = (0x3FFF) & dp;

      const float P_min = -1.0f;
      const float P_max = 1.0f;
      const float conv = 6894.757;
      float diff_psi = ((dp - 0.1f * 16383) * (P_max - P_min) / (0.8f * 16383) + P_min);
      float diff_pa = diff_psi*conv;

      sum += diff_pa;
      delay(50);
  
  }
  
  return sum / nSamples;
}

void gps_lat_long(SPortSensor* sensor) {
	if (sensor->pollCount) {
		//Longitude
    sensor->setValue(GPS.longitude * (GPS.lon == 'N' ? 1 : -1));
	} else {
		//Latitude
    sensor->setValue(GPS.latitude * (GPS.lat == 'E' ? 1 : -1));
	}
}

void gps_time_date(SPortSensor* sensor) {
	if (sensor->pollCount) {
		//Date
		sensor->setValue(1,2,3);
	} else {
		//Time
		sensor->setValue(4,5,6);
	}
}

void imu_acc_X(SPortSensor* sensor) { sensor->setValue(imu.getAccX()); }
void imu_acc_Y(SPortSensor* sensor) { sensor->setValue(imu.getAccY()); }
void imu_acc_Z(SPortSensor* sensor) { sensor->setValue(imu.getAccZ()); }
void imu_ang_X(SPortSensor* sensor) { sensor->setValue(imu.getAngleX()); }
void imu_ang_Y(SPortSensor* sensor) { sensor->setValue(imu.getAngleY()); }
void imu_ang_Z(SPortSensor* sensor) { sensor->setValue(imu.getAngleZ()); }

void anal_cour_1(SPortSensor* sensor) { sensor->setValue(analogRead(I1_PIN*facteur_I1)); }
void anal_volt_1(SPortSensor* sensor) { sensor->setValue(analogRead(V1_PIN*facteur_V1)); }
void anal_volt_2(SPortSensor* sensor) { sensor->setValue(analogRead(V2_PIN*facteur_V2)); }

void pitot_press(SPortSensor* sensor) {
  Wire.requestFrom(0x28,2);

  byte value1 = Wire.read();
  byte value2 = Wire.read();

  int16_t dp = value1 << 8 | value2;
  dp = (0x3FFF) & dp;

  const float P_min = -1.0f;
  const float P_max = 1.0f;
  const float conv = 6894.757;
  float diff_psi = ((dp - 0.1f * 16383) * (P_max - P_min) / (0.8f * 16383) + P_min);
  float diff_pa = diff_psi*conv -pitotBias;

  sensor->setValue(diff_pa);
}
