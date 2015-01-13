#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import exit
from numpy import arange


class FresnelArray:

    def __init__(self):
        self.width = 0.065
        self.n_zones = 160
        self.obstruction = 0.
        self.central_offset = 0.75

    def transmission(self, wavefront):

        size = len(wavefront)
        if size % 2:
            print("Error : Wavefront sampling (%i) has to give an even number !"
                  % size)
            exit(1)

        # Width in meters of a pixel
        pixel_width = self.width / size

        # The edges of the Fresnel arrays will be in the center of pixels "0"
        # and "len(wavefront)-1"
        # So the Fresnel array have a width of "len(wavefront)-1"
        # Although the wavefront have a width of "len(wavefront)"

        # The Fresnel array center is on the edge between "len(wavefront)/2-1"
        # and "len(wavefront)/2"

        x_center = self.width / 2
        y_center = self.width / 2

        print pixel_width

        for i in arange(size/2):
            for j in arange(size/2):
                x = i * pixel_width - x_center
                y = j * pixel_width - y_center
                if self.is_perforated(x, y):
                    wavefront[i][j] = 1
                    # Due to the double symmetry
                    wavefront[i][size-1-j] = 1
                    wavefront[size-1-i][j] = 1
                    wavefront[size-1-i][size-1-j] = 1

    def is_perforated(self, x, y):
        return True