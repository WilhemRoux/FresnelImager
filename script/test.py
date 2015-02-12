#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

import numpy as np

# Calcul integral telescope muon

theta_max = 35 / 180. * np.pi

(theta, d_theta) = np.linspace(0, theta_max, 1000, retstep=True)

alpha = 2 * np.arccos(np.tan(theta)/np.tan(theta_max))

f = (alpha - np.sin(alpha)) / np.pi * np.cos(theta) * np.sin(theta)

int = np.sum(f * d_theta) * 2

print int
