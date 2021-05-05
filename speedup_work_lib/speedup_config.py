#!/usr/bin/env python
"""
.. current_module:: speedup_config.py
.. created_by:: Darren Xie
.. created_on:: 05/05/2021

This is the config file for speedup work library package.
"""
import re

TIME_FORMAT = '%m/%d/%Y %H:%M:%S'
PERCENT_RE = re.compile(r'%(.+?)%')
FILE_TYPE_RE = re.compile(r'.*(\..+)$')
