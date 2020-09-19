import time
import matplotlib.pyplot as plt
from parser import parser
from mandelbrot import create_frame



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
        return 100*abs(iterations - v) % 255

    def continuous_color(v):
        return v

    if data['orbit']:
        pixels = orbit_color(pixels)
    else:
        pixels = continuous_color(pixels)

    if data['set_only']:
        for i,row in enumerate(pixels):
            for j,pixel in enumerate(row):
                pixels[i][j] = 0 if pixel < data['iterations'] else 1

    if data['save']:
        pic = f'./export/{time.time()}.png'
        plt.imsave(pic,pixels,cmap=data['palette'])
    else:
        pic = f'./tmp/{time.time()}.png'
        plt.imsave(pic,pixels,cmap=data['palette'])
    
    res = {'img':pic,'time':time.time()-start}
    return res



