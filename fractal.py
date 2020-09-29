#!/usr/bin/env python
# coding: utf-8

'''
Highly flexible fractal renderer
can produce generalized Mandelbrot and Julia sets with arbitrary escape thresholds
'''

import numpy as np
import matplotlib.pyplot as plt
from numba import jit, vectorize, cuda, uint8, uint32

'''
The core math function, JIT compiled
'''
@jit(nopython=True)
def fractal_generate(l, iterations, julia=None,v=None, mandelbrot=None):
    if julia != None: #Compute Julia set
        z = l #l for lambda
        for i in range(iterations):
            z = julia(z,l) # e.g. julia(z) = lambda z: z**2 + .34 -.05
            if v(z): # e.g. v(z) = lambda z: abs(z**2) >= 4 
                return i
        return iterations
    else: #Compute Mandelbrot set
        z = complex(0)
        for i in range(iterations):
            z = mandelbrot(z,l)
            if abs(np.power(z,2)) >= 4:
                return i
        return iterations

'''
Function that calls fractal_generate for each pixel in an image, returns 2D np array of floats 
'''
@jit(nopython=True)
def create_frame(center, window, im_w, im_h, iterations, julia=None, v=None, mandelbrot=None):
    center = complex(center)
    ratio = im_w / im_h
    min_x, max_x = center.real - ratio*window, center.real + ratio*window
    min_y, max_y = center.imag - window, center.imag + window
    reals = np.linspace(min_x,max_x,im_w)
    imags = np.linspace(min_y,max_y,im_h)

    #Initiate full array first, change contents in loop
    pixels = np.zeros((im_w*im_h),dtype=np.float64)

    for x,r in enumerate(reals):
        for y,j in enumerate(imags):
            iteration_count = fractal_generate(complex(r + j*1j),
             iterations, julia, v,mandelbrot) #Find escape iterations
            pixels[x + im_w*y] = iteration_count
     
    return pixels.reshape(im_h,im_w)


