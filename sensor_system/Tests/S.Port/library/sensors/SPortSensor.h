#ifndef SPORTSENSOR_H
	#define SPORTSENSOR_H

	// #include <SPort.h>
	#include <dataTypes.h>
	#include <sensors/SPortStandardSensorIDs.h>
	#include <stdlib.h> // abs()
	#include <math.h> // fmod()

	class SPortSensor {
		public:
			SPortSensor(int id); // Static value
			SPortSensor(int id, void (*updateValue)(SPortSensor*)); // Value on-demand
			sportData getData ();
			void setValue(float value);
			void setValue(float value0, float value1, float value2);
			bool dataSent;
			int sensorId;
			int typeId;
			int precision;
			int pollsNeeded;
			int pollCount;
			multiFloat rawValue;
		private:
			void ScanIdType();
			bool CheckIdType(int id, int ref_id);
			long prepareValue();
			void (*_updateValue)(SPortSensor*);
			bool isOnDemand;
	};

#endif