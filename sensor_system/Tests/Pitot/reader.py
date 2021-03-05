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

class Pitot:
	def __init__(self, uart):
		self._uart = uart
		self.clear_variables()

		self.p_abs = None
		self.R = 287.058
		self.T_offset = 0
	
	def read_output(self):
		self.last_message = self._uart.read_until(b'\n')
		if len(self.last_message) == 0 or self.last_message[-1] != ord('\n'):
			self.clear_variables()
			return 1
		else:
			try:
				self.decoded_message = self.last_message.decode().replace('\n', '').replace('\r', '')
				for d in self.decoded_message.split('\t'):
					data = d.split(':')
					if 'delta_p' in data[0].lower():
						self.delta_p = float(data[1])
					elif 'temp' in data[0].lower():
						self.temp = float(data[1])+self.T_offset
				self.calculate_velocity()
				return 0
			except UnicodeDecodeError:
				self.clear_variables()
				return 2
			except (IndexError, ValueError):
				self.clear_variables()
				return 3
	
	def calculate_rho(self):
		if self.p_abs is None or self.R is None or self.temp is None:
			self.rho = None
		else:
			self.rho = self.p_abs/self.R/(273.15+self.temp)

	def calculate_velocity(self):
		self.calculate_rho()
		if self.delta_p is None or self.rho is None:
			self.velocity = None
		else:
			self.velocity = sqrt(2*abs(self.delta_p/self.rho))*18/5 # km/h

	def clear_variables(self):
		self.delta_p = None
		self.temp = None
		self.rho = None
		self.velocity = None
	
	def flush_input(self):
		self._uart.reset_input_buffer()



def read_pitot_data(pitot, f_output, stop_event, q):
	i = q.get()
	start_time = q.get()
	pitot.flush_input()
	while not stop_event.is_set():
		# print(f'\rRECORDING ({i})... Press Enter to pause recording. ', end='')
		# i += 1
		status = pitot.read_output()
		if status == 0:
			delta = datetime.now()-start_time
			data_row = {'Time (s)': delta.seconds+delta.microseconds/1e6,
						'Delta_P (Pa)': pitot.delta_p,
						'Temp (C)': pitot.temp,
						'Rho (kg/m^3)': pitot.rho,
						'Velocity (km/h)': pitot.velocity}
			formatted_data_row = {k:f'{v:.3f}' for k,v in data_row.items()}
			i += 1
			# Print important information
			reprint(f'RECORDING {i}: {formatted_data_row}... ', end='')
			# Write to CSV file
			f_output(data_row)
		elif status == 1:
			reprint(f'TIMEOUT: Got no data after 2 seconds.')
		elif status == 2:
			reprint(f'ERROR: Undecodable data received ({pitot.last_message})')
		elif status == 3:
			reprint(f'ERROR: Incomplete data received ({pitot.last_message})')
		# try:
		# 	message = uart.read_until(b'\n')
		# 	# Careful here! Indexing a bytestring returns the ascii code of the character for some reason
		# 	if len(message) == 0 or message[-1] != ord('\n'): continue
		# 	decoded_message = message.decode().replace('\n', '').replace('\r', '')
		# 	delta = datetime.now()-start_time
		# 	data_row = {'Time (s)':delta.seconds+delta.microseconds/1e6,
		# 				**{d.split(':')[0]:float(d.split(':')[1]) for d in decoded_message.split('\t')}}
		# 	i += 1
		# 	# Print important information
		# 	reprint('RECORDING (%d, %s)... ' % (i, decoded_message.replace('\t', ', ')), end='')
		# 	# Write to CSV file
		# 	f_output(data_row)
		# except UnicodeDecodeError:
		# 	reprint(f'ERROR: Undecodable data received ({message})')
		# except (IndexError, ValueError):
		# 	reprint(f'ERROR: Incomplete data received ({message})')
	q.put(i)
	q.put(start_time)

def write_to_csv(f, data_row):
	writer = csv.DictWriter(f, fieldnames=list(data_row))
	if not f.seek(0,2):
		writer.writeheader()
	f.seek(f.tell()-2)
	writer.writerow(data_row)
	f.flush()


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
pitot = Pitot(uart=uart)

# Calibration of physical constants
print()
while pitot.p_abs is None:
	try:
		P = input('Atmospheric pressure in Pa (leave empty for 101\'325Pa): ') # Pa
		if P == '':
			pitot.p_abs = 101325
		else:
			pitot.p_abs = float(P)
	except ValueError:
		print('Invalid value.')
while 'ref_temp' not in locals():
	try:
		ref_temp = input('Current temperature (leave empty to skip calibration): ')
		if ref_temp != '':
			ref_temp = float(ref_temp)
			print('Calibrating temperature, this may take up to a minute...')
			temperatures = []
			# For at most 30 tries, get 20 values (prevents endless loop)
			for i in range(30):
				if pitot.read_output() == 0 and pitot.temp is not None:
					temperatures.append(pitot.temp)
				if len(temperatures) > 20:
					pitot.T_offset = ref_temp-mean(temperatures)
					print(f'Calibration successful (offset={pitot.T_offset:+.2f}C)')
					break
				elif i == 100:
					print('Communication problem with the pitot sensor, aborting calibration.')
	except ValueError:
		print('Invalid value.')
		del ref_temp

# Select the folder where the data will be saved
print()
folder_path = ''
while not os.path.isdir(folder_path):
	folder_path = input('Folder path where data will be saved (default ./): ') or '.'
	folder_path += ('/' if folder_path[-1] not in ('/', '\\') else '')
print(f'Data will be saved under "{os.path.abspath(folder_path)}\\YYYY-MM-DD_hh-mm-ss_[test_name].csv"')
print('WARNING! test_name shall contain only valid filename characters.')

# Main recording loop
stop_event = threading.Event()
q = queue.Queue()
while True:
	print()
	while True:
		file_name = input('Test name: ')
		# Append the date and time to the test name
		file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ('_' if file_name else '') + file_name + '.csv'
		# Only accept the file_name if a file doesn't already exist
		if os.path.isfile(folder_path + file_name):
			print(f'A file named "{file_name}" already exists. Please choose another name for your test.')
		else:
			break
	print('Save file: ' + file_name)
	f = open(folder_path + file_name, 'w')
	command = input('Press Enter to start/pause recording, or write "new". ')
	q.put(0) # i
	q.put(datetime.now())
	while command.lower() != 'new':
		# Start the UART reader in another thread because calling input() will halt the current thread
		uart_thread = threading.Thread(target=lambda: read_pitot_data(pitot, lambda data_row: write_to_csv(f, data_row), stop_event, q))
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
	q.get() # i
	q.get() # start time
	f.close()