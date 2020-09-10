#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from numba import jit, vectorize, cuda, uint8, uint32

@jit(nopython=True)
def fractal_generate(l, iterations, julia=None,v=None):
    if julia != None:
        z = l #l for lambda
        for i in range(iterations):
            z = julia(z) # julia(z) = lambda z: z**2 + .34 -.05
            if v(z): # v(z) = lambda z: abs(z**2) >= 4 
                return i
        return iterations
    else:
        z = complex(0)
        for i in range(iterations):
            z = z**2 + l
            if abs(np.power(z,2)) >= 4:
                return i
        return iterations

@jit(nopython=True)
def create_frame(center, window, im_w, im_h, iterations, julia=None, v=None):
    center = complex(center)
    ratio = im_w / im_h
    min_x, max_x = center.real - ratio*window, center.real + ratio*window
    min_y, max_y = center.imag - window, center.imag + window
    reals = np.linspace(min_x,max_x,im_w)
    imags = np.linspace(min_y,max_y,im_h)

    #Initiate full array first, change contents in loop
    pixels = np.zeros((im_w*im_h),dtype=np.uint8)

    for x,r in enumerate(reals):
        for y,j in enumerate(imags):
            iteration_count = fractal_generate(complex(r + j*1j), iterations, julia, v) #Find escape iterations
            pixels[x + im_w*y] = iteration_count
     
    return pixels.reshape(im_h,im_w)


