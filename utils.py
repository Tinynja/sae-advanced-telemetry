# Built-in libraries
import math
import re

# Pipy libraries
from PyQt5.QtWidgets import QProxyStyle, QStyle
from PyQt5.QtCore import Qt


class MutableObject:
	pass

def calculate_distance(lat1, lon1, lat2, lon2):
	# Radius of the earth in meters
	R = 6371e3
	# Unit conversion to radians
	lat1 = math.radians(lat1)
	lon1 = math.radians(lon1)
	lat2 = math.radians(lat2)
	lon2 = math.radians(lon2)
	delta_lat = (lat2-lat1)
	delta_lon = (lon2-lon1)
	# Haverside
	a = math.sin(delta_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon/2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = R * c # in metres
	return d

def calculate_heading(lat1, lon1, lat2, lon2):
	# Radius of the earth in meters
	R = 6371e3
	# Unit conversion to radians
	lat1 *= math.pi/180
	lon1 *= math.pi/180
	lat2 *= math.pi/180
	lon2 *= math.pi/180
	delta_lat = (lat2-lat1)
	delta_lon = (lon2-lon1)
	# Bearing calculation
	y = math.sin(delta_lon) * math.cos(lat2)
	x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(delta_lon)
	theta = math.atan2(y, x)
	hdg = math.degrees(theta) % 360 # in degrees
	return hdg

def convert_degminsec_to_deg(text):
	values = re.split(r'[°\'"]', text.upper())
	sign = (1 if values.pop(-1) in ('N', 'E') else -1)
	values = list(map(float, values))
	return sign*(values[0]+values[1]/60+values[2]/3600)

class InvalidComboBoxStyle(QProxyStyle):
	# def __init__(self, current_style):
	# 	super().__init__()
	# 	self.current_style = current_style

	def drawControl(self, element, option, painter, widget):
		if element == QStyle.CE_ComboBoxLabel:
			painter.setPen(Qt.red)
			font = painter.font()
			font.setBold(True)
			painter.setFont(font)
		QProxyStyle.drawControl(self, element, option, painter, widget)


# app = QApplication([])

# style = MyProxyStyle()
# # app.setStyle(style)

# cb = QComboBox()
# cb.addItem("Option 1")
# cb.addItem("Option 2")
# cb.addItem("Option 3")
# cb.show()
# cb.setStyle(style)
# app.exec()