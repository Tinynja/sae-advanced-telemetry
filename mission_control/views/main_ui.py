# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainUi:
	def __init__(self):
		self._create_gauges()
		self._create_PFD()
		self._create_drop_history()
		self._create_MAP()

	def _create_gauges(self):
		pass

	def _create_PFD(self):
		pass

	def _create_drop_history(self):
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

		self.texteditor1 = QLineEdit(self) #change la taille
		font = self.texteditor1.font()
		font.setPointSize(32)
		self.texteditor1.setFont(font)

		self.texteditor2 = QLineEdit(self) #change la taille
		font = self.texteditor2.font()
		font.setPointSize(32)
		self.texteditor2.setFont(font)

		self.texteditor3 = QLineEdit(self) #change la taille
		font = self.texteditor3.font()
		font.setPointSize(32)
		self.texteditor3.setFont(font)

		self.texteditor4 = QLineEdit(self) #change la taille
		font = self.texteditor4.font()
		font.setPointSize(32)
		self.texteditor4.setFont(font)

		self.label1 = QLabel("Planeur 1", self)
		self.label1.setFont(QFont('Arial',32))

		self.label2 = QLabel("Planeur 2", self)
		self.label2.setFont(QFont('Arial',32))

		self.label3 = QLabel("Vivres", self)
		self.label3.setFont(QFont('Arial',32))

		self.label4 = QLabel("Habitats", self)
		self.label4.setFont(QFont('Arial',32))
		
		Glayout = QGridLayout()
		Glayout.addWidget(QPushButton("Enregistrement"),0,2)
		Glayout.addWidget(QPushButton("Settings"),0,3)
		Glayout.addWidget(self.label1,1,0,1,1)
		Glayout.addWidget(self.label2,2,0,2,1)
		Glayout.addWidget(self.label3,3,0,3,1)
		Glayout.addWidget(self.label4,4,0,4,1)
		Glayout.addWidget(self.texteditor1,1,2,1,3)
		Glayout.addWidget(self.texteditor2,2,2,2,3)
		Glayout.addWidget(self.texteditor3,3,2,3,3)
		Glayout.addWidget(self.texteditor4,4,2,4,3)


		widget = QWidget()
		widget.setLayout(Glayout)
		self.setCentralWidget(widget)

	def _create_MAP(self):
		pass
