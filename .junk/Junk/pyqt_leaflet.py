#!/usr/bin/env python

from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
import functools


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.show()
        self.raise_()
    
    def setupUi(self):
        self.setFixedSize(800, 500)
        
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        
        label = self.label = QtWidgets.QLabel()
        vbox.addWidget(label)

        view = self.view = QtWebEngineWidgets.QWebEngineView()
        view.page().mainFrame().addToJavaScriptWindowObject("MainWindow", self)
        view.load(QtCore.QUrl('map.html'))
        view.loadFinished.connect(self.onLoadFinished)
        vbox.addWidget(view)
        
        button = QtWidgets.QPushButton('Go to Paris')
        panToParis = functools.partial(self.panMap, 2.3272, 48.8620)
        button.clicked.connect(panToParis)
        vbox.addWidget(button)
    
    def onLoadFinished(self):
        with open('map.js', 'r') as f:
            frame = self.view.page().mainFrame()
            frame.evaluateJavaScript(f.read())

    @QtCore.pyqtSlot(float, float)
    def onMapMove(self, lat, lng):
        self.label.setText('Lng: {:.5f}, Lat: {:.5f}'.format(lng, lat))
    
    def panMap(self, lng, lat):
        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript('map.panTo(L.latLng({}, {}));'.format(lat, lng))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = MainWindow()
    app.exec_()