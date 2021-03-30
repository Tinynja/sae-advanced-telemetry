# Pour que ce programme fonctionne, il a besoin de recevoir les variables suivantes : 
GS            = 11.1
HDG_GS        = 360
WS            = 12
HDG_WS        = 135
VerticalSpeed = 0.0
target_alt    = 0.0
plane_alt     = 85
finesse       = 2.36
vitesse_verticale = 4.35
#pour l'instant, les valeurs ci-dessus sont des valeurs bidons






from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
def calculate_glide(finesse, vitesse_verticale, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, VerticalSpeed):
	hauteur = (plane_alt - target_alt)*0.3048
	temps_de_descente = hauteur/vitesse_verticale


	t = temps_de_descente
	dx = hauteur*finesse/0.3048

	Gx = GS * math.cos(math.pi/180 * (90 - HDG_GS)) 
	Gy = GS * math.sin(math.pi/180 * (90 - HDG_GS))
	Gz = VerticalSpeed
	Wx = WS * math.cos(math.pi/180 * (90 - HDG_WS)) 
	Wy = WS * math.sin(math.pi/180 * (90 - HDG_WS))
	Wz = 0
	return dx, t
	

dx, t = calculate_glide(finesse, vitesse_verticale, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, VerticalSpeed)
print('distance de plannée sans vent = ' + str(dx))
print('temps de plannée              = ' + str(t))
