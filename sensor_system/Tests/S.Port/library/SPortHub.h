#ifndef SPORTHUB_H
	#define SPORTHUB_H

	#include <SPort.h>
	#include <SoftwareSerial.h> //debug

	class SPortHub {
		public:
			SPortHub(int hubId);
			void begin();
			void registerSensor(SPortSensor& sensor);
			void handle();
		private:
			void SendSensor();
			void SendData(sportData data, int header);
			void SendByte(byte B);
			byte GetChecksum(byte data[], int len);

			SoftwareSerial* mySerial; //debug

			SPortSensor** _sensors;
			int _hubId;
			int _sensorIndex;
			int _sensorCount;
	};
	
#endif