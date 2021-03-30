// Test code for Adafruit GPS That Support Using I2C
//
// This code shows how to test a passthru between USB and I2C
//
// Pick one up today at the Adafruit electronics shop
// and help support open source hardware & software! -ada

#include <Adafruit_GPS.h>
#include <SPort.h>

void gps_lati_long(SPortSensor* gps);

// Connect to the GPS on the hardware I2C port
Adafruit_GPS GPS(&Wire);
SPortHub hub(0);

SPortSensor gps_sensor(SPORT_SENSOR_GPS_LATI_LONG, gps_lati_long);

void setup() {
	// wait for hardware serial to appear
	//   while (!Serial);

	// make this baud rate fast enough to we aren't waiting on it
	//   Serial.begin(115200);

	//   Serial.println("Adafruit GPS library basic I2C test!");
	GPS.begin(0x10);  // The I2C address to use is 0x10
	
	// SPort
	hub.registerSensor(gps_sensor);
	hub.begin();
}


void loop() {
	// if (Serial.available()) {
	// 	char c = Serial.read();
	// 	GPS.write(c);
	// }
	// if (GPS.available()) {
	// 	char c = GPS.read();
	// 	Serial.write(c);
	// }
	hub.handle();
}

void gps_lati_long(SPortSensor* sensor) {
	if (sensor->pollCount) {
		//Longitude
		sensor->setValue(0);
		// sensor->setValue(GPS.longitude * ((GPS.lon == 'N') ? 1 : -1));
	} else {
		//Latitude
		sensor->setValue(0);
		// sensor->setValue(GPS.latitude * ((GPS.lat == 'E') ? 1 : -1));
	}
}