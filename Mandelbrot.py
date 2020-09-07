#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from numba import jit, vectorize, cuda, uint8, uint32

@jit(nopython=True)
def fractal_generate(c, iterations, julia=None):
    if julia != None:
        z = c
        for i in range(iterations):
            z = z**2 + julia 
            if (z.real**2 + z.imag**2) >= 4:
                return i
        return iterations
    else:
        z = complex(0)
        for i in range(iterations):
            z = z**2 + c
            if (z.real**2 + z.imag**2) >= 4:
                return i
        return iterations

@jit(nopython=True)
def create_frame(center, window, im_w, iterations, julia):
    center = complex(center)
    min_x, max_x = center.real - window, center.real + window
    min_y, max_y = center.imag - window, center.imag + window
    reals = np.linspace(min_x,max_x,im_w)
    imags = np.linspace(min_y,max_y,im_w)

    #Initiate full array first, change contents in loop
    pixels = np.zeros((im_w*im_w),dtype=np.uint8)

    for x,r in enumerate(reals):
        for y,j in enumerate(imags):
            iteration_count = fractal_generate(complex(r + j*1j), iterations, julia) #Find escape iterations
            pixels[x + im_w*y] = iteration_count
     
    return pixels.reshape(im_w,im_w)

