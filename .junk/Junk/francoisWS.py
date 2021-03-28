
import math

def calculate_wind_direction(TAS, HDG_TAS, GS, HDG_GS):
	A = GS
	theta_A = 90 - HDG_GS
	B = TAS
	theta_B = 90 - HDG_TAS
	sigma_A = math.pi/180 * theta_A
	sigma_B = math.pi/180 * theta_B
	num   = A*math.sin(sigma_A) - B*math.sin(sigma_B)
	denum = A*math.cos(sigma_A) - B*math.cos(sigma_B)
	sigma_C = math.atan2(num, denum)
	theta_C = sigma_C * 180/math.pi
	HDG_WS = 90 - theta_C
	C = (A*math.cos(sigma_A) - B*math.cos(sigma_B))/math.cos(sigma_C)
	WS = C
	return HDG_WS, WS


#            calculate_wind_direction(TAS,       HDG_TAS,       GS,   HDG_GS)
HDG_WS, WS = calculate_wind_direction(2.236068, 26.56505, 1.802775, 326.3099)
print(HDG_WS)
print(WS)