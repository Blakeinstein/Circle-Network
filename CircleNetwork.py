#!/usr/bin/env python
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
class circle():
    def __init__(self, radius=random.random()*100):
        self.radius = radius
class gui():
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()
        
    def exec(self):
        self.layout.addWidget(QPushButton('Top'))
        self.layout.addWidget(QPushButton('Bottom'))
        self.window.setLayout(self.layout)
        self.window.show()
        return self.app.exec_()
        
if __name__ == "__main__":
    test = gui()
    test.exec()