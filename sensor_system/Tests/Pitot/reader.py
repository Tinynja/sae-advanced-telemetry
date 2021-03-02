# Built-in libraries
import serial
from serial.tools import list_ports
import os, csv, time
import threading, queue


################## FUNCTIONS ##################
def read_pitot_data(uart, f_output, stop_event, q):
	i = q.get()
	while not stop_event.is_set():
		print(f'\rRECORDING ({i})... Press Enter to pause recording. ', end='')
		i += 1
		# last_print = print(f'\rRECORDING ({i})... Press Enter to pause recording. ', end='')
		# try:
		# 	message = uart.read_until(b'\n').decode()
		# 	if len(message) == 0 or message[-1] != '\n': continue
		# 	data_row = {d.split(':')[0]:float(d.split(':')[1]) for d in message.split('\t')}
		# 	f_output(data_row)
		# 	i += 1
		# except UnicodeDecodeError:
		# 	print(f'\rERROR: Undecodable data received' + ' '*(len(last_print)-32))
		# except IndexError:
		# 	print(f'\rERROR: Incomplete data received' + ' '*(len(last_print)-31))
	q.put(i)

def write_to_csv(f, data_row):
	writer = csv.DictWriter(f, fieldnames=list(data_row))
	if not f.seek(0,2):
		writer.writeheader()
	writer.writerow(data_row)


################## MAIN CODE ##################
# List all the available COM port and prompt for selection
ports = list_ports.comports()
for i,p in enumerate(ports):
	print(f'{p.device}: {p.manufacturer} ({p.description})')
while 'uart' not in locals():
	try:
		uart = serial.Serial(input('COM Port: '), 115200, timeout=2)
	except serial.SerialException:
		print('Couldn\'t connect, please retry. ', end='')

# Select the folder where the data will be saved
folder_path = ''
while not os.path.isdir(folder_path):
	folder_path = input('Folder path where data will be saved (default ./): ') or '.'
	folder_path += ('/' if folder_path[-1] not in ('/', '\\') else '')
	
print(f'\nData will be saved under "{os.path.abspath(folder_path)}\\YYYY-MM-DD_hh-mm-ss_[test_name].csv"')
print('WARNING! test_name shall contain only valid filename characters.')

# Main recording loop
stop_event = threading.Event()
q = queue.Queue()
while True:
	print()
	while True:
		file_name = input('Test name: ')
		# Append the date and time to the test name
		file_name = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + ('_' if file_name else '') + file_name + '.csv'
		# Only accept the file_name if a file doesn't already exist
		if os.path.isfile(folder_path + file_name):
			print(f'A file named "{file_name}" already exists. Please choose another name for your test.')
		else:
			break
	print('Save file: ' + file_name)
	f = open(folder_path + file_name, 'w')
	q.put(0)
	command = input('Press Enter to start recording, or write "new". ')
	while command.lower() != 'new':
		uart_thread = threading.Thread(target=lambda: read_pitot_data(uart, print, stop_event, q))
		uart_thread.start()
		for i in range(10):
			uart.write((input()+'\n').encode())
		stop_event.set()
		uart_thread.join()
		stop_event.clear()
		command = input('\rSTOPPED... Press Enter to resume recording, or write "new". ')
	q.get()