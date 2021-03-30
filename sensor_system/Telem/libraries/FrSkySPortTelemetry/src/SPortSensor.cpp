#include <SPortSensor.h>

SPortSensor::SPortSensor(int id):
	sensorId(id), dataSent(false), precision(1), isOnDemand(false), pollsNeeded(1), pollCount(0) {
	ScanIdType();
}

SPortSensor::SPortSensor(int id, void (*updateValue)(SPortSensor*)):
	sensorId(id), dataSent(false), precision(1), isOnDemand(true), pollsNeeded(1), pollCount(0), _updateValue(updateValue) {
	ScanIdType();
}

sportData SPortSensor::getData() {
	sportData data;
	data.sensorId = sensorId;
	data.value = prepareValue();
	pollCount++;
	if (pollCount == pollsNeeded) {
		dataSent = true;
		pollCount = 0;
	}
	return data;
}

long SPortSensor::prepareValue() {
	//If the sensor is OnDemand type, fetch the new value (any type)
	if (isOnDemand) {
		_updateValue(this);
		//Depending on the sensor type, different post-processing of the rawValue is required
		// long result;
		if (typeId == SPORT_SENSOR_GPS_LATI_LONG) {
			//RMC NMEA: $GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
			//RMC NMEA: MSGID,TIME,STATUS,LAT,N/S,LONG,E/W,SPEED,HEADING,DATE,MAGNETIC_VAR,CHECKSUM
			//SPort GPS Data:
			//  b1-28: minutes*10000
			//  b30: N/E(0) or S/W(1)
			//	b31: Lat(0) or Long(1)
			int degrees = abs(rawValue.value0)/100;
			float minutes = fmod(abs(rawValue.value0),100);
			long isLongitude = pollCount;
			long isSouthOrWest = rawValue.value0 < 0;
			return (long) ((degrees*60+minutes)*precision+0.5) | (isLongitude << 31) | (isSouthOrWest << 30);
		} else if (typeId == SPORT_SENSOR_GPS_TIME_DATE) {
			//SPort Time/Date Data:
			//  b24-31: Year or Hour
			//  b16-23: Month or Minute
			//  b8-15: Seconds or Day
			//  Any b0-7: Time(0) or Date(1)
			long YearOrHour = (long) rawValue.value0 << 24;
			long MonthOrMinute = (long) rawValue.value1 << 16;
			long SecondsOrDay = (long) rawValue.value2 << 8;
			short isDate = pollCount;
			return YearOrHour | MonthOrMinute | SecondsOrDay | isDate;
		} //TODO: Other not simple sensors
	}
	return rawValue.value0*precision;
}

void SPortSensor::setValue(float value) {
	rawValue.value0 = value;
}

void SPortSensor::setValue(float value0, float value1, float value2) {
	rawValue.value0 = value0;
	rawValue.value1 = value1;
	rawValue.value2 = value2;
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
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_LATI_LONG)) {
		precision = 10000;
		pollsNeeded = 2;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_ALT)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_SPEED)) {
		precision = 1000;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_COURSE)) {
		precision = 100;
	} else if (CheckIdType(sensorId, SPORT_SENSOR_GPS_TIME_DATE)) {
		precision = 1;
		pollsNeeded = 2;
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