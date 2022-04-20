# MT-EEG-dataset

Code for [Mouse-Tracking EGI dataset](https://openneuro.org/datasets/ds003766) preprocessing and preliminary analysis.

## Description

Welcome to the GitHub repository for our paper entitled ***A resource for assessing dynamic binary choices in the adult brain using EEG and mouse tracking***.

We provide a dataset combining high-density Electroencephalography (**HD-EEG**, 128 channels) and **mouse-tracking** intended as a resource for investigating dynamic decision processing of semantic and preference choices in the brain.

Here, you can find the analysis scripts used in this project. In addition, the results from our analysis were uploaded to this repository.

For a detailed question of the content of this repository, please get in touch with um.andlab@gmail.com.

## History

16.08.2021 - Submission date

16.04.2022 - Revision

## Structure

> See well-rendered `2_eeg/d_task_visualization.ipynb` version [here](https://nbviewer.org/github/andlab-um/MT-EEG-dataset/blob/main/2_eeg/d_task_visualization.ipynb) since GitHub didn't render it correctly.

```bash
├── 0_format
│   ├── convert2bids.ipynb          # BIDS conversion from raw data to BIDS
│   └── mff2set.m                   # convert .mff file to .set file
├── 1_behavior
│   ├── a_behavior.ipynb            # rt/acc etc. for different tasks/conditions
│   ├── b_trajectory.ipynb          # trajectory analysis
│   └── traj_util.py
├── 2_eeg
│   ├── a_rest_preprocessing.m      # resting EEG preprocessing
│   ├── b_rest_microstate.m         # microstate analysis
│   ├── c_task_preprocessing.m      # task EEG preprocessing
│   └── d_task_visualization.ipynb  # ERP/TFR/topomap/MVPA analysis
├── assets
│   ├── animacy.csv                 # animate/inanimate words (with chinese and corresponding english version)
│   ├── association.csv             # mathing between words and images
│   ├── GSN-HydroCel-129.sfp        # standard channel location
│   └── Helvetica.ttf               # font for plotting
├── LICENSE
└── README.md
```

## Requirements

Python

```bash
mne
mne-bids
numpy
scipy
scikit-learn
pandas
seaborn
squeak  # https://github.com/const7/Squeak
```

MATLAB

```bash
EEGLAB  # and related plugins
```

## Usage

Most of the time you only need to change the data path to your own one.

### BIDS conversion (`0_format`)

This part may not run smoothly since I started from the actual raw, dirty data, and there are several outside data imported. But still, you can refer to most of it to convert your mff data to BIDS compatible format data.

### Behavior analysis (`1_behavior`)

Change the data path to the BIDS path in your computer, and you can run this automatically. The `a_behavior.ipynb` will generate several .csv files for further use in `b_trajectory.ipynb`.

### EEG analysis (`2_eeg`)

Change the data path to the path in your computer again you can run it smoothly. `*_preprocessing.m` will generate preprocessed data for further use, and the rest files will do the analysis and visualization.

## References

To be provided.
