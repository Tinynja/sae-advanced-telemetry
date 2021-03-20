#include "MPU6050_light.h"
#include "Arduino.h"

CustomPitot::CustomPitot(){
	Wire.beginTransmission(0x28);
	Wire.write(0x00);
	Wire.endTransmission();
}

/*float CustomPitot::getDeltaP(){
	int16_t dp_raw = getDP_Raw();
	
	float diff_psi = ((dp_raw - 0.1f * 16383) * (P_max - P_min) / (0.8f * 16383) + P_min);
    float diff_pa = diff_psi*PSI_2_Pa;
}*/

std::vector<float> CustomPitot::getAll(){
	Wire.requestFrom(0x28,4);

	byte value1 = Wire.read();
	byte value2 = Wire.read();
	byte value3 = Wire.read();
	byte value4 = Wire.read();

	int16_t dp = value1 << 8 | value2;
	dp = (0x3FFF) & dp;

	int16_t dT = value3 << 8 | value4;
	dT = ((0xFFE0) & dT) >> 5;

	const float P_min = -1.0f;
	const float P_max = 1.0f;
	const float conv = 6894.757;
	float diff_psi = ((dp - 0.1f * 16383) * (P_max - P_min) / (0.8f * 16383) + P_min);
	float diff_pa = diff_psi*conv - bias;
	float temp = ((200.0f * dT) / 2047) - 50;
	
	std::vector<float> allvector;
	
	allvector.push(diff_pa);
	allvector.push(temp);
}

/*int16_t CustomPitot::getDP_Raw(){
	Wire.requestFrom(0x28,2);

	byte value1 = Wire.read();
	byte value2 = Wire.read();

	int16_t dp = value1 << 8 | value2;
	dp = (0x3FFF) & dp;
	
	return dp;
}*/

/*std::vector<int16_t> CustomPitot::getAllRaw(){
	
}*/


float CustomPitot::Calibrate(int nSamples){
	
	 for (int i = 0; i < nSamples; i++) {
      Wire.requestFrom(PITOT_ADDR,2);

      byte value1 = Wire.read();
      byte value2 = Wire.read();
    
      int16_t dp = value1 << 8 | value2;
      dp = (0x3FFF) & dp;
    
      
      float diff_psi = ((dp - 0.1f * 16383) * (P_max - P_min) / (0.8f * 16383) + P_min);
      float diff_pa = diff_psi*PSI_2_Pa;

      sum += diff_pa;
      delay(50);
	
	}
  
  p_bias = sum / nSamples;
  
  return p_bias;
}