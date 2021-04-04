# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# User libraries
from views.main_ui import MainUi


class MainView(QMainWindow):
	def __init__(self, data_model, config_model, debug=False):
		super().__init__()
		self._ui = MainUi(self)
		self._data_model = data_model

		self._debug = debug
		
		self._connect_signals()
	
	def _connect_signals(self):
		self._data_model.dataChanged.connect(self._process_data_change)
		# if self._ui.buttons[0].isChecked():
		# 	self._ui.buttons[1].setChecked(True)
		# 	self._ui.buttons[2].setChecked(False)
		# 	self._ui.buttons[3].setChecked(False)
		# PFD
		# self._ui.b2.clicked.connect(self._ui._activer_bouton_standby)
		# self._ui.buttons_drop_history[0].clicked.connect...
	
	def _process_data_change(self, src, data):
		if self._debug: print(f'{src}: {data}')
		value, data_time = float(data[0]), int(data[1])
		# Do action based on type of data received
		if src == 'ch1':
			if 'Alt' in self._ui.data and value > 0 and 'ch1' in self._ui.data and self._ui.data['ch1'] < 0:
				# Only record altitude if:
				#  - We have Altitude data
				#  - The switch is ON
				#  - The switch was OFF
				self._ui.record_altitude(0, self._ui.data['Alt'])
			elif value > 0 or ('ch1' in self._ui.data and self._ui.data['ch1'] > 0):
				# Dont record switch position if:
				# 	- Switch is ON and other conditions were not met
				#	- We already recorded altitude 
				src, value, data_time = '_', 0, 0
		elif src == 'ch2':
			# Same as ch1
			if 'Alt' in self._ui.data and value > 0 and 'ch2' in self._ui.data and self._ui.data['ch2'] < 0:
				self._ui.record_altitude(1, self._ui.data['Alt'])
			elif value > 0 or ('ch2' in self._ui.data and self._ui.data['ch2'] > 0):
				src, value, data_time = '_', 0, 0
		elif src == 'ch3':
			# Same as ch1
			if 'Alt' in self._ui.data and value > 0 and 'ch3' in self._ui.data and self._ui.data['ch3'] < 0:
				self._ui.record_altitude(2, self._ui.data['Alt'])
			elif value > 0 or ('ch3' in self._ui.data and self._ui.data['ch3'] > 0):
				src, value, data_time = '_', 0, 0
		elif src == 'ch4':
			# Same as ch1
			if 'Alt' in self._ui.data and value > 0 and 'ch4' in self._ui.data and self._ui.data['ch4'] < 0:
				self._ui.record_altitude(3, self._ui.data['Alt'])
			elif value > 0 or ('ch4' in self._ui.data and self._ui.data['ch4'] > 0):
				src, value, data_time = '_', 0, 0
		elif src == 'TAS':
			self._ui.set_TAS(value)
			self._ui.data[src] = value
		elif src == 'Alt':
			self._ui.set_color_label(value)
			self._ui.set_ALT(value)
			#self._ui.VSI_variables['value'].setText(f'{(value-self._ui.data[src][-1])/(data_time-self._ui.data_time[src][-1])}')
			self._ui.data[src] = value
			self._ui.data_time[src]= data_time
		elif src == 'GS':
			self._ui.GS_variables['value'].setText(f'{float(data[0]):.1f}')
		# Save the data in self._ui for later use
		self._ui.data[src] = value
		self._ui.data_time[src] = data_time
