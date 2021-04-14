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

		# No action
		self._no_action = lambda e: None

		# Variables
		self.target_coords = [None, None]
		self.target_radius_1 = 3 # meters
		self.target_radius_2 = 15.24 # meters
		self.target_radius_3 = 60.96 # meters
		
		# Create map image widget
		self.map_pixmap = QPixmap('resources/map.png')
		self.map = QLabel()
		# self.map.setScaledContents(True)
		# self.map.setMinimumSize(1,1)
		self.map.setPixmap(self.map_pixmap)

		# Create map painter overlay widget
		self.map_drawing_layer = QLabel()
		# self.map_drawing_layer.paintEvent = self._no_action
		# self.mapPaintEvent = lambda e: None
		self.map_drawing_layer.paintEvent = self.mapPaintEvent

		# Create the sidebar buttons
		self.calibration_button = QPushButton('Calibrer')
		self.target_button = QPushButton('Cible')
		self.target_button.setDisabled(True)
		self.test_button = QPushButton('Test')
		self.buttons_overlay = QWidget()
		layout = QGridLayout(self.buttons_overlay)
		layout.addWidget(self.calibration_button, 0, 1)
		layout.addWidget(self.target_button,1, 1)
		layout.addWidget(self.test_button,2, 1)
		layout.setRowStretch(3, 1)
		layout.setColumnStretch(0, 1)

		# Create the calibration status indicator
		self.helper_text = QLabel()
		self.helper_text.setVisible(False)
		font = QFont(); font.setBold(True); font.setPointSize(20)
		self.helper_text.setFont(font)
		shadow = QGraphicsDropShadowEffect(); shadow.setOffset(3); shadow.setColor(Qt.black)
		self.helper_text.setGraphicsEffect(shadow)
		self.helper_text.setStyleSheet('color:red')
		self.helper_text.setAlignment(Qt.AlignCenter)

		# Build the main layout
		self.setContentsMargins(0,0,0,0)
		self.setLayout(QStackedLayout())
		self.layout().setStackingMode(QStackedLayout.StackingMode.StackAll)
		self.layout().addWidget(self.buttons_overlay)
		self.layout().addWidget(self.helper_text)
		self.layout().addWidget(self.map_drawing_layer)
		self.layout().addWidget(self.map)

		# Save the original mouse press event
		self._mousePressEvent_backup = self.mousePressEvent
		self.mousePressEvent = self._no_action

		# Connect signals
		self.calibration_button.clicked.connect(self.init_calibration)
		self.target_button.clicked.connect(self.init_target)
		self.test_button.clicked.connect(self.test)
	
	def test(self):
		self.mousePressEvent = self.test_mousePressEvent
	
	def test_mousePressEvent(self, e):
		self.lat_lon_to_x_y(45.201028, -73.652845)
		self.mousePressEvent = self._no_action
	
	def mapPaintEvent(self, event):
		qp = QPainter()
		qp.begin(self.map_drawing_layer)
		self.draw_elements(qp)
		qp.end()
	
	def draw_elements(self, qp):
		if all(self.target_coords):
			center = QPoint(*self.target_coords)
			radius = self.convert_meters_to_pixels(self.target_radius_1)
			pen = QPen(); pen.setWidth(3)
			brush = QBrush()
			pen.setColor(Qt.red); qp.setPen(pen)
			brush.setStyle(Qt.SolidPattern); brush.setColor(Qt.red); qp.setBrush(brush)
			# qp.setBrush(Qt.red)
			qp.drawEllipse(center, radius, radius)
			radius = self.convert_meters_to_pixels(self.target_radius_2)
			pen.setColor(Qt.red); qp.setPen(pen)
			qp.setBrush(QBrush())
			qp.drawEllipse(center, radius, radius)
			radius = self.convert_meters_to_pixels(self.target_radius_3)
			pen.setColor(Qt.cyan); qp.setPen(pen)
			qp.setBrush(QBrush())
			qp.drawEllipse(center, radius, radius)
	
	def calibration_mousePressEvent(self, event):
		self.helper_text.setVisible(False)
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
				self.helper_text.setText('Sélectionnez le 2e point dont la position est connue.')
				self.helper_text.setVisible(True)
			else:
				self.apply_new_calibration()
		else:
			self.cancel_calibration()

	def init_calibration(self):
		self._calibration_step = 0
		self._new_calibration_points = []
		self.calibration_button.setDisabled(True)
		self.target_button.setDisabled(True)
		self.helper_text.setText('Sélectionnez le 1er point dont la position est connue.')
		self.helper_text.setVisible(True)
		self.mousePressEvent = self.calibration_mousePressEvent
	
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
		# Ratio of the pixel distance over lat/lon delta
		delta_y = -(p[1]['y']-p[0]['y'])
		delta_x = p[1]['x']-p[0]['x']
		pixel_dist = math.sqrt(delta_y**2+delta_x**2)
		self.pixel_lat_ratio = abs((delta_y*math.cos(math.radians(self.map_angle)) + delta_x*math.sin(math.radians(self.map_angle))) / (p[1]['lat']-p[0]['lat']))
		self.pixel_lon_ratio = abs((delta_y*math.sin(math.radians(self.map_angle)) + delta_x*math.cos(math.radians(self.map_angle))) / (p[1]['lat']-p[0]['lat']))
		# Ratio of the pixel distance over the distance in meters
		dist = calculate_distance(p[0]['lat'], p[0]['lon'], p[1]['lat'], p[1]['lon'])
		self.pixel_dist_ratio = pixel_dist/calculate_distance(p[0]['lat'], p[0]['lon'], p[1]['lat'], p[1]['lon'])
		# Calculate lat/long of the origin (x=0, y=0), taking p0 as origin
		corner_lon_pixels = p[0]['x']*math.cos(self.map_angle) + p[0]['y']*math.sin(self.map_angle)
		corner_lat_pixels = -p[0]['x']*math.sin(self.map_angle) + p[0]['y']*math.cos(self.map_angle)
		corner_lon_offset = corner_lon_pixels/self.pixel_lon_ratio
		corner_lat_offset = corner_lat_pixels/self.pixel_lat_ratio
		self.origin_position = {'lat':p[0]['lat']+corner_lat_offset, 'lon':p[0]['lon']+corner_lon_offset}
		
		# self.origin = 
		print('Pixels:', pixel_dist)
		print('Distance:', dist)
		print('self.map_angle:', self.map_angle)
		print('Lat Pixel Ratio:', self.pixel_lat_ratio)
		print('Lon Pixel Ratio:', self.pixel_lon_ratio)
		print('Dist Pixel Ratio:', self.pixel_dist_ratio)
		self.end_calibration()
		self.target_coords = [None, None]
		self.target_button.setDisabled(False)
	
	def target_mousePressEvent(self, event):
		self.target_coords = [event.x(), event.y()]
		self.end_target()
	
	def init_target(self):
		self.target_coords = [None, None]
		self.calibration_button.setDisabled(True)
		self.target_button.setDisabled(True)
		self.helper_text.setText('Cliquez pour indiquer la position de la cible')
		self.mousePressEvent = self.target_mousePressEvent
	
	def end_target(self):
		self.helper_text.setVisible(False)
		self.calibration_button.setDisabled(False)
		self.target_button.setDisabled(False)
		self.mousePressEvent = self._mousePressEvent_backup
		self.hide()
		self.show()

	def convert_meters_to_pixels(self, d):
		return d*self.pixel_dist_ratio
	
	def spawnValidatedInputDialog(self, validator, *args, **kwargs):
		dialog = QInputDialog()
		dialog.textValueChanged.connect(lambda text: validator(text, dialog.setTextValue))
		return dialog.getText(self, *args, **kwargs)

	def lat_lon_to_x_y(self, lat, lon):
		lat_relative = -(lat-self.origin_position['lat'])
		lon_relative = -(lon-self.origin_position['lon'])
		lat_relative_pixels = lat_relative * self.pixel_lat_ratio
		lon_relative_pixels = lon_relative * self.pixel_lon_ratio
		x = lon_relative_pixels*math.cos(self.map_angle) + lat_relative_pixels*math.sin(self.map_angle)
		y = -lon_relative_pixels*math.sin(self.map_angle) + lat_relative_pixels*math.cos(self.map_angle)
		return x, 727+y

	# def switch_coord_sys(self, lat, lon):
	# 	angle = math.radians(-self.map_angle)
	# 	lat_relative = lat - self.origin_position['lat']
	# 	lon_relative = lon - self.origin_position['lon']
	# 	x = (lon_relative - lat_relative * math.tan(angle))*math.cos(angle)
	# 	y = -(lat_relative/math.cos(angle) + (lon_relative - lat_relative * math.tan(angle)) * math.sin(angle))
	# 	return x, y

	# def calibration_prompt(self):
	# 	pos = 



if __name__ == '__main__':
	app = QApplication([])
	gps_map = MapUi()
	gps_map.show()
	app.exec()