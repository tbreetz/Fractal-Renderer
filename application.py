import sys
from Mandelbrot import create_frame
import numpy as np
import time
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtGui import QPixmap, QImage
app = QApplication(sys.argv)
root = QMainWindow()

yoff = 25
button = QPushButton(root)
button.setText('Render')
button.move(0,yoff)
xoff = button.width()

center_label = QLabel(root)
center_label.setText('Center')
center_label.move(xoff,0)
center_box = QLineEdit(root)
center_box.setText('-.5+0j')
center_box.move(button.width(),yoff)
xoff = xoff + center_box.width()

window_label = QLabel(root)
window_label.setText('Window')
window_label.move(xoff,0)
window_box = QLineEdit(root)
window_box.setText('1')
window_box.move(xoff,yoff)
xoff = xoff + window_box.width()

iterations_label = QLabel(root)
iterations_label.setText('Iterations')
iterations_label.move(xoff,0)
iterations_box = QLineEdit(root)
iterations_box.setText('128')
iterations_box.move(xoff,yoff)
xoff = xoff + iterations_box.width()

width_label = QLabel(root)
width_label.setText('Width')
width_label.move(xoff,0)
width_box = QLineEdit(root)
width_box.setText('5000')
width_box.move(xoff,yoff)
xoff = xoff + width_box.width()

save_button = QCheckBox(root)
save_button.setText('Save?')
save_button.move(xoff,yoff)
xoff = xoff + save_button.width()

julia_button = QCheckBox(root)
julia_button.setText('Julia?')
julia_button.move(xoff,yoff)
xoff = xoff + julia_button.width()

julia_label = QLabel(root)
julia_label.setText("'c' Value")
julia_label.move(xoff,0)
julia_box = QLineEdit(root)
julia_box.setText('.34-.05j')
julia_box.move(xoff,yoff)
xoff = xoff + julia_box.width()

set_only_button = QCheckBox(root)
set_only_button.setText('Set Only?')
set_only_button.move(xoff,yoff)
xoff = xoff + set_only_button.width()

color_label = QLabel(root)
color_label.setText('Color Palette')
color_label.move(xoff,0)
color_option = QComboBox(root)
color_option.addItem('inferno')
color_option.addItem('magma')
color_option.addItem('plasma')
color_option.addItem('viridis')
color_option.addItem('cividis')
color_option.move(xoff,yoff)
xoff = xoff + color_option.width()

orbit_trap_button = QCheckBox(root)
orbit_trap_button.setText('Orbit?')
orbit_trap_button.move(xoff,yoff)
xoff = xoff + orbit_trap_button.width()

time_label = QLabel(root)
time_label.move(xoff,yoff)
time_label.resize(200,30)
xoff = xoff + time_label.width()

image = QLabel(root)
image.move(20,60)
image.resize(1400,1400)

root.resize(1440,1440)
root.setWindowTitle('Fractal Renderer')
root.show()

def parse_complex(s):
    return complex(s.replace(' ','').replace('i','j'))

def render():
    start = time.time()
    center = parse_complex(center_box.text())
    window = float(window_box.text())
    iterations = int(iterations_box.text())
    pixels = None
    pic = None
    
    if save_button.isChecked():
        width = int(width_box.text())
    else:
        width = int(root.width()-30)

    if julia_button.isChecked():
        julia = parse_complex(julia_box.text())
        pixels = create_frame(center, window, width, iterations,julia)
    else:
        pixels = create_frame(center, window, width, iterations,None)
    
    def orbit_color(v):
        return 100*abs(iterations - v) % 255

    def continuous_color(v):
        return v

    if orbit_trap_button.isChecked():
        pixels = orbit_color(pixels)
    else:
        pixels = continuous_color(pixels)

    if set_only_button.isChecked():
        for i,row in enumerate(pixels):
            for j,pixel in enumerate(row):
                pixels[i][j] = 0 if pixel < iterations else 1

    if save_button.isChecked():
        pic = f'./export/{time.time()}.png'
        plt.imsave(pic,pixels,cmap=color_option.currentText() + '_r')
    else:
        pic = f'./tmp/{time.time()}.png'
        plt.imsave(pic,pixels,cmap=color_option.currentText() + '_r')

    image.resize(root.width()-40,root.height()-80)
    image.setPixmap(QPixmap(pic))
    image.setScaledContents(False)
    end = time.time()
    time_label.setText('Render: %.3fs' % (end-start))

button.clicked.connect(render)
sys.exit(app.exec_())
