# Built-in libraries
import time
import serial
from serial.serialutil import SerialException
from serial.tools import list_ports
import threading

# Pipy libraries
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication


class UartModel(QObject):
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
	
	def _port_listing_task(self, delay=1):
		while self._do_port_listing:
			last_listing_time = time.time()
			self._update_port_list({p.device:p for p in list_ports.comports()})
			# Wait at least `delay` seconds until next port list
			time.sleep(max(0, last_listing_time + delay - time.time()))

	def configure_comport(self, port=None, timeout=1, **kwargs):
		self.comport_config = {'port': port, 'timeout':timeout, **kwargs}
		if isinstance(self._serial_port, serial.Serial):
			self._serial_port.close()
		while port is None or self.available_ports is None or port in self.available_ports:
			try:
				self._serial_port = serial.Serial(port=port, timeout=timeout, **kwargs)
				break
			except SerialException:
				time.sleep(0.5)
	
	def start_port_polling(self):
		self._do_port_polling = True
		self._port_polling_thread = threading.Thread(target=self._port_polling_task)
		self._port_polling_thread.start()

	def stop_port_polling(self):
		self._do_port_polling = False

	def _port_polling_task(self):
		# protocol: \x01 + [type] + \x02 + [name] + \x03 + \x01 + [type] + \x02 + [value] + \x03
		# 	type :=
		# 		n: name
		# 		v: value
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
	mdl = UartModel()
	mdl.portListChanged.connect(lambda ports: print(list(ports.keys())))
	mdl.linkStatusChanged.connect(lambda link_status: print(f'Link status: {("BAD", "DATA LOSS", "GOOD")[link_status]}'))
	mdl.dataChanged.connect(lambda name, value: print(f'{name}: {value}'))
	# mdl.configure_comport('COM4', timeout=1, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
	mdl.configure_comport('COM5')
	mdl.start_port_polling()
	app.exec()