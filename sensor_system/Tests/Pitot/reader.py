# Built-in libraries
import serial
from serial.tools import list_ports
import os, csv, time
import threading, queue


################## FUNCTIONS ##################

def read_pitot_data(uart, f_output, stop_event, q):
	i = q.get()
	while not stop_event.is_set():
		# print(f'\rRECORDING ({i})... Press Enter to pause recording. ', end='')
		# i += 1
		try:
			message = uart.read_until(b'\n').decode()
			if len(message) == 0 or message[-1] != '\n': continue
			data_row = {d.split(':')[0]:float(d.split(':')[1]) for d in message.split('\t')}
			i += 1
			# Print important information
			last_print = 'RECORDING (%d, %s)... Press Enter to pause recording. ' % (i, message.replace('\t', ', ').replace('\n', ''))
			print('\r' + last_print, end='')
			# Write to CSV file
			f_output(data_row)
		except UnicodeDecodeError:
			print(f'\rERROR: Undecodable data received' + ' '*(len(last_print)-32))
		except IndexError:
			print(f'\rERROR: Incomplete data received' + ' '*(len(last_print)-31))
	q.put(i)

def write_to_csv(f, data_row):
	writer = csv.DictWriter(f, fieldnames=list(data_row))
	if not f.seek(0,2):
		writer.writeheader()
	f.seek(f.tell()-2)
	writer.writerow(data_row)
	f.flush()


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
		# Start the UART reader in another thread because calling input() will halt the current thread
		uart_thread = threading.Thread(target=lambda: read_pitot_data(uart, lambda data_row: write_to_csv(f, data_row), stop_event, q))
		uart_thread.start()
		# Test
		for i in range(10):
			uart.write((f'Diff_p (Pa):{i}\n').encode())
		input('RECORDING (0)... Press Enter to pause recording. ')
		stop_event.set()
		uart_thread.join()
		stop_event.clear()
		command = input('\rSTOPPED... Press Enter to resume recording, or write "new". ')
	q.get()
	f.close()