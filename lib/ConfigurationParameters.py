#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import ConfigParser
from os.path import isdir
from os import makedirs
import FresnelArray


class ConfigurationParameters:

    def __init__(self):
        self.output_directory_path = ''
        self.wavefront_sampling = 10000
        self.source_optical_axis_angle = 0.
        self.source_direction_angle = 0.
        self.wavelength = 260.e-9
        self.fresnel_array = FresnelArray.FresnelArray()
        self.distance01 = 10.

    def read_configuration(self, configuration_file_path):

        parser = ConfigParser.RawConfigParser()
        parser.read(configuration_file_path)

        read_parameters = {}
        for section in parser.sections():
            for item in parser.items(section):
                read_parameters[item[0]] = item[1]

        if 'output_directory_path' in read_parameters:
            self.output_directory_path = read_parameters[
                'output_directory_path']
            if not isdir(self.output_directory_path):
                makedirs(self.output_directory_path)
        else:
            print ('Warning : No output_directory_path in %s .'
                   % configuration_file_path)
            print ('Default value : output_directory_path = %s'
                   % self.output_directory_path)

        if 'wavefront_sampling' in read_parameters:
            if int(read_parameters['wavefront_sampling']) > 0:
                if int(read_parameters['wavefront_sampling']) % 2 == 0:
                    self.wavefront_sampling = int(
                        read_parameters['wavefront_sampling'])
                else:
                    raise ValueError('wavefront_sampling must be an even '
                                     'number.')
            else:
                raise ValueError('wavefront_sampling must be positive.')
        else:
            print ('Warning : No wavefront_sampling in %s .' %
                   configuration_file_path)
            print ('Default value : wavefront_sampling = %s' %
                   self.wavefront_sampling)

        if 'source_optical_axis_angle' in read_parameters:
            self.source_optical_axis_angle = float(
                read_parameters['source_optical_axis_angle'])
        else:
            print ('Warning : No source_optical_axis_angle in %s .' %
                   configuration_file_path)
            print ('Default value : source_optical_axis_angle = %s' %
                   self.source_optical_axis_angle)

        if 'source_direction_angle' in read_parameters:
            self.source_direction_angle = float(
                read_parameters['source_direction_angle'])
        else:
            print ('Warning : No source_direction_angle in %s .' %
                   configuration_file_path)
            print ('Default value : source_direction_angle = %s' %
                   self.source_direction_angle)

        if 'wavelength' in read_parameters:
            if float(read_parameters['wavelength']) >= 0:
                self.wavelength = float(read_parameters['wavelength'])
                self.fresnel_array.wavelength = self.wavelength
            else:
                raise ValueError('wavelength must be positive.')
        else:
            print ('Warning : No wavelength in %s .' % configuration_file_path)
            print ('Default value : wavelength = %s' % self.wavelength)

        if 'width' in read_parameters:
            if float(read_parameters['width']) > 0:
                self.fresnel_array.width = float(read_parameters['width'])
            else:
                raise ValueError('width must be positive.')
        else:
            print ('Warning : No width in %s .' % configuration_file_path)
            print ('Default value : width = %s' % self.fresnel_array.width)

        if 'n_zones' in read_parameters:
            if int(read_parameters['n_zones']) > 0:
                self.fresnel_array.n_zones = int(read_parameters['n_zones'])
            else:
                raise ValueError('n_zones must be positive')
        else:
            print ('Warning : No n_zones in %s .' % configuration_file_path)
            print ('Default value : n_zones = %s' %
                   self.fresnel_array.n_zones)

        if 'obstruction' in read_parameters:
            if float(read_parameters['obstruction']) >= 0:
                self.fresnel_array.obstruction = float(
                    read_parameters['obstruction'])
            else:
                raise ValueError('obstruction must be zero or positive')
        else:
            print ('Warning : No obstruction in %s .' % configuration_file_path)
            print ('Default value : obstruction = %s' %
                   self.fresnel_array.obstruction)

        if 'central_offset' in read_parameters:
            if float(read_parameters['central_offset']) >= 0:
                self.fresnel_array.offset = float(
                    read_parameters['central_offset'])
            else:
                raise ValueError('central_offset must be zero or positive')
        else:
            print ('Warning : No central_offset in %s .' %
                   configuration_file_path)
            print ('Default value : central_offset = %s' %
                   self.fresnel_array.offset)

        if 'distance01' in read_parameters:
            if float(read_parameters['distance01']) > 0:
                self.wavelength = float(read_parameters['distance01'])
            else:
                raise ValueError('distance01 must be positive')
        else:
            print ('Warning : No distance01 in %s .' % configuration_file_path)
            print ('Default value : distance01 = %s' % self.distance01)