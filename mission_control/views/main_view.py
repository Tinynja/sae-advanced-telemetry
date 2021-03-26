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
		# Save the data in self._ui for later use
		value, update_time = float(data[0]), int(data[1])
		# Do action based on type of data received
		if src == "switch_glider1":
			print(value)
			if value > 0 and 'altitude' in self._ui.data and ('switch_glider1' in self._ui.data and self._ui.data['switch_glider1'] < 0):
				self._ui.record_altitude(0, self._ui.data['altitude'])	
				self._ui.data[src] = value
			elif 'switch_glider1' not in self._ui.data or self._ui.data['switch_glider1'] < 0:
				self._ui.data[src] = value

		if src == 'TAS':
			self._ui.set_TAS(value)
			self._ui.data[src] = value
		elif src == "altitude":
			self._ui.set_color_label(value)
			self._ui.data[src] = value
	
	def __record_altitude(self, input_command, src, data):
		if src == "switch_glider1":
			if float(data[0])>1023:
				self._ui._crea
			
		# elif src == 'TX_LAR':
		# 	self._ui.

	# 	if src == 'altitude':
	# 		pass
	# 	if src == 'switch':
	# 		if 