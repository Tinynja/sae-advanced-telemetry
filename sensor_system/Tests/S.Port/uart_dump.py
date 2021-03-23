# Built-in libraries
import serial
from serial.tools import list_ports
from datetime import datetime
import os, csv
import threading, queue
from math import sqrt
from statistics import mean


################## FUNCTIONS ##################
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


def listen_uart(uart, file, stop_event):
	uart.reset_input_buffer()
	while not stop_event.is_set():
		# print(f'\rRECORDING ({i})... Press Enter to pause recording. ', end='')
		# i += 1
		byte = uart.read()
		if byte:
			print(byte.hex().upper()+' ', end='', flush=True)
			file.write(byte)


################## MAIN CODE ##################
reprint = Reprint()

# List all the available COM port and prompt for selection
print('Scanning COM ports...')
ports = list_ports.comports()
for i,p in enumerate(ports):
	print(f'{p.device}: {p.manufacturer} ({p.description})')
while 'uart' not in locals():
	try:
		uart = serial.Serial(input('COM Port: '), 57600, timeout=2)
	except serial.SerialException:
		print('Couldn\'t connect, please retry. ', end='')
while 'baud' not in locals():
	try:
		baud = int(input('Baud (default=57600): '))
		uart.baudrate = baud
	except ValueError:
		print('Please enter an integer. ', end='')

# Main recording loop
stop_event = threading.Event()
while True:
	print()
	while True:
		file_name = input('Test name: ')
		# Append the date and time to the test name
		file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ('_' if file_name else '') + file_name + '.bin'
		# Only accept the file_name if a file doesn't already exist
		if os.path.isfile(file_name):
			print(f'A file named "{file_name}" already exists. Please choose another name for your test.')
		else:
			break
	print('Save file: ' + file_name)
	f = open(file_name, 'wb', buffering=0)
	command = input('Press Enter to start/pause recording, or write "new". ')
	# baud = -1
	# baud_list = [110, 150, 300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
	while command.lower() != 'new':
		# baud = (baud+1)%len(baud_list)
		# print(baud_list[baud])
		# uart.baudrate = baud_list[baud]
		# Start the UART reader in another thread because calling input() will halt the current thread
		uart_thread = threading.Thread(target=lambda: listen_uart(uart, f, stop_event))
		uart_thread.start()
		# Test
		# for i in range(10):
		# 	uart.write((f'Diff_p (Pa):{i}\n').encode())
		input('')
		stop_event.set()
		uart_thread.join()
		stop_event.clear()
		reprint('PAUSED... Press Enter to resume recording, or write "new". ', end='')
		command = input()
	f.close()