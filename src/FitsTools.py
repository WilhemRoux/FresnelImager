#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import numpy
import pyfits
from math import sqrt


def save_complex_wavefront(fits_file_path, wavefront):

    height = len(wavefront)
    width = len(wavefront[0])
    image = numpy.zeros((2, height, width))

    for i in numpy.arange(height):
        for j in numpy.arange(width):
            image[0][i][j] = wavefront[i][j].real
            image[1][i][j] = wavefront[i][j].imag

    pyfits.writeto(fits_file_path, image, clobber=True)


def save_module_wavefront(fits_file_path, wavefront):

    height = len(wavefront)
    width = len(wavefront[0])
    image = numpy.zeros((height, width))

    for i in numpy.arange(height):
        for j in numpy.arange(width):
            image[i][j] = sqrt(wavefront[i][j].real ^ 2 + wavefront[i][
                j].imag ^ 2)

    pyfits.writeto(fits_file_path, image, clobber=True)