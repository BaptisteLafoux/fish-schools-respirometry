#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module loads and segment raw data acquired from a YST oxygen meter
"""
import pandas as pd 
import numpy as np
import xarray as xr

from types import SimpleNamespace  

import json
import os 

#%% Raw data loaders 

def load_metadata(file_name: str):
    """Loads a metadata file (containing starting points for experiments) located in the same path as the raw data .csv file. 
    The metadata file (.json) can be created with the metadata_generator file. 
    The metadata filename is the same as the .csv file but with _metadata.json as un suffix 

    Parameters
    ----------
    file_name: str
        relative path to a raw data .csv file from YST oxygen meter.

    Returns
    ----------
    metadata: SimpleNamespace
        dict-like structure with all metadata available (call metadata.attribute)
    """

    with open(f'{os.path.splitext(file_name)[0]}_metadata.json', 'r') as metadata_content:
        metadata = SimpleNamespace(**json.load(metadata_content))

    return metadata

def load_rawdata(file_name: str):
    """Load raw data from a csv file from YST oxygen meter.     

    Parameters
    ----------
    file_name : str
        relative path to a raw data .csv file from YST oxygen meter.

    Returns
    -------
    data: pd.Dataframe
        pandas Dataframe containing the data
    """

    data = pd.read_csv(file_name, sep=';')
    
    return data

def select_data_segment(data, metadata, time_skipped_begin_exp: int):
    """Time segmentation to keep interesting part of the raw data only. 
    Trims a raw dataframe: removes indices frome before the 1st exp. and from after the last experiment. Breaks this DF into successive experiments and merges the different experiments together.
    It keeps only 'metadata.exp_duration' seconds for each experiments, then also removes the first **time_skipped_begin_exp** seconds.
    The length of each segment (in seconds) is specified in metadata.exp_duration.

    Parameters
    ----------
    data : pd.Dataframe
        Raw data Dataframe from load_data function
    metadata : SimpleNamespace 
        Experiment metadata from load_metadata function
    time_skipped_begin_exp : int    
        Time (in seconds) that we remove at the beginning of each segment of experiment to take into account the transient part

    Returns
    -------
    cleaned_data: pd.Dataframe
        updated Dataframe with only interesting time period inside. The indices of the DF are reseted
    updated_metadata: SimpleNamespace
        same metadata as before but we added some info relative to the time-segmentation process
    """

    segmented_data = []

    for t in metadata.t_exp[:-1]:
        i_exp = int(data.index[data['Time (HH:mm:ss)'] == t].tolist()[0])

        index_begin = i_exp + int(time_skipped_begin_exp / metadata.dt)
        index_end = i_exp + int(metadata.exp_duration / metadata.dt)

        segmented_data.append(data[index_begin: index_end])

    cleaned_data = pd.concat(segmented_data)
    cleaned_data = cleaned_data.reset_index(drop=True)

    updated_metadata = metadata 

    updated_metadata.i_exps = np.linspace(0, len(cleaned_data) - (
        metadata.exp_duration-time_skipped_begin_exp) // metadata.dt, metadata.n_exp, dtype=np.uint32)

    updated_metadata.time_skipped_begin_exp = time_skipped_begin_exp
    updated_metadata.pts_per_exp = int((metadata.exp_duration-time_skipped_begin_exp) // metadata.dt)

    return cleaned_data, updated_metadata

def log_info(data, metadata: SimpleNamespace) -> None: 
    """Print in the console the different info related to the loading of the data files

    Parameters
    ----------
    data : pd.Dataframe
        segmented DF from 'select_data_segment' function
    metadata : SimpleNamespace
        updated metadata from 'select_data_segment' function
    """
    print('\n\n\n#############################################################')
    print(f'\n*************************\nProcessing {metadata.file_name}')
    print('*************************\n\nLoading data and selecting time')
    print(f'\nExp : from {metadata.t_exp[0]} - {metadata.t_exp[-1]}')

    print(f'Exp. with {metadata.n_exp} speeds : {metadata.speeds} BL/s')

    print('\n Speed start time :')
    for i_exp in metadata.i_exps:
        print('\t', data['Time (HH:mm:ss)'][i_exp])

    print(f'{len(data)} data points @ {1/metadata.dt} pt/s >>> total duration : {int(len(data)*metadata.dt):d} s')
    print(f'\nEach experiment is initially {metadata.exp_duration} s >>> We kep only the last {metadata.exp_duration-metadata.time_skipped_begin_exp} s')


def load_and_segment_rawdata(file_name, verbose=True): 
    """A wrapper

    Parameters
    ----------
    file_name : str
        relative path to a raw data .csv file from YST oxygen meter.    
    verbose : bool, optional
        If you want to display the data information in the console or not, by default True

    Returns
    -------
    cleaned_data : pd.Dataframe
        Clean and segmented DF
    updated_metadata : SimpleNamespace
        Complete metadata info for the whole experiment
    """

    metadata = load_metadata(file_name)
    raw_data = load_rawdata(file_name)

    # I usually skip the first 5 min of the experiments to avoid seeing transient effects
    cleaned_data, updated_metadata = select_data_segment(raw_data, metadata, time_skipped_begin_exp=5*60)

    if verbose:
        log_info(cleaned_data, updated_metadata)

    return cleaned_data, updated_metadata

#%% cleaned data loaders 

def load_and_merge_multi_ds(paths, dim='number_of_fish'):
    
    concat_ds = xr.open_mfdataset(paths, combine='nested', concat_dim=dim)

    return concat_ds

