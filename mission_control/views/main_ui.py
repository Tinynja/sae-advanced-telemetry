# Built-in libraries
from math import cos, sin, radians
import time

# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,QDateTime

# User libraries
from lib.analog_gauge_widget import AnalogGaugeWidget
# from lib.utils import *
from views.utils import InvalidComboBoxStyle
# from views.map_ui import MapUi


class MainUi:
	def __init__(self, main_window):
		self._main_window = main_window

		# Useful variables
		self.data = {}
		self.data_time = {}
		self._comports = []

		# Init main window
		self._main_window.setWindowTitle('Avion-Cargo Mission Control')
		# self._main_window.setWindowIcon(QIcon('resources/icons/nomad.ico'))
		self._main_window.setCentralWidget(QWidget())

		# Create all sub-layouts
		self._create_gauges()
		self._create_PFD()
		self._create_drop_history()
		# self._create_MAP()

		# Merge all sub-layouts to the main layout
		self._create_main_layout()
		
		self._main_window.show()
	
	def _create_main_layout(self):
		main_layout = QVBoxLayout(self._main_window.centralWidget())

		row1_layout = QHBoxLayout()
		row2_layout = QHBoxLayout()
		main_layout.addLayout(row1_layout)
		main_layout.addLayout(row2_layout)

		row1_layout.addLayout(self._gauges_layout)
		row1_layout.setStretch(0,1)
		row1_layout.addLayout(self._PFD_layout)
		row1_layout.addLayout(self._drop_history_layout)

		# row2_layout.addWidget(self.map)
	
	def _activer_bouton_standby(self):
		print('LOOL')

	def _create_gauges(self):
		self._gauges_layout = QVBoxLayout()
		
		# #Switch active/stand by
		activation_layout = QHBoxLayout()
		self.b1 = QPushButton("ACTIVE")
		self.b1.setGeometry(0,0,60,50)
		self.b1.setStyleSheet("background-color: green; color: white")
		self.b1.clicked.connect(lambda: print('Actif'))


		self.b2 = QPushButton("Stand by")
		self.b2.setGeometry(0,0,60,50)
		self.b2.setStyleSheet("background-color: red; color: white")
		self.b2.move(60,0)
		# self.b2.clicked.connect(lambda: print('Inactif'))

		activation_layout.addWidget(self.b1)
		activation_layout.addWidget(self.b2)

		# Batterie Avion mère
		self.Label_avion=QLabel("Charge de l'avion")
		self.Bat1 = QProgressBar()
		self.Bat1.setGeometry(30,40,200,175)
		#self.Bat1.setValue(self.charge1)
		activation_layout.addWidget(self.Label_avion)
		activation_layout.addWidget(self.Bat1)
		self._gauges_layout.addLayout(activation_layout)
		

		# Battérie télémétrie
		self.Label_tel=QLabel('Charge de la télémétrie')
		self.Bat2 = QProgressBar()
		#self.Bat2.setValue(self.charge2)
		activation_layout.addWidget(self.Label_tel)
		activation_layout.addWidget(self.Bat2)
		self._gauges_layout.addLayout(activation_layout)		
		#Jauges

		jauges = QGridLayout()
		#self.jauges=QVBoxLayout()

		#Jauge de la puissance
		puiss=QVBoxLayout()

		self.puissance = AnalogGaugeWidget()
		self.puissance.value_min=0
		self.puissance.value_max=1200
		puiss.addWidget(self.puissance)
		title_puissance=QLabel(("Puissance (Watts)"), alignment=Qt.AlignCenter)
		#title_puissance.setFont(QFont('Arial',15)
		puiss.addWidget(title_puissance)

		jauges.addLayout(puiss, 0, 0)
		#self.jauges.addWidget(self.puissance, 0, 0)
		
		# # # Jauges de voltage remplacées par afficheur de batterie # # # 

		#Jauge de l'accéléromètre en X
		ax=QVBoxLayout()

		self.acc_x = AnalogGaugeWidget()
		self.acc_x.value_min=-5
		self.acc_x.value_max=5
		#
		ax.addWidget(self.acc_x)
		ax.addWidget(QLabel("Accélération en X (m/s^2)"), alignment=Qt.AlignCenter)
		jauges.addLayout(ax, 0, 1)
		#
		#jauges.addWidget(self.acc_x, 0, 1)


		#Jauge de l'accéléromètre en Z
		az=QVBoxLayout()

		self.acc_z = AnalogGaugeWidget()
		self.acc_z.value_min=-5
		self.acc_z.value_max=5
		#
		ax.addWidget(self.acc_z)
		ax.addWidget(QLabel("Accélération en Z (m/s^2)"), alignment=Qt.AlignCenter)
		jauges.addLayout(ax, 1, 1)
		#
		#jauges.addWidget(self.acc_z, 1, 1)
		

		self._gauges_layout.addLayout(jauges)

	def _create_PFD(self):
		self._PFD_layout = QVBoxLayout()
		
		top_layout    = QHBoxLayout()
		bottom_layout = QHBoxLayout()
		self._PFD_layout.addLayout(top_layout)
		self._PFD_layout.addLayout(bottom_layout)

		GS_display     = QVBoxLayout()
		Clock_display  = QVBoxLayout()
		VSI_display    = QVBoxLayout()

		TAS_display    = QStackedLayout()
		TAS_display.setStackingMode(QStackedLayout.StackAll)
		Attitude_display = QStackedLayout()
		ALT_display    = QStackedLayout()
		ALT_display.setStackingMode(QStackedLayout.StackAll)
		#... à continuer pour la partie du bas

		self._PFD_layout.setContentsMargins(5,5,5,5)

		#indicateur de GS
		self.GS_variables={}
		self.GS_variables['label']=QLabel('Vitesse sol (m/s)')
		self.GS_variables['label'].setAlignment(Qt.AlignCenter)
		self.GS_variables['value']= QLabel('12.3')
		self.GS_variables['value'].setAlignment(Qt.AlignCenter)
		self.GS_variables['value'].setFont(QFont('Arial',20))
		self.GS_variables['value'].setFrameStyle(QFrame.Panel | QFrame.Sunken)
		GS_display.addWidget(self.GS_variables['label'])
		GS_display.addWidget(self.GS_variables['value'])


		#indicateur de temps écoulé
		self.Clock_variables ={}
		self.Clock_variables['label']= QLabel('Temps écoulé depuis le début du vol')
		self.Clock_variables['label'].setAlignment(Qt.AlignCenter)
		self.Clock_variables['value']=QLabel('00:00')
		self.Clock_variables['value'].setAlignment(Qt.AlignCenter)
		self.Clock_variables['value'].setFont(QFont('Arial',20))
		self.Clock_variables['value'].setFrameStyle(QFrame.Panel | QFrame.Sunken)
		Clock_display.addWidget(self.Clock_variables['label'])
		Clock_display.addWidget(self.Clock_variables['value'])
		self.clock = []
		#self.clock.append(time.time())

		#indicateur de vertical speed
		self.VSI_variables={}
		self.VSI_variables['label']= QLabel('Vitesse verticale (fps)')
		self.VSI_variables['label'].setAlignment(Qt.AlignCenter)
		self.VSI_variables['value']= QLabel('+ 50')
		self.VSI_variables['value'].setAlignment(Qt.AlignCenter)
		self.VSI_variables['value'].setFrameStyle(QFrame.Panel | QFrame.Sunken)
		self.VSI_variables['value'].setFont(QFont('Arial',20))
		VSI_display.addWidget(self.VSI_variables['label'])
		VSI_display.addWidget(self.VSI_variables['value'])
	

		#indicateur de TAS
		self.TAS_variables = {}
		self.TAS_variables['height'] = 300
		self.TAS_variables['original_img_TAS'] = QPixmap('resources/TAS_Graphic.JPG')
		# original_img_TAS = QPixmap('resources/TAS_Graphic.JPG')
		self.data['tas'] = 0
		# height = 300
		self.TAS_variables['TAS_img'] = QLabel()
		self.TAS_variables['TAS_img'].setFrameStyle(QFrame.Box)
		self.TAS_variables['TAS_value'] = QLabel()
		self.TAS_variables['TAS_value'].setFont(QFont('Arial',25))
		self.TAS_variables['TAS_value'].setAlignment(Qt.AlignCenter)	
		self.TAS_variables['TAS_value'].setFrameStyle(QFrame.Panel | QFrame.Raised)
		self.TAS_variables['TAS_value'].setStyleSheet("background-color: black; color: white")
		dummy_widget = QWidget()
		TAS_layout = QVBoxLayout(dummy_widget)
		TAS_layout.setContentsMargins(5,0,5,0)
		TAS_layout.addStretch(1)
		TAS_layout.addWidget(self.TAS_variables['TAS_value'])
		TAS_layout.addStretch(1)
		TAS_display.addWidget(self.TAS_variables['TAS_img'])
		TAS_display.addWidget(dummy_widget)
		self.set_TAS(self.data['tas'])

		#Attitude
		self._original_attitude_img = QPixmap('resources/Attitude_Graphic.png')
		self.pitch, self.roll = 0, 0
		self._attitude = QLabel()
		# Attitude_label = QLabel('Roll and pitch angle')
		self._attitude.setFrameStyle(QFrame.Box)
		Attitude_display.addWidget(self._attitude)
		# Attitude_value = QLabel('Pitch = -0.5 deg | Roll = 12.2 deg')
		# Attitude_display.addWidget(Attitude_value)
		self.set_attitude(pitch=20, roll=30)


		#indicateur de ALT
		self.ALT_variables={}
		self.ALT_variables['height']=300
		self.ALT_variables['original_img_ALT']=QPixmap('resources/ALT_Graphic_Default.jpg')
		self.data['Alt']=0
		# calculated_top = 100 - 5.464490874 * (alt-94)
		# top = round(calculated_top)
		# def __update_img(adj=0):
		# 	global top1
		# 	top1 = max(0, min(top+adj, original_img_ALT.height()-height))
		# 	ALT_img.setPixmap(original_img_ALT.copy(QRect(0, top, original_img_ALT.width(), height)))
		self.ALT_variables['ALT_img']=QLabel()
		self.ALT_variables['ALT_img'].setFrameStyle(QFrame.Box)
		self.ALT_variables['ALT_value']=QLabel()
		self.ALT_variables['ALT_value'].setFont(QFont('Arial',25))
		self.ALT_variables['ALT_value'].setAlignment(Qt.AlignCenter)
		self.ALT_variables['ALT_value'].setFrameStyle(QFrame.Panel | QFrame.Raised)
		self.ALT_variables['ALT_value'].setStyleSheet("background-color: gray; color: white")
		# __update_img()
		alt_dummy_widget = QWidget()
		ALT_layout = QVBoxLayout(alt_dummy_widget)
		ALT_layout.setContentsMargins(5,0,5,0)
		ALT_layout.addStretch(1)
		ALT_layout.addWidget(self.ALT_variables['ALT_value'])
		ALT_layout.addStretch(1)
		ALT_display.addWidget(self.ALT_variables['ALT_img'])
		ALT_display.addWidget(alt_dummy_widget)
		#self.set_ALT(self.data['Alt'])

		#Assemblage de top_layout et bottom_layout
		top_layout.addLayout( GS_display )
		top_layout.addLayout( Clock_display )
		top_layout.addLayout( VSI_display )

		bottom_layout.addLayout( TAS_display )
		bottom_layout.addLayout( Attitude_display )
		bottom_layout.addLayout( ALT_display )
		# bottom_layout.addLayout( VSI_graphic_display )

	def convert(self, seconds):
		min, sec = divmod(seconds, 60)
		return "%02d:%02d:%01d" % (min, sec, sec*10%10)

	def set_clock(self, time):
		current_time = time-self.clock
		self.Clock_variables['value'].setText(self.convert(current_time))
		#self.Clock_variables['value'].setText(f'{time-self.clock[0]:.1f}')
	
	def set_VSI(self,src, altitude, time):
		# self.data['Alt']= altitude
		# self.data_time['time'] = time
		self.VSI_variables['value'].setText(f'{(altitude-self.data[src])/(time-self.data_time[src]):.1f}')
	
	def set_TAS(self, TAS):
		self.data['tas'] = TAS
		if TAS > 67.2:
			calculated_top = 0
		else:
			calculated_top = 100 - 9.803921569 * (TAS-57)
		top = round(calculated_top)
		#top1 = max(0, min(top, self.TAS_variables['original_img_TAS'].height()-self.TAS_variables['height']))
		self.TAS_variables['TAS_img'].setPixmap(self.TAS_variables['original_img_TAS'].copy(QRect(0, top, self.TAS_variables['original_img_TAS'].width(), self.TAS_variables['height'])))
		self.TAS_variables['TAS_value'].setText(str(int(TAS)) + ' m/s')
		limits = [0, 8, 18]
		if TAS > limits[-1]:
			self.TAS_variables['TAS_value'].setStyleSheet("background-color: red; color: white")
		elif TAS > limits[-2]:
			self.TAS_variables['TAS_value'].setStyleSheet("background-color: green; color: white")
		else:
			self.TAS_variables['TAS_value'].setStyleSheet("background-color: gray; color: white")

	def set_ALT(self, ALT):
		#self.data['Alt'] = ALT
		#calculated_top = 100 - 5.464490874 * (ALT-94)
		calculated_top = 200-5.384615385*(ALT-140)
		#calculated_top = 250-5.416666667*(ALT-130)
		top = round(calculated_top)
		#top1 = max(0, min(top, self.ALT_variables['original_img_ALT'].height()-self.ALT_variables['height']))
		self.ALT_variables['ALT_img'].setPixmap(self.ALT_variables['original_img_ALT'].copy(QRect(0, top, self.ALT_variables['original_img_ALT'].width(), self.ALT_variables['height'])))
		self.ALT_variables['ALT_value'].setText(str(int(ALT))+ ' m')
		if self.buttons[0].isChecked():
			self.ALT_variables['original_img_ALT']=QPixmap('resources/ALT_Graphic.PNG')
			limits = [0, 50, 100]
			if ALT > limits[-1]:
				self.ALT_variables['ALT_value'].setStyleSheet("background-color: red; color: white")
			elif ALT > limits[-2]:
				self.ALT_variables['ALT_value'].setStyleSheet("background-color: green; color: white")
			else:
				self.ALT_variables['ALT_value'].setStyleSheet("background-color: red; color: white")
		elif self.buttons[2].isChecked():
			self.ALT_variables['original_img_ALT']=QPixmap('resources/ALT_Graphic_LARG.PNG')
			limits = [0,100]
			if ALT > limits[-1]:
				self.ALT_variables['ALT_value'].setStyleSheet("background-color: green; color: white")
			else:
				self.ALT_variables['ALT_value'].setStyleSheet("background-color: red; color: white")
		else:
			self.ALT_variables['original_img_ALT']=QPixmap('resources/ALT_Graphic_Default.PNG')
			self.ALT_variables['ALT_value'].setStyleSheet("background-color: gray; color: white")


	# Indicateur d'assiette
	def set_attitude(self, pitch=None, roll=None):
		pitch = pitch or self.pitch
		roll = roll or self.roll
		self.pitch = pitch
		self.roll = roll

		# Calibration de l'indicateur d'assiette:
		# 	pitch := 1023px/160deg
		width, height = 400, 300
		radius, angle = pitch*1023/160, roll+90
		x_center, y_center = radius*cos(radians(angle)), radius*sin(radians(angle))
		
		rotation = QTransform().rotate(roll)
		new_attitude = self._original_attitude_img.transformed(rotation, Qt.SmoothTransformation)
		crop = QRect(int(new_attitude.width()/2-x_center-width/2), int(new_attitude.height()/2-y_center-height/2), width, height)
		self._attitude.setPixmap(new_attitude.copy(crop))

	def set_color_label(self, ALT):
		#self.data['Alt'] = ALT
		if self.buttons[0].isChecked():
			self.buttons[2].setStyleSheet("background-color: none")
			self.buttons[3].setStyleSheet("background-color: none")
			limits = [0,50,100]
			if ALT > limits[-1]:
				self.buttons[0].setStyleSheet("background-color: red")
				self.buttons[1].setStyleSheet("background-color: red")
			elif ALT > limits[-2]:
				self.buttons[0].setStyleSheet("background-color: green")
				self.buttons[1].setStyleSheet("background-color: green")
			else:
				self.buttons[0].setStyleSheet("background-color: red")
				self.buttons[1].setStyleSheet("background-color: red")
		elif self.buttons[2].isChecked():
			self.buttons[0].setStyleSheet("background-color: none")
			self.buttons[1].setStyleSheet("background-color: none")
			limits = [0,100]
			if ALT > limits[-1]:
				self.buttons[2].setStyleSheet("background-color: green")
				self.buttons[3].setStyleSheet("background-color: green")
			else: 
				self.buttons[2].setStyleSheet("background-color: red")
				self.buttons[3].setStyleSheet("background-color: red")
		else:
			self.buttons[0].setStyleSheet("background-color: none")
			self.buttons[1].setStyleSheet("background-color: none")
			self.buttons[2].setStyleSheet("background-color: none")
			self.buttons[3].setStyleSheet("background-color: none")

	# def _create_top_buttons(self):
	# 	self._top_buttons_layout = QHBoxLayout()

	def _create_drop_history(self):
		self._drop_history_layout = QGridLayout()
		self._create_top_buttons()
	
		self.labels = []
		self.buttons = []
		# def set_drop_checked(boolqweqweqwe):
		# 		self.buttons[0].setChecked(boolqweqweqwe)
		# 		btn.setStyleSheet("background-color: " + colors[boolqweqweqwe])
							
		def click_drop_type(self, btn, checked):
			if btn.text() in ("Glider 1", "Glider 2"):
				self.buttons[0].setChecked(checked)
				# btn.setStyleSheet("background-color: " + colors[checked])
				self.buttons[1].setChecked(checked)
				# btn.setStyleSheet("background-color: green")
				if checked:
					self.buttons[2].setChecked(not checked)
					# btn.setStyleSheet("background-color: green")
					self.buttons[3].setChecked(not checked)
					# btn.setStyleSheet("background-color: green")
			elif btn.text() in ("Front Door", "Back Door"):
				self.buttons[2].setChecked(checked)
				self.buttons[3].setChecked(checked)
				if checked:
					self.buttons[0].setChecked(not checked)
					self.buttons[1].setChecked(not checked)
			# btn.setStyleSheet("background-color: green")
			# if not btn.isChecked():
			# 	btn.setStyleSheet("background-color: none")
			

		def __create_button(text):
			btn = QPushButton(text)
			self.buttons.append(btn)
			# btn.setFont(QFont('Arial',75))
			btn.setCheckable(True)
			btn.clicked.connect(lambda checked, self=self, btn=btn: click_drop_type(self, btn, checked))

		def __create_label(text):
			self.labels.append(QLabel(text))
			# self.labels[-1].setFont(QFont('Arial',75))
			self.labels[-1].setFrameStyle(QFrame.Box|QFrame.Plain)
			self.labels[-1].setLineWidth(2)

		__create_button("Glider 1")
		__create_button("Glider 2")
		__create_button("Front Door")
		__create_button("Back Door")

		__create_label("")
		__create_label("")
		__create_label("")
		__create_label("")
		# __create_label("Altitude Glider 1")
		# __create_label("Altitude Glider 2")
		# __create_label("Altitude Front Door")
		# __create_label("Altitude Back Door")
		
		for i in range(2):
			for j in range(4):
				if i == 0:
					self._drop_history_layout.addWidget(self.buttons[j],j+1,0,1,2)
				elif i == 1:
					self._drop_history_layout.addWidget(self.labels[j],j+1,2,1,2)
		
	def _create_top_buttons(self):
		self._top_buttons = {}
		self._top_buttons['ports'] = QComboBox()
		self._invalid_comport_style = InvalidComboBoxStyle()
		self._top_buttons['ports'].addItem('Sélectionner un port COM')
		self._top_buttons['record'] = QPushButton("Enregistrement")
		self._top_buttons['record'].setCheckable(True)
		self._top_buttons['settings'] = QPushButton("Paramètres")
		self._drop_history_layout.addWidget(self._top_buttons['ports'],0,0,1,2)
		self._drop_history_layout.addWidget(self._top_buttons['record'],0,2)
		self._drop_history_layout.addWidget(self._top_buttons['settings'],0,3)

	def update_ports(self, new_ports):
		combobox = self._top_buttons['ports']
		# print([p.device for p in new_ports])
		# Format new ports
		new_ports = [f'{p.device}: {p.description}' for p in new_ports]
		# Delete all the ports that are no longer available
		for i,p in enumerate(self._comports):
			if p not in new_ports:
				if i+1 == combobox.currentIndex():
					combobox.model().item(i+1).setForeground(Qt.red)
					font = combobox.model().item(i+1).font()
					font.setBold(True)
					combobox.model().item(i+1).setFont(font)
					combobox.setStyle(self._invalid_comport_style)
				else:
					del self._comports[i]
					combobox.removeItem(i+1)
			elif i+1 == combobox.currentIndex():
				combobox.model().item(i+1).setForeground(Qt.black)
				font = combobox.model().item(i+1).font()
				font.setBold(False)
				combobox.model().item(i+1).setFont(font)
				combobox.setStyle(self._main_window.style())
		# Add all the new ports to the list
		for p in new_ports:
			if p not in self._comports:
				self._comports.append(p)
		# Sort the new list and add the missing items in the combobox
		self._comports.sort()
		for i,p in enumerate(self._comports):
			if combobox.itemText(i+1) != p:
				combobox.insertItem(i+1, p)

		# current_port = combobox.currentText()
		# combobox.clear()
		# combobox.addItems(new_ports)
		# if current_port not in new_ports:
		# 	new_ports.insert(0, current_port)
		# 	combobox.insertItem(0, current_port)
		# 	combobox.setCurrentIndex(0)
		# if  not in new_ports:
		# 	new_ports.insert(0, combo.currentText())
		
		# for p in self._comports:

	def record_altitude(self, label, ALT):
		#self.data['Alt']= ALT
		# self.data['switch']= switch
		# if switch > 1023:
		self.labels[label].setText(f'{ALT:.1f}'+ " m")

	def _create_MAP(self):
		self.map = MapUi()
		


# # Color est ajouté pour PFD, à voir si on laisse ça là
# class Color(QWidget):

# 	def __init__(self, color, *args, **kwargs):
# 		super(Color, self).__init__(*args, **kwargs)
# 		self.setAutoFillBackground(True)

# 		palette = self.palette()
# 		palette.setColor(QPalette.Window, QColor(color))
# 		self.setPalette(palette)