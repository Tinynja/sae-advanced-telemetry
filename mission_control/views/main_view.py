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
		self._data_model = data_model

		self._connect_signals()
	
	def _connect_signals(self):
		self._data_model.dataChanged.connect(self._update_data)
		# if self._ui.buttons[0].isChecked():
		# 	self._ui.buttons[1].setChecked(True)
		# 	self._ui.buttons[2].setChecked(False)
		# 	self._ui.buttons[3].setChecked(False)
		# PFD
		# self._ui.b2.clicked.connect(self._ui._activer_bouton_standby)
		# self._ui.buttons_drop_history[0].clicked.connect...
	
	def _update_data(self, src, data):
		
		if src == 'TAS':
			self._ui.set_TAS(float(data[0]))
		elif src == "altitude":
			print(f'{src}:{data[0]}')
			self._ui.set_color_label(float(data[0]))

			# self._ui.
		# elif src == 'TX_LAR':
			# self._ui.

	# 	if src == 'altitude':
	# 		pass
	# 	if src == 'switch':
	# 		if 