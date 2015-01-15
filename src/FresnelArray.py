#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import exit
from numpy import arange
from math import sqrt, pow


class FresnelArray:
    def __init__(self):
        self.width = 0.065
        self.n_zones = 160
        self.obstruction = 0.
        self.offset = 0.75
        self.rings = []
        self.wavelength = 260.e-9

    def apply_transmission(self, wavefront):

        self.__construction()
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

        # Search pixel after pixel on only one quadrant if the zone is
        # perforated or not
        # To improve performances, for each line, when a ring is detected,
        # the program search the next
        for i in arange(size / 2):
            for j in arange(size / 2):
                x = i * pixel_width - x_center
                y = j * pixel_width - y_center
                if self.__is_perforated(x, y):
                    wavefront[i][j] = 1
                    # Due to the double symmetry
                    wavefront[i][size - 1 - j] = 1
                    wavefront[size - 1 - i][j] = 1
                    wavefront[size - 1 - i][size - 1 - j] = 1

    def __is_perforated(self, x, y):
        r = sqrt(pow(x, 2) + pow(y, 2))
        is_perforated = False
        n_rings = len(self.rings)
        i = 0
        while i < n_rings and not is_perforated:
            if self.rings[i][0] <= r <= self.rings[i][1]:
                is_perforated = True
            i += 1
        return is_perforated

    def __construction(self):

        # Construction of rings in a list
        del self.rings[:]

        k = 0
        beta_0 = 0.25
        f_lambda = pow(self.width / 2, 2) / (2 * self.n_zones + self.offset -
                                             0.75)

        while k <= self.n_zones * 2:
            k_adj = k + self.offset - beta_0
            r_int = sqrt(2 * f_lambda * k_adj + pow(k_adj * self.wavelength, 2))
            k_adj = k + self.offset + beta_0
            r_ext = sqrt(2 * f_lambda * k_adj + pow(k_adj * self.wavelength, 2))
            self.rings.append([r_int, r_ext])
            k += 1

        # Adding obstruction
        is_obstructed = False
        while not is_obstructed:
            if self.obstruction <= self.rings[0][0]:
                is_obstructed = True
            elif self.rings[0][0] < self.obstruction < self.rings[0][1]:
                self.rings[0][0] = self.obstruction
                is_obstructed = True
            else:
                del self.rings[0]