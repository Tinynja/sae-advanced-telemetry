#ifndef CUSTOM_PITOT_H
#define CUSTOM_PITOT_H

#include "Arduino.h"
#include "Wire.h"
#include <vector>

#define PITOT_ADDR	0x28

class CustomPitot{
	public:
	
	MPU6050();
	
	//float getDeltaP();
	std::vector<float> getAll();
	
	//int16_t getDP_Raw();
	//std::vector<int16_t> getAllRaw();
	
	//float getVelocity();
	
	float getPressureBias() { return p_bias; };
	
	float calibrate(int nSamples);
	
	private:
		float p_bias;
		
		const float P_min = -1.0f;
		const float P_max =  1.0f;
		const float PSI_2_Pa = 6894.757;
}

#endif