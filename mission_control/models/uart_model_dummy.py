# Built-in libraries
import time
import serial
from serial.serialutil import SerialException
from serial.tools import list_ports
import threading
import random
from math import pi, sin

# Pipy libraries
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication


class DummySerial:
	def __init__(self, *args, **kwargs):
		self.is_open = (True if 'port' in kwargs else False)
		self.device = kwargs.pop('port', None)
		self.description = 'Dummy Serial Port'

		self.max_step = 0.3
		self.variables = {
			'Roll':[-180, 180],
			'Ptch':[-90, 90],
			'Yaw':[0, 360],
			'GPS': [[4538.43528, 4538.77854], [-7344.64902, -7344.75814]],
			'AccX':[-5, 5],
			'AccY':[-5, 5],
			'AccZ':[-5, 5],
			'dPrs':[0, 50],			# Delta_P Pitot
			'Bat1':[0, 30],
			'Curr':[2.5, 5],
			'Bat2':[0, 9],
			'Alt':[0, 150],
			'ch1':[-1024, 1024],
			'ch2':[-1024, 1024],
			'ch3':[-1024, 1024],
			'ch4':[-1024, 1024],
			'TAS':[0,65],
			'GS':[0,50]
		}
		# We want to get 5Hz data refresh rate
		self.delay = 1/2/len(self.variables)/2
		# Set a random initial value for each variable so they get phase shifted (sinusoid)
		self._last_values = [(2*pi*random.random() if src != 'GPS' else [2*pi*random.random(), 2*pi*random.random()]) for src in self.variables]
		# Keep track of the last data sent (since uart.read_until splits the text)
		# even: variable name
		# odd: variable value
		self._last_data_sent = 2*len(self.variables)-1
	
	def read_until(self, *args, **kwargs):
		self._last_data_sent = (self._last_data_sent+1)%(2*len(self.variables))
		idx = int(self._last_data_sent/2)
		src = list(self.variables)[int(self._last_data_sent/2)]
		if not self._last_data_sent % 2:
			# even: variable name
			packet = f'\x01s\x02{src}\x03'
		else:
			# odd: variable value
			if src == 'GPS':
				values = []
				for i in range(2):
					self._last_values[idx][i] = (self._last_values[idx][i]+self.max_step*random.random())%(2*pi)
					limits = self.variables[src][i]
					value = (limits[1]-limits[0])/2*sin(self._last_values[idx][i])+(limits[1]+limits[0])/2
					values.append(value)
				value = ','.join(map(str,values))
			else:
				self._last_values[idx] = (self._last_values[idx]+self.max_step*random.random())%(2*pi)
				limits = self.variables[src]
				value = (limits[1]-limits[0])/2*sin(self._last_values[idx])+(limits[1]+limits[0])/2
			packet = f'\x01v\x02{value}\x03\n'
		time.sleep(self.delay)
		return packet.encode()
	
	def close(self):
		self.is_open = False


