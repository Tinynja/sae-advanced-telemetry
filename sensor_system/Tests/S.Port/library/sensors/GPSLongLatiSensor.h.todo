#ifndef GPSLONGLATISENSOR_H
	#define GPSLONGLATISENSOR_H

	#include <SPort.h>
	
	class GPSLontLatiSensor : public SPortSensor {
		public: 
			GPSLontLatiSensor(int id); // Static value
			GPSLontLatiSensor(int id, float (*fetchValue)()); // Value on-demand
			float formatValue();
		private:
			char _NMEA[128];
	};

#endif