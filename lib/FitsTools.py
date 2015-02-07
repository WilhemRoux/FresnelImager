#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import numpy
import pyfits
import glob
from time import strftime
from os.path import join

# BITPIX    Numpy Data Type
# 8         numpy.uint8 (note it is unsigned integer)
# 16        numpy.int16
# 32        numpy.int32
# -32       numpy.float32
# -64       numpy.float64


def save_complex_image(fits_file_path, image, dtype='float64'):
    image = numpy.array([image.real, image.imag])

    pyfits.writeto(fits_file_path, image.astype(dtype), clobber=True)


def save_module_image(fits_file_path, image, dtype='float64'):
    image = numpy.sqrt(image.real ** 2 + image.imag ** 2)

    pyfits.writeto(fits_file_path, image.astype(dtype), clobber=True)

def save_wavefront(parameters, wavefront):
    file_name = 'Wavefront_' + strftime('%Y%m%d_%H%M%S') + '.fits'
    file_path = join(parameters.output_directory_path, file_name)
    print('Save wavefront in : %s' % file_path)
    hdu = pyfits.PrimaryHDU()
    hdu.data = numpy.array([wavefront.real.transpose(),
                            wavefront.imag.transpose()])
    # Save the .fits
    hdu.writeto(file_path)

def save_wavefront_module(parameters, wavefront):
    file_name = 'WavefrontModule_' + strftime('%Y%m%d_%H%M%S') + '.fits'
    file_path = join(parameters.output_directory_path, file_name)
    print('Save wavefront in : %s' % file_path)
    hdu = pyfits.PrimaryHDU()
    hdu.data = numpy.array((wavefront.real**2+wavefront.imag**2).transpose())
    # Save the .fits
    hdu.writeto(file_path)

def read_fresnel_array(file_path):
    hdu = pyfits.open(file_path)
    return hdu[0].data.astype('bool')


def create_fresnel_array(file_path, parameters):
    image = parameters.fresnel_array.create_binary_transmission(
        parameters.wavefront_sampling)
    hdu = pyfits.PrimaryHDU(image.astype('uint8'))
    # Creation of header containing the characteristics of the Fresnel Array
    fresnel_array_params = parameters.fresnel_array.get_params_list()
    for param in fresnel_array_params:
        hdu.header.append((param[0], param[1], param[2]), end=True)
    # Scaling image
    hdu.scale(bscale=1 / 255.)
    # Save the .fits
    hdu.writeto(file_path)
    return image


def read_or_create_fresnel_array(parameters):
    # Search fits file in the output directory
    fits_files = glob.glob(join(parameters.output_directory_path, '*.fits'))
    for fits_file in fits_files:
        # The Fresnel array already exists
        if has_same_parameters(parameters, fits_file):
            print('Reading the Fresnel array : %s' % fits_file)
            return read_fresnel_array(fits_file)
    # The Fresnel array doesn't exist
    file_name = 'FresnelArray_' + strftime('%Y%m%d_%H%M%S') + '.fits'
    file_path = join(parameters.output_directory_path, file_name)
    print('Creating the Fresnel array in : %s' % file_path)
    return create_fresnel_array(file_path, parameters)


def has_same_parameters(parameters, fits_file):
    # Gets the header
    header = pyfits.open(fits_file)[0].header
    # Compare the size
    if not header['NAXIS'] == 2:
        return False
    if not header['NAXIS1'] == parameters.wavefront_sampling:
        return False
    if not header['NAXIS2'] == parameters.wavefront_sampling:
        return False
    # Compare Fresnel array parameter
    params = parameters.fresnel_array.get_params_list()
    for param in params:
        if param[0] in header:
            if param[1] == header[param[0]]:
                pass
            else:
                return False
        else:
            return False
    return True