class UartModelDummy(QObject):
	# Configure the model signals:
	# 	linkStatusChanged :=
	#		0: bad
	#		1: data loss
	#		2: good
	#
	#	dataChanged := (data_name, data_value)
	#	
	#	portListChanged := {port_name: ListPortInfo, ...}
	
	linkStatusChanged = pyqtSignal(int)
	dataChanged = pyqtSignal(str, object)
	portListChanged = pyqtSignal(list)

	def __init__(self):
		super().__init__()

		# Initialize properties
		self.link_status = -1
		self.data = {} # {data_name: [value, update_time], ...}
		self.available_ports = {}

		# Set a dummy serial port (or else errors will get raised)
		self._serial_port = DummySerial()

		# Start the port listing loop
		self._start_port_listing()
	
	def stop_model(self):
		self._stop_port_listing()
		self._stop_port_polling()
		self._stop_comport_config()

	def _start_port_listing(self):
		self._do_port_listing = True
		self._port_listing_thread = threading.Thread(target=self._port_listing_task)
		self._port_listing_thread.start()
	
	def _stop_port_listing(self):
		try:
			self._do_port_listing = False
			self._port_listing_thread.join()
		except (AttributeError, RuntimeError) as e:
			pass
	
	def _port_listing_task(self, delay=1):
		while self._do_port_listing:
			last_listing_time = time.time()
			self._update_port_list([DummySerial(port='DUMMY1'),] + [DummySerial(port=f'DUMMY{p+1}') for p in random.sample(range(1,4), k=2)])
			# self._update_port_list({'DUMMY1': [], **{f'DUMMY{p+1}': [] for p in random.sample(range(4), k=2)}})
			# Wait at least `delay` seconds until next port list
			time.sleep(max(0, last_listing_time + delay - time.time()))

	def _update_port_list(self, new_port_list):
		if new_port_list != self.available_ports:
			self.portListChanged.emit(new_port_list)
		self.available_ports = new_port_list

	def configure_comport(self, port=None, timeout=1, **kwargs):
		# Safely stop the current serial port
		self._stop_port_polling()
		self._serial_port.close()
		# Save the disered config for later use (useful when trying to reconnect)
		self.comport_config = {'port': port, 'timeout':timeout, **kwargs}
		# Stop the comport_config thread if it is already running
		self._stop_comport_config()
		# Launch the comport configuration thread
		self._do_comport_config = True
		self._comport_config_thread = threading.Thread(target=self._comport_config_task)
		self._comport_config_thread.start()

	def _stop_comport_config(self):
		try:
			self._do_comport_config = False
			self._comport_config_thread.join()
		except (AttributeError, RuntimeError) as e:
			pass
			
	def _comport_config_task(self, *args, **kwargs):
		while self._do_comport_config and not self._serial_port.is_open: # (port is None or self.available_ports == {} or port in self.available_ports):
			try:
				self._serial_port = DummySerial(**self.comport_config)
				self._start_port_polling()
			except SerialException:
				time.sleep(0.5)
	
	def _start_port_polling(self):
		self._do_port_polling = True
		self._port_polling_thread = threading.Thread(target=self._port_polling_task)
		self._port_polling_thread.start()

	def _stop_port_polling(self):
		try:
			self._do_port_polling = False
			self._port_polling_thread.join()
		except (AttributeError, RuntimeError) as e:
			pass

	def _port_polling_task(self):
		# protocol: \x01 + [type] + \x02 + [name] + \x03 + \x01 + [type] + \x02 + [value] + \x03
		# 	type :=
		# 		0: name
		# 		1: value
		# 	\x01: start_of_heading
		# 	\x02: start_of_text
		# 	\x03: end_of_text
		last_response, last_response_time = '', time.time()
		while self._do_port_polling:
			try:
				response = self._serial_port.read_until(b'\x03').replace(b'\n', b'')
				if len(response) == 0:
					# Timeout
					last_response = b''
					self._change_link_status(0)
					if time.time()-last_response_time > 5:
						self.configure_comport(**self.comport_config)
				elif response[0] != 1 or response[2] != 2 or response[-1] != 3:
					# Indexing a byte string returns an int
					# Protocol mismatch
					last_response_time = time.time()
					last_response = b''
					self._change_link_status(1)
				else:
					# Protocol match
					response = response.decode()
					last_response_time = time.time()
					if response[1] == 's':
						# Got a data name
						last_response = response
					elif response[1] == 'v':
						# Got a data value
						if last_response[1] == 's':
							# Got a data_name/data_value pair
							name = last_response[3:-1]
							value = response[3:-1]
							current_time = time.time()
							# Update the data value
							self.data[name] = [value, current_time]
							self.dataChanged.emit(name, self.data[name])
							# Check that all data is being updated within 1s
							if all([(current_time-d[1]) <= 1 for d in self.data.values()]):
								self._change_link_status(2)
							else:
								self._change_link_status(1)
						# Reset `last_response` for the next data_name/data_value pair
						last_response = ''
			except:
				self._change_link_status(0)
				if time.time()-last_response_time > 5:
					self.configure_comport(**self.comport_config)
				time.sleep(0.5)
	
	def _change_link_status(self, new_link_status):
		if new_link_status != self.link_status:
			self.linkStatusChanged.emit(new_link_status)
		self.link_status = new_link_status

	# def _inherit_signals(self):
	# 	for name in dir(self._signals):
	# 		if isinstance((attr := getattr(self._signals, name)), pyqtBoundSignal):
	# 			setattr(self.__class__, name, attr)


if __name__ == '__main__':
	# Init
	app = QApplication([])
	mdl = UartModelDummy()
	# Signal connections
	mdl.portListChanged.connect(lambda ports: print([p.device for p in ports]))
	mdl.linkStatusChanged.connect(lambda link_status: print(f'Link status: {("BAD", "DATA LOSS", "GOOD")[link_status]}'))
	mdl.dataChanged.connect(lambda name, value: print(f'{name}: {value}'))
	# mdl.configure_comport('COM4', timeout=1, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
	# Config
	mdl.configure_comport('DUMMY3')
	input()
	mdl.configure_comport('DUMMY3')
	app.exec()