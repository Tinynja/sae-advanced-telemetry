#ifndef ONDEMANDSPORTSENSOR_H
	#define ONDEMANDSPORTSENSOR_H

	#include <SPort.h>

	class OnDemandSPortSensor : public SPortSensor {
		public:
			OnDemandSPortSensor(int id, float (*fetchValue)());
			sportData getData();
		private:
			float (*_fetchValue)();
	};

#endif