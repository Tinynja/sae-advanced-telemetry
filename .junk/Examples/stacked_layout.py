from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

class Color(QWidget):

	def __init__(self, color, *args, **kwargs):
		super(Color, self).__init__(*args, **kwargs)
		self.setAutoFillBackground(True)

		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)


class MainWindow(QMainWindow):

	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("My Awesome App")

		layout = QStackedLayout()
		layout.setStackingMode(QStackedLayout.StackAll)

		layout.addWidget(Color('yellow'))
		layout.addWidget(QLabel('Thérèse'))
		layout.currentWidget.setAlignment(Q)
#        layout.addWidget(Color('green'))
		

		# layout.setCurrentIndex(3)

		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)

		
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()