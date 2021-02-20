import os
import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from pylab import rcParams
from mne.preprocessing import ICA

rcParams['figure.figsize'] = [21, 9]
# pd.set_option('display.max_columns', None)
# # pd.set_option('display.max_rows', None)
# pd.set_option('show_dimensions', True)
# bh_path = "./data/1. 2020 0919 KHM/行为数据/KHM 0919 FC_foodChoice_2020_Sep_19_0708.csv"
eeg_path = r"C:\Users\const\OneDrive\Desktop\research\projects\mouse-eeg\data\sub-002\EEG DATA\fil_edf\sub-002-F_fil.edf".replace("\\", r"\\")
raw = mne.io.read_raw_edf(eeg_path, preload=True)
filt_raw = raw.copy().load_data().filter(l_freq=0.5, h_freq=30)
filt_raw.plot(duration=5, start=0, n_channels=129, scalings=0.0001)
# plt.show()


test_eeg_path = r"C:\Users\const\Downloads\2020 1030 Testing\EEG DATA\ori_mff\HJM WM_20201030_114134.mff".replace("\\", r"\\")
test_raw = mne.io.read_raw_egi(test_eeg_path, preload=True)
test_filt_raw = test_raw.copy().load_data().filter(l_freq=0.5, h_freq=30)
test_filt_raw.plot(duration=5, start=0, n_channels=129, scalings=0.0001)
plt.show()
# %%
