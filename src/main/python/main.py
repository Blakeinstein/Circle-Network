#!/usr/bin/env python
import random
from sys import exit, platform
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel,
                             QPushButton, QGridLayout, QStyleFactory, QHBoxLayout,
                             QWidget, QComboBox, QGraphicsScene, QGraphicsView)
from PyQt5.QtGui import QPainter, QPalette, QColor, QBrush, QPen, QPixmap, QImage
from PyQt5.QtCore import Qt

class circle():
    def __init__(self, radius=None, name=None, x=None, y=None):
        self.radius = radius if radius else random.random()*500
        self.label = name if name else "cirA"
        self.x = x if x else random.randint(0, 900)
        self.y = y if y else random.randint(0, 600)
        # self.center = complex(self.x, self.y)
        
    def __str__(self):
        return f'Circle called {self.label} centered at {self.x}, {self.y}'
    
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
        self.painter = QGraphicsScene(10, 10, 900, 600)
        self.createTopLayout()
        self.canvas = QGraphicsView(self.painter)
        mainLayout = QGridLayout()
        mainLayout.addLayout(self.topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.canvas, 1, 0, 6, 2)
        self.setLayout(mainLayout)
        self.circleList = []

    def changeCanvasBG(self, style):
        if style == 'white background':
            self.painter.setBackgroundBrush(QBrush(Qt.white))
        else:
            self.painter.setBackgroundBrush(QBrush())
        self.canvas = QGraphicsView(self.painter)

    def createTopLayout(self):
        self.topLayout = QHBoxLayout()
        button1 = QPushButton("Add", clicked = self.addCircle)
        button2 = QPushButton("Generate Report")
        button3 = QPushButton("Save", clicked = self.renderPng)
        styleComboBox = QComboBox()
        styleComboBox.addItems(['transparent background', 'white background'])
        styleComboBox.activated[str].connect(self.changeCanvasBG)
        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)
        self.topLayout.addWidget(styleLabel)
        self.topLayout.addWidget(styleComboBox)
        self.topLayout.addStretch(1)
        self.topLayout.addWidget(button1)
        self.topLayout.addWidget(button2)
        self.topLayout.addWidget(button3)
    
    def drawCircle(self):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        self.painter.clear()
        for cir in self.circleList:
            self.painter.addEllipse(cir.x, cir.y, cir.radius, cir.radius, pen=QPen(Qt.black, 2, Qt.SolidLine))
        self.painter.update()
        self.canvas.update()
        self.update()
    
    def newCircle(self, cir):
        self.circleList.append(cir)
        self.drawCircle()
    
    def addCircle(self):
        return self.newCircle(circle())
    
    def renderPng(self):
        printed = QImage(300, 200, QImage.Format_ARGB32)
        printer = QPainter(printed)
        self.painter.render(printer)
        printer.end()
        printed.save("./output.png", "PNG")
        
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
    cir1 = circle(name='cirA')
    cir2 = circle(name='cirB')
    test.newCircle(cir = cir1)
    test.newCircle(cir = cir2)
    exit(app.app.exec_())
