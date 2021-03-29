#include <sensors/GPSLongLatiSensor.h>

GPSLontLatiSensor::GPSLontLatiSensor(int id):
	SPortSensor(id) {
	pollsNeeded = 2;
}

GPSLontLatiSensor::GPSLontLatiSensor(int id, float (*fetchValue)()):
	SPortSensor(id, formatValue) {
	pollsNeeded = 2;
}

float GPSLontLatiSensor::formatValue() {
	if (polls == 0) {
		//We send North/South data

	} else
}

void parseNMEA()

sportData OnDemandSPortSensor::getData() {
	sportData data;
	data.sensorId = sensorId;
	data.value = _fetchValue()*precision;
	dataSent = true;
	return data;
}