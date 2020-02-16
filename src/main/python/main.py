#!/usr/bin/env python
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import random
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QStyleFactory, QDialog
class circle():
    def __init__(self, radius=random.random()*100):
        self.radius = radius
class gui(QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
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
    sys.exit(appctxt.app.exec_())