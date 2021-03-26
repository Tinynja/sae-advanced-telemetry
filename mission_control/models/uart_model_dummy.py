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
		self.max_step = 0.3
		self.delay = 0.1
		self.variables = {'ALT':[0, 200], 'TAS':[0, 60], 'voltage': [10, 14], 'GLI1':[-1024, 1024], 'GLI2':[-1024, 1024], 'FDOR':[-1024, 1024], 'BDOR':[-1024, 1024]}

		# Set a random initial value for each variable so they get phase shifted (sinusoid)
		self._last_values = [2*pi*random.random() for limits in self.variables]
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
			packet = f'\x010\x02{src}\x03'
		else:
			# odd: variable value
			self._last_values[idx] = (self._last_values[idx]+self.max_step*random.random())%(2*pi)
			limits = self.variables[src]
			packet = f'\x011\x02{(limits[1]-limits[0])/2*sin(self._last_values[idx])+(limits[1]+limits[0])/2}\x03\n'
		time.sleep(self.delay)
		return packet.encode()


class UartDummyModel(QObject):
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
	portListChanged = pyqtSignal(dict)

	def __init__(self):
		super().__init__()

		# Initialize properties
		self.link_status = -1
		self.data = {} # {data_name: [value, update_time], ...}
		self.available_ports = None

		# Set a dummy serial port (or else errors will get raised)
		self._serial_port = None

		# Start the port listing loop
		self.start_port_listing()

	def start_port_listing(self):
		self._do_port_listing = True
		self._port_listing_thread = threading.Thread(target=self._port_listing_task)
		self._port_listing_thread.start()
	
	def stop_port_listing(self):
		self._do_port_listing = False
		self._port_listing_thread.join()
	
	def _port_listing_task(self, delay=1):
		while self._do_port_listing:
			last_listing_time = time.time()
			self._update_port_list({'DUMMY1': [], **{f'DUMMY{p+1}': [] for p in random.sample(range(4), k=2)}})
			# Wait at least `delay` seconds until next port list
			time.sleep(max(0, last_listing_time + delay - time.time()))

	def configure_comport(self, port=None, timeout=1, **kwargs):
		self.comport_config = {'port': port, 'timeout':timeout, **kwargs}
		# if isinstance(self._serial_port, serial.Serial):
		# 	self._serial_port.close()
		while port is None or self.available_ports is None or port in self.available_ports:
			try:
				self._serial_port = DummySerial(port=port, timeout=timeout, **kwargs)
				break
			except SerialException:
				time.sleep(0.5)
	
	def start_port_polling(self):
		self._do_port_polling = True
		self._port_polling_thread = threading.Thread(target=self._port_polling_task)
		self._port_polling_thread.start()

	def stop_port_polling(self):
		self._do_port_polling = False
		self._port_polling_thread.join()

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
					if response[1] == '0':
						# Got a data name
						last_response = response
					elif response[1] == '1':
						# Got a data value
						if last_response[1] == '0':
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

	def _update_port_list(self, new_port_list):
		if new_port_list != self.available_ports:
			self.portListChanged.emit(new_port_list)
		self.available_ports = new_port_list
	
	def stop_model(self):
		self.stop_port_listing()
		self.stop_port_polling()

	# def _inherit_signals(self):
	# 	for name in dir(self._signals):
	# 		if isinstance((attr := getattr(self._signals, name)), pyqtBoundSignal):
	# 			setattr(self.__class__, name, attr)


if __name__ == '__main__':
	app = QApplication([])
	mdl = UartDummyModel()
	mdl.portListChanged.connect(lambda ports: print(list(ports.keys())))
	mdl.linkStatusChanged.connect(lambda link_status: print(f'Link status: {("BAD", "DATA LOSS", "GOOD")[link_status]}'))
	mdl.dataChanged.connect(lambda name, value: print(f'{name}: {value}'))
	# mdl.configure_comport('COM4', timeout=1, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
	mdl.configure_comport('DUMMY1')
	mdl.start_port_polling()
	app.exec()