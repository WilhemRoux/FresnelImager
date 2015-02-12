#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import ConfigParser
from os.path import isdir
from os import makedirs, getcwd
import FresnelArray


class ConfigurationParameters:
    def __init__(self, conf_file):

        print('Reading the configuration file : %s' % conf_file)

        # Reads the configuration file

        parser = ConfigParser.RawConfigParser()
        parser.read(conf_file)
        read_parameters = {}
        for section in parser.sections():
            for item in parser.items(section):
                read_parameters[item[0]] = item[1]

        # Organize parameters

        self.output_directory = getcwd()
        if 'output_directory' in read_parameters:
            print read_parameters['output_directory']
            self.output_directory = read_parameters['output_directory']
            if not isdir(self.output_directory):
                makedirs(self.output_directory)
        print('output_directory = %s' % self.output_directory)

        self.wavefront_sampling = 10000
        if 'wavefront_sampling' in read_parameters:
            n = int(read_parameters['wavefront_sampling'])
            if n > 0:
                if n % 2 == 0:
                    self.wavefront_sampling = n
                else:
                    raise ValueError('wavefront_sampling must be an even int'
                                     '(%d given)' % n)
            else:
                raise ValueError('wavefront_sampling must be positive (%d '
                                 'given)' % n)
        print('wavefront_sampling = %s' % self.wavefront_sampling)

        self.source_optical_axis_angle = 0.
        if 'source_optical_axis_angle' in read_parameters:
            angle = float(read_parameters['source_optical_axis_angle'])
            if 0 <= angle < 90:
                self.source_optical_axis_angle = angle
            else:
                raise ValueError('source_optical_axis_angle must be between '
                                 '0 and 90 (%f given)' % angle)
        print('source_optical_axis_angle = %s' % self.source_optical_axis_angle)

        self.source_direction_angle = 0.
        if 'source_direction_angle' in read_parameters:
            angle = float(read_parameters['source_direction_angle'])
            if 0 <= angle < 360:
                self.source_direction_angle = angle
            else:
                raise ValueError('source_direction_angle must be between '
                                 '0 and 360 (%f given)' % angle)
        print('source_optical_axis_angle = %s' % self.source_direction_angle)

        self.wavelength = 260.e-9
        if 'wavelength' in read_parameters:
            wavelength = float(read_parameters['wavelength'])
            if wavelength > 0:
                self.wavelength = wavelength
            else:
                raise ValueError('wavelength must be positive (%f given)' %
                                 wavelength)
        print('wavelength = %s' % self.wavelength)

        self.distance01 = 10.
        if 'distance01' in read_parameters:
            distance01 = float(read_parameters['distance01'])
            if distance01 > 0:
                self.distance01 = distance01
            else:
                raise ValueError('distance01 must be positive')
        print('distance01 = %s' % self.distance01)

        width = 0.065
        if 'width' in read_parameters:
            width = float(read_parameters['width'])
            if width < 0:
                raise ValueError('width must be positive (%f given)' % width)
        print('width = %s' % width)

        n_zones = 160
        if 'n_zones' in read_parameters:
            n_zones = int(read_parameters['n_zones'])
            if n_zones < 0:
                raise ValueError(
                    'n_zones must be positive (%d given)' % n_zones)
        print('n_zones = %s' % n_zones)

        obstruction = 0.
        if 'obstruction' in read_parameters:
            obstruction = float(read_parameters['obstruction'])
            if obstruction < 0:
                raise ValueError('obstruction must be zero or positive '
                                 '(%f given)' % obstruction)
        print('obstruction = %s' % obstruction)

        offset = 0.75
        if 'central_offset' in read_parameters:
            offset = float(read_parameters['central_offset'])
            if offset < 0:
                raise ValueError('central_offset must be zero or positive '
                                 '(%f given)' % offset)
        print('central_offset = %s' % offset)

        self.fresnel_array = FresnelArray.FresnelArray(width,
                                                       n_zones,
                                                       obstruction,
                                                       offset,
                                                       self.wavelength)