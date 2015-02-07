#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from sys import exit
from numpy import arange, zeros
from math import sqrt, pow


class FresnelArray:
    def __init__(self):

        self.width = 0.065
        self.n_zones = 160
        self.obstruction = 0.
        self.offset = 0.75
        self.rings = []
        self.wavelength = 260.e-9
        self.focal_length = pow(self.width / 2, 2)\
                            / (2 * self.n_zones + self.offset - 0.75)

    def create_binary_transmission(self, size):

        self.__construction()
        fresnel_array = zeros((size, size), dtype='bool')
        if size % 2:
            print("Error : Wavefront size (%d) must be an even number !" % size)
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

        precedent_current_ring = len(self.rings) - 1
        precedent_on_blank = False
        current_ring = len(self.rings) - 1
        on_blank = False

        for i in arange(0, size / 2 + 1):

            x = i * pixel_width - x_center

            for j in arange(0, size / 2 + 1):

                y = j * pixel_width - y_center
                r = sqrt(pow(x, 2) + pow(y, 2))

                if j == 0:
                    on_blank = precedent_on_blank
                    current_ring = precedent_current_ring

                # Central black zone
                if current_ring == -1:
                    on_blank = False

                else:

                    # Changing zone
                    if on_blank and r < self.rings[current_ring][0]:
                        on_blank, current_ring = \
                            self.__next_ring(current_ring, r)

                    else:
                        # Changing zone
                        if r < self.rings[current_ring][0]:
                            on_blank, current_ring = \
                                self.__next_ring(current_ring, r)
                        # Change color but same zone
                        elif r < self.rings[current_ring][1]:
                            on_blank = True

                full_four_quadrant(fresnel_array, i, j, on_blank)

                if j == 0:
                    precedent_on_blank = on_blank
                    precedent_current_ring = current_ring
        return fresnel_array

    def __construction(self):

        # Construction of rings in a list
        del self.rings[:]

        k = 0
        beta_0 = 0.25
        self.focal_length = pow(self.width / 2, 2) / (2 * self.n_zones +
                                                      self.offset - 0.75)

        while k <= self.n_zones * 2:
            k_adj = k + self.offset - beta_0
            r_int = sqrt(
                2 * self.focal_length * k_adj + pow(k_adj * self.wavelength, 2))
            k_adj = k + self.offset + beta_0
            r_ext = sqrt(
                2 * self.focal_length * k_adj + pow(k_adj * self.wavelength, 2))
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

    def __next_ring(self, current_ring, r):
        current_ring -= 1
        while r < self.rings[current_ring][0] and current_ring >= 0:
            current_ring -= 1
        if r >= self.rings[current_ring][1]:
            on_blank = False
        else:
            on_blank = True
        return on_blank, current_ring

    def get_params_list(self):
        params = [('WIDTH', self.width, 'Width of the grid'),
                  ('NZONES', self.n_zones, 'Number of Fresnel areas'),
                  ('OBSTR', self.obstruction, 'Central obstruction'),
                  ('OFFSET', self.offset, 'Central offset '),
                  ('LAMBDA', self.wavelength, 'Wavelength')]
        return params


def full_four_quadrant(wavefront, i, j, value):
    size = len(wavefront)
    wavefront[i][j] = value
    wavefront[i][size - 1 - j] = value
    wavefront[size - 1 - i][j] = value
    wavefront[size - 1 - i][size - 1 - j] = value