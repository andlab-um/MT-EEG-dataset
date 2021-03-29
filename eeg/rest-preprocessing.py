# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# from IPython import get_ipython

# %%
import os
import time

import mne
import numpy as np
import pandas as pd
from mne.preprocessing import ICA
# from pylab import rcParams
from autoreject import AutoReject
from autoreject import get_rejection_threshold


# matplotlib.use("Qt5Agg")
# get_ipython().run_line_magic('matplotlib', 'inline')
mne.set_config("MNE_USE_CUDA", "true")


# %%
# set path
data_path = "D:\\EGI_DATA\\EGI_BIDS"
epoch_path = "D:\\EGI_DATA\\EGI_EPOCH"
eeg_path = "eeg"
# set task name
foodtask = "foodchoice"
wordtask = "wordchoice"
imagetask = "imagechoice"
# witask = "wordimagematch"
rest = "rest"
# set current mark type && epoch windows
tmin = 0
tmax = 2
random_state = 97

event_dict = {"seg": 1}

df = pd.DataFrame(columns=["sub", "rest"])

task = rest
for sub in os.listdir(data_path):
    if "sub" not in sub:
        continue
    if not os.path.exists(os.path.join(epoch_path, sub, eeg_path)):
        os.makedirs(os.path.join(epoch_path, sub, eeg_path))
    # record one row
    row = [sub]
    # read data
    raw = mne.io.read_raw_edf(os.path.join(data_path, sub, eeg_path, "{}_task-{}_eeg.edf".format(sub, task)), preload=True)
    # set montage
    montage = mne.channels.make_standard_montage("GSN-HydroCel-129")
    montage.ch_names[-1] = "E129"
    raw.set_montage(montage)

    # filter
    raw_filetered = raw.copy().notch_filter(np.arange(50, 250, 50), n_jobs="cuda")
    raw_filetered.filter(l_freq=1, h_freq=30, n_jobs="cuda")
    # resample
    raw_downsampled = raw_filetered.copy().resample(sfreq=256, n_jobs="cuda")

    # rebuild events
    events = mne.events_from_annotations(raw_downsampled)

    max_id = max(events[0][:,2])
    rsrs = [events[1].get("rsrs", -1)]
    rsfi = [events[1].get("rsfi", -1)]

    rest_events = []
    events_n = len(events[0])
    for i in range(events_n - 1):
        # current mark: stimulus mark
        if events[0][i][2] == rsfi and events[0][i+1][2] == rsrs:
            rest_events.append([events[0][i][0], events[0][i][1], event_dict["seg"]])
            rest_events.append([events[0][i][0] + 2, events[0][i][1], event_dict["seg"]])
            rest_events.append([events[0][i][0] + 4, events[0][i][1], event_dict["seg"]])
    rest_events = np.array(rest_events)

    # detect EOG event
    # raw_downsampled = mne.set_bipolar_reference(raw_downsampled, ["E8"], ["E126"], ["EVR"])
    # raw_downsampled = mne.set_bipolar_reference(raw_downsampled, ["E25"], ["E127"], ["EVL"])
    # raw_downsampled.set_channel_types({"EVR": "eog", "EVL": "eog"})
    eog_chan = ["E1", "E8", "E14", "E17", "E21", "E25", "E32", "E38", "E121", "E126", "E127"]
    eog_type = ["eog"] * len(eog_chan)
    raw_downsampled.set_channel_types(dict(zip(eog_chan, eog_type)))
    eog_events = mne.preprocessing.find_eog_events(raw_downsampled)
    # eog_events = mne.preprocessing.find_eog_events(raw_downsampled, thresh=0.0001)

    # write eog events to annotatioin
    onsets = eog_events[:, 0] / raw_downsampled.info["sfreq"] - 0.25
    durations = [0.5] * len(eog_events)
    descriptions = ["bad blink"] * len(eog_events)
    blink_annot = mne.Annotations(onsets, durations, descriptions, orig_time=raw_downsampled.info["meas_date"])
    raw_downsampled.set_annotations(blink_annot)

    # drop bad channels
    # TODO: necessary??
    bad_channel = ["E125", "E128", "E43", "E48", "E49", "E56", "E63", "E68", "E73", "E81", "E88", "E94", "E99", "E107", "E113", "E120", "E119"]
    raw_mark_bad = raw_downsampled.copy()
    # raw_mark_bad.info["bads"] = bad_channel
    raw_mark_bad.drop_channels(bad_channel)

    # re-reference
    raw_ref = raw_mark_bad.copy().set_eeg_reference("average", ch_type="eeg")

    # epoch
    epochs = mne.Epochs(raw_ref, events=rest_events, event_id=event_dict, tmin=tmin, tmax=tmax, preload=True)

    # ## ICA
    reject = get_rejection_threshold(epochs)
    ica = ICA(n_components=20, random_state=random_state)
    ica.fit(epochs, reject=reject)
    eog_inds, scores = ica.find_bads_eog(epochs)
    ica.exclude += eog_inds
    ica.apply(epochs)

    # autoreject
    ar = AutoReject(random_state=random_state, n_jobs=16, verbose="tqdm")
    epochs_clean = ar.fit_transform(epochs)

    # save epochs
    epochs_clean.save(os.path.join(epoch_path, sub, eeg_path, "{}_task-{}_epo.fif".format(sub, task)), overwrite=True)

    row.append("{:.2f}%".format((320-len(epochs_clean))/320*100))

    df = df.append(dict(zip(list(df.columns), row)), ignore_index=True)

time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
df.to_csv("log_{}.csv".format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), index=False)