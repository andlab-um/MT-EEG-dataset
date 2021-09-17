import os
import shutil

# set path
# first copy original files into food_path
root_path = "C:\\Users\\brain\\Desktop\\KunChen"
raw_path = os.path.join(root_path, "EGI_RAW")
food_path = os.path.join(root_path, "EGI_FOOD")
beh_path = "behavior"
rec_path = "rec"
eeg_path = "eeg"
# set task name
foodtask = "foodchoice"

if os.path.exists(food_path):
    shutil.rmtree(food_path)
else:
    os.makedirs(os.path.join(food_path, eeg_path))
    os.mkdir(os.path.join(food_path, beh_path))
task_set = set(["foodEnd", "foodChoice", "foodHealthy", "foodTaste"])
task_dict = {"F": "foodchoice", "FC": "foodchoice"}
total = 0

for sub in os.listdir(raw_path):
    for directory in os.listdir(os.path.join(raw_path, sub)):
        # eeg data
        if "EEG DATA" in directory or "EEG_DATA" in directory:
            # sub-001 to sub-015
            cur_eeg_path = os.path.join(raw_path, sub, directory)
            if sub <= "sub-015":
                cur_eeg_path = os.path.join(cur_eeg_path, "fil_edf")
            for edf in os.listdir(cur_eeg_path):
                if "fil.edf" in edf:
                    for key, value in task_dict.items():
                        if key in edf[:-4].upper().replace('-', ' ').replace('_', ' ').split():
                            print(os.path.join(cur_eeg_path, edf))
                            shutil.copy(os.path.join(cur_eeg_path, edf), os.path.join(food_path, eeg_path, "{}_task-{}_eeg.edf".format(sub, value)))
                            break
        # behavioral data
        elif "Beha" in directory:
            for csv in os.listdir(os.path.join(raw_path, sub, directory)):
                cross = set(csv.split("_")) & task_set
                if len(cross) != 0:
                    total += 1
                    # print(os.path.join(food_path, sub, beh_path, csv))
                    if not os.path.exists(os.path.join(food_path, beh_path, list(cross)[0].lower())):
                        os.mkdir(os.path.join(food_path, beh_path, list(cross)[0].lower()))
                    shutil.copy(os.path.join(raw_path, sub, directory, csv), os.path.join(food_path, beh_path, list(cross)[0].lower(), "{}_task-{}_beh.csv".format(sub, list(cross)[0]).lower()))