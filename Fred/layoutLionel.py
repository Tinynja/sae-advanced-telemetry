from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        hbox = QHBoxLayout(self)

        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)

        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.setGeometry(300, 300, 450, 400)
        self.setWindowTitle('QSplitter')

        self.layout= QVBoxLayout()

        #Switch active/stand by
        self.b1=QPushButton("ACTIVE",self)
        self.layout.addWidget(self.b1)
        self.b2=QPushButton("Stand by",self)
        self.layout.addWidget(self.b2)



        #self.b1.connect(active)
        #act = QAction("Active", self)
        #act.setStatusTip("This is your button")
        #act.setCheckable(True)


        #Batterie

        #Récuperer la charge de la battérie avec un connect maybe ? Voir Amine

        #self.bat=QProgressBar()
        #self.bat.setMinimum(0)
        #self.bat.setMaximum(100) #Le max de la charge
        #layout.addWidget(self.bat)


        #Jauges
        






app=QApplication(sys.argv)

Window = MainWindow()
Window.show()   # Toujours mettre cette commande

app.exec()        