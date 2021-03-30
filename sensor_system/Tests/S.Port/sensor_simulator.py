# Built-in libraries
import serial
from serial.tools import list_ports
import threading, time, random


################## FUNCTIONS & CLASSES ##################
class Reprint:
	def __init__(self):
		self._last_print = ''
	
	def __call__(self, text, end='\n'):
		text = str(text)
		filler = len(self._last_print)-len(text)
		print('\r' + text + ' '*filler + '\x08'*filler, end=end)
		if end == '\n':
			self._last_print = ''
		else:
			self._last_print = text

class UARTListener:
	def __init__(self):
		self.uart = serial.Serial()
		self.stop_event = threading.Event()
		self.listener_thread = threading.Thread()
	
	def comport_wizard(self):
		self.uart.close()
		# List all the available COM port and prompt for selection
		print('Scanning COM ports...')
		ports = list_ports.comports()
		for i,p in enumerate(ports):
			print(f'{p.device}: {p.manufacturer} ({p.description})')
		while not self.uart.is_open:
			try:
				self.uart = serial.Serial(input('COM Port: '), 57600, timeout=2)
			except serial.SerialException:
				print('Couldn\'t connect, please retry. ', end='')
		while 'baud' not in locals():
			try:
				baud = int(input('Baud (default=57600): ') or 57600)
				self.uart.baudrate = baud
			except ValueError:
				print('Please enter an integer. ', end='')
	
	def start_comport_listener(self, data_handler):
		self.stop_event.clear()
		self.listener_thread = threading.Thread(target=self.comport_listener, args=(data_handler,))
		self.listener_thread.start()
	
	def comport_listener(self, data_handler):
		self.uart.reset_input_buffer()
		while not self.stop_event.is_set():
			byte = self.uart.read()
			data_handler(byte)

	def stop_comport_listener(self):
		self.stop_event.set()
		if self.listener_thread.is_alive():
			self.listener_thread.join()


class SPortSensor:
	def __init__(self):
		self.endian = 'little'

		self.last_request = b''
		self.clear_reponse_info()
		
		self.uart_listener = UARTListener()
		self.uart_listener.comport_wizard()
		self.uart_listener.start_comport_listener(self.respond)

	def respond(self, request):
		# Only send a response if we are ready to respond (data ready, got 0x7E header, correct sensor_id was polled)
		if None in (self.sensor_id, self.data_id, self.value) or self.last_request != b'\x7E' or request != self.sensor_id:
			if request: self.last_request = request
			return
		# We are ready to respond
		# self.programmed_data_input()
		self.uart_listener.uart.write(self.packet)
		# self.clear_reponse_info()
		self.last_request = request
	
	def generate_packet(self):
		self.packet = b'\x10' + self.data_id + self.value
		self.packet += self.calculate_crc(self.packet)
	
	def interactive_data_input(self):
		# Sensor physical ID
		# sensor_id = 0
		sensor_id = int(input('Sensor ID (1B): 0x'), 16)
		assert sensor_id < 0xFF
		# Data ID
		data_id = int(input('Data ID (2B): 0x'), 16)
		assert data_id < 0xFFFF
		# Data ID
		value = int(eval(input('Value (4B): ')))
		assert value < 0xFFFFFFFF
		# Save new sensor information
		self.sensor_id = sensor_id.to_bytes(1, self.endian)
		self.data_id = data_id.to_bytes(2, self.endian)
		self.value = value.to_bytes(4, self.endian)
		self.generate_packet()
	
	def new_value(self):
		# Data ID
		value = int(eval(input('Value (4B): ')))
		assert value < 0xFFFFFFFF
		self.value = value.to_bytes(4, self.endian)
		self.generate_packet()

	def loop_data_input(self):
		input()
		# self.packet = b'\x10' + self.data_id + self.value
		# self.crc = (self.crc+1)%0x100
		# self.packet = self.packet + self.crc.to_bytes(1, self.endian)
		self.data_id = ((int.from_bytes(self.data_id, self.endian)+0x10)%0xFFFF).to_bytes(4, self.endian)
		# self.value = int(random.random()*0xFFFFFFFF).to_bytes(4, self.endian)
		# print(f'Using value: {self.value[::-1].hex()}')
		self.generate_packet()

	def programmed_data_input(self):
		self.sensor_id = int('00'.replace(' ',''), 16).to_bytes(1, self.endian)
		self.data_id = int('04 00'.replace(' ',''), 16).to_bytes(2, self.endian)
		self.value = int(123).to_bytes(4, self.endian)
		self.generate_packet()
	
	def clear_reponse_info(self):
		self.sensor_id = None
		self.data_id = None
		self.value = None
		self.crc = 0xFF
	
	def calculate_crc(self, data):
		# https://www.digi.com/resources/documentation/Digidocs/90002002/Tasks/t_calculate_checksum.htm?TocPath=API%20Operation%7CAPI%20frame%20format%7C_____1
		# 1. Add all bytes of the packet
		CRC = sum(data)
		# 2. Add the carry bits so that we only have 8 bits
		CRC = (CRC & 0xFF) + (CRC >> 8)
		# 3. Subtract this quantity from 0xFF
		CRC = 0xFF-CRC
		return CRC.to_bytes(1, self.endian)

################## MAIN CODE ##################
reprint = Reprint()

sensor = SPortSensor()

print()
print('Sensor IDs: https://www.ordinoscope.net/static/arduino-frskysp/docs/html/index.html')
print('Data IDs: https://www.ordinoscope.net/static/arduino-frskysp/docs/html/_frsky_s_p_8h.html')
print()

sensor.interactive_data_input()
while True:
	try:
		# time.sleep(10)
		# sensor.interactive_data_input()
		sensor.new_value()
		# sensor.programmed_data_input()
		# sensor.loop_data_input()
		# print(f'Waiting for receiver to poll sensor 0x{sensor.sensor_id.hex().upper()}...')
		print(f"New packet to send: {' '.join([f'{B:02X}' + ('  ' if i in [0, 2,  6] else '') for i,B in enumerate(sensor.packet)])}")
		# start_time = time.time()
		# while sensor.sensor_id is not None:
		# 	if time.time()-start_time > 2:
		# 		print('Timed out!')
		# 		sensor.clear_reponse_info()
		# 		break
	except KeyboardInterrupt:
		print('\nExiting...')
		sensor.uart_listener.stop_comport_listener()
		exit()
	except:
		print('ERROR: Incorrect value!')
		# SPortSensor.clear_reponse_info