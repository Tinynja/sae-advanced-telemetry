# Built-in libraries
import math

# Pipy libraries
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# User libraries
from utils import *

class MapUi(QWidget):
	def __init__(self):
		super().__init__()
		
		# Create map image widget
		self.map_pixmap = QPixmap('resources/map.png')
		self.map = QLabel()
		self.map.setScaledContents(True)
		self.map.setMinimumSize(1,1)
		self.map.setPixmap(self.map_pixmap)

		# Create the sidebar buttons
		self.calibration_button = QPushButton('Calibrer')
		self.target_button = QPushButton('Cible')
		self.buttons_overlay = QWidget()
		layout = QGridLayout(self.buttons_overlay)
		layout.addWidget(self.calibration_button, 0, 1)
		layout.setRowStretch(1, 1)
		layout.setColumnStretch(0, 1)

		# Create the calibration status indicator
		self.calibration_status = QLabel()
		self.calibration_status.setVisible(False)
		font = QFont(); font.setBold(True); font.setPointSize(20)
		self.calibration_status.setFont(font)
		shadow = QGraphicsDropShadowEffect(); shadow.setOffset(3); shadow.setColor(Qt.black)
		self.calibration_status.setGraphicsEffect(shadow)
		self.calibration_status.setStyleSheet('color:red')
		self.calibration_status.setAlignment(Qt.AlignCenter)

		# Build the main layout
		self.setContentsMargins(0,0,0,0)
		self.setLayout(QStackedLayout())
		self.layout().setStackingMode(QStackedLayout.StackingMode.StackAll)
		self.layout().addWidget(self.buttons_overlay)
		self.layout().addWidget(self.calibration_status)
		self.layout().addWidget(self.map)

		# Save the original mouse press event
		self._mousePressEvent_backup = self.mousePressEvent
	
	def mousePressEvent_handler(self, event):
		self.calibration_status.setVisible(False)
		regexp = QRegExp(r'([+-]?[0-9]+[.,]?[0-9]*;[+-]?[0-9]+[.,]?[0-9]*)|([0-9]+°[0-9]+\'[0-9]+[.,]?[0-9]*"[NS] [0-9]+°[0-9]+\'[0-9]+[.,]?[0-9]*"[EW])')
		validator = QRegExpValidator(regexp)
		def __validate(text, setText):
			setText(validator.fixup(text))
		pos, ok = self.spawnValidatedInputDialog(__validate, 'Calibration de la carte', 'Entrez la position du point sélectionné (Lat[deg];Long[deg] ou #°#\'#"N #°#\'#"W):')
		if ok and regexp.exactMatch(pos):
			if '°' in pos:
				pos = pos.split(' ')
				pos = [convert_degminsec_to_deg(p) for p in [pos[0], pos[-1]]]
			else:
				pos = list(map(float, pos.split(';')))
			self._new_calibration_points.append({'x':event.x(), 'y':event.y(), 'lat':pos[0], 'lon':pos[1]})
			self._calibration_step += 1
			if self._calibration_step == 1:
				self.calibration_status.setText('Sélectionnez le 2e point dont la position est connue.')
				self.calibration_status.setVisible(True)
			else:
				self.apply_new_calibration()
		else:
			self.cancel_calibration()

	def init_calibration(self):
		self._calibration_step = 0
		self._new_calibration_points = []
		self.calibration_button.setDisabled(True)
		self.calibration_status.setText('Sélectionnez le 1er point dont la position est connue.')
		self.calibration_status.setVisible(True)
		self.mousePressEvent = self.mousePressEvent_handler
	
	def end_calibration(self):
		self.calibration_button.setDisabled(False)
		self.mousePressEvent = self._mousePressEvent_backup
	
	def cancel_calibration(self):
		QMessageBox().warning(self, 'Calibration de la carte', 'Calibration interrompue.')
		self.end_calibration()
	
	def apply_new_calibration(self):
		p = self._new_calibration_points
		# Calculate the angle y axis is making with the north
		self.map_angle = (calculate_heading(p[0]['lat'], p[0]['lon'], p[1]['lat'], p[1]['lon']) - math.degrees(math.atan2(p[1]['y']-p[0]['y'], p[1]['x']-p[0]['x']))-90) % 360
		# Ratio of the pixel distance over latitude/longitude delta
		delta_y = -(p[1]['y']-p[0]['y'])
		delta_x = p[1]['x']-p[0]['x']
		self.lat_pixel_ratio = abs((delta_y*math.cos(math.radians(self.map_angle)) + delta_x*math.sin(math.radians(self.map_angle))) / (p[1]['lat']-p[0]['lat']))
		self.lon_pixel_ratio = abs((delta_y*math.sin(math.radians(self.map_angle)) + delta_x*math.cos(math.radians(self.map_angle))) / (p[1]['lat']-p[0]['lat']))
		# Ratio of the pixel distance over longitude delta
		# self.lon_pixel_ratio = 
		# self.y_distance_ratio = ()/()
		# Calculate lat/long of the origin (x=0, y=0)
		# self.origin = 
		print('Angle:', self.map_angle)
		print('Lat Pixel Ratio:', self.lat_pixel_ratio)
		print('Lon Pixel Ratio:', self.lon_pixel_ratio)
		self.end_calibration()
	
	def spawnValidatedInputDialog(self, validator, *args, **kwargs):
		dialog = QInputDialog()
		dialog.textValueChanged.connect(lambda text: validator(text, dialog.setTextValue))
		return dialog.getText(self, *args, **kwargs)

	
	# def calibration_prompt(self):
	# 	pos = 



if __name__ == '__main__':
	app = QApplication([])
	gps_map = MapUi()
	gps_map.calibration_button.clicked.connect(gps_map.init_calibration)
	gps_map.show()
	app.exec()