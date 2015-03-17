#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import numpy as np
from cmath import pi
from time import strftime
from os.path import join
from pyfits import PrimaryHDU


class SquarePlane:
    """
    Class defining the electric state of a square plane perpendicular to the
    optical axes.

    Attributes
    ----------

    wavelength : float
        Wavelength of light generating the electric state.
    n : int
        The array length.
    size : float
        The square plane side size in meters.
    dx : float
        The size in meters of an array element.
    array : ndarray of complex
        The array containing the complex values of electric field at the
        center of the surface elements.
    """

    def __init__(self, wavelength, size, real_size, deviation=0., azimuth=0.):
        """
        Creates an initial wavefront of a coherent light source located at
        infinity.
        :param deviation:
        :param azimuth:
        :return:
        """




    def apply(self, wavelength, size, arg):
        """
        Constructor of a SquarePlane.

        Parameters
        ----------
        size : float
            The square plane side size in meters.
        arg : int or ndarray
            If int : Defines the array length and generate a random ndarray.
            If ndarray : Copy this array in the square plane and calculate
            other parameters.

        Raises
        ------
        ValueError : If arg is an 'int' and is negative or if n is negative.
        TypeError : If arg is not an 'int' or a 'ndarray'.

        """
        if isinstance(arg, int):
            if arg > 0:
                if size > 0:
                    self.wavelength = wavelength
                    self.n = arg
                    self.size = size
                    self.dx = size / arg
                    self.array = np.ndarray((arg, arg), complex)
                else:
                    raise ValueError('The size of a SquarePlane must be '
                                     'strictly positive !')
            else:
                raise ValueError('The number of elements on a SquarePlane'
                                 'must be strictly positive !')
        elif isinstance(arg, np.ndarray):
            self.wavelength = wavelength
            self.size = size
            self.array = arg.astype('complex')
            self.n = len(arg)
            self.dx = size / self.n
        else:
            raise TypeError('The second argument must be an int or ndarray !')

    def fresnel_propagation(self, distance):
        """
        fresnel_propagation(distance, wavelength)

        This function simulates a SquarePlane after a propagation in vacuum
        along a certain distance on this axis.
        It uses the Fresnel diffraction theory to compute the new values of
        electric field after the propagation.

        1/ Multiply the field to be propagated for a complex exponential:
            exp(i*k/(2z)*(x^2+y^2)) = exp(i*pi/(lambda*z)*(x^2+y^2))
        2/ Calculate its two-dimensional Fourier transform and replace
        coordinates by (x/(lambda*z), y/(lambda*z))
        3/ Multiply it by another factor:
            exp(i*k/(2z)*(x^2+y^2)) = exp(i*pi/(lambda*z)*(x^2+y^2))
        4/ Multiply it by exp(i*2*pi*z/lambda)/(i*lambda*z)

        Parameters
        ----------

        distance : float
            Distance of propagation.

        """
        const = pi / distance / self.wavelength
        # First step
        end = (self.size - self.dx) / 2
        x = np.linspace(-end, end, num=self.n)
        y = x[:, np.newaxis]
        self.array = self.array * np.exp(1j * (x ** 2 + y ** 2) * const)
        # Second step
        self.array = np.fft.fft2(self.array) / self.n
        self.array = np.fft.fftshift(self.array)
        self.size = self.n * self.wavelength * distance / self.size
        self.dx = self.size / self.n
        # Third step
        end = (self.size - self.dx) / 2
        x = np.linspace(-end, end, num=self.n)
        y = x[:, np.newaxis]
        self.array *= np.exp(1j * (x ** 2 + y ** 2) * const)

    def save_module(self, output_directory_path):
        file_name = 'WavefrontModule_' + strftime('%Y%m%d_%H%M%S') + '.fits'
        file_path = join(output_directory_path, file_name)
        print('Save wavefront in : %s' % file_path)
        hdu = PrimaryHDU()
        hdu.data = np.sqrt(self.array.real ** 2 + self.array.imag ** 2).T
        # Save the .fits
        hdu.writeto(file_path)