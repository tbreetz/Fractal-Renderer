import sys
from Mandelbrot import create_frame
import numpy as np
from numba import jit
import time
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtGui import QPixmap, QImage
app = QApplication(sys.argv)
root = QMainWindow()

root.resize(1920,1080)
root.setWindowTitle('Fractal Renderer')

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
width_box.setText('1920')
width_box.move(xoff,yoff)
xoff = xoff + width_box.width()

height_label = QLabel(root)
height_label.setText('Height')
height_label.move(xoff,0)
height_box = QLineEdit(root)
height_box.setText('1080')
height_box.move(xoff,yoff)
xoff = xoff + height_box.width()

orbit_trap_button = QCheckBox(root)
orbit_trap_button.setText('Orbit?')
orbit_trap_button.move(xoff,0)

save_button = QCheckBox(root)
save_button.setText('Save?')
save_button.resize(save_button.width()-20,save_button.height())
save_button.move(xoff,yoff)
xoff = xoff + save_button.width()


set_only_button = QCheckBox(root)
set_only_button.setText('Set Only?')
set_only_button.move(xoff,0)

julia_button = QCheckBox(root)
julia_button.setText('Julia?')
julia_button.resize(julia_button.width()-20,julia_button.height())
julia_button.move(xoff,yoff)
xoff = xoff + julia_button.width()


julia_label = QLabel(root)
julia_label.setText('\tf(z)')
julia_label.move(xoff,0)
julia_box = QLineEdit(root)
julia_box.resize(julia_box.width()+30,julia_box.height())
julia_box.setText('z**2 + .34-.05j')
julia_box.move(xoff,yoff)
xoff = xoff + julia_box.width()

v_label = QLabel(root)
v_label.setText('V (threshold)')
v_label.move(xoff,0)
v_box = QLineEdit(root)
v_box.resize(v_box.width()+30,v_box.height())
v_box.setText('abs(z**2) <= 4')
v_box.move(xoff,yoff)
xoff = xoff + v_box.width()

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


time_label = QLabel(root)
time_label.move(xoff,yoff)
time_label.resize(200,30)
xoff = xoff + time_label.width()

image = QLabel(root)
image.move(0,60)

root.show()

def parse_complex(s):
    return complex(s.replace(' ','').replace('i','j'))

def julia_func(zn):
    func_string = 'lambda z: %s' % zn
    func = eval(func_string)
    numba_func = jit(nopython=True)(func)
    return numba_func

def render():
    start = time.time()
    center = parse_complex(center_box.text())
    window = float(window_box.text())
    iterations = int(iterations_box.text())
    width = int(width_box.text())
    height = int(height_box.text())
    pixels = None
    pic = None

    if julia_button.isChecked():
        #julia = parse_complex(julia_box.text())
        julia = julia_func(julia_box.text())
        v = julia_func(v_box.text())
        pixels = create_frame(center, window, width, height, iterations,julia,v)
    else:
        pixels = create_frame(center, window, width, height, iterations,None,None)
    
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
        plt.imsave(pic,pixels,cmap=color_option.currentText())
    else:
        pic = f'./tmp/{time.time()}.png'
        plt.imsave(pic,pixels,cmap=color_option.currentText())
    root.resize(width,height+60)
    image.resize(width,height)
    image.setPixmap(QPixmap(pic))
    end = time.time()
    time_label.setText('Render: %.3fs' % (end-start))

button.clicked.connect(render)
sys.exit(app.exec_())
