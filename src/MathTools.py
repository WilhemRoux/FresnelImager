#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from numpy import cos, sin, pi


def add_phase(x, phi):
    """
    add_phase(x, phi)

    Add a phase to a complex.

    Parameters
    ----------
    :param x: Number
    :type x: complex
    :param phi: Phase
    :type phi: float

    Returns
    -------
    :return: Number with added phase
    :rtype: complex
    """
    cos_phase = cos(phi * 2 * pi)
    sin_phase = sin(phi * 2 * pi)
    return complex(x.real * cos_phase - x.imag * sin_phase,
                   x.imag * cos_phase + x.real * sin_phase)