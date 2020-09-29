from PyQt5.QtWidgets import QApplication
from renderer import renderer
from MainApp import MainApp
import sys
'''
Create an instance of the fractal application and show it
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp(renderer)
    window.show()
    app.exec_()
