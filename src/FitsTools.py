#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import numpy
import pyfits
from math import sqrt, pow


def save_complex_wavefront(fits_file_path, wavefront):

    height = len(wavefront)
    width = len(wavefront[0])
    image = numpy.empty((2, height, width))

    i = 0
    while i < height:
        j = 0
        while j < width:
            image[0][i][j] = wavefront[i][j].real
            image[1][i][j] = wavefront[i][j].imag
            j += 1
        i += 1

    pyfits.writeto(fits_file_path, image, clobber=True)


def save_module_wavefront(fits_file_path, wavefront):

    height = len(wavefront)
    width = len(wavefront[0])
    image = numpy.empty_like((height, width))

    i = 0
    while i < height:
        j = 0
        while j < width:
            c = wavefront[i][j]
            image[i][j] = sqrt(pow(c.real, 2) + pow(c.imag, 2))
            j += 1
        i += 1

    pyfits.writeto(fits_file_path, image, clobber=True)