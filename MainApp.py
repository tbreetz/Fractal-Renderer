from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
'''
This module contains a class containing the UI elements
    and data for a fractal rendering application.

The class is also responsible for passing the UI data
    to the renderer in order to generate the desired fractal.
'''

class MainApp(QMainWindow):
    def __init__(self,renderer):
        super().__init__()
        self.root = QWidget()
        self.setCentralWidget(self.root)
        self.root.setWindowTitle('Fractal Renderer')

        yoff = 25
        button = QPushButton(self.root)
        button.setText('Render')
        button.move(0,yoff)
        xoff = button.width()

        mandelbrot_label = QLabel(self.root)
        mandelbrot_label.setText('Mandelbrot Fam')
        mandelbrot_label.move(xoff,0)
        self.mandelbrot_box = QLineEdit(self.root)
        self.mandelbrot_box.resize(self.mandelbrot_box.width()+30,self.mandelbrot_box.height())
        self.mandelbrot_box.setText('z**2 - l')
        self.mandelbrot_box.move(xoff,yoff)
        xoff = xoff + self.mandelbrot_box.width()

        center_label = QLabel(self.root)
        center_label.setText('Center')
        center_label.move(xoff,0)
        self.center_box = QLineEdit(self.root)
        self.center_box.setText('.5+0j')
        self.center_box.move(xoff,yoff)
        xoff = xoff + self.center_box.width()

        window_label = QLabel(self.root)
        window_label.setText('Window')
        window_label.move(xoff,0)
        self.window_box = QLineEdit(self.root)
        self.window_box.setText('1')
        self.window_box.move(xoff,yoff)
        xoff = xoff + self.window_box.width()

        iterations_label = QLabel(self.root)
        iterations_label.setText('Iterations')
        iterations_label.move(xoff,0)
        self.iterations_box = QLineEdit(self.root)
        self.iterations_box.setText('128')
        self.iterations_box.move(xoff,yoff)
        xoff = xoff + self.iterations_box.width()

        width_label = QLabel(self.root)
        width_label.setText('Width')
        width_label.move(xoff,0)
        self.width_box = QLineEdit(self.root)
        self.width_box.setText('1920')
        self.width_box.move(xoff,yoff)
        xoff = xoff + self.width_box.width()

        height_label = QLabel(self.root)
        height_label.setText('Height')
        height_label.move(xoff,0)
        self.height_box = QLineEdit(self.root)
        self.height_box.setText('1080')
        self.height_box.resize(self.height_box.width()-30,self.height_box.height())
        self.height_box.move(xoff,yoff)
        xoff = xoff + self.height_box.width()

        self.orbit_trap_button = QCheckBox(self.root)
        self.orbit_trap_button.setText('Orbit?')
        self.orbit_trap_button.move(xoff,0)

        self.save_button = QCheckBox(self.root)
        self.save_button.setText('Save?')
        self.save_button.resize(self.save_button.width()-20,self.save_button.height())
        self.save_button.move(xoff,yoff)
        xoff = xoff + self.save_button.width()


        self.set_only_button = QCheckBox(self.root)
        self.set_only_button.setText('Set Only?')
        self.set_only_button.move(xoff,0)

        self.julia_button = QCheckBox(self.root)
        self.julia_button.setText('Julia?')
        self.julia_button.resize(self.julia_button.width()-20,self.julia_button.height())
        self.julia_button.move(xoff,yoff)
        xoff = xoff + self.julia_button.width()


        julia_label = QLabel(self.root)
        julia_label.setText('\tf(z)')
        julia_label.move(xoff,0)
        self.julia_box = QLineEdit(self.root)
        self.julia_box.resize(self.julia_box.width()+30,self.julia_box.height())
        self.julia_box.setText('z**2 + .34-.05j')
        self.julia_box.move(xoff,yoff)
        xoff = xoff + self.julia_box.width()

        v_label = QLabel(self.root)
        v_label.setText('V (threshold)')
        v_label.move(xoff,0)
        self.v_box = QLineEdit(self.root)
        self.v_box.resize(self.v_box.width()+30,self.v_box.height())
        self.v_box.setText('abs(z**2) >= 4')
        self.v_box.move(xoff,yoff)
        xoff = xoff + self.v_box.width()

        color_label = QLabel(self.root)
        color_label.setText('Color Palette')
        color_label.move(xoff,0)
        self.color_option = QComboBox(self.root)
        options = ['inferno','inferno_r','magma',
                   'magma_r','plasma','plasma_r',
                   'viridis','viridis_r','cividis',
                   'cividis_r']
        for option in options:
            self.color_option.addItem(option)
        self.color_option.move(xoff,yoff)
        xoff = xoff + self.color_option.width()

        self.time_label = QLabel(self.root)
        self.time_label.move(xoff,yoff)
        self.time_label.resize(200,30)
        xoff = xoff + self.time_label.width()

        self.image = QLabel(self.root)
        self.image.move(0,60)

        self.renderer = renderer
        self.current = None
        button.clicked.connect(self.render)

    '''
    Retrieve the latest data found in the UI's boxes and buttons
    '''
    def updateData(self):
        self.data = {'mandelbrot':self.mandelbrot_box.text(),
                     'center':self.center_box.text(),
                     'window':float(self.window_box.text()),
                     'iterations':int(self.iterations_box.text()),
                     'width':int(self.width_box.text()),
                     'height':int(self.height_box.text()),
                     'orbit':self.orbit_trap_button.isChecked(),
                     'save':self.save_button.isChecked(),
                     'set_only':self.set_only_button.isChecked(),
                     'julia':self.julia_button.isChecked(),
                     'fz':self.julia_box.text(),
                     'v':self.v_box.text(),
                     'palette':self.color_option.currentText()}
    '''
    Pass the UI data to the renderer and update the UI
     to show the resultant image
    '''
    def render(self):
        self.updateData()
        self.current = self.renderer(self.data)
        self.image.resize(self.data['width'],self.data['height'])
        self.image.setPixmap(QPixmap(self.current['img']))
        self.time_label.setText('Render: %.3fs' % self.current['time'])
        self.root.resize(self.data['width'],self.data['height']+60)
