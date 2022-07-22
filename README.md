# MT-EEG-dataset

[![GitHub repo size](https://img.shields.io/github/repo-size/andlab-um/MT-EEG-dataset?color=brightgreen&logo=github)](https://github.com/andlab-um/MT-EEG-dataset)
[![Paper](https://img.shields.io/badge/Paper-10.1038%2Fs41597--022--01538--5-blue)](https://doi.org/10.1038/s41597-022-01538-5)
[![OpenNeuro](https://img.shields.io/badge/OpenNeuro-ds003766-blue)](https://openneuro.org/datasets/ds003766)
[![Twitter URL](https://img.shields.io/twitter/url?label=%40ANDlab3&style=social&url=https%3A%2F%2Ftwitter.com%2FANDlab3)
](https://twitter.com/ANDlab3)

Code for [[OpenNeuro] Mouse-Tracking EGI dataset](https://openneuro.org/datasets/ds003766) preprocessing and preliminary analysis, accompanying with the following paper:

Chen, K., Wang, R., Huang, J., Gao, F., Yuan, Z., Qi, Y., & Wu, H. (2022). **A resource for assessing dynamic binary choices in the adult brain using EEG and mouse-tracking**. *Scientific Data*, 9(1), 416. https://doi.org/10.1038/s41597-022-01538-5

## Description

We provide a dataset combining high-density Electroencephalography (**HD-EEG**, 128 channels) and **mouse-tracking** intended as a resource for investigating *dynamic decision processing* of **semantic** and **food preference** choices in the brain.

Here, you can find the analysis scripts used in this project with result figures. Please contact Kun CHEN (yc17307@um.edu.mo) if you have any questions about the code or dataset.

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
│   ├── GSN-HydroCel-129.sfp        # standard channel location, get from MNE
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
squeak  # https://github.com/const7/Squeak (fixed some API compatibility issues and adapted some functions)
```

MATLAB

```bash
EEGLAB  # and related plugins
Microstate plugin # for microstate analysis, see here https://www.thomaskoenig.ch/index.php/software/microstates-in-eeglab/getting-started
```

## Usage

Most of the time you only need to change the data path to your own one. Make sure to install all packages before you start.

### BIDS conversion (`0_format`)

This part may not run smoothly since I started from the actual raw, dirty data, and there are several outside data imported. But still, you can refer to most of the scripts to convert your mff data to BIDS compatible format data.

### Behavior analysis (`1_behavior`)

Change the data path to the BIDS path in your computer, and you can run this automatically. The `a_behavior.ipynb` will generate several .csv files for further use in `b_trajectory.ipynb`.

### EEG analysis (`2_eeg`)

Change the data path to the path in your computer again you can run it smoothly. `*_preprocessing.m` will generate preprocessed data for further use, and the rest scripts will do the analysis and visualization.
