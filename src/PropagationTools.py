#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from numpy import pi, cos, sin


def add_inclination(parameters, wavefront):
    """
    add_inclination(parameters, wavefront)

    This function adds a phase difference to the electric field, in a
    perpendicular plan to the optical axis, due to the shift of the point source
    from the optical axis in function of two parameters : the angle between
    optical axis and the source (from 0° to 90°) and the angle between the
    horizontal semi-axis and the source (from -180° to +180°).

    Parameters
    ----------
    :param parameters: Configuration parameters
    :type parameters: ConfigurationParameters
    :param wavefront: Wavefront
    :type wavefront: ndarray
    """
    if parameters.source_optical_axis_angle > 0:
        width = parameters.fresnel_array.width
        n = parameters.wavefront_sampling
        deviation = parameters.source_optical_axis_angle / 180. * pi
        azimuth = parameters.source_direction_angle / 180. * pi
        # Compute the unit vector pointing to the source
        source_x = cos(azimuth) * sin(deviation)
        source_y = sin(azimuth) * sin(deviation)
        # Compute the phase to add to each pixel
        for x, line in enumerate(wavefront):
            pixel_x = - (n - 1) / 2. + x
            for y, element in enumerate(line):
                pixel_y = - (n - 1) / 2. + y
                r_cos_alpha = source_x * pixel_x + source_y * pixel_y
                opd = r_cos_alpha * width / n
                wavefront[x][y] += 1j * opd
                # dOpd / conf.dWavelength * 2 * M_PI