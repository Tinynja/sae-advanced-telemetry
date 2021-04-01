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
		self._data_model.dataChanged.connect(self._update_data)
		# if self._ui.buttons[0].isChecked():
		# 	self._ui.buttons[1].setChecked(True)
		# 	self._ui.buttons[2].setChecked(False)
		# 	self._ui.buttons[3].setChecked(False)
		# PFD
		# self._ui.b2.clicked.connect(self._ui._activer_bouton_standby)
		# self._ui.buttons_drop_history[0].clicked.connect...
	
	def _update_data(self, src, data):
		if self._debug: print(f'{src}: {data}')
		# Save the data in self._ui for later use
		value, update_time = float(data[0]), int(data[1])
		# Do action based on type of data received
		if src == "ch1":
			if value > 0 and 'Alt' in self._ui.data and ('ch1' in self._ui.data and self._ui.data['ch1'] < 0):
				self._ui.record_altitude(0, self._ui.data['Alt'])	
				self._ui.data[src] = value
				self._ui.data_time[src]= update_time
			elif 'ch1' not in self._ui.data or self._ui.data['ch1'] > 0: #@amine si on met < lorsque sa commence positif sa foire alors jai change pour > mais sa fait que si l<operateur switch off et back on ca va record une 2e fois
					self._ui.data[src] = value
					self._ui.data_time[src]= update_time
		elif src == "ch2":
			if value > 0 and 'Alt' in self._ui.data and ('ch2' in self._ui.data and self._ui.data['ch2'] < 0):
				self._ui.record_altitude(1, self._ui.data['Alt'])	
				self._ui.data[src] = value
				self._ui.data_time[src]= update_time
			elif 'ch2' not in self._ui.data or self._ui.data['ch2'] > 0:
				self._ui.data[src] = value
				self._ui.data_time[src]= update_time
		elif src == "ch3":
			if value > 0 and 'Alt' in self._ui.data and ('ch3' in self._ui.data and self._ui.data['ch3'] < 0):
				self._ui.record_altitude(2, self._ui.data['Alt'])	
				self._ui.data[src] = value
				self._ui.data_time[src]= update_time
			elif 'ch3' not in self._ui.data or self._ui.data['ch3'] > 0:
				self._ui.data[src] = value
				self._ui.data_time[src]= update_time
		elif src == "ch4":
			if value > 0 and 'Alt' in self._ui.data and ('ch4' in self._ui.data and self._ui.data['ch4'] < 0):
				self._ui.record_altitude(3, self._ui.data['Alt'])	
				self._ui.data[src] = value
				self._ui.data_time[src]= update_time
			elif 'ch4' not in self._ui.data or self._ui.data['ch4'] > 0:
				self._ui.data[src] = value
				self._ui.data_time[src]= update_time
		elif src == 'TAS':
			self._ui.set_TAS(value)
			self._ui.data[src] = value
			self._ui.data_time[src]= update_time
		elif src == "Alt":
			self._ui.set_color_label(value)
			self._ui.set_ALT(value)
			#self._ui.VSI_variables['value'].setText(f'{(value-self._ui.data[src][-1])/(update_time-self._ui.data_time[src][-1])}')
			self._ui.data[src] = value
			self._ui.data_time[src]= update_time
		elif src == 'GS':
			self._ui.GS_variables['value'].setText(f'{float(data[0]):.1f}')
			self._ui.data_time[src]= update_time