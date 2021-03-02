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
		pass

	def _create_PFD(self):
		self._PFD_layout = QVBoxLayout()
		_Top_layout    = QHBoxLayout()
		_Bottom_layout = QHBoxLayout()

		_GS_display     = QVBoxLayout()
		_Clock_display  = QVBoxLayout()
		_VSI_display    = QVBoxLayout()
		
		self._PFD_layout.setContentsMargins(5,5,5,5)

		#indicateur de GS
		_label_GS_label = QLabel('Ground speed (kts)')
		_label_GS_label.setAlignment(Qt.AlignCenter)		
		_GS_display.addWidget(_label_GS_label)
		_label_GS_value = QLabel('19')
		_label_GS_value.setAlignment(Qt.AlignCenter)
		_label_GS_value.setFont(QFont('Arial',20))
		_GS_display.addWidget(_label_GS_value)

		#indicateur de temps écoulé
		_label_Clock_label = QLabel('Time since beggining of flight')
		_label_Clock_label.setAlignment(Qt.AlignCenter)	
		_Clock_display.addWidget(_label_Clock_label)
		_label_Clock_value = QLabel('01:22.1')
		_label_Clock_value.setAlignment(Qt.AlignCenter)	
		_label_Clock_value.setFont(QFont('Arial',20))
		_Clock_display.addWidget(_label_Clock_value)

		#indicateur de VS
		_label_VSI_label = QLabel('Vertical speed (fpm)')
		_label_VSI_label.setAlignment(Qt.AlignCenter)		
		_VSI_display.addWidget(_label_VSI_label)
		_label_VSI_value = QLabel('+ 50')
		_label_VSI_value.setAlignment(Qt.AlignCenter)
		_label_VSI_value.setFont(QFont('Arial',20))
		_VSI_display.addWidget(_label_VSI_value)


		#indicateur de TAS
		_Bottom_layout.addWidget(Color('green'))  
		#indicateur d'assiette
		_Bottom_layout.addWidget(Color('orange'))
		#indicateur de VS graphique
		_Bottom_layout.addWidget(Color('white'))
		#indicateur d'altitude
		_Bottom_layout.addWidget(Color('purple'))

		_Top_layout.addLayout( _GS_display )
		_Top_layout.addLayout( _Clock_display )
		_Top_layout.addLayout( _VSI_display )


		self._PFD_layout.addLayout( _Top_layout )
		self._PFD_layout.addLayout( _Bottom_layout )



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

	def _create_MAP(self):
		pass


if __name__ == '__main__':
	app = QApplication([])
	main_ui = MainUi(None)
	dummy_widget = QWidget()
	dummy_widget.setLayout(main_ui._drop_history_layout) # Indiquer ici le nom du layout que vous voulez afficher
	#dummy_widget.setLayout(main_ui._PFD_layout) # Indiquer ici le nom du layout que vous voulez afficher
	dummy_widget.show()
	app.exec()
