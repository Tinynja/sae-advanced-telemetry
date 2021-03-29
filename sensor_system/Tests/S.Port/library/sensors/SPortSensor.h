#ifndef SPORTSENSOR_H
	#define SPORTSENSOR_H

	// #include <SPort.h>
	#include <dataTypes.h>
	#include <sensors/SPortStandardSensorIDs.h>

	class SPortSensor {
		public:
			SPortSensor(int id); // Static value
			SPortSensor(int id, float (*fetchValue)()); // Value on-demand
			sportData getData ();
			bool dataSent;
			int sensorId;
			int typeId;
			int precision;
			int pollsNeeded;
			int polls;
			float value;
		private:
			void ScanIdType();
			bool CheckIdType(int id, int ref_id);
			float (*_fetchValue)();
			bool isOnDemand;
	};

#endif