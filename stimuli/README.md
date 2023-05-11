# Tasks

**2023-05-11 update**: The default EGI connection package has been updated from [egi](https://pypi.org/project/egi) to [egi-pynetstation](https://pypi.org/project/egi-pynetstation) since Standalone PsychoPy (2022.2.0). See [here](https://psychopy.org/api/hardware/egi.html). **Current PsychoPy programs were based on the old version of egi package.**

## Structure

```bash
├── food
│   ├── foodChoice              # food choice task
│   │   ├── foodChoice.psyexp   # psychopy experimental program
│   │   └── ...
│   ├── foodEnd                 # behavior task, rating about how much do you want to eat this food after the experiment
│   ├── foodHealthy             # behavior task, rating about how healthy do you think this food is
│   ├── foodTaste               # behavior task, rating about how do you like this food
│   └── README.md
├── imageChoice                 # image choice task
├── wordChoice                  # word choice task
└── README.md
```
