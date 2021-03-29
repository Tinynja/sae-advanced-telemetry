#include <SPort.h>                  //Include the SPort library
#include <math.h>

float constant456();

SPortHub hub(0); // Physical ID 
SPortSensor sensor1(SPORT_SENSOR_ALT);
SPortSensor sensor2(SPORT_SENSOR_ACCX, constant456);

void setup() {
	sensor1.precision = 10000;		//Sets a custom precision for the sensor (see SPortSensor.cpp for default precisions)
	hub.registerSensor(sensor1);	//Add sensor to the hub
	hub.registerSensor(sensor2);	//Add sensor to the hub
	hub.begin();					//Begin the serial interface for S.Port
}

void loop() {
	sensor1.value = 123; //Update the value of the sensor
	// sensor1.value = fmod(sensor1.value+1,100);
	// sensor2.value = fmod(sensor2.value+1,100);
	hub.handle();
}

float constant456() {
	return 456;
}