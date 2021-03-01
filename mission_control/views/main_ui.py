# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainUi:
	def __init__(self):
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
		pass

	def _create_MAP(self):
		pass


if __name__ == '__main__':
	app = QApplication([])
	main_ui = MainUi()
	dummy_widget = QWidget()
	dummy_widget.setLayout(main_ui._PFD_layout) # Indiquer ici le nom du layout que vous voulez afficher
	dummy_widget.show()
	app.exec()
