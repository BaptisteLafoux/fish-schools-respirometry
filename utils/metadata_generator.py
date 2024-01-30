#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module saves metadata in a json file. Metadata needed are :
fish wet masses, start time of each speed experiment, speeds tested in BL/S, etc... 
"""

import json 
import os 
import numpy as np 

def create_metadata_file(file_name, t_exp, dt, exp_duration, speeds, m_fish=0, V=48.6):


    metadata = {
        'file_name': file_name,
        't_exp': t_exp,
        'dt': dt,
        'exp_duration': exp_duration,
        'n_fish': 0,
        'speeds': speeds,
        'tank_volume': V, 
        'n_exp': len(speeds)
    }

    if np.sum(m_fish) != 0:
        metadata['m_fish'] = m_fish
        metadata['n_fish'] = len(m_fish)

    json_dump = json.dumps(metadata)
    metadata_save_to = f'{os.path.splitext(file_name)[0]}_metadata.json'

    print('\n*****************')
    print(f'Saving a metadata file under : {metadata_save_to}')
    f = open(metadata_save_to, 'w')
    f.write(json_dump)
    f.close()    
    print('\tDone\n*****************\n')

