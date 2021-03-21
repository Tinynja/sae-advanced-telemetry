#include <SoftwareSerial.h>

SoftwareSerial s_port(2, 3, true); // RX, TX, inverted
SoftwareSerial pix(10, 11); // RX, TX

void setup()
{
	// Open serial communications and wait for port to open:
	pix.begin(57600);

	// set the data rate for the SoftwareSerial port
	s_port.begin(57600);
}

void loop() // run over and over
{
	if (s_port.available())
		pix.write(s_port.read());
	if (pix.available())
		s_port.write(pix.read());
}
