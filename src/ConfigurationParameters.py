#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import ConfigParser
from os.path import isdir
from os import makedirs
from sys import exit
import FresnelArray


class ConfigurationParameters:

    def __init__(self):
        self.output_directory_path = ""
        self.n_threads = 0
        self.wavefront_sampling = 10000
        self.source_optical_axis_angle = 0.
        self.source_direction_angle = 0.
        self.wavelength = 260.e-9
        self.fresnel_array = FresnelArray.FresnelArray()
        self.distance01 = 10.

    def read_configuration(self, configuration_file_path):
        parser = ConfigParser.RawConfigParser()
        parser.read(configuration_file_path)

        if parser.has_option('conf', 'output_directory_path'):
            self.output_directory_path = parser.get('conf',
                                                    'output_directory_path')
            if not isdir(self.output_directory_path):
                makedirs(self.output_directory_path)
        else:
            print ("Warning : No output_directory_path in %s ."
                   % configuration_file_path)
            print ("Default value : output_directory_path = %s"
                   % self.output_directory_path)

        if parser.has_option('conf', 'n_threads'):
            if parser.getint('conf', 'n_threads') >= 0:
                self.n_threads = parser.getint('conf', 'n_threads')
            else:
                print("Error : n_threads is negative.")
                exit(1)
        else:
            print ("Warning : No n_threads in %s ." % configuration_file_path)
            print ("Default value : n_threads = %s" % self.n_threads)

        if parser.has_option('conf', 'wavefront_sampling'):
            if parser.getint('conf', 'wavefront_sampling') > -1:
                self.wavefront_sampling = parser.getint('conf',
                                                        'wavefront_sampling')
            else:
                print("Error : wavefront_sampling is negative.")
                exit(1)
        else:
            print ("Warning : No wavefront_sampling in %s ." %
                   configuration_file_path)
            print ("Default value : wavefront_sampling = %s" %
                   self.wavefront_sampling)

        if parser.has_option('conf', 'source_optical_axis_angle'):
            self.source_optical_axis_angle = \
                parser.getfloat('conf', 'source_optical_axis_angle')
        else:
            print ("Warning : No source_optical_axis_angle in %s ." %
                   configuration_file_path)
            print ("Default value : source_optical_axis_angle = %s" %
                   self.source_optical_axis_angle)

        if parser.has_option('conf', 'source_direction_angle'):
            self.source_direction_angle = \
                parser.getfloat('conf', 'source_direction_angle')
        else:
            print ("Warning : No source_direction_angle in %s ." %
                   configuration_file_path)
            print ("Default value : source_direction_angle = %s" %
                   self.source_direction_angle)

        if parser.has_option('conf', 'wavelength'):
            if parser.getfloat('conf', 'wavelength') >= 0:
                self.wavelength = parser.getfloat('conf', 'wavelength')
            else:
                print("Error : wavelength is negative.")
                exit(1)
        else:
            print ("Warning : No wavelength in %s ." % configuration_file_path)
            print ("Default value : wavelength = %s" % self.wavelength)

        if parser.has_option('conf', 'width'):
            if parser.getfloat('conf', 'width') >= 0:
                self.fresnel_array.width = parser.getfloat('conf', 'width')
            else:
                print("Error : width is negative.")
                exit(1)
        else:
            print ("Warning : No width in %s ." % configuration_file_path)
            print ("Default value : width = %s" % self.fresnel_array.width)

        if parser.has_option('conf', 'n_zones'):
            if parser.getint('conf', 'n_zones') >= 0:
                self.fresnel_array.n_zones = parser.getfloat('conf', 'n_zones')
            else:
                print("Error : n_zones is negative.")
                exit(1)
        else:
            print ("Warning : No n_zones in %s ." % configuration_file_path)
            print ("Default value : n_zones = %s" %
                   self.fresnel_array.n_zones)

        if parser.has_option('conf', 'obstruction'):
            if parser.getfloat('conf', 'obstruction') >= 0:
                self.fresnel_array.obstruction =\
                    parser.getfloat('conf', 'obstruction')
            else:
                print("Error : obstruction is negative.")
                exit(1)
        else:
            print ("Warning : No obstruction in %s ." % configuration_file_path)
            print ("Default value : obstruction = %s" %
                   self.fresnel_array.obstruction)

        if parser.has_option('conf', 'central_offset'):
            if parser.getfloat('conf', 'central_offset') >= 0:
                self.fresnel_array.central_offset =\
                    parser.getfloat('conf', 'central_offset')
            else:
                print("Error : central_offset is negative.")
                exit(1)
        else:
            print ("Warning : No central_offset in %s ." %
                   configuration_file_path)
            print ("Default value : central_offset = %s" %
                   self.fresnel_array.central_offset)

        if parser.has_option('conf', 'distance01'):
            if parser.getfloat('conf', 'distance01') >= 0:
                self.wavelength = parser.getfloat('conf', 'distance01')
            else:
                print("Error : distance01 is negative.")
                exit(1)
        else:
            print ("Warning : No distance01 in %s ." % configuration_file_path)
            print ("Default value : distance01 = %s" % self.distance01)