# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# User libraries
from views.main_ui import MainUi


class MainView(QMainWindow):
	def __init__(self, data_model, config_model):
		super().__init__()
		self._ui = MainUi(self)

		self._connect_signals()
	
	def _connect_signals(self):
		
		model.dataChanged.connect(self._ui.set_attitude)


if __name__ == '__main__':
	import os
	os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
	app = QApplication([])
	main_view = MainView()
	main_view.show()
	app.exec()