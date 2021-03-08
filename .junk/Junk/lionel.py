from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys


class MainWindow(QMainWindow):

    def __init__(self, parent= None):
        super(MainWindow, self).__init__(parent)
		self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())








        self.setTextVisible(False)
        self.charging = False
        self.setStyleSheet('''
        QProgressBar {
            border: 4px solid white;
            background-color: #0070db;
            margin-top: 12px;
        }
        QProgressBar:horizontal {
            height: 60px;
            width: 120px;
            margin-right: 12px;
        }
        QProgressBar:vertical {
            height: 120px;
            width: 60px;
            margin-left: 12px;
        }
        QProgressBar::chunk {
            background-color: white;
            margin: 4px;
        }''')

    def setCharging(self, state):
        self.charging = state
        self.repaint()

    def paintEvent(self, event):
        super().paintEvent(event)
        qp = QPainter(self)
        qp.setPen(Qt.NoPen); qp.setBrush(Qt.white)
        w, h = self.width(), self.height()
        if self.orientation() == Qt.Horizontal:
            qp.drawRect(w, 12 + h / 4, -12, h / 2 - 12)
            dx, dy = 0, 12
        else:
            qp.drawRect(12 + w / 4, 0, w / 2 - 12, 12)
            dx, dy = 12, 0

        qp.setPen(self.palette().text().color())
        qp.drawText(self.rect().adjusted(dx, dy, 0, 0), Qt.AlignCenter, self.text())
        qp.setPen(Qt.NoPen)
        
        if self.charging:
            qp.setBrush(self.parent().palette().window())
            path = QPainterPath()
            if self.orientation() == Qt.Horizontal:
                qp.drawRect(0, 0, 12, h)
                path.moveTo(12, h)
                path.lineTo(12, 12 + h / 3)
                path.quadTo(22, 12 + h / 3, 22, 24)
                path.lineTo(22, 14)
                path.lineTo(2, 14)
                path.lineTo(2, 24)
                path.quadTo(2, 12 + h / 3, 12, 12 + h / 3)
                path.moveTo(7, 12); path.lineTo(7, 0)
                path.moveTo(17, 12); path.lineTo(17, 0)
            else:
                qp.drawRect(0, h, w, -12)
                path.moveTo(w, h - 12)
                path.lineTo(12 + w / 3, h - 12)
                path.quadTo(12 + w / 3, h - 22, 24, h - 22)
                path.lineTo(14, h - 22)
                path.lineTo(14, h - 2)
                path.lineTo(24, h - 2)
                path.quadTo(12 + w / 3, h - 2, 12 + w / 3, h - 12)
                path.moveTo(12, h - 7); path.lineTo(0, h - 7)
                path.moveTo(12, h - 17); path.lineTo(0, h - 17)
            
            pen = QPen(qp.brush(), 12, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
            qp.strokePath(path, pen)
            pen.setWidth(4); pen.setColor(Qt.white); qp.setPen(pen)
            qp.setBrush(self.palette().window())
            qp.drawPath(path)


class Template(QWidget):

    def __init__(self):
        super().__init__()
        grid = QGridLayout(self)
        grid.setSpacing(50)
        pbar = Battery(value=100)
        pbar.setCharging(True)
        grid.addWidget(Battery(value=100), 0, 0)
        grid.addWidget(pbar, 0, 1)
        
        pbar = Battery(value=100, orientation=Qt.Vertical)
        pbar.setCharging(True)
        grid.addWidget(Battery(value=100, orientation=Qt.Vertical), 1, 0, Qt.AlignCenter)
        grid.addWidget(pbar, 1, 1, Qt.AlignCenter)
        self.setStyleSheet('''
        Template {
            background-color: #0070db;
        }''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Template()
    window.show()
    sys.exit(app.exec_())

