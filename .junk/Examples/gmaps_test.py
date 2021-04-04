from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class EventTypes:
	def __init__(self):
		self._types = {getattr(QEvent, attr):attr for attr in dir(QEvent) if isinstance(getattr(QEvent, attr), int)}
	
	def get_type(self, id):
		try:
			return self._types[id]
		except:
			return "ERROR: Unknown type"

event_types = EventTypes()

class MouseEater(QObject):
	# def __init__(self):
	# 	super().__init__()

	def eventFilter(self, obj, event):
		print(event_types.get_type(event.type()))
		# if event.type() == QMouseEvent:
		# 	keyEvent = event
		# 	print("Ate key press", keyEvent.key())
		# 	return True
		# else:
		return True
		# else:
		# 	# pass the event on to the parent class
		# 	return QMainWindow.eventFilter(self, obj, event)

def set_filter(checked):
	if checked:
		# maps.setContextMenuPolicy(Qt.NoContextMenu)
		# maps.installEventFilter(mouse_eater)
		maps.setEnabled(False)
	else:
		# maps.setContextMenuPolicy(Qt.DefaultContextMenu)
		# maps.removeEventFilter(mouse_eater)
		maps.setEnabled(True)

app = QApplication([])

widget = QWidget()
layout = QVBoxLayout(widget)

maps = QWebEngineView()
maps.load(QUrl("https://maps.google.com"))

mouse_eater = MouseEater()
button = QPushButton("Filter")
button.setCheckable(True)
button.clicked.connect(set_filter)

layout.addWidget(button)
layout.addWidget(maps)

widget.show()
app.exec()