#include <sensors/SPortSensor.h>

SPortSensor::SPortSensor(int id):
	sensorId(id), dataSent(false), precision(1), isOnDemand(false), pollsNeeded(1), polls(0) {
	ScanIdType();
}

SPortSensor::SPortSensor(int id, float (*fetchValue)()):
	sensorId(id), dataSent(false), precision(1), isOnDemand(true), pollsNeeded(1), polls(0), _fetchValue(fetchValue) {
	ScanIdType();
}

sportData SPortSensor::getData() {
	sportData data;
	data.sensorId = sensorId;
	if (isOnDemand) {
		data.value = _fetchValue()*precision;
	} else {
		data.value = value*precision;
	}
	polls++;
	if (polls == pollsNeeded) {
		dataSent = true;
		polls = 0;
	}
	return data;
}

void SPortSensor::ScanIdType() {
	if (CheckIdType(sensorId, SPORT_SENSOR_ALT)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_VARIO)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_CURR)) {
		precision = 10;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_VFAS)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_CELLS)) {
		//NOTE: SPORT_SENSOR_CELLS is not a simple sensor (see CellsSensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_T1)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_T2)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_RPM)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_FUEL)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ACCX)) {
		precision = 1000;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ACCY)) {
		precision = 1000;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ACCZ)) {
		precision = 1000;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_LONG_LATI)) {
		//NOTE: SPORT_SENSOR_GPS_LONG_LATI is not a simple sensor (see GPSLongLatiSensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_ALT)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_SPEED)) {
		precision = 1000;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_COURSE)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_TIME_DATE)) {
		//NOTE: SPORT_SENSOR_GPS_TIME_DATE is not a simple sensor (see GPSTimeDateSensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_A3)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_A4)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_AIR_SPEED)) {
		precision = 10;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_FUEL_QTY)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_POWERBOX_BATT1)) {
		//NOTE: SPORT_SENSOR_POWERBOX_BATT1 is not a simple sensor (see PowerBoxBatt1Sensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_POWERBOX_BATT2)) {
		//NOTE: SPORT_SENSOR_POWERBOX_BATT2 is not a simple sensor (see PowerBoxBatt2Sensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_POWERBOX_STATE)) {
		//NOTE: SPORT_SENSOR_POWERBOX_STATE is not a simple sensor (see PowerBoxStateSensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_POWERBOX_CNSP)) {
		//NOTE: SPORT_SENSOR_POWERBOX_CNSP is not a simple sensor (see PowerBoxCNSPSensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_CHAN)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ESC_V_A)) {
		//NOTE: SPORT_SENSOR_ESC_V_A is not a simple sensor (see ESCVASensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ESC_RPM_ENERGY)) {
		//NOTE: SPORT_SENSOR_ESC_RPM_ENERGY is not a simple sensor (see ESCRPMEnergySensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ESC_TEMP)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_RBES)) {
		//NOTE: SPORT_SENSOR_RBES ¯\_(ツ)_/¯
	} else if (CheckIdType(sensorId, SPORT_SENSOR_CH1A_CH2A)) {
		//NOTE: SPORT_SENSOR_CH1A_CH2A is not a simple sensor (see CH1ACH2ASensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_CH3A_CH4A)) {
		//NOTE: SPORT_SENSOR_CH3A_CH4A is not a simple sensor (see CH3ACH4ASensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_CH5A_CH6A)) {
		//NOTE: SPORT_SENSOR_CH5A_CH6A is not a simple sensor (see CH5ACH6ASensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_CH7A_CH8A)) {
		//NOTE: SPORT_SENSOR_CH7A_CH8A is not a simple sensor (see CH7ACH8ASensor.cpp)
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ENG_T1)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ENG_T2)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ENG_RPM)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ENG_FUEL)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ENG_PERC)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ENG_FUEL_FLOW)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ENG_MFI)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_ENG_AFI)) {
		precision = 1;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_BEC)) {
		//NOTE: SPORT_SENSOR_BEC is not a simple sensor (see BECSensor.cpp)
	}
}

bool SPortSensor::CheckIdType(int id, int ref_id) {
	if (ref_id <= id && id <= ref_id+15) {
		typeId = ref_id;
		return true;
	}
	return false;
}