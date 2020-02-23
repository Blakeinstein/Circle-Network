#!/usr/bin/env python
from sys import exit, platform

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPalette, QPdfWriter, QPagedPaintDevice
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGraphicsScene,
                             QGraphicsView, QGridLayout, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QStyleFactory, QWidget)

from shapes import Circle, conLine


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
    
    def lineList(self):
        return [item for item in self.painter.items() if isinstance(item, conLine)]

    def newCircle(self, cir):
        self.painter.addItem(cir)
        return cir

    def addCircle(self):
        return self.newCircle(Circle())
    
    def clearCanvas(self):
        return self.painter.clear()
    
    def generateReport(self):
        # lineList = {}
        # padding = self.painter.height()*10
        # for i in self.circleList:
        #     for j,k in i.lineItems:
        #         if j not in lineList:
        #             lineList[j] = [i, k]
        # print (lineList)
        printed = QPdfWriter("Output.pdf")
        printed.setCreator("Circle Networks Program by Blaine")
        printed.setPageSize(QPagedPaintDevice.A4)
        printer = QPainter(printed)
        self.painter.render(printer)
        for i,j in enumerate(self.lineList()):
            # lineList[j][0].scene().render(printer)
            # lineList[j][1].scene().render(printer)
            printer.drawText(0, printer.viewport().height() - 400 + i*200, f'{j.nameItem.toPlainText()}: {j.ref1.m_items[4].toPlainText()}, {j.ref2.m_items[4].toPlainText()}')
        printer.end()
        
    
    def renderPng(self):
        printed = QImage(1000, 1000, QImage.Format_ARGB32)
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
        elif event.key() == Qt.Key_Space:
            temp = self.painter.selectedItems()
            for i in range(0, len(temp) - 1):
                temp[i].addLine(temp[i+1])
                
if __name__ == "__main__":
    app = ApplicationContext()
    test = gui()
    test.show()
    exit(app.app.exec_())
