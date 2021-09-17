# -*- coding: utf-8 -*-
"""
Updated on Sept 17 2021

@author: kunchen
"""

"""
Created on Thu Oct 29 09:47:08 2020

@author: nd269
"""

"""
Created on Wed Dec  5 12:56:31 2018
@author: skjerns
Gist to save a mne.io.Raw object to an EDF file using pyEDFlib
(https://github.com/holgern/pyedflib)
Disclaimer:
    - Saving your data this way will result in slight 
      loss of precision (magnitude +-1e-09).
    - It is assumed that the data is presented in Volt (V), 
      it will be internally converted to microvolt
    - BDF or EDF+ is selected based on the filename extension
    - Annotations are lost in the process.
      Let me know if you need them, should be easy to add.
"""

import pyedflib # pip install pyedflib
from pyedflib import FILETYPE_BDFPLUS, FILETYPE_EDFPLUS
from datetime import datetime, timezone, timedelta
import mne
import os

def _stamp_to_dt(utc_stamp):
    """Convert timestamp to datetime object in Windows-friendly way."""
    if 'datetime' in str(type(utc_stamp)): return utc_stamp
    # The min on windows is 86400
    stamp = [int(s) for s in utc_stamp]
    if len(stamp) == 1:  # In case there is no microseconds information
        stamp.append(0)
    return (datetime.fromtimestamp(0, tz=timezone.utc) +
            timedelta(0, stamp[0], stamp[1]))  # day, sec, μs


def write_mne_edf(mff_path, fname, tmin=0, tmax=None, overwrite=False):
    """
    Saves the raw content of an MNE.io.Raw and its subclasses to
    a file using the EDF+/BDF filetype
    pyEDFlib is used to save the raw contents of the RawArray to disk
    Parameters
    ----------
    mff_path : string
        File path of the egi file. Filenames should end with .edf
    fname : string
        File name of the new data. This has to be a new filename
        unless data have been preloaded. Filenames should end with .edf
    tmin : float | None
        Time in seconds of first sample to save. If None first sample
        is used.
    tmax : float | None
        Time in seconds of last sample to save. If None last sample
        is used.
    overwrite : bool
        If True, the destination file (if it exists) will be overwritten.
        If False (default), an error will be raised if the file exists.
    """
    # exclude=[]: keep "0000" mark
    mne_raw = mne.io.read_raw_egi(mff_path, exclude=[], preload=True)
    # if not issubclass(type(mne_raw), mne.io.BaseRaw):
    #     raise TypeError('Must be mne.io.Raw type')
    if not overwrite and os.path.exists(fname):
        raise OSError('File already exists. No overwrite.')
        
    # static settings
    # has_annotations = True if len(mne_raw.annotations)>0 else False
    if os.path.splitext(fname)[-1] == '.edf':
        file_type = FILETYPE_EDFPLUS
        dmin, dmax = -32768, 32767 
    else:
        file_type = FILETYPE_BDFPLUS
        dmin, dmax = -8388608, 8388607
    
    print('saving to {}, filetype {}'.format(fname, file_type))
    sfreq = mne_raw.info['sfreq']
    date = _stamp_to_dt(mne_raw.info['meas_date'])
    
    if tmin:
        date += timedelta(seconds=tmin)
    # no conversion necessary, as pyedflib can handle datetime.
    #date = date.strftime('%d %b %Y %H:%M:%S')
    first_sample = int(sfreq*tmin)
    last_sample  = int(sfreq*tmax) if tmax is not None else None

    # convert data
    channels = mne_raw.get_data("eeg", start=first_sample, stop=last_sample)
    # convert to microvolts to scale up precision
    channels *= 1e6
    # set conversion parameters
    n_channels = len(channels)

    # # for multiple segments
    # for i, annotation in enumerate(raw.annotations):
    #     pass
    
    # create channel from this   
    try:
        f = pyedflib.EdfWriter(fname, n_channels=n_channels, file_type=file_type)
        # get 
        channel_info = []
        ch_idx = range(n_channels)
        for i in ch_idx:
            try:
                ch_dict = {'label': mne_raw.ch_names[i], 
                           'dimension': mne_raw._raw_extras[0]["chan_unit"][i], 
                           'sample_rate': mne_raw._raw_extras[0]['n_samps'][i], 
                           'physical_min': mne_raw._raw_extras[0]['physical_min'][i], 
                           'physical_max': mne_raw._raw_extras[0]['physical_max'][i], 
                           'digital_min':  mne_raw._raw_extras[0]['digital_min'][i], 
                           'digital_max':  mne_raw._raw_extras[0]['digital_max'][i], 
                           'transducer': '', 
                           'prefilter': ''}
            except:
                ch_dict = {'label': mne_raw.ch_names[i], 
                           'dimension': mne_raw._raw_extras[0]["chan_unit"][i], 
                           'sample_rate': sfreq, 
                           'physical_min': channels.min(), 
                           'physical_max': channels.max(), 
                           'digital_min':  dmin, 
                           'digital_max':  dmax, 
                           'transducer': '', 
                           'prefilter': ''}
        
            channel_info.append(ch_dict)
        f.setTechnician('mne-gist-save-edf-skjerns')
        f.setSignalHeaders(channel_info)
        f.setStartdatetime(date)
        f.writeSamples(channels)
        # write original annotation
        for ann in mne_raw.annotations:
            f.writeAnnotation(ann['onset'], ann['duration'], ann['description'])
        # write event as annotation
        events = mne.find_events(mne_raw)
        id2desc = {v: k for k, v in mne_raw.event_id.items()}
        annotations = mne.annotations_from_events(events, sfreq)
        for ann in annotations:
            f.writeAnnotation(ann['onset'], ann['duration'], id2desc[int(ann['description'])])
        
    except Exception as e:
        raise e
    finally:
        f.close()    
    return True