from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

app = QApplication([])

main_widget = QWidget()
QGridLayout(main_widget)

original = QPixmap('Speeds.png')

top = 0
height = 80

def update_img(adj=0):
	global top
	top = max(0, min(top+adj, original.height()-height))
	img.setPixmap(original.copy(QRect(0, top, original.width(), height)))

img = QLabel()
update_img()
# img.setPixmap(original.copy(QRect(0, top, original.width(), height)))

up = QPushButton()
up.setCheckable(True)
up.setIcon(up.style().standardIcon(QStyle.SP_TitleBarShadeButton))

down = QPushButton()
down.setIcon(up.style().standardIcon(QStyle.SP_TitleBarUnshadeButton))


main_widget.layout().addWidget(img, 0, 0, 4, 1)
main_widget.layout().addWidget(up, 1, 1)
main_widget.layout().addWidget(down, 2, 1)

main_widget.layout().setRowStretch(0, 1)
main_widget.layout().setRowStretch(3, 1)
main_widget.layout().setColumnStretch(0, 1)

up.clicked.connect(lambda: update_img(-10))
down.clicked.connect(lambda: update_img(10))

main_widget.show()
app.exec()