#include <SPort.h>                  // SPort library
#include "Wire.h"
#include <MPU6050_light.h>          // IMU library
#include <Adafruit_BMP085.h>        // Altimeter library
#include <Adafruit_GPS.h>           // GPS library



// --- PARAMÈTRE AJUSTABLES ---
#define V1_PIN A1 // Pin d'entrée du capteur de voltage de la batterie principale
#define I1_PIN A7 // Pin d'entrée du capteur de courant de la batterie principale
#define V2_PIN A2 // Pin d'entrée du capteur de voltage de la batterie télémétrie
const float Vin = 5.123;
// Facteurs de conversion pour capteurs analog
const float facteur_V1 = 25.2/1023;       
const float facteur_I1 = (Vin/1023)/39.5;
const int   bias_I1    = 511;
const float facteur_V2 = 8.4/1023;


// Variables misc.
#define PITOT_ADDR 0x28 // Addresse I2C du pitot
float pitotBias;     // Bias du pitot, calculé automatiquement pendant calibration
int32_t pressionSol; // Pression au sol, pour altimètre

// Variables de conversion
const float m2ft = 3.28084;

// Enregtistrement de Capteurs - I2C
MPU6050 imu(Wire);
Adafruit_BMP085 alt;
Adafruit_GPS GPS(&Wire);

// --- Fonctions de capteur ---
// GPS
void gps_lat_long(SPortSensor* sensor);
void gps_alt(SPortSensor* sensor);
void gps_course(SPortSensor* sensor);
void gps_speed(SPortSensor* sensor);
// IMU
void imu_acc_X(SPortSensor* sensor);
void imu_acc_Y(SPortSensor* sensor);
void imu_acc_Z(SPortSensor* sensor);
void imu_ang_X(SPortSensor* sensor);
void imu_ang_Y(SPortSensor* sensor);
void imu_ang_Z(SPortSensor* sensor);
// Analog
void anal_cour_1(SPortSensor* sensor);
void anal_volt_1(SPortSensor* sensor);
void anal_volt_2(SPortSensor* sensor);
// Pitot
void pitot_press(SPortSensor* sensor);


// --- Enregristrement de capteurs - SPort ---
SPortHub hub(0xFF); // Physical ID - 0xFF pour répondre à tous les polls du receiver - Augmente la fréquence des mises à jour
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
SPortSensor sGPSspeed(SPORT_SENSOR_GPS_SPEED, gps_speed);
SPortSensor sCourse(SPORT_SENSOR_GPS_COURSE, gps_course);
SPortSensor sGPSalt(SPORT_SENSOR_GPS_ALT, gps_alt);
// Analog
SPortSensor sCurr1(SPORT_SENSOR_CURR, anal_cour_1);
SPortSensor sVolt1(SPORT_SENSOR_A3,   anal_volt_1);
SPortSensor sVolt2(SPORT_SENSOR_A4,   anal_volt_2);
// Pitot
SPortSensor sPitot(0x340, pitot_press);

void setup() {
  // --- Initialisation SPort ---
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
  hub.registerSensor(sGPSalt);
  hub.registerSensor(sGPSspeed);
  hub.registerSensor(sCourse);
  // Pitot
  hub.registerSensor(sPitot);
  // Courant et voltage
  hub.registerSensor(sCurr1);
  hub.registerSensor(sVolt1);
  hub.registerSensor(sVolt2);
  //Begin the serial interface for S.Port
  hub.begin();                  

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
  imu.writeData(MPU6050_CONFIG_REGISTER, 0x06); // Activer le low pass filter built-in du MPU6050 (pour aider avec les vibrations)
  imu.calcOffsets(true, true); // Gyro et Accelero
}

void loop() {
  // Mettre à jour l'attitude
  imu.update();

  // Mettre à jour l'altitude
  sAlt.setValue(alt.readAltitude(pressionSol));

  // Mettre à jour le GPS
  GPS.read();
  if(GPS.newNMEAreceived()) {
    GPS.parse(GPS.lastNMEA());    
  }

  // Envoyer/Recevoir données via S.Port
  hub.handle();
}

// --- Fonctions de mise à jour des capteurs (pour S.Port) ---

void gps_lat_long(SPortSensor* sensor) {
	if (sensor->pollCount) {
		//Longitude
    sensor->setValue(GPS.longitude * (GPS.lon == 'N' ? 1 : -1));
	} else {
		//Latitude
    sensor->setValue(GPS.latitude * (GPS.lat == 'E' ? 1 : -1));
	}
}

void gps_alt(SPortSensor* sensor) {sensor->setValue(GPS.angle);}
void gps_course(SPortSensor* sensor) {sensor->setValue(GPS.angle);}
void gps_speed(SPortSensor* sensor) {sensor->setValue(GPS.speed);}

void imu_acc_X(SPortSensor* sensor) { sensor->setValue(imu.getAccX()); }
void imu_acc_Y(SPortSensor* sensor) { sensor->setValue(imu.getAccY()); }
void imu_acc_Z(SPortSensor* sensor) { sensor->setValue(imu.getAccZ()); }
void imu_ang_X(SPortSensor* sensor) { sensor->setValue(imu.getAngleX()); }
void imu_ang_Y(SPortSensor* sensor) { sensor->setValue(imu.getAngleY()); }
void imu_ang_Z(SPortSensor* sensor) { sensor->setValue(imu.getAngleZ()); }

void anal_cour_1(SPortSensor* sensor) { sensor->setValue((bias_I1-analogRead(I1_PIN))*facteur_I1); }
void anal_volt_1(SPortSensor* sensor) { sensor->setValue(analogRead(V1_PIN)*facteur_V1); }
void anal_volt_2(SPortSensor* sensor) { sensor->setValue(analogRead(V2_PIN)*facteur_V2); }

// --- Fin des fonctions de mise à jour des capteurs (pour S.Port) ---

// Fonctions spécifiques au Pitot (il n'a pas de librairie)

void pitot_press(SPortSensor* sensor) {
  // Lecture des données via I2C
  Wire.requestFrom(0x28,2);
  byte value1 = Wire.read();
  byte value2 = Wire.read();

  int16_t dp = value1 << 8 | value2;
  dp = (0x3FFF) & dp;

  // Conversion en delta_P via fonction du capteur
  const float P_min = -1.0f;
  const float P_max = 1.0f;
  const float conv = 6894.757;
  float diff_psi = ((dp - 0.1f * 16383) * (P_max - P_min) / (0.8f * 16383) + P_min);
  float diff_pa = diff_psi*conv -pitotBias;

  sensor->setValue(diff_pa);
}

float pitotCalibrate(int nSamples){ // Calibration initiale du Pitot

   float sum = 0;
   for (int i = 0; i < nSamples; i++) {
      // Lecture des données via I2C
      Wire.requestFrom(PITOT_ADDR,2);
      byte value1 = Wire.read();
      byte value2 = Wire.read();
    
      int16_t dp = value1 << 8 | value2;
      dp = (0x3FFF) & dp;

      // Conversion en delta_P via fonction du capteur
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
