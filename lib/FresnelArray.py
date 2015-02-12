#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from numpy import arange, zeros, newaxis, sqrt


class FresnelArray:

    def __init__(self, width=0.065, n_zones=160, obstruction=0, offset=0.75,
                 wavelength=260.e-9):

        self.width = width
        self.n_zones = n_zones
        self.obstruction = obstruction
        self.offset = offset
        self.wavelength = wavelength
        self.focal_length = (self.width / 2) ** 2 / \
                            (2 * self.n_zones + self.offset - 0.75) / \
                            self.wavelength
        self.white_rings = []

    def create_binary_transmission(self, size):

        # Lists the rings
        self.white_rings = []
        k_ring = 0
        beta_0 = 0.25
        while k_ring <= self.n_zones * 2:
            k_adj = k_ring + self.offset - beta_0
            r_int = sqrt(2 * self.focal_length * self.wavelength * k_adj +
                         (k_adj * self.wavelength) ** 2)
            k_adj = k_ring + self.offset + beta_0
            r_ext = sqrt(2 * self.focal_length * self.wavelength * k_adj +
                         (k_adj * self.wavelength) ** 2)
            self.white_rings.append([r_int, r_ext])
            k_ring += 1

        # Create the array
        pixel_width = self.width / size
        x = arange(size) * pixel_width - (self.width - pixel_width) / 2
        y = x[:, newaxis]
        distance = sqrt(x ** 2 + y ** 2)
        del x, y

        mask = zeros((size, size), dtype='bool')

        for white_ring in self.white_rings:
            mask[white_ring[0] < distance] = 1
            mask[white_ring[1] < distance] = 0

        del distance
        return mask.astype('bool')

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