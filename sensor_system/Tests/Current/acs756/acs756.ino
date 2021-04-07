const int AREF = 1046; // Measured AREF voltage in mV
float sensitivity = 39.5; // Sensitivity of the current sensor (in mV/A)


float curr_center; //Offset from 1023/2=511.5 of the current sensor when 0A is applied
//int Vcc;
//float curr_vdiv;

//long readVcc();

void setup() {
//  analogReference(INTERNAL);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  Serial.begin(115200);
//  Vcc = readVcc(); // measures the Vin of the Arduino
//  Serial.println(Vcc);
//  curr_vdiv = Vcc/2/AREF; // Calculate the voltage divider on the current sensor
//  sensitivity /= curr_vdiv; // Adjust the current sensor sensitivity to the 1.1V range
  sensitivity = sensitivity/5000*1023; // Convert the sensitivity from mV/A to analogRead_input/A to speed up calculations
//  Serial.println(sensitivity);
}

void loop() {
  //Serial.println(analogRead(A0));
  curr_center = 1023*0.5*(1-0.1)+analogRead(A1)*0.1;
  Serial.println((curr_center-analogRead(A0))/sensitivity);
}

//long readVcc() {
//  long result; // Read 1.1V reference against AVcc
//  ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
//  delay(2); // Wait for Vref to settle
//  ADCSRA |= _BV(ADSC); // Convert
//  while (bit_is_set(ADCSRA,ADSC));
//    result = ADCL;
//  result |= ADCH<<8;
//  result = 1126400L / result; // Back-calculate AVcc in mV
//  return result;
//}
