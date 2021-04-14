import math
import matplotlib.pyplot as plt

def switch_coord_sys(Latitude, Longitude, Angle, Latitude_top_left, Longitude_top_left):
	Angle = -Angle
	Latitude_relative = Latitude - Latitude_top_left
	Longitude_relative = Longitude - Longitude_top_left
	Angle = Angle * math.pi/180
	x = (Longitude_relative - Latitude_relative * math.tan(Angle))*math.cos(Angle)
	y = -(Latitude_relative/math.cos(Angle) + (Longitude_relative - Latitude_relative * math.tan(Angle)) * math.sin(Angle))

	return x, y



#Exemple de code
Angle = 45

x1, y1 = switch_coord_sys(45.197902, -73.653736, Angle, 45.197902, -73.653736)
x2, y2 = switch_coord_sys(45.199800, -73.655646, Angle, 45.197902, -73.653736)
x3, y3 = switch_coord_sys(45.201569, -73.654562, Angle, 45.197902, -73.653736)
x4, y4 = switch_coord_sys(45.201032, -73.653167, Angle, 45.197902, -73.653736)
x5, y5 = switch_coord_sys(45.199701, -73.652191, Angle, 45.197902, -73.653736)
x6, y6 = switch_coord_sys(45.198666, -73.649777, Angle, 45.197902, -73.653736)
x7, y7 = switch_coord_sys(45.199089, -73.652556, Angle, 45.197902, -73.653736)

print(x1)
print(y1)



plt.plot([x1, x2, x3, x4, x5, x6, x7], [y1, y2, y3, y4, y5, y6, y7])
plt.ylabel('y')
plt.xlabel('x')
# plt.ylim([0, max(glide_range_x)])
plt.show()