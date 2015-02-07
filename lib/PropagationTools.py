#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from numpy import pi, cos, sin
from numpy.fft import fft2, fftshift
from lib.MathTools import add_phase


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
        wavelength = parameters.wavelength
        # Compute the unit vector pointing to the source
        source_x = cos(azimuth) * sin(deviation)
        source_y = sin(azimuth) * sin(deviation)
        # Compute the phase to add to each pixel
        for x, line in enumerate(wavefront):
            pixel_x = - (n - 1) / 2. + x
            for y, pixel in enumerate(line):
                pixel_y = - (n - 1) / 2. + y
                r_cos_alpha = source_x * pixel_x + source_y * pixel_y
                opd = r_cos_alpha * width / n
                wavefront[x][y] = add_phase(pixel, opd / wavelength * 2 * pi)


def add_inclination_bis(parameters, wavefront):
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
        wavelength = parameters.wavelength
        # Compute the unit vector pointing to the source
        source_x = cos(azimuth) * sin(deviation)
        source_y = sin(azimuth) * sin(deviation)
        # Compute the phase to add to each pixel
        for x, line in enumerate(wavefront):
            pixel_x = - (n - 1) / 2. + x
            for y, pixel in enumerate(line):
                pixel_y = - (n - 1) / 2. + y
                r_cos_alpha = source_x * pixel_x + source_y * pixel_y
                opd = r_cos_alpha * width / n
                wavefront[x][y] = add_phase(pixel, opd / wavelength * 2 * pi)


def fresnel_propagation(plane, size, distance, wavelength):
    """
    fresnel_propagation(plane, size, distance, wavelength)

    This function compute the electric field in a perpendicular plane to the
    optical axis after a propagation in vacuum along a certain distance on
    this axis.
    It uses the Fresnel diffraction theory to compute the new values of
    electric field after the propagation.

    1/ Multiply the field to be propagated for a complex exponential:
        exp(i*k/(2z)*(x^2+y^2)) = exp(i*pi/(lambda*z)*(x^2+y^2))
    2/ Calculate its two-dimensional Fourier transform and replace
    coordinates by (x/(lambda*z), y/(lambda*z))
    3/ Multiply it by another factor:
        exp(i*k/(2z)*(x^2+y^2)) = exp(i*pi/(lambda*z)*(x^2+y^2))

    :param plane:
    :param size:
    :param distance:
    :param wavelength:
    :return:
    """
    length = len(plane)
    d_x = size / length
    d_y = size / length
    c = pi / distance / wavelength

    for m, line in enumerate(plane):
        x = (m - (length - 1) / 2.) * d_x
        for n, pixel in enumerate(line):
            y = (n - (length - 1) / 2.) * d_y
            phase = c * (x*x + y*y)
            plane[m][n] = add_phase(plane[m][n], phase)

    out = fft2(plane)
    out2 = fftshift(out)

    print d_x
    d_x = d_x / wavelength / distance
    print d_x
    d_y = d_y / wavelength / distance
    for m, line in enumerate(out2):
        x = (m - (length - 1) / 2.) * d_x
        for n, pixel in enumerate(line):
            y = (n - (length - 1) / 2.) * d_y
            phase = c * (x*x + y*y)
            out2[m][n] = add_phase(out2[m][n], phase)

    return out2