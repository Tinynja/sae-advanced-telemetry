#define SPORT_START 0x7E
#define SENSOR_ID 0x00

byte buff[2]; // [0x7E, sensor_id, TEMPORARY]

void trash(size_t n);


byte GetChecksum(byte data[], int len){
	int total = 0;
	// 1. Sum all the bytes of the packet
	for(int i = 0; i < len; i++) {
		total += data[i];
	}
	// 2. Add the carry bits so that we only have 8 bits
	total = (total & 0xFF) + (total >> 8);
	// 3. Substract total from 0xFF
	return 0xFF - total;
}

void setup() {
	Serial.begin(57600);
}

void loop() {
	if (Serial.available() > 2) {
		// We are late, trash the earliest bytes because
		// we only need to listen to the 2 latest bytes.
		Serial.read();
	} else if (Serial.available()) {
		buff[1] = Serial.read();
		if (buff[1] == SPORT_START) {
			// We store '#' in the buffer because we expect to
			// receive a sensor_id next.
			buff[0] = buff[1];
		} else if (buff[0] == SPORT_START && buff[1] == SENSOR_ID) {
			// If we got '#' followed by the correct sensor_id, then it's
			// our turn to respond with our dummy data.
			byte data[8] = {0x10, 0x00, 0x02, 0x7B, 0x00, 0x00, 0x00};
			data[7] = GetChecksum(data, 7);
			// Since we also RX what we TX, we also need to trash
			// what we just sent to avoid triggering ourselves.
			trash(Serial.write(data, 8));
			buff[0] = 0;
		} else {
			// Unkown byte OR wrong sensor_id, reset the buffer.
			buff[0] = 0;
		}
	}
}

void trash(size_t n_bytes) {
	// Data doesn't instantaneously go from TX to RX, so we sometimes
	// need to wait up to [timeout] milliseconds for it to arrive.
	int timeout = 100;
	int timer = millis();
	while (Serial.available() != n_bytes && millis()-timer < timeout);
	for (int i=0; i<n_bytes; i++)
		Serial.read();
}
