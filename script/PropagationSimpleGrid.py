#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import argv
from lib import ConfigurationParameters
from os.path import exists, isfile
import lib.FitsTools as Fits
from lib.WaveFront import WaveFront
from time import strftime


def run(conf_file):

    # Gets the parameters for the simulation
    parameters = ConfigurationParameters.ConfigurationParameters(conf_file)

    # Reads or creates the Fresnel Array
    print strftime('%H:%M:%S')
    fresnel_array = Fits.read_or_create_fresnel_array(parameters)
    print strftime('%H:%M:%S')

    wavefront = WaveFront(parameters.wavelength,
                          parameters.wavefront_sampling,
                          parameters.fresnel_array.width,
                          parameters.source_optical_axis_angle,
                          parameters.source_direction_angle)

    wavefront.apply_mask(fresnel_array)

    wavefront.fresnel_propagation(parameters.fresnel_array.focal_length)

    wavefront.save_module(parameters.output_directory)

if __name__ == '__main__':
    if len(argv) == 2:
        arg = argv[1]  # Configuration file
        if exists(arg):
            if isfile(arg):
                run(argv[1])
            else:
                raise IOError('%s is not a file' % arg)
        else:
            raise IOError('%s does not exist' % arg)
    else:
        raise TypeError('Execution requires exactly 2 argument (%d given)' %
                        len(argv))