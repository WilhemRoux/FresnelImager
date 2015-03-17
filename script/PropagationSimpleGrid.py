#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import argv
from os.path import exists, isfile, join
from time import strftime


from lib import ConfigurationParameters
from lib.WaveFront import WaveFront
import lib.PreliminaryTests


def run(conf_file):

    # Gets the parameters for the simulation
    parameters = ConfigurationParameters.ConfigurationParameters(conf_file)

    # Preliminary test to validate parameters


    # Reads or creates the Fresnel Array
    print strftime('%H:%M:%S')
    file_name = 'FresnelArray_' + strftime('%Y%m%d_%H%M%S') +\
                '.fits'
    file_path = join(parameters.output_directory, file_name)
    fa = parameters.fresnel_array.create_fresnel_array(file_path)
    print strftime('%H:%M:%S')

    wavefront = WaveFront(parameters.wavelength,
                          parameters.wavefront_sampling,
                          parameters.fresnel_array.width,
                          parameters.source_optical_axis_angle,
                          parameters.source_direction_angle)

    wavefront.apply_mask(fa)

    #print wavefront.get_total_energy()

    wavefront.fresnel_propagation(parameters.fresnel_array.focal_length)

    #print wavefront.get_total_energy()

    wavefront.save_log10_module(parameters.output_directory)

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