from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

class ProgressbarBat(QWidget):
	def __init__(self):
		super().__init__()

		self.Bat = QProgressBar(self)
		self.Bat.setGeometry(30,40,200,75)
		self.timer = QBasicTimer()
		self.step = 25
	
		self.Bat.setValue(self.step)



app = QApplication(sys.argv)
window = ProgressbarBat()
window.show()

app.exec_()
