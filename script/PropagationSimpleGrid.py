#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import argv, exit
from lib import ConfigurationParameters
from os.path import exists, isfile
import lib.FitsTools as Fits
from lib.WaveFront import WaveFront


def run(conf_file):

    # Gets the parameters for the simulation
    print('Reading the configuration file : %s' % conf_file)
    parameters = ConfigurationParameters.ConfigurationParameters()
    parameters.read_configuration(conf_file)

    # Reads or creates the Fresnel Array
    print('Check if the Fresnel array already exists...')
    #fresnel_array = Fits.read_or_create_fresnel_array(parameters)
    #print ('The raw transmission is : %f'
           #% (float(fresnel_array.sum())/fresnel_array.size))

    # Transform in wavefront
    wavefront = WaveFront(parameters.wavelength,
                          parameters.wavefront_sampling,
                          parameters.fresnel_array.width,
                          parameters.source_optical_axis_angle,
                          parameters.source_direction_angle)
    wavefront.apply_mask(parameters.fresnel_array)
    wavefront.fresnel_propagation(parameters.fresnel_array.focal_length)
    wavefront.save_module(parameters.output_directory_path)

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