#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import argv, exit
from src import ConfigurationParameters
from os.path import exists, isfile
import numpy
from src.FitsTools import save_complex_wavefront


def run(conf_file):

    # Gets the parameters for the simulation
    params = ConfigurationParameters.ConfigurationParameters()
    params.read_configuration(conf_file)

    # Create a wavefront
    wavefront = numpy.zeros((params.wavefront_sampling,
                             params.wavefront_sampling), complex)

    # Wavefront through the Fresnel Array
    params.fresnel_array.apply_transmission(wavefront)

    # Save the wavefront
    fits_file_path = params.output_directory_path + "/wavefront.fits"
    save_complex_wavefront(fits_file_path, wavefront)

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