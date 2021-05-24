# Built-in libraries
import time
import serial
from serial.serialutil import SerialException
from serial.tools import list_ports
import threading

# Pipy libraries
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication


class LogsModel(QObject):
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

	def __init__(self, log_path=''):
		super().__init__()

		# Initialize properties
		self.log_file = open(log_path, 'r')

		# Start the port listing loop
		self._start_file_reading()
	
	def _start_file_reading(self):
		self._do_file_reading = True
		self._file_reading_thread = threading.Thread(target=self._file_reading_task)
		self._file_reading_thread.start()
	
	def _file_reading_task(self):
		time.sleep(10)
		last_time, offset = None, 0
		while self._do_file_reading:
			log_line = self.log_file.readline()
			if not log_line: break
			src, value, update_time = log_line.split(';')
			value = value.replace('[','').replace(']','')
			update_time = float(update_time)+offset
			if last_time is None:
				last_time = time.time()
				offset = last_time-update_time
			else:
				sleep_time = update_time-time.time()
				if sleep_time > 0: time.sleep(sleep_time)
			self.dataChanged.emit(src, [value, update_time])
		print("Done!")
		
	def stop_model(self):
		self._do_file_reading = False
		self._file_reading_thread.join()
		self.log_file.close()


if __name__ == '__main__':
	# Init
	app = QApplication([])
	mdl = UartModel()
	# Signal connections
	mdl.portListChanged.connect(lambda ports: print(ports))
	mdl.linkStatusChanged.connect(lambda link_status: print(f'Link status: {("BAD", "DATA LOSS", "GOOD")[link_status]}'))
	mdl.dataChanged.connect(lambda name, value: print(f'{name}: {value}'))
	# mdl.configure_comport('COM4', timeout=1, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
	# Config
	mdl.configure_comport('COM8')
	app.exec()