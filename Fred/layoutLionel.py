from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Switch active/stand by
        #self.layout.addWidget(self.b1)
        self.b1=QPushButton("ACTIVE",self)
        self.b1.setGeometry(0,0,60,50)
        # self.b1.clicked.connect()

        #self.layout.addWidget(self.b2)
        self.b2=QPushButton("Stand by",self)
        self.b2.setGeometry(0,0,60,50)
        self.b2.move(60,0)
        # self.b2.clicked.connect()
      




        #Batterie
# class ProgressbarBat(QWidget):
# 	def __init__(self):
# 		super().__init__()

# 		self.Bat = QProgressBar(self)
# 		self.Bat.setGeometry(30,40,200,75)
# 		self.timer = QBasicTimer()
# 		self.step = 25
	
# 		self.Bat.setValue(self.step)


        #Récuperer la charge de la battérie avec un connect maybe ? Voir Amine

        #self.bat=QProgressBar()
        #self.bat.setMinimum(0)
        #self.bat.setMaximum(100) #Le max de la charge
        #layout.addWidget(self.bat)


        #Jauges
        




app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()