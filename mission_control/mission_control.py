# Built-in libraries
import sys
from argparse import ArgumentParser

# Pipy libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# User libraries
# from models.main_model import MainModel
# from views.main_view import MainView


parser = ArgumentParser()
parser.add_argument('--debug', help='enable debug mode', action='store_true')
args = parser.parse_args()


class MissionControl(QApplication):
	def __init__(self, debug=False):
		super().__init__([])

		self.threadpool = QThreadPool()

		self.start_uart_model()
		# self.main_model = MainModel()
		# self.main_controller = MainController(self.main_model)
		# self.main_view = MainView(self.main_controller)
		# self.main_view.show()
		# self.main_controller.file_open('tests/config.json')
	
	def start_uart_model(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)


if __name__ == '__main__':
	app = MissionControl(args.debug)
	sys.exit(app.exec())