#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import argv, exit
from lib import ConfigurationParametersTools
from os.path import exists, isfile
from time import strftime
import lib.FitsTools as Fits
from lib.SquarePlane import SquarePlane


def run(conf_file):

    # Gets the parameters for the simulation
    print('Reading the configuration file : %s' % conf_file)
    parameters = ConfigurationParametersTools.ConfigurationParameters()
    parameters.read_configuration(conf_file)

    # Reads or creates the Fresnel Array
    print('Check if the Fresnel array already exists...')
    fresnel_array = Fits.read_or_create_fresnel_array(parameters)
    print ('The raw transmission is : %f'
           % (float(fresnel_array.sum())/fresnel_array.size))

    # Transform in wavefront
    wavefront = SquarePlane(parameters.wavelength,
                            parameters.fresnel_array.width, fresnel_array)
    # Adding a complex phase due to the offset of the source
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