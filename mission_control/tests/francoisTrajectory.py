# Pour que ce programme fonctionne, il a besoin de recevoir les variables suivantes : 
GS            = 11.1
HDG_GS        = 270
WS            = 0.1
HDG_WS        = 180
VerticalSpeed = 0.0
target_alt    = 0.0
plane_alt     = 150
Area          = 0.00502
mass          = 0.117
CD            = 0.350
#pour l'instant, les valeurs ci-dessus sont des valeurs bidons

import time


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
def calculate_acceleration(CD, Area, m, rho, Gx, Gy, Gz, Wx, Wy, Wz):
	# A = Object's Airspeed
	# G = Object's groundspeed
	# W = Windspeed
	Ax = Gx - Wx
	Ay = Gy - Wy
	Az = Gz - Wz
	Airspeed  = math.sqrt(pow(Ax, 2) + pow(Ay, 2) + pow(Az, 2))
	uAx = Ax/Airspeed
	uAy = Ay/Airspeed
	uAz = Az/Airspeed
	# F = m*a --> m = F/m
	q = 0.5 * rho * pow(Airspeed, 2)
	F = CD*q*Area
	Fx = F * uAx
	Fy = F * uAy
	Fz = F * uAz
	#a= acceleration
	ax = -Fx/m
	ay = -Fy/m
	az = -Fz/m
	gz = -9.81 #m/s2
	az = az + gz
	return ax, ay, az

#Initial parameters
t = 0
dt = 0.01
dx_parcouru = 0
dy_parcouru = 0
dz_parcouru = 0
hauteur = 0.3048*(plane_alt - target_alt)
Gx = GS * math.cos(math.pi/180 * (90 - HDG_GS)) 
Gy = GS * math.sin(math.pi/180 * (90 - HDG_GS))
Gz = VerticalSpeed
Wx = WS * math.cos(math.pi/180 * (90 - HDG_WS)) 
Wy = WS * math.sin(math.pi/180 * (90 - HDG_WS))
Wz = 0
arr_t = np.array([t])
arr_dx = np.array([dx_parcouru])
arr_dy = np.array([dy_parcouru])
arr_dz = np.array([dz_parcouru])


start_time = time.time()

while dz_parcouru < hauteur:
	#            calculate_acceleration(CD, Area, mass,   rho,  Gx, Gy, Gz, Wx, Wy, Wz)
	ax, ay, az = calculate_acceleration(CD, Area, mass, 1.225,  Gx, Gy, Gz, Wx, Wy, Wz)

	#a = V/t --> V = V0 + a*t
	Gx2 = Gx + ax*dt
	Gy2 = Gy + ay*dt
	Gz2 = Gz + az*dt
	t  = t  + dt
	dx_parcouru = dx_parcouru + dt*(Gx2 + Gx)/2
	dy_parcouru = dy_parcouru + dt*(Gy2 + Gy)/2
	dz_parcouru = dz_parcouru - dt*(Gz2 + Gz)/2
	Gx = Gx2
	Gy = Gy2
	Gz = Gz2
	arr_t2 = np.array([t])
	arr_dx2 = np.array([dx_parcouru])
	arr_dy2 = np.array([dy_parcouru])
	arr_dz2 = np.array([dz_parcouru])
	arr_t = np.concatenate((arr_t, arr_t2))
	arr_dx = np.concatenate((arr_dx, arr_dx2))
	arr_dy = np.concatenate((arr_dy, arr_dy2))
	arr_dz = np.concatenate((arr_dz, arr_dz2))

diff_hauteur = hauteur - dz_parcouru

print('t calcul = ' + str(time.time()-start_time))
print('t total = ' + str(t))
print('ax      = ' + str(ax))
print('ay      = ' + str(ay))
print('az      = ' + str(az))
print('dx      = ' + str(dx_parcouru))
print('dy      = ' + str(dy_parcouru))
print('dz      = ' + str(dz_parcouru))
print('diff h  = ' + str(diff_hauteur/(dt*(Gz2 + Gz)/2)*100) + '%')


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X = arr_dx
Y = arr_dy
Z = (-arr_dz + hauteur)/0.3048
ax.scatter(X, Y, Z, c='r', marker='o')
ax.set_xlabel('X longitude relative (m)')
ax.set_ylabel('Y latitude relative (m)')
ax.set_zlabel('Z Altitude (ft)')
# Create cubic bounding box to simulate equal aspect ratio
max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')
plt.show()