#!/usr/bin/env python
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import random
from sys import platform, exit
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QStyleFactory, QDialog
class circle():
    def __init__(self, radius=random.random()*100, name=None):
        self.radius = radius
        self.label = name
        
class gui(QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        if platform == 'win32':
            QApplication.setStyle(QStyleFactory.create('Fusion'))
            QApplication.setPalette(QApplication.style().standardPalette())
        self.layout = QVBoxLayout()
        self.layout.addWidget(QPushButton('Top'))
        self.layout.addWidget(QPushButton('Bottom'))
        self.setLayout(self.layout)

if __name__ == "__main__":
    appctxt = ApplicationContext()
    test = gui()
    test.show()
    exit(appctxt.app.exec_())