// Most receivers require an inverter on the sport line to work with the hardware serial of an Arduino
// Known receivers that DON'T need an inverter:
//		Jumper R8
//		*any that is directly compatible with Pixhawk
// Connect any S.Port pin on your receiver to the RX pin of the Arduino
// Put a 10K resistor (or a wire if it doesn't work with the resistor) between TX and RX of the Arduino

#include <SPort.h>                  //Include the SPort library

void zero_to_hundred(SPortSensor* sensor);

SPortHub hub(0); // Physical ID 
SPortSensor my_ondemand_sensor(SPORT_SENSOR_ALT, zero_to_hundred); 	//On-Demand sensor

int counter;

void setup() {
	hub.registerSensor(my_ondemand_sensor);		//Add sensor to the hub
	hub.begin();								//Begin the serial interface for S.Port
}

void loop() {
	hub.handle();		//Check if receiver asked for our physical ID and send him sensor data
}

void zero_to_hundred(SPortSensor* sensor) {
	counter = (counter+1)%101;
	sensor->setValue(counter);
}