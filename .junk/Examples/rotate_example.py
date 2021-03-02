import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import urllib

class myApplication(QWidget):
	def __init__(self, parent=None):
		super(myApplication, self).__init__(parent)

		#---- Prepare a Pixmap ----

		# url = ('http://sstatic.net/stackexchange/img/logos/' +
		#        'careers/careers-icon.png?v=0288ba302bf6')
		# self.img = QImage()
		# self.img.loadFromData(urllib.urlopen(url).read())

		self.img = 'chat.jpg'
		pixmap = QPixmap(self.img)

		#---- Embed Pixmap in a QLabel ----

		diag = (pixmap.width()**2 + pixmap.height()**2)**0.5

		self.label = QLabel()
		self.label.setMinimumSize(diag, diag)
		self.label.setAlignment(Qt.AlignCenter)
		self.label.setPixmap(pixmap)

		#---- Prepare a Layout ----

		grid = QGridLayout()

		button = QPushButton('Rotate 15 degrees')
		button.clicked.connect(self.rotate_pixmap)

		grid.addWidget(self.label, 0, 0)
		grid.addWidget(button, 1, 0)

		self.setLayout(grid)

		self.rotation = 0

	def rotate_pixmap(self):

		#---- rotate ----

		# Rotate from initial image to avoid cumulative deformation from
		# transformation

		pixmap = QPixmap(self.img)
		self.rotation += 15

		transform = QTransform().rotate(self.rotation)
		pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

		#---- update label ----

		self.label.setPixmap(pixmap)

if __name__ == '__main__':

	app = QApplication(sys.argv)

	instance = myApplication()  
	instance.show()    

	sys.exit(app.exec_())