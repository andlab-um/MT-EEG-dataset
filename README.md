# MT-EEG-dataset

Code for Mouse-Tracking EGI dataset preprocessing and preliminary analysis.
## Description

Welcome to the GitHub repository for our paper entitled ***A resource for assessing dynamic binary choices in the adult brain using EEG and mouse tracking***.

We provide a dataset combining high-density Electroencephalography (**HD-EEG**, 128 channels) and **mouse-tracking** intended as a resource for investigating dynamic decision processing of semantic and preference choices in the brain.

Here, you can find the analysis scripts used in this project. In addition, the results from our analysis were uploaded to this repository.

For a detailed question of the content of this repository, please get in touch with um.andlab@gmail.com.

## HISTORY

16.08.2021 - Submission date



### Structure

```bash
├── 0_format
│   ├── convert2bids.ipynb          # BIDS conversion from raw data to BIDS
│   └── mff2set.m                   # convert .mff file to .set file
├── 1_behavior                      # behavior data analysis
│   ├── a_behavior.ipynb            # rt/acc etc. for different tasks/conditions
│   ├── b_trajectory.ipynb          # trajectory plot
│   └── traj_util.py
├── 2_eeg
│   ├── a_rest_preprocessing.m      # resting EEG preprocessing
│   ├── b_rest_microstate.m         # microstate analysis
│   ├── c_task_preprocessing.m      # task EEG preprocessing
│   └── d_task_visualization.ipynb  # ERP/TFR/topomap/MVPA analysis
├── assets
│   ├── animacy.csv                 # animate/inanimate words (with english version)
│   ├── association.csv             # mathing between words and images
│   ├── GSN-HydroCel-129.sfp        # standard channel location
│   └── Helvetica.ttf               # font for plotting
├── LICENSE
└── README.md
```

## Requirements


## REFERENCES

To be provided.