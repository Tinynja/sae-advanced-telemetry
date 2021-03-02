import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Widget(QWidget):

	def __init__(self, parent= None):
		super(Widget, self).__init__()
		self.icons = [p for p in dir(QStyle) if 'SP_' in p]
		self.Col_size = 6
		self.layout = QGridLayout()
		self.count = 0

		self.add_icon()
			
		self.setLayout(self.layout)
	
	def add_icon(self):
		if self.count < len(self.icons):
			# select_button = QToolButton()
			select_button = QPushButton(self.icons[self.count])
			select_button.setIcon(self.style().standardIcon(getattr(QStyle, self.icons[self.count])))
			# select_button.setIconSize(QSize(40,40))
			# select_button.setDisabled(True)
			# select_button.setStyleSheet('border: none')
			select_button.clicked.connect(self.add_icon)

			self.layout.addWidget(select_button, int(self.count / self.Col_size), self.count % self.Col_size)
			self.count += 1
	
	def add_all_icons(self):
		while self.count < len(self.icons):
			self.add_icon()
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
			
	dialog = Widget()
	dialog.add_all_icons()
	dialog.show()
			
	app.exec_()