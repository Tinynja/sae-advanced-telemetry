# Pour que ce programme fonctionne, il a besoin de recevoir les variables suivantes : 
GS            = 13.1
HDG_GS        = 360
WS            = 12
HDG_WS        = 135
HDG_target    = 355
VerticalSpeed = 0.0
target_alt    = 0.0
plane_alt     = 85

finesse_planeur = 2.36
vitesse_verticale_planeur = 4.35
#pour l'instant, les valeurs ci-dessus sont des valeurs bidons


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math

vitesse_horizontale_planeur = vitesse_verticale_planeur * finesse_planeur
best_glide_speed = math.sqrt(pow(vitesse_horizontale_planeur, 2) + pow(vitesse_verticale_planeur, 2))

def calculate_glide(finesse_planeur, vitesse_verticale_planeur, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, VerticalSpeed):
	hauteur = (plane_alt - target_alt)*0.3048
	distance_franchie = 0

	Gx = GS * math.cos(math.pi/180 * (90 - HDG_GS)) 
	Gy = GS * math.sin(math.pi/180 * (90 - HDG_GS))
	Gz = VerticalSpeed
	Wx = WS * math.cos(math.pi/180 * (90 - HDG_WS)) 
	Wy = WS * math.sin(math.pi/180 * (90 - HDG_WS))
	Wz = 0
	Ax = Gx - Wx
	Ay = Gy - Wy
	Az = Gz - Wz
	Airspeed  = math.sqrt(pow(Ax, 2) + pow(Ay, 2) + pow(Az, 2))
	uAx = Ax/Airspeed
	uAy = Ay/Airspeed
	uAz = Az/Airspeed

	# m g h = ratio * 0.5 m v2 --> h = ratio * 0.5 * v2 /g
	ratio = 0.6 #perte d'énergie due au drag
	hauteur_sup = (ratio * 0.5 * (pow(Airspeed, 2) - pow(best_glide_speed, 2)))/9.81
	hauteur = hauteur + hauteur_sup
	distance_franchie = distance_franchie + math.cos(math.pi/180 * 45)*hauteur_sup 	#on suppose que le planeur monte à 45 deg vers le haut en étant relâché
	temps_de_descente = hauteur/vitesse_verticale_planeur
	t = temps_de_descente
	temps_flare = 4.0 #secondes
	t = t + temps_flare
	distance_planee_regime_permanent = hauteur*finesse_planeur/0.3048	
	distance_franchie_sans_vent = distance_franchie + distance_planee_regime_permanent
	
	ecart_angle_entre_WS_dGS = HDG_target - HDG_WS - 180
	crosswind = WS * math.sin(math.pi/180 * ecart_angle_entre_WS_dGS) #positif si provient de la gauche
	# crosswind = sin(beta)*vitesse_horizontale_planeur
	beta_rad = math.asin(crosswind/vitesse_horizontale_planeur) #TODO TODO TODO on perd le signe négatif si vent de dos...
	headwind = math.cos(beta_rad)*vitesse_horizontale_planeur# donc le vent de face ressenti est équivalent au headwind

	dx = distance_franchie_sans_vent
	return dx, t, crosswind, headwind
	

dx, t, crosswind, headwind = calculate_glide(finesse_planeur, vitesse_verticale_planeur, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, VerticalSpeed)
print('distance de plannée sans vent = ' + str(dx))
print('temps de plannée              = ' + str(t))
print('vitesse de meilleure plannée  = ' + str(best_glide_speed))
print('Crosswind                     = ' + str(crosswind))
print('Headwind                      = ' + str(headwind))