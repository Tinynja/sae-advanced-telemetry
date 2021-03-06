from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

class ProgressbarBat(QWidget):
	def __init__(self):
		super().__init__()

		self.Bat = QProgressBar(self)
		self.Bat.setGeometry(30,40,200,25)



app = QApplication(sys.argv)
window = ProgressbarBat()
window.show()

app.exec_()
