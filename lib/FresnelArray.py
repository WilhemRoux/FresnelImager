#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import glob
from os.path import join, exists
from os import remove
from subprocess import call
from sys import executable, exit
from time import strftime

from numpy import arange, zeros, newaxis, sqrt
import pyfits


class FresnelArray:
    def __init__(self, width=0.065, n_zones=160, obstruction=0, offset=0.75,
                 wavelength=260.e-9, size=10000, beta_0=0.25):

        self.fits_parameters = []
        self.fits_parameters.append(('NAXIS', 2))

        self.size = size
        self.fits_parameters.append(('NAXIS1', size))
        self.fits_parameters.append(('NAXIS2', size))

        self.fits_parameters.append(('TYPE', 'FresnelArray'))

        self.width = width
        self.fits_parameters.append(('WIDTH', width))

        self.n_zones = n_zones
        self.fits_parameters.append(('NZONES', n_zones))

        self.obstruction = obstruction
        self.fits_parameters.append(('OBSTR', obstruction))

        self.offset = offset
        self.fits_parameters.append(('OFFSET', offset))

        self.wavelength = wavelength
        self.fits_parameters.append(('LAMBDA', wavelength))

        self.beta_0 = beta_0
        self.fits_parameters.append(('BETA0', beta_0))

        self.focal_length = (self.width / 2) ** 2 / \
                            (2 * self.n_zones + self.offset - 0.75) / \
                            self.wavelength
        self.white_rings = []

    def __create_binary_transmission_C(self):

        # Delete the precedent C modules for auto re-compiling
        if exists('../lib/C_modules/fresnel_array_generator.so'):
            remove('../lib/C_modules/fresnel_array_generator.so')

        # Executes the setup.py to create the modules from C
        exit_code = call([executable, 'setup.py', 'build_ext', '--inplace'],
                         cwd='../lib/C_modules')

        if exit_code != 0:
            exit(exit_code)

        import lib.C_modules.fresnel_array_generator

        # Create the array, filled with False
        mask = lib.C_modules.fresnel_array_generator.get_mask(self.width,
                                                              self.n_zones,
                                                              self.obstruction,
                                                              self.offset,
                                                              self.wavelength,
                                                              self.size,
                                                              self.beta_0)

        return mask

    def read_or_create_fresnel_array(self, output_directory):
        print('Check if the Fresnel array already exists...')
        # Search fits file in the output directory
        fits_files = glob.glob(join(output_directory, '*.fits'))
        for fits_file in fits_files:
            header = pyfits.open(fits_file)[0].header
            # The Fresnel array already exists
            if self.__compare_parameters_with_header(header):
                print('Reading the Fresnel array : %s' % fits_file)
                return self.__read_fresnel_array(fits_file)
        # The Fresnel array doesn't exist
        file_name = 'FresnelArray_' + strftime('%Y%m%d_%H%M%S') + \
                    '.fits'
        file_path = join(output_directory, file_name)
        return self.__create_fresnel_array(file_path)

    def read_fresnel_array(self, file_path):
        hdu = pyfits.open(file_path)
        return hdu[0].data.astype('bool')

    def create_fresnel_array(self, file_path):
        print('Creating the new Fresnel array in %s' % file_path)
        image = self.__create_binary_transmission_C()
        hdu = pyfits.PrimaryHDU(image.astype('uint8'))
        hdu.scale('uint8', 'minmax')
        # Creation of header containing the characteristics of the Fresnel Array
        for parameter in self.fits_parameters:
            if not parameter[0] in hdu.header:
                hdu.header.append(parameter)
        # Save the .fits
        hdu.writeto(file_path)
        return image

    def __compare_parameters_with_header(self, head):
        for parameter in self.fits_parameters:
            if parameter[0] in head:
                if head[parameter[0]] != parameter[1]:
                    return False
            else:
                return False
        return True