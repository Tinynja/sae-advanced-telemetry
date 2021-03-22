# Built-in libraries
import serial
from serial.tools import list_ports
from datetime import datetime
import os, csv
import threading, queue
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
		uart = serial.Serial(input('COM Port: '), 115200, timeout=2)
	except serial.SerialException:
		print('Couldn\'t connect, please retry. ', end='')

while True:
	try:
		input('')