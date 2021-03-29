#ifndef STATICSPORTSENSOR_H
	#define STATICSPORTSENSOR_H

	#include <SPort.h>
	
	class StaticSPortSensor : public SPortSensor {
		public:
			StaticSPortSensor(int id);
			sportData getData ();
			float value;
	};

#endif