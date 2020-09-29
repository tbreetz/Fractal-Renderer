#!/usr/bin/env python
# coding: utf-8

'''
highly flexible fractal renderer
can produce the orbit traps, julia set
'''
import numpy as np
import math
import matplotlib.pyplot as plt
from numba import jit, vectorize, cuda, uint8, uint32

@cuda.jit
def apply_fractal_transformation(numbers,pixels,max_iter,mandelbrot):
    x,y = cuda.grid(2)
    c = numbers[x,y]
    if x < pixels.shape[0] and y < pixels.shape[1]:
        z = complex(0)
        for i in range(max_iter):
            z = mandelbrot(z,c)
            if abs(z**2) >= 4:
                pixels[x,y] = i
                
        if i == max_iter: pixels[x,y] = max_iter

@jit(nopython=True)
def fractal_generate(l, iterations, julia=None,v=None, mandelbrot=None):
    if julia != None:
        z = l #l for lambda
        for i in range(iterations):
            z = julia(z,l) # e.g. julia(z) = lambda z: z**2 + .34 -.05
            if v(z): # e.g. v(z) = lambda z: abs(z**2) >= 4 
                return i
        return iterations
    else:
        z = complex(0)
        for i in range(iterations):
            z = mandelbrot(z,l)
            if abs(np.power(z,2)) >= 4:
                return i
        return iterations


def create_frame(center, window, im_w, im_h, iterations, julia=None, v=None, mandelbrot=None):
    center = complex(center)
    ratio = im_w / im_h
    min_x, max_x = center.real - ratio*window, center.real + ratio*window
    min_y, max_y = center.imag - window, center.imag + window
    reals = np.linspace(min_x,max_x,im_w)
    imags = np.linspace(min_y,max_y,im_h)
    numbers = np.zeros((im_w,im_h),dtype=np.complex64)
    for x,r in enumerate(reals):
        for y,j in enumerate(imags):
            numbers[x,y] = complex(r,j)
    pixels = np.zeros((im_w,im_h),dtype=np.int32)
    threadsperblock = (32,32)
    blockspergrid_x = math.ceil(pixels.shape[0] / threadsperblock[0])
    blockspergrid_y = math.ceil(pixels.shape[1] / threadsperblock[1])
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    #Send empty pixel array to GPU, this is where the results will end up
    d_pixels = cuda.to_device(pixels) 
    #Send the complex numbers to calculate escape iteration for a given fractal function
    d_numbers = cuda.to_device(numbers) 
    d_func = cuda.to_device(mandelbrot)
    apply_fractal_transformation[blockspergrid, threadsperblock](d_numbers,d_pixels,iterations,d_func) #Apply the function to find escape time
    #Copy result back to current scope
    pixels = d_pixels.copy_to_host() 
    return pixels
    '''for x,r in enumerate(reals):
        for y,j in enumerate(imags):
            #iteration_count = fractal_generate(complex(r + j*1j),
            # iterations, julia, v,mandelbrot) #Find escape iterations
              
    return pixels.reshape(im_h,im_w)'''


