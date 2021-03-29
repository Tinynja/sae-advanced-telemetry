bool InArray(byte table, byte value) {
	Serial.println(sizeof(*table));
	//for (int i=0; i<len; i++) {
	//  if (array[i] == value)
	//    return true;
	//}
	//return false;
}

void setup() {
	Serial.begin(115200);
	byte test[] = {12, 23, 45, 67};
	InArray(test, 123);
}

void loop() {
}

