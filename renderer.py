import time
import os
import matplotlib.pyplot as plt
from parser import parser
from fractal import create_frame

'''
This module contains a rendering function that takes
input data specifying a fractal function to render.
To specify a fractal, a window size, width, height,
 and complex polynomial function are needed.
Render time and an image file path are returned.
'''

def renderer(data):
    start = time.time()
    mandelbrot = parser.string_to_func(data['mandelbrot'])
    center = parser.string_to_complex(data['center'])
    if data['julia']:
        julia = parser.string_to_func(data['fz'])
        v = parser.string_to_func(data['v'])
        pixels = create_frame(center, data['window'],
                              data['width'], data['height'], 
                              data['iterations'],julia,v,mandelbrot)
    else:
        pixels = create_frame(center, data['window'],
                              data['width'], data['height'], 
                              data['iterations'],None,None,mandelbrot)
    
    def orbit_color(v):
        return 100*abs(data['iterations'] - v) % 255

    def continuous_color(v):
        return v * (1/v.max())

    def continuous_color2(v):
        return v

    if data['orbit']:
        pixels = orbit_color(pixels)
    else:
        pixels = continuous_color2(pixels)

    if data['set_only']:
        for i,row in enumerate(pixels):
            for j,pixel in enumerate(row):
                pixels[i][j] = 0 if pixel < data['iterations'] else 1

    if data['save']:
        pic = f'./export/{time.time()}.png'
        plt.imsave(pic,pixels,cmap=data['palette'])
    else:
        if not os.path.exists('./tmp/'):
            os.mkdir('./tmp')
        files = [f for f in os.listdir('./tmp/') if f.endswith('.png')]
        for f in files:
            os.remove(os.path.join('./tmp/',f)) #Remove old tmp files
        pic = f'./tmp/{time.time()}.png'
        plt.imsave(pic,pixels,cmap=data['palette'])
    
    res = {'img':pic,'time':time.time()-start}
    return res



