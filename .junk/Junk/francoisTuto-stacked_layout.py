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



# class MainWindow(QMainWindow):

#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)

#         self.setWindowTitle("My Awesome App")

#         layout1 = QHBoxLayout()
#         layout2 = QVBoxLayout()
#         layout3 = QVBoxLayout()

#         layout1.setContentsMargins(0,0,0,0)
#         layout1.setSpacing(20)

#         layout2.addWidget(Color('red'))
#         layout2.addWidget(Color('yellow'))
#         layout2.addWidget(Color('purple'))

#         layout1.addLayout( layout2 )

#         layout1.addWidget(Color('green'))

#         layout3.addWidget(Color('red'))
#         layout3.addWidget(Color('purple'))

#         layout1.addLayout( layout3 )

#         widget = QWidget()
#         widget.setLayout(layout1)
#         self.setCentralWidget(widget)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        layout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(layout)

        for n, color in enumerate(['red','green','blue','yellow']):
            btn = QPushButton( str(color) )
            btn.pressed.connect( lambda n=n: layout.setCurrentIndex(n) )
            button_layout.addWidget(btn)
            layout.addWidget(Color(color))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()





app.exec_()
