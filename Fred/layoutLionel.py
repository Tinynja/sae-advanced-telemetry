from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import progress


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
		self.batterie = QHBoxLayout()

        #Switch active/stand by
        #self.b1=QPushButton("ACTIVE",self)
        #self.layout.addWidget(self.b1)
        #self.b2=QPushButton("Stand by",self)
        #self.layout.addWidget(self.b2)



        #self.b1.connect(active)
        #act = QAction("Active", self)
        #act.setStatusTip("This is your button")
        #act.setCheckable(True)


        #Batterie

	def batterie(self): 
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 300, 25)
        self.pbar.setAlignment(Qt.AlignCenter) 
        self.pbar.setMinimum(0)
        self.pbar.setValue(y)
        self.pbar.setValue(40)

        self.pbar.setRange(0,100)
        self.pbar.setStyleSheet("QProgressBar::chunk"
                         "{"
                         "background-color: Green;"
                         "margin: 4px;"
                         "}")
           
        self.setGeometry(300, 300, 480, 170)
        self.setWindowTitle('Batterie')


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