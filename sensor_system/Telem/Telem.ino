#include "Wire.h"
#include <MPU6050_light.h>
#include <Adafruit_BMP085.h>
#include <Adafruit_GPS.h>
//include <CustomPitot.h>

//******* PARAMÈTRE AJUSTABLES ******
#define V1_PIN A1 // Pin d'entrée du capteur de voltage de la batterie principale
#define I1_PIN A2 // Pin d'entrée du capteur de courant de la batterie principale
#define V2_PIN A3 // Pin d'entrée du capteur de voltage de la batterie télémétrie
float   facteur_V1 = 1;
float   facteur_I1 = 1;
float   facteur_V2 = 1;
int32_t pressionMer = 101300; // Pression au niveau de la mer, en Pa
bool    refMer = false; // True pour altitude p/r au niveau de la mer, false pour altitude p/r au sol

// Variables de conversion
float m2ft = 3.28084;

MPU6050 imu(Wire);
Adafruit_BMP085 alt;
Adafruit_GPS GPS(&Wire);
//CustomPitot pitot;

long timer = 0;
int32_t pressionSol;

void setup() {
  Serial.begin(112500); // Connection Serial pour debugging.

  Wire.begin(); // Connection I2C

  // Initialisation des pins analog
  pinMode(V1_PIN, INPUT);
  pinMode(I1_PIN, INPUT);
  pinMode(V1_PIN, INPUT);

  // Initialisation du GPS
  GPS.begin(0x10);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);

  // Initialisation du Pitot
  Wire.beginTransmission(0x28);
  Wire.write(0x00);
  Wire.endTransmission();

  // Initialisation de l'altimètre
  byte statusAlt = alt.begin();
  Serial.print(F("Altimeter status: "));
  if (statusAlt) {
    Serial.println("OK!");
  } else {
    Serial.println("ERROR!");
  }
  while (statusAlt = 0) { } // Tout arrêter si problème de connection

  if (refMer) {
    Serial.print(F("Entered sea-level pressure (Pa): "));
    Serial.println(pressionMer);
  } else {
    Serial.print(F("Calculating ground-level pressure (Pa): "));
    pressionSol = alt.readSealevelPressure();
    Serial.println(pressionSol);
  }


  // Intialisation du IMU (initialisé en dernier pour minimiser le temps entre imu.begin() et le premier imu.update()
  byte statusIMU = imu.begin();
  Serial.print(F("IMU status: "));
  if (!statusIMU) {
    Serial.println("OK!");
  } else {
    Serial.println("ERROR!");
  }
  while (statusIMU != 0) { } // Tout arrêter si problème de connection
  
  imu.writeData(MPU6050_CONFIG_REGISTER, 0x06); // Activer le low pass filter built-in du MPU6050

  Serial.print(F("Calculating offsets, do not move IMU"));
  delay(1000);
  imu.calcOffsets(true, true); // Gyro et Accelero
  Serial.println(".....Done!\n");

  Serial.println(F("=====================================================\n"));
}

void loop() {

  long startTime = millis();
  imu.update(); // Mise à jour du IMU (Requis en raison de l'intégration des mesures)
  
  
  if (millis() - timer > 250) { // Afficher données toutes les secondes

  Serial.print("Update time : ");
  Serial.println(millis()-startTime);

  startTime = millis();

    // Mesures du IMU
    Serial.println("--- IMU ---");
    Serial.print(F("TEMP(IMU): ")); Serial.println(imu.getTemp());
    Serial.print(F("ACCEL \tX: ")); Serial.print(imu.getAccX());
    Serial.print(" \tY: "); Serial.print(imu.getAccY());
    Serial.print(" \tZ: "); Serial.println(imu.getAccZ());
    Serial.print(F("ANGLE \tX: ")); Serial.print(imu.getAngleX());
    Serial.print(" \tY: "); Serial.print(imu.getAngleY());
    Serial.print(" \tZ: "); Serial.println(imu.getAngleZ());
    Serial.println();
    
    Serial.print("Fetch time: ");
    Serial.print(millis()-startTime);
    Serial.println(" ms");
    startTime = millis();

    // Mesures du GPS
    Serial.println("--- GPS ---");
    while(!GPS.newNMEAreceived()) {
      GPS.read();
    }
    Serial.println(GPS.lastNMEA());
    
    Serial.print("Fetch time: ");
    Serial.print(millis()-startTime);
    Serial.println(" ms");
    startTime = millis();
    
    // Mesures de l'altimètre
    Serial.println("--- Altimètre ---");
    if (refMer) {
      Serial.print(F("ALTITUDE(m) : ")); Serial.println(alt.readAltitude(pressionMer));
      Serial.print(F("ALTITUDE(ft) : ")); Serial.println(m2ft * alt.readAltitude(pressionMer));
    } else {
      Serial.print(F("ALTITUDE(m) : ")); Serial.println(alt.readAltitude(pressionSol));
      Serial.print(F("ALTITUDE(ft) : ")); Serial.println(m2ft * alt.readAltitude(pressionSol));
    }
    
    Serial.print(F("TEMP(ALT): ")); Serial.println(alt.readTemperature());

    Serial.print("Fetch time: ");
    Serial.print(millis()-startTime);
    Serial.println(" ms");
    startTime = millis();

    // Mesures du pitot
    Wire.requestFrom(0x28,4);
    
    byte value1 = Wire.read();
    byte value2 = Wire.read();
    byte value3 = Wire.read();
    byte value4 = Wire.read();
    
    int16_t dp = value1 << 8 | value2;
    dp = (0x3FFF) & dp;
    
    int16_t dT = value3 << 8 | value4;
    dT = ((0xFFE0) & dT) >> 5;
    
    const float P_min = -1.0f;
    const float P_max = 1.0f;
    const float conv = 6894.757;
    float diff_psi = ((dp - 0.1f * 16383) * (P_max - P_min) / (0.8f * 16383) + P_min);
    float diff_pa = diff_psi*conv;// - bias;
    float pitotTemp = ((200.0f * dT) / 2047) - 50;
    
    Serial.println("--- Pitot ---");
    Serial.print(F("DELTA_P (Pa) : "));Serial.println(diff_pa);
    //Serial.print(F("VITESSE (m/s) : "));//Serial.println(pitot.getVelMs());
    Serial.print(F("TEMP(PIT): "));Serial.println(pitotTemp);

    Serial.print("Fetch time: ");
    Serial.print(millis()-startTime);
    Serial.println(" ms");
    startTime = millis();

    // Mesures Analog
    Serial.println("--- Analog ---");
    Serial.print(F("VOLTAGE BATT1: ")); Serial.println(analogRead(V1_PIN) * (5 / 1023)*facteur_V1);
    Serial.print(F("COURANT BATT1: ")); Serial.println(analogRead(I1_PIN) * (5 / 1023)*facteur_I1);
    Serial.print(F("VOLTAGE BATT2: ")); Serial.println(analogRead(V2_PIN) * (5 / 1023)*facteur_V2);

    Serial.print("Fetch time: ");
    Serial.print(millis()-startTime);
    Serial.println(" ms");
    startTime = millis();
    
    Serial.println();
    Serial.println(F("=====================================================\n"));
    timer = millis();
  }

}
