from numba import jit, cuda
import numpy as np

'''
A parser class with methods for:
    Converting strings to complex numbers
    Converting strings into safe functions for plotting mandelbrot/julia sets
'''

class parser:
    def string_to_complex(s):
        return complex(s.replace(' ', '').replace('i','j'))

    def string_to_func(zn):
        func_string = 'lambda z,l = None: %s' % zn
        func = eval(func_string, {'__builtins__':None, 'exp':np.exp},
        {'pow':pow,'abs':abs})
        numba_func = cuda.jit(device=True)(func)
        return numba_func
