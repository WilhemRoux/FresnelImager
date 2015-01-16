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

    def create_binary_transmission(self, wavefront):

        self.__construction()
        size = len(wavefront)
        if size % 2:
            print("Error : Wavefront size (%i) must be an even number !"
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

        # Corner pixel
        r = sqrt(pow(x_center, 2) + pow(x_center, 2))

        current_ring = len(self.rings) - 1
        is_localized = False
        on_blank = False
        while not is_localized:
            if r >= self.rings[current_ring][1]:
                is_localized = True
                on_blank = False
            elif r >= self.rings[current_ring][1]:
                is_localized = True
                on_blank = True
            else:
                current_ring -= 1
        del is_localized
        precedent_on_blank = on_blank
        precedent_current_ring = current_ring
        full_four_quadrant(wavefront, 0, 0, on_blank)

        print "Line 0"
        print ("\tPixel 0 : On blank = %r" % on_blank)

        # First line
        for j in arange(1, size / 2 + 1):

                y = j * pixel_width - y_center
                r = sqrt(pow(x_center, 2) + pow(y, 2))

                if on_blank:
                    if r >= self.rings[current_ring][0]:
                        full_four_quadrant(wavefront, 0, j, True)
                    else:
                        on_blank = False
                        current_ring -= 1
                        full_four_quadrant(wavefront, 0, j, False)
                else:
                    if r >= self.rings[current_ring][1]:
                        full_four_quadrant(wavefront, 0, j, False)
                    else:
                        on_blank = True
                        full_four_quadrant(wavefront, 0, j, True)

                print ("\tPixel %d : On blank = %r" % (j, on_blank))

        # Next lines
        for i in arange(1, size / 2 + 1):

            # First line pixel
            x = i * pixel_width - x_center
            r = sqrt(pow(x, 2) + pow(y_center, 2))
            if precedent_on_blank:
                if r >= self.rings[precedent_current_ring][0]:
                    full_four_quadrant(wavefront, i, 0, True)
                else:
                    precedent_on_blank = False
                    precedent_current_ring -= 1
                    full_four_quadrant(wavefront, i, 0, False)
            else:
                if r >= self.rings[precedent_current_ring][1]:
                    full_four_quadrant(wavefront, i, 0, False)
                else:
                    precedent_on_blank = True
                    full_four_quadrant(wavefront, i, 0, True)
            on_blank = precedent_on_blank
            current_ring = precedent_current_ring

            print ("Line %d : On blank = %r" % (i, on_blank))

            for j in arange(1, size / 2 + 1):

                y = j * pixel_width - y_center
                r = sqrt(pow(x, 2) + pow(y, 2))

                if on_blank:
                    if r >= self.rings[current_ring][0]:
                        full_four_quadrant(wavefront, i, j, True)
                    else:
                        on_blank = False
                        current_ring -= 1
                        full_four_quadrant(wavefront, i, j, False)
                else:
                    if r >= self.rings[current_ring][1]:
                        full_four_quadrant(wavefront, i, j, False)
                    else:
                        on_blank = True
                        full_four_quadrant(wavefront, i, j, True)

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

    def __found_ring(self, start, r):
        is_found = False
        while not is_found and start >= 0:
            if r >= self.rings[start][0]:
                is_found = True
            else:
                start -= 1
        return start


def full_four_quadrant(wavefront, i, j, value):
    size = len(wavefront)
    wavefront[i][j] = value
    wavefront[i][size - 1 - j] = value
    wavefront[size - 1 - i][j] = value
    wavefront[size - 1 - i][size - 1 - j] = value