#!/usr/bin/env python
from sys import exit, platform

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt, QRectF, QSizeF, QPointF
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPalette, QPdfWriter, QPagedPaintDevice
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGraphicsScene,
                             QGraphicsView, QGridLayout, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QStyleFactory, QWidget)
from shapes import Circle, conLine, DirectionGripItem


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
        self.resize(1280, 720)
        self.painter = QGraphicsScene(0, 0, self.width() - 50, self.height() - 70)
        self.painter.setBackgroundBrush(QBrush(Qt.white))
        self.createTopLayout()
        self.sortedItems = []
        self.canvas = QGraphicsView(self.painter)
        mainLayout = QGridLayout()
        mainLayout.addLayout(self.topLayout, 0, 0, 1, -1)
        mainLayout.addWidget(self.canvas, 1, 0, -1, -1)
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
        button2 = QPushButton("Generate Report", clicked = self.generateReport)
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
    
    def resizeEvent(self, event):
        if self.painter:
            self.resizer()
        return super(gui, self).resizeEvent(event)
    
    def resizer(self):
        self.painter.setSceneRect(0, 0, self.width() - 50, self.height() - 70)
                
    @property
    def circleList(self):
        return [item for item in self.painter.items() if isinstance(item, Circle)]
    
    @property
    def lineList(self):
        return [item for item in self.painter.items() if isinstance(item, conLine)]

    @property
    def gripItems(self):
        return [item for item in self.painter.items() if isinstance(item, DirectionGripItem)]
    
    def newCircle(self, cir):
        self.painter.addItem(cir)
        return cir

    def addCircle(self):
        return self.newCircle(Circle())
    
    def clearCanvas(self):
        return self.painter.clear()
    
    def generateReport(self):
        printer = QPdfWriter("Output.pdf")
        printer.setPageSize(QPagedPaintDevice.A4)
        printer.setResolution(100)
        painter = QPainter(printer)
        delta = 20
        f = painter.font()
        f.setPixelSize(delta)
        painter.setFont(f)
        
        # hide all items
        last_states = []
        for item in self.painter.items():
            last_states.append(item.isVisible())
            item.setVisible(False)

        target = QRectF(0, 0, self.painter.width(), 0)

        for i, item in enumerate(self.lineList):
            cir1 = item.ref1
            cir2 = item.ref2
            item.setVisible(True)
            cir1.setVisible(True)
            cir2.setVisible(True)
            item.nameItem.setVisible(True)
            cir1.m_items[4].setVisible(True)
            cir2.m_items[4].setVisible(True)
            x1 = cir1.pos().x()
            y1 = cir1.pos().y()
            x2 = cir2.pos().x()
            y2 = cir2.pos().y()
            r1 = cir1.radius
            r2 = cir2.radius
            top = min(y1-r1, y2-r2)
            left = min(x1-r1, x2-r2)
            if y2 > y1 + abs(r1 - r2) or y2 < y1 - abs(r1 - r2):
                height = abs(y2 - y1) + r1 + r2
            else:
                height = 2*max(r2, r1)
            target.setHeight(height)
            
            renderBox = QRectF(left - delta, top - delta, self.painter.width() - delta, height + 2*delta)
            if target.bottom() > printer.height():
                printer.newPage()
                target.moveTop(0)
            
            self.painter.render(painter, target, renderBox)
            
            f = painter.font()
            f.setPixelSize(delta)
            painter.drawText(
                QRectF(
                    target.bottomLeft(), QSizeF(printer.width(), delta + 5)
                ),
                f"{item.nameItem.toPlainText()}: {cir1.m_items[4].toPlainText()}, {cir2.m_items[4].toPlainText()}",
            )
            item.setVisible(False)
            cir1.setVisible(False)
            cir2.setVisible(False)
            item.nameItem.setVisible(False)
            cir1.m_items[4].setVisible(False)
            cir2.m_items[4].setVisible(False)          
            target.setTop(target.bottom() + delta + 20)
            
        # restore visibility
        for item, state in zip(self.painter.items(), last_states):
            item.setVisible(state)
        painter.end()
        
    
    def renderPng(self):
        printed = QImage(self.painter.width(), self.painter.height(), QImage.Format_ARGB32)
        printer = QPainter(printed)
        for item in self.gripItems:
            item.setVisible(False)
        self.painter.render(printer)
        printer.end()
        for item in self.gripItems:
            item.setVisible(True)
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            for i in self.painter.selectedItems():
                i.setEnabled(False)
                for j in i.m_items:
                    self.painter.removeItem(j)
                    del j
                for line, ref in i.lineItems:
                    self.painter.removeItem(line)
                    i.lineItems.remove([line, ref])
                    ref.lineItems.remove([line, i])
                    del line
                self.painter.removeItem(i)
                del i
        if event.key() == Qt.Key_Space:
            temp = self.painter.selectedItems()
            for i in range(0, len(temp)):
                temp[i].addLine(temp[(i+1)%len(temp)])
        if event.modifiers() and Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                for items in self.circleList:
                    items.setSelected(True)
                
if __name__ == "__main__":
    app = ApplicationContext()
    test = gui()
    test.show()
    exit(app.app.exec_())
