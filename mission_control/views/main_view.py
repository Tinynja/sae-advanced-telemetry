# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
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
		self._data_model.portListChanged.connect(self._process_port_list_change)
		self._data_model.dataChanged.connect(self._process_data_change)
		# if self._ui.buttons[0].isChecked():
		# 	self._ui.buttons[1].setChecked(True)
		# 	self._ui.buttons[2].setChecked(False)
		# 	self._ui.buttons[3].setChecked(False)
		# PFD
		# self._ui.b2.clicked.connect(self._ui._activer_bouton_standby)
		self._ui._top_buttons['ports'].textActivated.connect(self._connect_COM_port)
		self._ui._top_buttons['record'].clicked.connect(self._handle_record)
	
	def _connect_COM_port(self, name):
		name = name.split(':')[0]
		print(name)
		self._data_model.configure_comport(name)

	def _handle_record(self, checked):
		if checked:
			self._ui.clock = time.time()
	
	def _process_port_list_change(self, ports):
		self._ui.update_ports(ports)

	def _process_data_change(self, src, data):
		if self._debug: print(f'{src}: {data}')
		data_time = float(data[1])
		# Convert the string data into numeric data
		if src == 'GPS':
			value = map(float, data[0].split(','))
			value = list(map(lambda degmin: int(degmin/100)+degmin%100/60, value))
		else:
			value = float(data[0])
		# Do action based on type of data received
		if self._ui._top_buttons['record'].isChecked():
			self._ui.set_clock(data_time)
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
		elif src == 'Roll':
			self._ui.set_attitude(roll=value)
		elif src == 'Ptch':
			self._ui.set_attitude(pitch=value)
		elif src == 'TAS':
			self._ui.set_TAS(value)
			self._ui.data[src] = value
		elif src == 'Alt':
			self._ui.set_color_label(value)
			self._ui.set_ALT(value)
			if 'Alt' in self._ui.data_time:
				self._ui.set_VSI(src, value, data_time)
				#self._ui.VSI_variables['value'].setText(f'{(value-self._ui.data[src])/(data_time-self._ui.data_time[src])}')
		elif src == 'GS':
			self._ui.GS_variables['value'].setText(f'{float(data[0]):.1f}')
		elif src == 'Bat1': #Bat1==voltage avion mère
			nb_cell_avion=6
			if value >= nb_cell_avion * 4.2:
				self._ui.Bat1.setValue(100)
			elif value < nb_cell_avion * 4.2 and value >=4.11:
				self._ui.Bat1.setValue(90)
			elif value < nb_cell_avion * 4.11 and value >=4.02:
				self._ui.Bat1.setValue(80)
			elif value < nb_cell_avion * 4.02 and value >=3.95:
				self._ui.Bat1.setValue(70)
			elif value < nb_cell_avion * 3.95 and value >=3.87:
				self._ui.Bat1.setValue(60)
			elif value < nb_cell_avion * 3.87 and value >=3.84:
				self._ui.Bat1.setValue(50)
			elif value < nb_cell_avion * 3.84 and value >=3.82:
				self._ui.Bat1.setValue(40)
			elif value < nb_cell_avion * 3.82 and value >=3.77:
				self._ui.Bat1.setValue(30)
			elif value < nb_cell_avion * 3.77 and value >=3.73:
				self._ui.Bat1.setValue(20)
			elif value < nb_cell_avion * 3.73 and value >=3.69:
				self._ui.Bat1.setValue(10)
			elif value < nb_cell_avion * 3.69:
				self._ui.Bat1.setValue(0)
			
			#self._ui.volt_Avion.update_value(value)
			# self._ui.gauge.update_value
		elif src == 'Bat2': #Bat2==voltage système de télémétrie
			nb_cell_tel=2
			if value >= nb_cell_tel * 4.2:
				self._ui.Bat2.setValue(100)
			elif value < nb_cell_tel * 4.2 and value >=4.11:
				self._ui.Bat2.setValue(90)
			elif value < nb_cell_tel * 4.11 and value >=4.02:
				self._ui.Bat2.setValue(80)
			elif value < nb_cell_tel * 4.02 and value >=3.95:
				self._ui.Bat2.setValue(70)
			elif value < nb_cell_tel * 3.95 and value >=3.87:
				self._ui.Bat2.setValue(60)
			elif value < nb_cell_tel * 3.87 and value >=3.84:
				self._ui.Bat2.setValue(50)
			elif value < nb_cell_tel * 3.84 and value >=3.82:
				self._ui.Bat2.setValue(40)
			elif value < nb_cell_tel * 3.82 and value >=3.77:
				self._ui.Bat2.setValue(30)
			elif value < nb_cell_tel * 3.77 and value >=3.73:
				self._ui.Bat2.setValue(20)
			elif value < nb_cell_tel * 3.73 and value >=3.69:
				self._ui.Bat2.setValue(10)
			elif value < nb_cell_tel * 3.69:
				self._ui.Bat2.setValue(0)
			#self._ui.volt_telem.update_value(value)
		elif src == 'Curr' and 'Bat1' in self._ui.data:
			voltage = self._ui.data['Bat1']
			self._ui.puissance.update_value(value*voltage)
		elif src == 'AccX':
			self._ui.acc_x.update_value(value)
		elif src == 'AccY':
			#self._ui.acc_y.update_value(value)
			pass
		elif src == 'AccZ':
			self._ui.acc_z.update_value(value)
		elif src == 'GPS':
			pass
			# print(value)
		# Save the data in self._ui for later use
		self._ui.data[src] = value
		self._ui.data_time[src] = data_time
