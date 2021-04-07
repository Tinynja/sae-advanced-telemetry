const int AREF = 1046; // Measured AREF voltage in mV
float sensitivity = 40; // Sensitivity of the current sensor (in mV/A)

int Vcc;
float curr_vdiv;

long readVcc();

void setup() {
  analogReference(INTERNAL);
  pinMode(A0, INPUT);
  Serial.begin(115200);
  Vcc = readVcc(); // measures the Vin of the Arduino
  Serial.println(Vcc);
  curr_vdiv = Vcc/2/AREF; // Calculate the voltage divider on the current sensor
  sensitivity /= curr_vdiv; // Adjust the current sensor sensitivity to the 1.1V range
  sensitivity = sensitivity/AREF*1023; // Convert the sensitivity from mV/A to analogRead_input/A to speed up calculations
}

void loop() {
  // Calculation:
  //   1. Current sensor outputs Vcc/2 when 0A, then lowers 40mV/Ampere
  //   2. 1023 is 0A
  //   3. AREF value needs to be calibrated because we want to measure precisely the amount of 40mV chunks
  //   4. Use the trim pot to calibrate the voltage divier until you get 0A
  Serial.println((1023-analogRead(A0))/sensitivity);
}

long readVcc() {
  long result; // Read 1.1V reference against AVcc
  ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  delay(2); // Wait for Vref to settle
  ADCSRA |= _BV(ADSC); // Convert
  while (bit_is_set(ADCSRA,ADSC));
    result = ADCL;
  result |= ADCH<<8;
  result = 1126400L / result; // Back-calculate AVcc in mV
  return result;
}
