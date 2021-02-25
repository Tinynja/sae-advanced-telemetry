# Built-in libraries
import sys
from argparse import ArgumentParser

# Pipy libraries
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QApplication

# User libraries
# from models.main_model import MainModel
from controllers.main_ctrl import MainController
from views.main_view import MainView


parser = ArgumentParser()
parser.add_argument('--debug', help='launches MDIDS-NOMAD in debug mode (dev)', action='store_true')
args = parser.parse_args()


class MissionControl(QApplication):
	def __init__(self, debug=False):
		super().__init__([])
		self.main_model = MainModel()
		self.main_controller = MainController(self.main_model)
		self.main_view = MainView(self.main_controller)
		self.main_view.show()
		self.main_controller.file_open('tests/config.json')


if __name__ == '__main__':
	app = MdidsNomad(args.debug)
	sys.exit(app.exec())