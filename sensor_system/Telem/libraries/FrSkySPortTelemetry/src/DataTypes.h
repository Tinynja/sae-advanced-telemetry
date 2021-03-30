#ifndef DATATYPES_H
	#define DATATYPES_H

	typedef union {
		char byteValue[4];
		long longValue;
	} longHelper;

	struct sportData {
		long value = 0; // 4-byte value
		int sensorId = 0; // 2-byte id
	};

	struct multiFloat {
		float value0 = 0;
		float value1 = 0;
		float value2 = 0;
	};
	
#endif