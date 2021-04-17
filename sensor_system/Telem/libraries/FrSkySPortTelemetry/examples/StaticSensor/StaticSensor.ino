// Most receivers require an inverter on the sport line to work with the hardware serial of an Arduino
// Known receivers that DON'T need an inverter:
//		Jumper R8
//		*any that is directly compatible with Pixhawk
// Connect any S.Port pin on your receiver to the RX pin of the Arduino
// Put a 10K resistor (or a wire if it doesn't work with the resistor) between TX and RX of the Arduino

#include <SPort.h>                  //Include the SPort library

SPortHub hub(0);		// Microcontroller physical ID 
SPortSensor my_static_sensor(SPORT_SENSOR_ALT);

int counter;

void setup() {
	hub.registerSensor(my_static_sensor);	//Add sensor to the hub
	hub.begin();							//Begin the serial interface for S.Port
}

void loop() {
	counter = (counter+1)%101;
	sensor1.setValue(counter);		//Update the value of the sensor
	hub.handle();					//Check if receiver asked for our physical ID and send him sensor data
}