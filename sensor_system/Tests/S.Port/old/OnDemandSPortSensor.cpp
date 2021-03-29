#include <sensors/OnDemandSPortSensor.h>

OnDemandSPortSensor::OnDemandSPortSensor(int id, float (*fetchValue)()):
	SPortSensor(id) {
	_fetchValue = fetchValue;
}

sportData OnDemandSPortSensor::getData() {
	sportData data;
	data.sensorId = sensorId;
	data.value = _fetchValue()*precision;
	dataSent = true;
	return data;
}