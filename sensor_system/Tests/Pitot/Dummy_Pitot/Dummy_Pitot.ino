void setup() {
	Serial.begin(115200);
	Serial.println("Début des mesures");
}

void loop() {

	/*Serial.print("Byte 1\t");
	Serial.println(value1, BIN);
	Serial.print("Byte 2\t");
	Serial.println(value2, BIN);

	Serial.print("Assembled value (dec)\t");
	Serial.println(value);
	Serial.print("Assembled value (bin)\t");
	Serial.println(value, BIN);

	Serial.print("Delta_P (PSI): \t");
	Serial.println(diff_psi);*/
	
	Serial.print("Delta_P (Pa):");
	Serial.print(10.123);

	Serial.print("\t");

	Serial.print("Temp (C):");
	Serial.print(23.4);

	// float rho = 1.1689;

	/*Serial.print("Vit (m/s):\t");
	Serial.println(sqrt(2*abs(diff_pa/rho)));*/

	Serial.println();
	delay(150); // Wait 5 seconds for next scan
}
