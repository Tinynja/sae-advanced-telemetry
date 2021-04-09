const int current_center = 511; // Center value of the current sensor (can be adjusted in the transmitter)
float sensitivity = 39.5; // Sensitivity of the current sensor (in mV/A)

void setup() {
  pinMode(A0, INPUT);
  sensitivity = sensitivity/5000*1023; // Convert the sensitivity from mV/A to analogRead/A to speed up calculations
}

void loop() {
  Serial.println((current_center-analogRead(A0))/sensitivity);
}