from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Switch active/stand by
        def active():
            print("active")
        self.b1=QPushButton("ACTIVE",self)
        #self.b1.connect(active)


        #Batterie
        layout=QVBoxLayout()
        #Récuperer la charge de la battérie avec un connect maybe ? Voir Amine

        self.bat=QProgressBar()
        self.bat.setMinimum(0)
        self.bat.setMaximum(100) #Le max de la charge
        layout.addWidget(self.bat)


        






app=QApplication(sys.argv)

Window = MainWindow()
Window.show()   # Toujours mettre cette commande

app.exec()        