#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import argv, exit
from src import ConfigurationParametersTools
from os.path import exists, isfile
from numpy import pi, cos, sin
import src.FitsTools as Fits


def run(conf_file):
    # Gets the parameters for the simulation
    print('Reading the configuration file : %s' % conf_file)
    parameters = ConfigurationParametersTools.ConfigurationParameters()
    parameters.read_configuration(conf_file)

    # Reads or creates the Fresnel Array
    print('Check if the Fresnel array already exists...')
    fresnel_array = Fits.read_or_create_fresnel_array(parameters)

    # Transform in wavefront
    wavefront = fresnel_array.astype('complex')

    # Adding a complex phase due to the offset of the source
    if parameters.source_optical_axis_angle > 0:
        deviation = parameters.source_optical_axis_angle / 180. * pi
        azimuth = parameters.source_direction_angle / 180. * pi
        # Compute the unit vector pointing to the source
        source_x = cos(azimuth) * sin(deviation)
        source_y = sin(azimuth) * sin(deviation)
        # Compute the phase to add to each pixel
        for line in wavefront:
            print line


if __name__ == '__main__':
    if len(argv) == 2:
        arg = argv[1]  # Configuration file
        if exists(arg):
            if isfile(arg):
                run(argv[1])
            else:
                print ("Error : %s is not a file !" % arg)
                exit(1)
        else:
            print ("Error : %s doesn't exist !" % arg)
            exit(1)
    elif len(argv) < 2:
        print "Error : There is no configuration file in arguments !"
        exit(1)
    else:
        print "Error : There is too much arguments to run the program !"
        exit(1)