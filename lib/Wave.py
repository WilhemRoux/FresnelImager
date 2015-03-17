#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from cmath import pi
from time import strftime
from os.path import join

import numpy as np
from pyfits import PrimaryHDU


class WaveFront:
    """
    Class defining the electric state of a square plane perpendicular to the
    optical axes.

    Attributes
    ----------

    wavelength : float
        Wavelength of light generating the electric state.
    size : int
        The array length.
    real_size : float
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

        Parameters
        ----------

        wavelength : float
            Wavelength of monochromatic source.
        size : int
            The size of the array.
        real_size : float
            The real size of the considered wavefront.
        deviation : float (between 0° and 90°)
            Angle between the considered optical axis and the source.
        azimuth : float (between 0° an 360°)
            Angle between the horizontal semi-axis and the source.
        """

        print('Creating the wavefront...')

        self.wavelength = wavelength
        self.size = size
        self.real_size = real_size
        self.dx = real_size / size
        self.array = np.ones((size, size), complex)

        source_x = np.cos(azimuth) * np.sin(deviation)
        source_y = np.sin(azimuth) * np.sin(deviation)

        x = np.arange(self.size) * self.dx - (self.real_size - self.dx) / 2
        y = x[:, np.newaxis]

        opd = source_x * x + source_y * y
        self.array *= np.exp(1j * opd * (2 * pi / wavelength))

    def apply_mask(self, mask):
        print('Applying mask...')
        if isinstance(mask, np.ndarray):
            if mask.shape == self.array.shape:
                self.array[-mask] = 0
            else:
                raise ValueError('The mask must have the same size that the '
                                 'wavefront !')
        else:
            raise TypeError('%s is not a mask !' % mask.__class__.__name__)

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
        Divide the fft by square root of sampling to respect the Parceval
        equality (energy conservation). In 2 dimension, this is the same to
        divide by the sampling on only one axis.
        3/ Multiply it by another factor:
                exp(i*k/(2z)*(x^2+y^2)) = exp(i*pi/(lambda*z)*(x^2+y^2))
        4/ IN THEORY multiply it by exp(i*2*pi*z/lambda)/(i*lambda*z).
        But the pixels have already their width multiply by a factor (
        lambda*z) so it's not necessary to divide the value by (lambda*z).
        Finally, multiply the value by the factor :
                                exp(i*2*pi*z/lambda)/i

        Parameters
        ----------

        distance : float
            Distance of propagation.

        """
        if distance < 0:
            raise ValueError('The distance of propagation must be positive ('
                             '%f given).' % distance)
        elif distance == 0:
            print('Warning : No propagation, the wavefront is unchanged.')
        else:
            print('Propagation of wavefront on %f meters...' % distance)
            const = pi / distance / self.wavelength
            # First step
            x = np.arange(self.size) * self.dx - (self.real_size - self.dx) / 2
            y = x[:, np.newaxis]
            self.array = self.array * np.exp(1j * (x ** 2 + y ** 2) * const)
            # Second step
            self.array = np.fft.fft2(self.array) / self.size
            self.array = np.fft.fftshift(self.array)
            self.real_size = self.size * self.wavelength * distance / self.real_size
            self.dx = self.real_size / self.size
            # Third step
            x = np.arange(self.size) * self.dx - (self.real_size - self.dx) / 2
            y = x[:, np.newaxis]
            self.array *= np.exp(1j * (x ** 2 + y ** 2) * const)
            # Fourth step
            self.array *= np.exp(1j * 2 * pi * distance / self.wavelength) / 1j

    def get_total_energy(self):
        return (self.array * self.array.conjugate()).sum().real

    def save_module(self, output_directory_path):
        print('Save the wavefront...')
        file_name = 'WavefrontModule_' + strftime('%Y%m%d_%H%M%S') + '.fits'
        file_path = join(output_directory_path, file_name)
        print('Save wavefront in : %s' % file_path)
        hdu = PrimaryHDU()
        hdu.data = np.sqrt(self.array.real ** 2 + self.array.imag ** 2).T
        hdu.header.append(('TYPE', 'WAVEFRONT', 'Mask or wavefront'),
                          end=True)
        hdu.header.append(('LAMBDA', self.wavelength, 'Wavelength'), end=True)
        hdu.header.append(('SIZE', self.real_size, 'Size of the wavefront'),
                          end=True)
        # Save the .fits
        hdu.writeto(file_path)

    def save_log10_module(self, output_directory_path):
        print('Save the wavefront...')
        file_name = 'WavefrontLog10Module_' + strftime('%Y%m%d_%H%M%S') + \
                    '.fits'
        file_path = join(output_directory_path, file_name)
        print('Save wavefront in : %s' % file_path)
        hdu = PrimaryHDU()
        hdu.data = (np.log10(np.sqrt(self.array.real ** 2 + self.array.imag **
                                     2).T))
        hdu.scale('uint8', 'minmax')
        hdu.header.append(('TYPE', 'WAVEFRONT', 'Mask or wavefront'),
                          end=True)
        hdu.header.append(('LAMBDA', self.wavelength, 'Wavelength'), end=True)
        hdu.header.append(('SIZE', self.real_size, 'Size of the wavefront'),
                          end=True)
        # Save the .fits
        hdu.writeto(file_path)

    def save_complex(self, output_directory_path):
        file_name = 'WavefrontComplex_' + strftime('%Y%m%d_%H%M%S') + '.fits'
        file_path = join(output_directory_path, file_name)
        print('Save wavefront in : %s' % file_path)
        hdu = PrimaryHDU()
        hdu.header.append(('TYPE', 'WAVEFRONT', 'Mask or wavefront'),
                          end=True)
        hdu.header.append(('LAMBDA', self.wavelength, 'Wavelength'), end=True)
        hdu.header.append(('SIZE', self.real_size, 'Size of the wavefront'),
                          end=True)
        hdu.data = np.array([self.array.real, self.array.imag])
        # Save the .fits
        hdu.writeto(file_path)