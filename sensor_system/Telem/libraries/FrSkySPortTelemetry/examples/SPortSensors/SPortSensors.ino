// Most receivers require an inverter on the sport line to work with the hardware serial of an Arduino
// Known receivers that DON'T need an inverter:
//		Jumper R8
//		*any that is directly compatible with Pixhawk
// Connect any S.Port pin on your receiver to the RX pin of the Arduino
// Put a 10K resistor between TX and RX of the Arduino

#include <SPort.h>                  //Include the SPort library
#include <math.h>

void constant456(SPortSensor* sensor);
void gps_lat_long(SPortSensor* sensor);
void gps_time_date(SPortSensor* sensor);

SPortHub hub(0); // Physical ID 
SPortSensor sensor1(SPORT_SENSOR_ALT);
SPortSensor sensor2(SPORT_SENSOR_ACCX, constant456);
SPortSensor sensor3(SPORT_SENSOR_GPS_LATI_LONG, gps_lat_long);
SPortSensor sensor4(SPORT_SENSOR_GPS_TIME_DATE, gps_time_date);

void setup() {
	sensor1.precision = 10000;		//Sets a custom precision for the sensor (see SPortSensor.cpp for default precisions)
	hub.registerSensor(sensor1);	//Add sensor to the hub
	hub.registerSensor(sensor2);	//Add sensor to the hub
	hub.registerSensor(sensor3);	//Add sensor to the hub
	hub.registerSensor(sensor4);	//Add sensor to the hub
	hub.begin();					//Begin the serial interface for S.Port
}

void loop() {
	sensor1.setValue(123); //Update the value of the sensor
	// sensor1.value = fmod(sensor1.value+1,100);
	// sensor2.value = fmod(sensor2.value+1,100);
	hub.handle();
}

void constant456(SPortSensor* sensor) {
	sensor->setValue(fmod(sensor->rawValue.value0+1, 100));
}

void gps_lat_long(SPortSensor* sensor) {
	if (sensor->pollCount) {
		//Longitude
		sensor->setValue(4512);
	} else {
		//Latitude
		sensor->setValue(-3655);
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