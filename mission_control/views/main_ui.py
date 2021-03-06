# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *




# Color est ajouté pour PFD, à voir si on laisse ça là
class Color(QWidget):

	def __init__(self, color, *args, **kwargs):
		super(Color, self).__init__(*args, **kwargs)
		self.setAutoFillBackground(True)

		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)
#fin de color


class MainUi:
	def __init__(self, main_window):
		self._main_window = main_window

		# Init main window
		# self._main_window.setWindowTitle('Avion-Cargo Mission Control')
		# # self._main_window.setWindowIcon(QIcon('resources/icons/nomad.ico'))
		# self._main_window.setCentralWidget(QWidget())

		self._create_gauges()
		self._create_PFD()
		self._create_drop_history()
		self._create_MAP()


	def _create_gauges(self):
		self._gauges_layout = QHBoxLayout 
		
		#Switch active/stand by
	
		b1 = QPushButton("ACTIVE")
		b1.setGeometry(0,0,60,50)
		b1.setStyleSheet("background-color: green; color: white")
		b1.clicked.connect(lambda: print('Actif'))

		b2 = QPushButton("Stand by")
		b2.setGeometry(0,0,60,50)
		b2.setStyleSheet("background-color: red; color: white")
		b2.move(60,0)
		b2.clicked.connect(lambda: print('Inactif'))

		self._gauges_layout.addWidget(b1)
		self._gauges_layout.addWidget(b2)

		# #Batterie
		Bat = QProgressBar()
		Bat.setGeometry(30,40,200,75)
		step = 25
		Bat.setValue(step)

		self._gauges_layout.addWidget(Bat)


		#Jauges
		#Module pour Jauges 

		from analoggaugewidget import AnalogGaugeWidget
		jauges=QGridLayout

		#Jauge de la puissance
		puissance = AnalogGaugeWidget()
		puissance.update_value(500)
		jauges.addWidget(puissance)

		#Jauge du voltage de l'avion mère
		volt_Avion = AnalogGaugeWidget()
		volt_Avion.update_value(200)
		jauges.addWidget(volt_Avion)

		#Jauge du voltage de la télémétrie
		volt_telem = AnalogGaugeWidget()
		volt_telem.update_value(350)
		jauges.addWidget(volt_telem)

		#Jauge de l'accéléromètre en X
		acc_x = AnalogGaugeWidget()
		acc_x.update_value(350)
		jauges.addWidget(acc_x)

		#Jauge de l'accéléromètre en Y
		acc_y = AnalogGaugeWidget()
		acc_y.update_value(350)
		jauges.addWidget(acc_y)

		self._gauges_layout.addLayout(jauges)





	def _create_PFD(self):
		self._PFD_layout = QVBoxLayout()
		Top_layout    = QHBoxLayout()
		Bottom_layout = QHBoxLayout()

		GS_display     = QVBoxLayout()
		Clock_display  = QVBoxLayout()
		VSI_display    = QVBoxLayout()

		TAS_display    = QStackedLayout()
		TAS_display.setStackingMode(QStackedLayout.StackAll)
		Attitude_display = QStackedLayout()
		#... à continuer pour la partie du bas

		self._PFD_layout.setContentsMargins(5,5,5,5)

		#indicateur de GS
		GS_label = QLabel('Ground speed (kts)')
		GS_label.setAlignment(Qt.AlignCenter)		
		GS_display.addWidget(GS_label)
		GS_value = QLabel('19')
		GS_value.setAlignment(Qt.AlignCenter)
		GS_value.setFont(QFont('Arial',20))
		GS_value.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		GS_display.addWidget(GS_value)

		#indicateur de temps écoulé
		Clock_label = QLabel('Time since beggining of flight')
		Clock_label.setAlignment(Qt.AlignCenter)	
		Clock_display.addWidget(Clock_label)
		Clock_value = QLabel('01:22.1')
		Clock_value.setAlignment(Qt.AlignCenter)	
		Clock_value.setFont(QFont('Arial',20))
		Clock_value.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		Clock_display.addWidget(Clock_value)

		#indicateur de VS
		VSI_label = QLabel('Vertical speed (fpm)')
		VSI_label.setAlignment(Qt.AlignCenter)		
		VSI_display.addWidget(VSI_label)
		VSI_value = QLabel('+ 50')
		VSI_value.setAlignment(Qt.AlignCenter)
		VSI_value.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		VSI_value.setFont(QFont('Arial',20))
		VSI_display.addWidget(VSI_value)


		#indicateur de TAS
		original_img_TAS = QPixmap('mission_control/views/TAS_Graphic.JPG')
		tas = 12
		calculated_top = 100 - 9.803921569 * (tas-57)
		top = round(calculated_top)
		height = 300
		def update_img(adj=0):
			global top1
			top1 = max(0, min(top+adj, original_img_TAS.height()-height))
			TAS_IMG.setPixmap(original_img_TAS.copy(QRect(0, top, original_img_TAS.width(), height)))
		TAS_IMG = QLabel()
		update_img()

		TAS_IMG.setFrameStyle(QFrame.Box)
		
		TAS_value = QLabel(str(tas))
		TAS_value.setFont(QFont('Arial',25))
		TAS_value.setAlignment(Qt.AlignCenter)	
		TAS_value.setFrameStyle(QFrame.Panel | QFrame.Raised)
		TAS_value.setStyleSheet("background-color: black; color: white")
		dummy_widget = QWidget()
		TAS_layout = QVBoxLayout(dummy_widget)
		TAS_layout.setContentsMargins(5,0,5,0)
		TAS_layout.addStretch(1)
		TAS_layout.addWidget(TAS_value)
		TAS_layout.addStretch(1)
		TAS_display.addWidget(TAS_IMG)
		TAS_display.addWidget(dummy_widget)

		#indicateur d'assiette
		original_img_attitude = QPixmap('mission_control/views/Attitude_Graphic.JPG')

		Attitude_label = QLabel('Roll and pitch angle')
		Attitude_label.setFrameStyle(QFrame.Box)
		Attitude_display.addWidget(Attitude_label)
		Attitude_value = QLabel('Pitch = -0.5 deg | Roll = 12.2 deg')
		Attitude_display.addWidget(Attitude_value)
		# #indicateur de VS graphique
		# Altitude_display = Bottom_layout.addWidget(Color('black'))
		# #indicateur d'altitude
		# VSI_graphic_display = Bottom_layout.addWidget(Color('purple'))

		#Assemblage de Top_layout et Bottom_layout
		Top_layout.addLayout( GS_display )
		Top_layout.addLayout( Clock_display )
		Top_layout.addLayout( VSI_display )

		Bottom_layout.addLayout( TAS_display )
		Bottom_layout.addLayout( Attitude_display )
		# Bottom_layout.addLayout( Altitude_display )
		# Bottom_layout.addLayout( VSI_graphic_display )



		self._PFD_layout.addLayout( Top_layout )
		self._PFD_layout.addLayout( Bottom_layout )



	def _create_drop_history(self):
		self._drop_history_layout = QGridLayout()
	
		labels = []
		def __create_label(text):
			labels.append(QLabel(text))
			labels[-1].setFont(QFont('Arial',32))
			labels[-1].setFrameStyle(QFrame.Box|QFrame.Plain)
			labels[-1].setLineWidth(2)

		__create_label("Planeur 1")
		__create_label("Planeur 2")
		__create_label("Vivres")
		__create_label("Habitats")
		__create_label("Altitude Planeur 1")
		__create_label("Altitude Planeur 2")
		__create_label("Altitude Vivres")
		__create_label("Altitude Habitats")
		
		self._drop_history_layout.addWidget(QPushButton("Enregistrement"),0,2)
		self._drop_history_layout.addWidget(QPushButton("Settings"),0,3)
		for i in range(2):
			for j in range(4):
				if i == 0:
					self._drop_history_layout.addWidget(labels[j],j+1,0,1,2)
				elif i == 1:
					self._drop_history_layout.addWidget(labels[j+4],j+1,2,1,2)
		
		for i in range(4): #changement de couleur lorsque l'utilisateur click sur le label
			if labels[i-1].mousePressEvent is True:
				labels[i-1].setStyleSheet("background-color: green")
		
		if labels[0].mousePressEvent or labels[1].mousePressEvent and labels[2].mousePressEvent or labels[3].mousePressEvent: #Verification que planeur et largage ne soient pas clicker en meme temps
			labels[2].setStyleSheet("background-color: red")
			labels[3].setStyleSheet("background-color: red")
			print("Erreur! Incompatibilité entre les composantes à larguer")

		for i in range(4): #Double click pour modifier le text et save l'altitude de largage
			if labels[i-1].mouseDoubleClickEvent is True:
				labels[i+4].setText(self.__record_altitude)

		def __record_altitude(self):
			pass

	def _create_MAP(self):
		pass


if __name__ == '__main__':
	app = QApplication([])
	main_ui = MainUi(None)
	dummy_widget = QWidget()
	#dummy_widget.setLayout(main_ui._gauges_layout) # Indiquer ici le nom du layout que vous voulez afficher
	#dummy_widget.setLayout(main_ui._drop_history_layout) # Indiquer ici le nom du layout que
	# dummy_widget.setLayout(main_ui._PFD_layout) # Indiquer ici le nom du layout que vous voulez afficher
	dummy_widget.show()
	app.exec()
