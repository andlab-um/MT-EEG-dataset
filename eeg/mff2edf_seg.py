# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 09:47:08 2020

@author: nd269
"""
# -*- coding: utf-8 -*-
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

from genericpath import exists
from os.path import join
import pyedflib # pip install pyedflib
from pyedflib import highlevel # new high-level interface
from pyedflib import FILETYPE_BDF, FILETYPE_BDFPLUS, FILETYPE_EDF, FILETYPE_EDFPLUS
from datetime import datetime, timezone, timedelta
import mne
import os

def _stamp_to_dt(utc_stamp):
    """Convert timestamp to datetime object in Windows-friendly way."""
    if "datetime" in str(type(utc_stamp)): return utc_stamp
    # The min on windows is 86400
    stamp = [int(s) for s in utc_stamp]
    if len(stamp) == 1:  # In case there is no microseconds information
        stamp.append(0)
    return (datetime.fromtimestamp(0, tz=timezone.utc) +
            timedelta(0, stamp[0], stamp[1]))  # day, sec, μs


def write_mne_edf(mff_path, export_type="edf"):
    """
    Saves the raw content of an MNE.io.Raw and its subclasses to
    a file using the EDF+/BDF filetype
    pyEDFlib is used to save the raw contents of the RawArray to disk
    Parameters
    ----------
    raw : mne.io.Raw
        An object with super class mne.io.Raw that contains the data
        to save
    fname : string
        File name of the new dataset. This has to be a new filename
        unless data have been preloaded. Filenames should end with .edf
    picks : array-like of int | None
        Indices of channels to include. If None all channels are kept.
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
    if not os.path.exists(mff_path):
        raise OSError("File doesn't exists.")
    else:
        raw = mne.io.read_raw_egi(mff_path, preload=True)
    # if not issubclass(type(raw), mne.io.BaseRaw):
    #     raise TypeError("Must be mne.io.Raw type")
    # if not overwrite and os.path.exists(fname):
    #     raise OSError("File already exists. No overwrite.")

    # static settings
    if export_type == "edf":
        file_type = FILETYPE_EDFPLUS
        dmin, dmax = -32768, 32767 
    else:
        file_type = FILETYPE_BDFPLUS
        dmin, dmax = -8388608, 8388607
    
    # print("saving to {}, filetype {}".format(fname, file_type))
    sfreq = raw.info["sfreq"]
    date = _stamp_to_dt(raw.info["meas_date"])

    # no conversion necessary, as pyedflib can handle datetime.
    #date = date.strftime("%d %b %Y %H:%M:%S")
    # first_sample = int(sfreq*tmin)

    # TODO
    assert len(raw.annotations) > 0, "Your data doesn't need to segment, please modify code by yourself."
    # data segment according to annotation
    start_sample = 0
    for i, annotation in enumerate(raw.annotations):
        # convert data
        last_sample = annotation["onset"] if i != len(raw.annotations) else None
        channels = raw.get_data("eeg", start=start_sample, stop=last_sample)
        first_sample = annotation["onset"] + annotation["duration"]
        # convert to microvolts to scale up precision
        # TODO ???????????
        channels *= 1e6
        # set conversion parameters
        n_channels = len(channels)
        # create channel from this
        try:
            # assume your mff file named like "sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_eeg.mff"
            f = pyedflib.EdfWriter("{}_run-{}_eeg.{}".format(mff_path[:-8], ), n_channels=n_channels, file_type=file_type)
            # create channel info
            channel_info = []
            for i in range(n_channels):
                try:
                    ch_dict = {"label": raw.ch_names[i], 
                            "dimension": raw._raw_extras[0]["chan_unit"][i], 
                            "sample_rate": raw._raw_extras[0]["n_samps"][i], 
                            "physical_min": raw._raw_extras[0]["physical_min"][i], 
                            "physical_max": raw._raw_extras[0]["physical_max"][i], 
                            "digital_min":  raw._raw_extras[0]["digital_min"][i], 
                            "digital_max":  raw._raw_extras[0]["digital_max"][i], 
                            "transducer": "", 
                            "prefilter": ""}
                except:
                    ch_dict = {"label": raw.ch_names[i], 
                            "dimension": raw._raw_extras[0]["chan_unit"][i], 
                            "sample_rate": sfreq, 
                            "physical_min": channels.min(), 
                            "physical_max": channels.max(), 
                            "digital_min":  dmin, 
                            "digital_max":  dmax, 
                            "transducer": "", 
                            "prefilter": ""}
                channel_info.append(ch_dict)
            # f.setTechnician("mne-gist-save-edf-skjerns")
            f.setSignalHeaders(channel_info)
            f.setStartdatetime(date + timedelta(seconds=first_sample))
            f.writeSamples(channels)
            # write annotation
            events = mne.find_events(raw) 
            anno = mne.annotations_from_events(events, sfreq)
        except Exception as e:
            raise e
        finally:
            f.close()
    # create channel from this
    try:
        f = pyedflib.EdfWriter(fname,
                               n_channels=n_channels, 
                               file_type=file_type)
        
        channel_info = []
        
        ch_idx = range(n_channels) if picks is None else picks
        # keys = list(raw._orig_units.keys())
        for i in ch_idx:
            try:
                ch_dict = {"label": raw.ch_names[i], 
                           "dimension": raw._raw_extras[0]["chan_unit"][i], 
                           "sample_rate": raw._raw_extras[0]["n_samps"][i], 
                           "physical_min": raw._raw_extras[0]["physical_min"][i], 
                           "physical_max": raw._raw_extras[0]["physical_max"][i], 
                           "digital_min":  raw._raw_extras[0]["digital_min"][i], 
                           "digital_max":  raw._raw_extras[0]["digital_max"][i], 
                           "transducer": "", 
                           "prefilter": ""}
            except:
                ch_dict = {"label": raw.ch_names[i], 
                           "dimension": raw._raw_extras[0]["chan_unit"][i], 
                           "sample_rate": sfreq, 
                           "physical_min": channels.min(), 
                           "physical_max": channels.max(), 
                           "digital_min":  dmin, 
                           "digital_max":  dmax, 
                           "transducer": "", 
                           "prefilter": ""}
        
            channel_info.append(ch_dict)
        # f.setPatientCode(raw._raw_extras[0]["subject_info"]["id"])
        # f.setPatientName(raw._raw_extras[0]["subject_info"]["name"])
        f.setTechnician("mne-gist-save-edf-skjerns")
        f.setSignalHeaders(channel_info)
        f.setStartdatetime(date)
        f.writeSamples(channels)
        for annotation in raw.annotations:
            onset = annotation["onset"]
            duration = annotation["duration"]
            description = annotation["description"]
            f.writeAnnotation(onset, duration, description)
        
    except Exception as e:
        raise e
    finally:
        f.close()    
    return True