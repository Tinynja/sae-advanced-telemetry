#include <Wire.h>

void setup() {
	Wire.begin();

	Serial.println("Début des mesures");
	
	Serial.begin(115200);
}

void loop() {

	Wire.beginTransmission(0x28);
	Wire.write(0x00);
	Wire.endTransmission();

	Wire.requestFrom(0x28,4);

	byte value1 = Wire.read();
	byte value2 = Wire.read();
	byte value3 = Wire.read();
	byte value4 = Wire.read();

	int16_t dp = value1 << 8 | value2;
	dp = (0x3FFF) & dp;

	int16_t dT = value3 << 8 | value4;
	dT = ((0xFFE0) & dT) >> 5;

	const float P_min = -1.0f;
	const float P_max = 1.0f;
	const float conv = 6894.757;
	float diff_psi = ((dp - 0.1f * 16383) * (P_max - P_min) / (0.8f * 16383) + P_min);
	float diff_pa = diff_psi*conv;
	float temp = ((200.0f * dT) / 2047) - 50;

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
	Serial.print(diff_pa);
	Serial.print("\t")

	float rho = 1.1689;

	/*Serial.print("Vit (m/s): \t");
	Serial.println(sqrt(2*abs(diff_pa/rho)));*/

	/*Serial.print("Temp (C): \t");
	Serial.println(temp);*/

	Serial.println()
	delay(150); // Wait 5 seconds for next scan
}
