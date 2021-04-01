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



from mpl_toolkits.mplot3d import Axes3D
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
	t = t + temps_flare
	# distance_planee_regime_permanent = hauteur*finesse_planeur/0.3048	
	
	ecart_angle_entre_WS_dGS = HDG_target - HDG_WS - 180
	crosswind = WS * math.sin(math.pi/180 * ecart_angle_entre_WS_dGS) #positif si provient de la gauche
	headwind = WS * math.cos(math.pi/180 * ecart_angle_entre_WS_dGS)
	# crosswind = sin(beta)*vitesse_horizontale_planeur
	if vitesse_horizontale_planeur<crosswind:
		erreur = 'vent trop fort et de travers, impossible de compenser'
		#mettre un break ici TODO-->Amine
	beta_rad = math.asin(crosswind/vitesse_horizontale_planeur)
	beta_deg = beta_rad * 180/math.pi
	GS_planeur_vers_target = vitesse_horizontale_planeur - headwind
	distance_franchissable_en_planee = distance_franchissable_en_planee + t * GS_planeur_vers_target

	return distance_franchissable_en_planee, t, crosswind, headwind, beta_deg, best_glide_speed, erreur, GS_planeur_vers_target
	


#EXEMPLE DE ROULEMENT DE LA FONCTION POUR LES PARAMÈTRES SUIVANTS
GS            = 11.1
HDG_GS        = 360
WS            = 5
HDG_WS        = 135
HDG_target    = 360
Initial_Vertical_Speed = 0.0
target_alt    = 0.0
plane_alt     = 55
finesse_planeur = 2.36
taux_descente_planeur = 4.35
#
distance_franchissable_en_planee, t, crosswind, headwind, beta_deg, best_glide_speed, erreur, GS_planeur_vers_target = calculate_glide(finesse_planeur, taux_descente_planeur, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, Initial_Vertical_Speed, HDG_target)
print('distance_franchissable_en_planee en ft = ' + str(distance_franchissable_en_planee/0.3048))
print('temps de plannée              = ' + str(t))
print('vitesse de meilleure plannée  = ' + str(best_glide_speed))
print('Crosswind                     = ' + str(crosswind))
print('Headwind                      = ' + str(headwind))
print('Angle de crabe                = ' + str(beta_deg))
print('GS_planeur_vers_target        = ' + str(GS_planeur_vers_target))
print('Erreur?                       = ' + str(erreur))





##VÉRIFICATION DE L'INFLUENCE DE CHAQUE PARAMÈTRE EN ENTRÉE
glide_range = []

# input = 'finesse'
# array = [2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7] #finesse
# for finesse_planeur in array:

# input = 'vitesse verticale'
# array = [3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
# for taux_descente_planeur in array:

# input = 'plane alt'
# array = [40, 60, 80, 100, 120]
# for plane_alt in array:

# input = 'GS de l avion-mere'
# array = [8, 10, 12, 14, 16]
# for GS in array:

# input = 'HDG_GS de l avion-mère'
# array = [0, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
# for HDG_GS in array:

# input = 'WS (Wind Speed)'
# array = [0, 2, 4, 8, 12]
# for WS in array:

# input = 'HDG_WS'
# array = [0, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
# for HDG_WS in array:

# input = 'Initial vertical speed'
# array = [-3, 0, 3, 6, 7]
# for Initial_Vertical_Speed in array:

# input = 'HDG target (where is target from airplane?)'
# array = [0, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
# for HDG_target in array:


	par1, par2, par3, par4, par5, par6, par7, par8 = calculate_glide(finesse_planeur, taux_descente_planeur, plane_alt, target_alt, GS, HDG_GS, WS, HDG_WS, Initial_Vertical_Speed, HDG_target)
	glide_range.append(par1/0.3048)

plt.plot(array, glide_range)
plt.ylabel('distance franchissable')
plt.xlabel(input)
plt.ylim([0, max(glide_range)])
plt.show()