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
		pass