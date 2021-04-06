# Built-in libraries
import os
from argparse import ArgumentParser

# Pipy libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# User libraries
from models.uart_model import UartModel
from models.uart_model_dummy import UartModelDummy
from models.config_model import ConfigModel
from views.main_view import MainView


parser = ArgumentParser()
parser.add_argument('-d', '--dummy', help='use dummy data for testing', action='store_false')
parser.add_argument('--debug', help='enable debug mode', action='store_true')
args = parser.parse_args().__dict__


class MissionControl(QApplication):
	def __init__(self, dummy=False, debug=False):
		super().__init__([])

		# Needed in order to load resources correctly
		self._goto_mc_root_directory()

		# Initiliaze all components of the application
		self.config_model = ConfigModel()
		if dummy:
			self.uart_model = UartModelDummy()
			self.uart_model.configure_comport('DUMMY1')
		else:
			self.uart_model = UartModel()
			self.uart_model.configure_comport('COM8')
		
		self.main_view = MainView(self.uart_model, self.config_model, debug)
		self.main_view.show()
	
	def run(self):
		self.exec()
		self.uart_model.stop_model()
	
	def _goto_mc_root_directory(self):
		os.chdir(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
	app = MissionControl(**args)
	app.run()
