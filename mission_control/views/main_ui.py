# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


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
		self._PFD_layout.addWidget(QLabel('Test!'))

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
	# dummy_widget.setLayout(main_ui._PFD_layout) # Indiquer ici le nom du layout que vous voulez afficher
	dummy_widget.show()
	app.exec()
