#!/usr/bin/python
# -*-coding:Utf-8 -*
# Copyright 2014 Wilhem Roux

from distutils.core import setup, Extension


# define the extension module
cos_module = Extension('cos_module', sources=['cos_module.c'])
# run the setup
setup(ext_modules=[cos_module])