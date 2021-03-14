#include "Wire.h"
#include <MPU6050_light.h>
#include <Adafruit_BMP085.h>


//******* PARAMÈTRE AJUSTABLES ******
#define V1_PIN A1 // Pin d'entrée du capteur de voltage de la batterie principale
#define I1_PIN A2 // Pin d'entrée du capteur de courant de la batterie principale
#define V2_PIN A3 // Pin d'entrée du capteur de voltage de la batterie télémétrie
int32_t pressionMer = 101300; // Pression au niveau de la mer, en Pa
bool refMer = false; // True pour altitude p/r au niveau de la mer, false pour altitude p/r au sol

MPU6050 imu(Wire);
Adafruit_BMP085 alt;


long timer = 0;
int32_t pressionSol;

void setup() {
  Serial.begin(112500); // Connection Serial pour debugging. Commenter lors du fonctionnement réel.
  
  Wire.begin(); // Connection I2C

  // Initialisation de l'altimètre
  byte statusAlt = alt.begin();
  Serial.print(F("Altimeter status: "));
  if (statusAlt) { 
    Serial.println("OK!");
  } else {
    Serial.println("ERROR!");
  }
  while(statusAlt=0){ } // Tout arrêter si problème de connection

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
  while(statusIMU!=0){ } // Tout arrêter si problème de connection
  
  Serial.print(F("Calculating offsets, do not move IMU"));
  delay(1000);
  imu.calcOffsets(true,true); // Gyro et Accelero
  Serial.println(".....Done!\n");

  Serial.println(F("=====================================================\n"));
}

void loop() {
  imu.update(); // Mise à jour du IMU (Requis en raison de l'intégration des mesures)

  if(millis() - timer > 1000){ // Afficher données toutes les secondes
    
    // Mesures du IMU
    Serial.println("--- IMU ---");
    Serial.print(F("TEMP(IMU): "));Serial.println(imu.getTemp());
    Serial.print(F("ACCEL \tX: "));Serial.print(imu.getAccX());
      Serial.print(" \tY: ");Serial.print(imu.getAccY());
      Serial.print(" \tZ: ");Serial.println(imu.getAccZ());
    Serial.print(F("ANGLE \tX: "));Serial.print(imu.getAngleX());
      Serial.print(" \tY: ");Serial.print(imu.getAngleY());
      Serial.print(" \tZ: ");Serial.println(imu.getAngleZ());
    Serial.println();
    
    // Mesures de l'altimètre
    Serial.println("--- Altimètre ---");
    if (refMer) {
      Serial.print(F("ALTITUDE(m) : "));Serial.println(alt.readAltitude(pressionMer));
      Serial.print(F("ALTITUDE(ft) : "));Serial.println(3.28084*alt.readAltitude(pressionMer));
    } else {
      Serial.print(F("ALTITUDE(m) : "));Serial.println(alt.readAltitude(pressionSol));
      Serial.print(F("ALTITUDE(ft) : "));Serial.println(3.28084*alt.readAltitude(pressionSol));
    }
    Serial.print(F("TEMP(ALT): "));Serial.println(alt.readTemperature());


    // Mesures du pitot
    Serial.println("--- Pitot ---");
    Serial.print(F("DELTA_P (Pa) : "));//Serial.println(pitot.getDeltaPa());
    Serial.print(F("VITESSE (m/s) : "));//Serial.println(pitot.getVelMs());
    Serial.print(F("TEMP(PIT): "));//Serial.println(pitot.getTemp());*/

    // Mesures du GPS
    Serial.println("--- GPS ---");
    Serial.print(F("COORD : "));//Serial.println(pitot.getDeltaPa());
    Serial.print(F("VEL : "));//Serial.println(pitot.getVelMs());

    // Mesures Analog
    Serial.println("--- Analog ---");
    Serial.print(F("VOLTAGE BATT1: "));//Serial.println(pitot.getDeltaPa());
    Serial.print(F("COURANT BATT1: "));//Serial.println(pitot.getVelMs());
    Serial.print(F("VOLTAGE BATT1: "));//Serial.println(pitot.getTemp());*/
    
    Serial.println();
    Serial.println(F("=====================================================\n"));
    timer = millis();
  }

}
