#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module does  
"""

from metadata_generator import create_metadata_file
from loader import load_and_segment_rawdata
from pd2xarray import pd2xarray

import glob
import os 

def csv2xarray(rawdata_file_path, generate_metadata=False, is_calibration=False):

    if generate_metadata:
        create_metadata_file(rawdata_file_path, t_exp=None, dt=None, exp_duration=None, m_fish=None, speeds=None)
    
    raw_data, metadata = load_and_segment_rawdata(rawdata_file_path, verbose=False)

    ds = pd2xarray(raw_data, metadata, is_calibration)


if __name__ == '__main__':

    rawdata_file_paths = glob.glob("./raw_data/2022*/*.csv")

    for rawdata_file_path in rawdata_file_paths: 
        print('>>>>>>>>>>>>>>>>', rawdata_file_path)
        csv2xarray(rawdata_file_path)
