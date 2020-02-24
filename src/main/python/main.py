#!/usr/bin/env python
from sys import exit as sexit
from sys import platform

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QRectF, QSizeF, Qt
from PyQt5.QtGui import (QBrush, QColor, QImage, QPagedPaintDevice, QPainter,
                         QPalette, QPdfWriter)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGraphicsScene,
                             QGraphicsView, QGridLayout, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QStyleFactory)

from shapes import Circle, DirectionGripItem, ConLine


class Gui(QDialog):
    """
    Extends PyQt5's QDialog to create the general application window for the app
    """
    def __init__(self, parent=None):
        """
        Extends PyQt5's QDialog to create the general application window for the app
        """
        super(Gui, self).__init__(parent)
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
        self.createToolbar()
        self.canvas = QGraphicsView(self.painter)
        mainLayout = QGridLayout()
        mainLayout.addLayout(self.topLayout, 0, 0, 1, -1)
        mainLayout.addWidget(self.canvas, 1, 0, -1, -1)
        self.setLayout(mainLayout)

    def changeCanvasBG(self, style):
        """
        used in conjunction with the combox box to toggle between transparent and white canvas background
        """
        if style == 'white background':
            self.painter.setBackgroundBrush(QBrush(Qt.white))
        else:
            self.painter.setBackgroundBrush(QBrush())
        self.canvas = QGraphicsView(self.painter)

    def createToolbar(self):
        """
        Builds the toolbar containing the style combo box, add circle to canvas, clear canvas and save to png or pdf
        """
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
        """
        resizes canvas on window resize
        """
        if self.painter:
            self.painter.setSceneRect(0, 0, self.width() - 50, self.height() - 70)
        return super(Gui, self).resizeEvent(event)

    @property
    def circleList(self):
        """
        returns a list of circles on the canvas
        """
        return [item for item in self.painter.items() if isinstance(item, Circle)]

    @property
    def lineList(self):
        """
        returns a list of lines on the canvas
        """
        return [item for item in self.painter.items() if isinstance(item, ConLine)]

    @property
    def gripItems(self):
        """
        returns a list of gripItems on the canvas
        """
        return [item for item in self.painter.items() if isinstance(item, DirectionGripItem)]

    def newCircle(self, cir):
        """
        used to manually add circles, mainly for debugging
        """
        self.painter.addItem(cir)
        return cir

    def addCircle(self):
        """
        called to add a new circle with random attributes on canvas
        """
        cir = Circle()
        self.painter.addItem(cir)
        return cir

    def clearCanvas(self):
        """
        used as a proxy function to clear QGraphicsScene before definition
        """
        return self.painter.clear()

    def generateReport(self):
        """
        generates a pdf report with information for every connection on canvas, with line name and reference circle names
        """
        #Show error if no connections exist
        if not self.lineList:
            QMessageBox.warning(self, "Generate Report", "No connections exist on canvas").exec()
            return 0
        #create write device and set it up
        printer = QPdfWriter("Output.pdf")
        printer.setPageSize(QPagedPaintDevice.A4)
        printer.setResolution(100)
        painter = QPainter(printer)
        delta = 20 #font height and padding
        f = painter.font()
        f.setPixelSize(delta)
        painter.setFont(f)

        # hide all items
        last_states = []
        for item in self.painter.items():
            last_states.append(item.isVisible())
            item.setVisible(False)

        #create render map, to render screen to
        target = QRectF(0, 0, self.painter.width(), 0)

        for item in self.lineList:
            cir1 = item.ref1
            cir2 = item.ref2
            
            #set items to be rendered as visible
            item.setVisible(True)
            cir1.setVisible(True)
            cir2.setVisible(True)
            item.nameItem.setVisible(True)
            cir1.m_items[4].setVisible(True)
            cir2.m_items[4].setVisible(True)
            
            #build render area from current item positons
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
            renderBox = QRectF(left - delta,
                               top - delta,
                               self.painter.width() - delta,
                               height + 2*delta)
            
            #move to new page if target box exceeds page bottom
            if target.bottom() > printer.height():
                printer.newPage()
                target.moveTop(0)
            
            #render diagram and text to pdf 
            self.painter.render(painter, target, renderBox)
            f = painter.font()
            f.setPixelSize(delta)
            painter.drawText(
                QRectF(
                    target.bottomLeft(), QSizeF(printer.width(), delta + 5)
                ),
                f"{item.nameItem.toPlainText()}: {cir1.m_items[4].toPlainText()}, {cir2.m_items[4].toPlainText()}",
            )
            
            #remove items that were previously set visible
            item.setVisible(False)
            cir1.setVisible(False)
            cir2.setVisible(False)
            item.nameItem.setVisible(False)
            cir1.m_items[4].setVisible(False)
            cir2.m_items[4].setVisible(False)
            
            #padd down and target top to bottom + padding
            target.setTop(target.bottom() + delta + 20)
        
        # restore visibility for all items
        for item, state in zip(self.painter.items(), last_states):
            item.setVisible(state)
        painter.end()
        QMessageBox.about(self, "Generate Report", "The canvas was saved as output.pdf").exec()
        
    def renderPng(self):
        """
        renders current items in cavas to png
        """
        
        #show error if canvas has no circles
        if not self.circleList:
            QMessageBox.warning(self, "Save File", "Canvas is empty! nothing to save").exec()
            return 0
        
        #create file to print to
        printed = QImage(self.painter.width(), self.painter.height(), QImage.Format_ARGB32)
        printer = QPainter(printed)
        
        #set grip items invisible
        for item in self.gripItems:
            item.setVisible(False)
        
        #render screen
        self.painter.render(printer)
        printer.end()
        
        #restore visibilty for grip items
        for item in self.gripItems:
            item.setVisible(True)

        #save file
        printed.save("./output.png", "PNG")
        QMessageBox.about(self, "Save File", "The canvas was saved as output.png").exec()
      
    def set_dark(self):
        """
        create dark palette for fusion theme of PyQt, basically DARK MODE!!!!!!!!!
        """
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
        """
        overloads QDialog to handle key press events
        """
        
        #to delete items and free the memory occupied
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
        
        #attach lines between two selected circles, only if 2 or more items are selected, though the order the items are selected in are not taken into consideration
        if event.key() == Qt.Key_Space:
            temp = self.painter.selectedItems()
            if len(temp) >= 2:
                for i in range(0, len(temp)-1):
                    temp[i].addLine(temp[(i+1)])
        
        #handle select all on Ctrl +
        if event.modifiers() and Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                for items in self.circleList:
                    items.setSelected(True)
                
if __name__ == "__main__":
    app = ApplicationContext()
    test = Gui()
    test.show()
    sexit(app.app.exec_())
