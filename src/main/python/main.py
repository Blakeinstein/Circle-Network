#!/usr/bin/env python
import random
from sys import exit, platform
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel,
                             QPushButton, QGridLayout, QGroupBox, QStyleFactory, QHBoxLayout,
                             QWidget, QComboBox)
from PyQt5.QtGui import QPainter, QPalette, QColor, QBrush, QPen
from PyQt5.QtCore import Qt

class circle():
    def __init__(self, radius=random.random()*100, name=None, x=random.random()*100, y=random.random()*100):
        self.radius = radius
        self.label = name
        self.center = complex(x,y)
        
class canvas(QMainWindow):
    def __init__(self, parent=None):
        super(canvas, self).__init__(parent)
        self.setGeometry(100, 100, 1000, 700)
    
    def paintEvent(self, e):
        cir = circle(name='cirA')
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        painter.drawEllipse(self, cir.center.x + cir.radius, cir.center.x - cir.radius, cir.center.y + cir.radius, cir.center.y + cir.radius)
         
class gui(QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        if platform == 'win32':
            QApplication.setStyle(QStyleFactory.create('Fusion'))
            self.set_dark()   
        elif platform == 'darwin':
            QApplication.setStyle(QStyleFactory.create('Macintosh'))            
            QApplication.setPalette(QApplication.style().standardPalette())
        self.setWindowTitle('Circle Networks')
        self.createTopLayout()
        self.painter = canvas(self)
        mainLayout = QGridLayout()
        mainLayout.addLayout(self.topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.painter, 1, 0, 6, 2)
        self.setLayout(mainLayout)
    
    def createTopLayout(self):
        self.topLayout = QHBoxLayout()
        button1 = QPushButton("Add")
        button2 = QPushButton("Pdf")
        button3 = QPushButton("Png")
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())
        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)
        self.topLayout.addWidget(styleLabel)
        self.topLayout.addWidget(styleComboBox)
        self.topLayout.addStretch(1)
        self.topLayout.addWidget(button1)
        self.topLayout.addWidget(button2)
        self.topLayout.addWidget(button3)
        
    def set_dark(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)
if __name__ == "__main__":
    app = ApplicationContext()
    test = gui()
    test.show()
    exit(app.app.exec_())
