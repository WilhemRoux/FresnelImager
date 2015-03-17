#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from distutils.core import setup, Extension
from os.path import exists
import numpy

if exists('fresnel_array_generator.c'):
    # Defines the extension module
    fresnel_array_generator = Extension('fresnel_array_generator',
                                        sources=['fresnel_array_generator.c'],
                                        include_dirs=[numpy.get_include()])
    # Runs the setup
    setup(ext_modules=[fresnel_array_generator])
else:
    raise IOError('The file \'fresnel_array_generator.c\' doesn\'t exist in '
                  'the directory /lib/C_modules/')