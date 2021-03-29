#include <SPortHub.h>

SPortHub::SPortHub(int hubId):
	_hubId(hubId), // Range: 0-27
	_sensorIndex(0) {
}

void SPortHub::begin() {
	Serial.begin(SPORT_BAUD);
}

void SPortHub::registerSensor(SPortSensor& sensor) {
	//Check if the new sensor's id hasn't already been taken
	//Otherwise assign a new one
	SPortSensor** newSensors = new SPortSensor*[_sensorCount + 1];
	//Duplicate the current sensors array
	for(int i = 0; i < _sensorCount; i++) {
		newSensors[i] = _sensors[i];
	}
	//Add the new sensor
	newSensors[_sensorCount] = &sensor;
	// ¯\_(ツ)_/¯
	if(_sensors != nullptr) {
		free(_sensors);
	}
	_sensors = newSensors;
	_sensorCount++;
}

void SPortHub::handle() {
	while (Serial.available() > 2) {
		// We are late, trash the earliest bytes because
		// we only need to listen to the 2 latest bytes
		// to figure out if the sensor is polling us.
		Serial.read();
	}
	// Just in case the receiver is not connected
	if (Serial.available() == 2 && Serial.read() == SPORT_POLL) {
		byte newByte = Serial.read();
		if ((_hubId == 0xFF || (newByte & 0x1F) == _hubId) && Serial.available() == 0) {
			SendSensor();
		}
	}
}

void SPortHub::SendSensor() {
	if (_sensorCount == 0) {
		return;
	}
	//Send the data of the current sensor
	sportData data = _sensors[_sensorIndex]->getData();
	SendData(data, SPORT_HEADER_DATA);
	//If the current sensor is dataSent sending its data (e.g. GPS must
	//send its data on multiple polls), select the next sensor
	//for the next poll
	if (_sensors[_sensorIndex]->dataSent) {
		_sensors[_sensorIndex]->dataSent = false;
		_sensorIndex = (_sensorIndex+1)%_sensorCount;
	}
}

void SPortHub::SendData(sportData data, int header) {
	//longHelper helps to swap endianness of a long
    longHelper lh;
    lh.longValue = data.value;
	//Construct the frame (with the correct endianness)
	byte frame[8];
	frame[0] = header;    
	frame[1] = lowByte(data.sensorId);
	frame[2] = highByte(data.sensorId);
	frame[3] = lh.byteValue[0];
	frame[4] = lh.byteValue[1];
	frame[5] = lh.byteValue[2];
	frame[6] = lh.byteValue[3];
	frame[7] = GetChecksum(frame, 7);
	//Send the frame
	for(short i = 0; i < 8; i++)
		SendByte(frame[i]);
}

byte SPortHub::GetChecksum(byte data[], int len) {
	int total = 0;
	//1. Sum all the bytes of the packet
	for(int i = 0; i < len; i++) {
		total += data[i];
	}
	//2. Add the carry bits so that we only have 8 bits
	total = (total & 0xFF) + (total >> 8);
	//3. Substract total from 0xFF
	return 0xFF - total;
}

// Send a data byte the FrSky way
void SPortHub::SendByte(byte B) {
	if(B == 0x7E) {
		Serial.write(0x7D);
		Serial.write(0x5E);
	} else if(B == 0x7D) {
		Serial.write(0x7D);
		Serial.write(0x5D);
	} else {
		Serial.write(B);
	}
}