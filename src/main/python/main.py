#!/usr/bin/env python
import random
from string import ascii_uppercase
from sys import exit, platform
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel,
                             QPushButton, QGridLayout, QStyleFactory, QHBoxLayout,
                             QWidget, QComboBox, QGraphicsScene, QGraphicsView, QGraphicsItem)
from PyQt5.QtGui import QPainter, QPalette, QColor, QBrush, QPen, QImage
from PyQt5.QtCore import Qt, QRectF, QPointF

class Circle(QGraphicsItem):
    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }
    def __init__(self, radius=None, name="", x=0, y=0, parent=None):
        super(Circle, self).__init__(parent)
        self.radius = radius or 50 + random.random() * 300
        self.label = name if name else f'cir{random.choice(ascii_uppercase)}'
        self.setPos(x or random.randint(0, 300), y or random.randint(0, 450))
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()
    
    def updateHandlesPos(self):
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        self.prepareGeometryChange()
        if self.handleSelected in [self.handleTopLeft,
                                   self.handleTopRight,
                                   self.handleBottomLeft,
                                   self.handleBottomRight,
                                   self.handleTopMiddle,
                                   self.handleBottomMiddle,
                                   self.handleMiddleLeft,
                                   self.handleMiddleRight]:
            self.radius += (mousePos.y() + mousePos.x() + self.mousePressPos.x() - self.mousePressPos.y())/64
            self.setPos(self.x(),self.y())
        self.update()   
        self.updateHandlesPos()
    
    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawEllipse(0, 0, self.radius, self.radius)
        painter.drawText(0, 0, self.radius, self.radius, Qt.AlignCenter, self.label)
     
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
        self.painter.setBackgroundBrush(QBrush(Qt.white))
        self.createTopLayout()
        self.canvas = QGraphicsView(self.painter)
        mainLayout = QGridLayout()
        mainLayout.addLayout(self.topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.canvas, 1, 0, 6, 2)
        self.setLayout(mainLayout)

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
        button4 = QPushButton("Clear", clicked = self.clearCanvas)
        styleComboBox = QComboBox()
        styleComboBox.addItems(['white background', 'transparent background'])
        styleComboBox.activated[str].connect(self.changeCanvasBG)
        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)
        self.topLayout.addWidget(styleLabel)
        self.topLayout.addWidget(styleComboBox)
        self.topLayout.addStretch(1)
        self.topLayout.addWidget(button1)
        self.topLayout.addWidget(button4)
        self.topLayout.addWidget(button2)
        self.topLayout.addWidget(button3)
        
    @property
    def circleList(self):
        return [item for item in self.painter.items() if isinstance(item, Circle)]

    def newCircle(self, cir):
        self.painter.addItem(cir)
        return cir

    def addCircle(self):
        return self.newCircle(Circle())
    
    def clearCanvas(self):
        return self.painter.clear()
    
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
    exit(app.app.exec_())
