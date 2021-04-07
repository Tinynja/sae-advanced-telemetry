from PyQt5.QtWidgets import QProxyStyle, QStyle
from PyQt5.QtCore import Qt

class InvalidComboBoxStyle(QProxyStyle):
	# def __init__(self, current_style):
	# 	super().__init__()
	# 	self.current_style = current_style

	def drawControl(self, element, option, painter, widget):
		if element == QStyle.CE_ComboBoxLabel:
			painter.setPen(Qt.red)
			font = painter.font()
			font.setBold(True)
			painter.setFont(font)
		QProxyStyle.drawControl(self, element, option, painter, widget)

# app = QApplication([])

# style = MyProxyStyle()
# # app.setStyle(style)

# cb = QComboBox()
# cb.addItem("Option 1")
# cb.addItem("Option 2")
# cb.addItem("Option 3")
# cb.show()
# cb.setStyle(style)
# app.exec()