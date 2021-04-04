from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class KeyEater(QObject):
	# def __init__(self):
	# 	super().__init__()
		# self.textEdit = QTextEdit()
		# self.setCentralWidget(self.textEdit)
		# self.textEdit.installEventFilter(self)

	def eventFilter(self, obj, event):
		if isinstance(event, QMouseEvent):
			print(event.type())
		# if obj == self.textEdit:
		if event.type() == QEvent.KeyPress and event.key() == Qt.Key.Key_A:
			keyEvent = event
			# print("Ate key press", keyEvent.key())
			return True
		else:
			return False
		# else:
			# pass the event on to the parent class
		# return QMainWindow.eventFilter(self, obj, event)

app = QApplication([])
eater = KeyEater()
text = QTextEdit()
text.installEventFilter(eater)
text.show()
# window.show()
app.exec()