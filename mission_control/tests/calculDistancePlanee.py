# Pour que ce programme fonctionne, il a besoin de recevoir les variables suivantes : 
# GS
# HDG_GS 
# WS
# HDG_WS
# HDG_target 
# Initial_Vertical_Speed
# target_alt
# plane_alt
# finesse_planeur
# taux_descente_planeur

import matplotlib.pyplot as plt
import numpy as np
import math


def calculate_glide(finesse_planeur, taux_descente_planeur, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, Initial_Vertical_Speed, HDG_target):
	vitesse_horizontale_planeur = taux_descente_planeur * finesse_planeur
	best_glide_speed = math.sqrt(pow(vitesse_horizontale_planeur, 2) + pow(taux_descente_planeur, 2))
	hauteur = (plane_alt - target_alt)*0.3048
	distance_franchissable_en_planee = 0
	erreur = 'pas derreur'

	Gx = GS * math.cos(math.pi/180 * (90 - HDG_GS)) 
	Gy = GS * math.sin(math.pi/180 * (90 - HDG_GS))
	Gz = Initial_Vertical_Speed
	Wx = WS * math.cos(math.pi/180 * (90 - HDG_WS)) 
	Wy = WS * math.sin(math.pi/180 * (90 - HDG_WS))
	Wz = 0
	Ax = Gx - Wx 
	Ay = Gy - Wy 
	Az = Gz - Wz 
	Airspeed  = math.sqrt(pow(Ax, 2) + pow(Ay, 2) + pow(Az, 2))

	# m g h = ratio * 0.5 m v2 --> h = ratio * 0.5 * v2 /g
	ratio = 0.6 #perte d'énergie due au drag
	hauteur_sup = (ratio * 0.5 * (pow(Airspeed, 2) - pow(best_glide_speed, 2)))/9.81
	hauteur = hauteur + hauteur_sup
	distance_franchissable_en_planee = distance_franchissable_en_planee + math.cos(math.pi/180 * 45)*hauteur_sup 	#on suppose que le planeur monte à 45 deg vers le haut en étant relâché
	temps_de_descente = hauteur/taux_descente_planeur
	t = temps_de_descente
	temps_flare = 4.0 #secondes
	t = t + temps_flare * math.sqrt(0.5) # prendre en compte la vitesse moyenne quadratique lors du flare
	# distance_planee_regime_permanent = hauteur*finesse_planeur/0.3048	
	
	ecart_angle_entre_WS_dGS = HDG_target - HDG_WS - 180
	crosswind = WS * math.sin(math.pi/180 * ecart_angle_entre_WS_dGS) #positif si provient de la gauche
	headwind = WS * math.cos(math.pi/180 * ecart_angle_entre_WS_dGS)
	# crosswind = sin(beta)*vitesse_horizontale_planeur
	if vitesse_horizontale_planeur<crosswind:
		erreur = 'vent trop fort et de travers, impossible de compenser'
		distance_franchissable_en_planee = 0
		GS_planeur_vers_target = 0
		GS_planeur_laterale = 0
	else:
		beta_rad = math.asin(crosswind/vitesse_horizontale_planeur)
		# beta_deg = beta_rad * 180/math.pi
		GS_planeur_vers_target = math.cos(beta_rad) * vitesse_horizontale_planeur - headwind
		GS_planeur_laterale    = math.sin(beta_rad) * vitesse_horizontale_planeur - crosswind
		distance_franchissable_en_planee = distance_franchissable_en_planee + t * GS_planeur_vers_target

	dx = distance_franchissable_en_planee * math.cos(math.pi/180 * (90-HDG_target))
	dy = distance_franchissable_en_planee * math.sin(math.pi/180 * (90-HDG_target))

	return dx, dy, erreur, GS_planeur_vers_target, GS_planeur_laterale, t
	


#EXEMPLE DE ROULEMENT DE LA FONCTION POUR LES PARAMÈTRES SUIVANTS
GS            = 11.1      
HDG_GS        = 360
WS            = 5.0
HDG_WS        = 60
HDG_target    = 360
Initial_Vertical_Speed = 0.0
target_alt    = 0.0
plane_alt     = 55.0
finesse_planeur = 2.36
taux_descente_planeur = 4.35
#
dx, dy, erreur, GS_to, GS_lat, t = calculate_glide(finesse_planeur, taux_descente_planeur, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, Initial_Vertical_Speed, HDG_target)
print('dx et ft = ' + str(dx))
print('dy et ft = ' + str(dy))
print('erreur   = ' + str(erreur))
print('GS vers la cible   = ' + str(GS_to))
print('GS latéralement   = ' + str(GS_lat))
print('temps de vol   = ' + str(t))



# ##VÉRIFICATION DE L'INFLUENCE DE CHAQUE PARAMÈTRE EN ENTRÉE
# glide_range_x = []
# glide_range_y = []


# array = [0, 2,4,6,8,9,9.9,10,10.1,10.2,10.3,10.4]
# for WS in array:


# 	dx, dy, erreur, GS_to, GS_lat, t  = calculate_glide(finesse_planeur, taux_descente_planeur, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, Initial_Vertical_Speed, HDG_target)
# 	glide_range_x.append(dx)
# 	glide_range_y.append(dy)

# plt.plot(glide_range_x, glide_range_y)
# plt.ylabel('y')
# plt.xlabel('x')
# # plt.ylim([0, max(glide_range_x)])
# plt.show()