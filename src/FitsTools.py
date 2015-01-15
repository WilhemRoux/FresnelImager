#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import numpy as np
import pyfits

# BITPIX    Numpy Data Type
# 8         numpy.uint8 (note it is UNsigned integer)
# 16        numpy.int16
# 32        numpy.int32
# -32       numpy.float32
# -64       numpy.float64


def save_complex_wavefront(fits_file_path, wavefront, dtype='float64'):

    image = np.array([wavefront.real, wavefront.imag])

    pyfits.writeto(fits_file_path, image.astype(dtype), clobber=True)


def save_module_wavefront(fits_file_path, wavefront, dtype = 'float64'):

    image = np.sqrt(np.power(wavefront.real, 2) + np.power(wavefront.imag, 2))

    pyfits.writeto(fits_file_path, image.astype(dtype), clobber=True)