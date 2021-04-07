from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyProxyStyle(QProxyStyle):
	def drawControl(self, element, option, painter, widget):
		if element == QStyle.CE_ComboBoxLabel:
			painter.setBackgroundMode(Qt.OpaqueMode)
			painter.setBackground(Qt.red)
			font = painter.font()
			font.setBold(True)
			painter.setFont(font)
		QProxyStyle.drawControl(self, element, option, painter, widget)

app = QApplication([])

style = MyProxyStyle()
# app.setStyle(style)

cb = QComboBox()
cb.addItem("Option 1")
cb.addItem("Option 2")
cb.addItem("Option 3")
cb.show()
cb.setStyle(style)
app.exec()