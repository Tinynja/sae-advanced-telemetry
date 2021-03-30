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
#include <SoftwareSerial.h> //debug

SoftwareSerial mySerial(2,3); //debug
unsigned long debugTimer;
unsigned long debugTimer2;


//******* PARAMÈTRE AJUSTABLES ******
#define V1_PIN A1 // Pin d'entrée du capteur de voltage de la batterie principale
#define I1_PIN A2 // Pin d'entrée du capteur de courant de la batterie principale
#define V2_PIN A3 // Pin d'entrée du capteur de voltage de la batterie télémétrie
float   facteur_V1 = 1;
float   facteur_I1 = 1;
float   facteur_V2 = 1;
int32_t pressionSol; // Pression au niveau de la mer, en Pa
bool    refMer = false; // True pour altitude p/r au niveau de la mer, false pour altitude p/r au sol

// Variables de conversion
float m2ft = 3.28084;

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


// Enregristrement de capteurs - SPort
SPortHub hub(0xFF); // Physical ID 
SPortSensor sAlt(SPORT_SENSOR_ALT); // Altimètre
SPortSensor sRoll(0x310,  imu_ang_X); // IMU
SPortSensor sPitch(0x320, imu_ang_Y);
SPortSensor sYaw(0x330,   imu_ang_Z);
SPortSensor sAccX(SPORT_SENSOR_ACCX, imu_acc_X);
SPortSensor sAccY(SPORT_SENSOR_ACCY, imu_acc_Y);
SPortSensor sAccZ(SPORT_SENSOR_ACCZ, imu_acc_Z);
SPortSensor sLatLong(SPORT_SENSOR_GPS_LATI_LONG, gps_lat_long); // GPS
//SPortSensor sTimeDate(SPORT_SENSOR_GPS_TIME_DATE, gps_time_date);

void setup() {
  mySerial.begin(115200); //debug

  // Initialisation SPort
  hub.registerSensor(sRoll);
  hub.registerSensor(sAlt);
  hub.registerSensor(sRoll);
  hub.registerSensor(sPitch);
  hub.registerSensor(sYaw);
  hub.registerSensor(sAccY);
  hub.registerSensor(sAccX);
  hub.registerSensor(sAccZ);
  hub.registerSensor(sLatLong);
  //hub.registerSensor(sensor4);
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
  debugTimer = millis();
  imu.update();
  mySerial.print("IMU update : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");

  debugTimer = millis();
  sAlt.setValue(alt.readAltitude(pressionSol));
  mySerial.print("Alt : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");

  debugTimer = millis();
  GPS.read();
  if(GPS.newNMEAreceived()) {
    GPS.parse(GPS.lastNMEA());    
  }
  mySerial.print("GPS Parse : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");

  debugTimer2 = millis();
	hub.handle();
  mySerial.print("SPort Handle : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");
 
}

void gps_lat_long(SPortSensor* sensor) {
  debugTimer = millis();
	if (sensor->pollCount) {
		//Longitude
    sensor->setValue(GPS.longitude * (GPS.lon == 'N' ? 1 : -1));
	} else {
		//Latitude
    sensor->setValue(GPS.latitude * (GPS.lat == 'E' ? 1 : -1));
	}
  mySerial.print("GPS Send : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");
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

void imu_acc_X(SPortSensor* sensor) { 
  debugTimer = millis();
  sensor->setValue(imu.getAccX()); 
  mySerial.print("AccX : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");
 }

void imu_acc_Y(SPortSensor* sensor) {
  debugTimer = millis(); 
  sensor->setValue(imu.getAccY()); 
  mySerial.print("AccY : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");
}

void imu_acc_Z(SPortSensor* sensor) { 
  debugTimer = millis();
  sensor->setValue(imu.getAccZ());
  mySerial.print("AccZ : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");
}

void imu_ang_X(SPortSensor* sensor) { 
  debugTimer = millis();
  sensor->setValue(imu.getAngleX());
  mySerial.print("AngX : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");
}

void imu_ang_Y(SPortSensor* sensor) { 
  debugTimer = millis();
  sensor->setValue(imu.getAngleY());
  mySerial.print("AngY : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");
}

void imu_ang_Z(SPortSensor* sensor) { 
  debugTimer = millis();
  sensor->setValue(imu.getAngleZ());
  mySerial.print("AngZ : ");
  mySerial.print(millis()-debugTimer);
  mySerial.print(" ms");
}
