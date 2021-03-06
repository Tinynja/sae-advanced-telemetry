# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


app = QApplication([])

main_widget = QWidget()
QGridLayout(main_widget)



original = QPixmap('.junk/Examples/Speeds.png')

top = 0
height = 80

def update_img(adj=0):
	global top
	top = max(0, min(top+adj, original.height()-height))
	img.setPixmap(original.copy(QRect(0, top, original.width(), height)))

img = QLabel()
img.setFrameStyle(QFrame.Box)
update_img()
# img.setPixmap(original.copy(QRect(0, top, original.width(), height)))


main_widget.layout().addWidget(img)


main_widget.show()
app.exec()