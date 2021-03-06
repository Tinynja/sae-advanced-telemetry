from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys



class MainUIClass(QMainWindow,progress.Ui_MainWindow):

    def __init__(self, parent= None):
        super(MainUIClass, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())








