import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class Example(QWidget):

	def __init__(self):
		super().__init__()
		self.show()
		time.sleep(1)
		self.paintEvent = lambda x: None

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawText(event, qp)
		qp.end()

	def drawText(self, event, qp):
		qp.setPen(Qt.red)
		qp.setBrush(Qt.red)
		# qp.setFont(QFont('Decorative', 10))
		qp.drawEllipse(QPoint(50,50), 10, 10)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())