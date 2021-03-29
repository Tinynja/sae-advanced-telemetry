#include <sensors/StaticSPortSensor.h>

StaticSPortSensor::StaticSPortSensor(int id):
	SPortSensor(id), value(0) {}

sportData StaticSPortSensor::getData() {
	sportData data;
	data.sensorId = sensorId;
	data.value = value*precision;
	dataSent = true;
	return data;
}