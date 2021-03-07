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

        self.setWindowTitle("GUI TELEMETRIE")

        Vlayout = QVBoxLayout()
        Hlayout = QHBoxLayout()
        Glayout = QGridLayout()

        Vlayout.addLayout(Hlayout)
        Hlayout.addWidget(Color('red'))
        Hlayout.addWidget(Color('blue'))
        Hlayout.addLayout(Glayout)
        Glayout.addWidget(QLabel("Planeur 1"),0,0)
        Glayout.addWidget(QLabel("Planeur 2"),1,0)
        Glayout.addWidget(QLabel("Vivres"),2,0)
        Glayout.addWidget(QLabel("Habitats"),3,0)
        Vlayout.addWidget(Color('green'))

        widget = QWidget()
        widget.setLayout(Vlayout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()





app.exec_()

