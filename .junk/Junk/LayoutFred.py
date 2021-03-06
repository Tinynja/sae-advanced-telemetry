from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.label1 = QLabel("Planeur 1", self)
        self.label1.setFont(QFont('Arial',32))
        self.label1.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.label1.setLineWidth(2)

        self.label2 = QLabel("Planeur 2", self)
        self.label2.setFont(QFont('Arial',32))
        self.label2.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.label2.setLineWidth(3)

        self.label3 = QLabel("Vivres", self)
        self.label3.setFont(QFont('Arial',32))
        self.label3.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.label3.setLineWidth(2)

        self.label4 = QLabel("Habitats", self)
        self.label4.setFont(QFont('Arial',32))
        self.label4.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.label4.setLineWidth(2)

        self.label10 = QLabel("Altitude Planeur 1", self)
        self.label10.setFont(QFont('Arial',32))
        self.label10.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.label10.setLineWidth(2)

        self.label20 = QLabel("Altitude Planeur 2", self)
        self.label20.setFont(QFont('Arial',32))
        self.label20.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.label20.setLineWidth(2)

        self.label30 = QLabel("Altitude Vivres", self)
        self.label30.setFont(QFont('Arial',32))
        self.label30.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.label30.setLineWidth(2)

        self.label40 = QLabel("Altitude Habitats", self)
        self.label40.setFont(QFont('Arial',32))
        self.label40.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.label40.setLineWidth(2)
        
        Glayout = QGridLayout()
        Glayout.addWidget(QPushButton("Enregistrement"),0,2)
        Glayout.addWidget(QPushButton("Settings"),0,3)
        Glayout.addWidget(self.label1,1,0,1,2)
        Glayout.addWidget(self.label2,2,0,1,2)
        Glayout.addWidget(self.label3,3,0,1,2)
        Glayout.addWidget(self.label4,4,0,1,2)
        Glayout.addWidget(self.label10,1,2,1,2)
        Glayout.addWidget(self.label20,2,2,1,2)
        Glayout.addWidget(self.label30,3,2,1,2)
        Glayout.addWidget(self.label40,4,2,1,2)


        widget = QWidget()
        widget.setLayout(Glayout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()





app.exec_()