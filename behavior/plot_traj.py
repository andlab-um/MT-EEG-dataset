# For self.data analysis
import os
import squeak
import numpy as np
import pandas as pd

# For plotting
import seaborn
import matplotlib.pyplot as plt 
from pylab import rcParams
rcParams['figure.figsize'] = 21, 9

class mouseData:
    def __init__(self, data_path, task):
        self.data = pd.read_csv(os.path.join(data_path, task + ".csv"))
        self.task = task

    def preprocess(self):
        # string to list
        self.data["x"] = self.data.xTrajectory.map(squeak.list_from_string)
        self.data["y"] = self.data.yTrajectory.map(squeak.list_from_string)
        self.data["t"] = self.data.tTrajectory.map(squeak.list_from_string)
        # convert time
        self.data.t = self.data.t.apply(lambda x: np.round((np.array(x) - x[0]) * 1000))
        # Flip the leftward responses
        self.data.x = self.data.x.map(squeak.remap_right)
        # space normalize
        self.data.x = self.data.x.map(squeak.normalize_space)
        self.data.y = self.data.y.map(squeak.normalize_space)

    def time_normalize(self):
        # time normalize
        self.data["nx"], self.data["ny"] = zip(*[squeak.even_time_steps(x, y, t) for x, y, t, in zip(self.data.x, self.data.y, self.data.t)])
        self.data.nx = self.data.nx.apply(lambda x: list(x))
        self.data.ny = self.data.ny.apply(lambda y: list(y))
    
    def time_extend(self):
        max_time = 5000
        self.data['rx'] = [squeak.uniform_time(x, t, max_duration=max_time) for x, t in zip(self.data.x, self.data.t)]
        self.data['ry'] = [squeak.uniform_time(y, t, max_duration=max_time) for y, t in zip(self.data.y, self.data.t)]
    
    def cal_metrics(self):
        # Mouse Stats
        self.data["md"] = self.data.apply(lambda trial: squeak.max_deviation(trial["nx"], trial["ny"]), axis=1)
        self.data["auc"] = self.data.apply(lambda trial: squeak.auc(trial["nx"], trial["ny"]), axis=1)
        self.data["xflips"] = self.data.nx.map(squeak.count_x_flips)
        self.data["init_time"] = self.data.ry.map(lambda y: y.index[np.where(y > .05)][0])

    def print_metrics(self, condition="animacy"):
        print(self.data.groupby(condition)["md", "auc", "xflips", "rt"].mean())

    ## plot figures
    def plot_normalized_traj(self, sample_frac=1):
        for _, row in self.data.sample(frac=sample_frac, random_state=1).iterrows():
            plt.plot(row["x"], row["y"], color="blue", alpha=.5)
        plt.text(0, 0, 'START', horizontalalignment='center')
        plt.text(1, 1, 'END', horizontalalignment='center')
        plt.show()
    
    def plot_normalized_time_x(self, sample_frac=1):
        for _, x in self.data.sample(frac=sample_frac, random_state=1).nx.iteritems():
            plt.plot(x, color='blue', alpha=.3)
        plt.xlabel('Normalized time step')
        plt.ylabel('x axis position')
        plt.show()
    
    def plot_real_time_x(self):
        for i in range(len(self.data)):
            x = self.data.rx.iloc[i]
            plt.plot(x.index, x, color='blue', alpha=.3)
        plt.xlabel('Time (msec)')
        plt.ylabel('x axis position')
        plt.show()

    # Plot average trajectories by condition
    def draw_avg_trajectory(self, condition, condition0, condition1, title="Average trajectories"):
        condition0_indices = self.data[self.data[condition] == condition0].index
        condition1_indices = self.data[self.data[condition] == condition1].index
        nx = np.array(list(self.data.nx)).T
        ny = np.array(list(self.data.ny)).T
        condition0X = nx[:,condition0_indices].mean(axis=1)
        condition0Y = ny[:,condition0_indices].mean(axis=1)
        condition1X = nx[:,condition1_indices].mean(axis=1)
        condition1Y = ny[:,condition1_indices].mean(axis=1)

        plt.plot(condition0X, condition0Y, '-o', color="green", label=condition0)
        plt.plot(condition1X, condition1Y, '-o', color="purple", label=condition1)
        plt.legend(loc="lower right", fontsize=30)
        plt.title(title)
        plt.xlim((-.15, 1.05))
        plt.ylim((-.05, 1.1))
        plt.show()

    def draw_avg_trajectory_and_normal(self, condition, condition0, condition1, sample_frac=1):
        condition0_indices = self.data[self.data[condition] == condition0].index
        condition1_indices = self.data[self.data[condition] == condition1].index
        nx = np.array(list(self.data.nx)).T
        ny = np.array(list(self.data.ny)).T
        condition0X = nx[:,condition0_indices].mean(axis=1)
        condition0Y = ny[:,condition0_indices].mean(axis=1)
        condition1X = nx[:,condition1_indices].mean(axis=1)
        condition1Y = ny[:,condition1_indices].mean(axis=1)

        plt.figure(figsize=((16,6)))
        plt.subplot(121)

        plt.plot(condition0X, condition0Y, linewidth=8, color='black')
        plt.plot(condition0X, condition0Y, linewidth=5, color='green', label=condition0)
        for _, row in self.data[self.data[condition] == condition0].sample(frac=sample_frac, random_state=1).iterrows():
            plt.plot(row["nx"], row["ny"], color="green", alpha=.5)
        plt.xlim((-1.5, 1.5))
        plt.ylim((-.1, 1.2))
        plt.title(condition0)

        plt.subplot(122)
        # Plot line in black slightly larger first, to get an outline
        plt.plot(condition1X, condition1Y, linewidth=8, color='black')
        plt.plot(condition1X, condition1Y, linewidth=5, color='red', label=condition1)
        for _, row in self.data[self.data[condition] == condition1].sample(frac=sample_frac, random_state=1).iterrows():
            plt.plot(row["nx"], row["ny"], color="red", alpha=.5)
        plt.xlim((-1.5, 1.5))
        plt.ylim((-.1, 1.2))
        plt.title(condition1)
        plt.show()
    
    def plot_avg_x(self, condition, condition0, condition1):
        condition0_indices = self.data[self.data[condition] == condition0].index
        condition1_indices = self.data[self.data[condition] == condition1].index
        nx = np.array(list(self.data.nx)).T
        # ny = np.array(list(self.data.ny)).T

        condition0X = nx[:,condition0_indices].mean(axis=1)
        # condition0Y = ny[:,condition0_indices].mean(axis=1)
        condition1X = nx[:,condition1_indices].mean(axis=1)
        # condition1Y = ny[:,condition1_indices].mean(axis=1)

        # Standard Error = st dev / sqrt(N)
        condition0SEM = nx[:,condition0_indices].std(axis=1) / np.sqrt(len(condition0_indices))
        condition1SEM = nx[:,condition1_indices].std(axis=1) / np.sqrt(len(condition1_indices))

        plt.plot(condition0X, color='green', label=condition0)
        plt.errorbar(range(101), condition0X, yerr=condition0SEM,
                    color='green', alpha=.3)
        plt.plot(condition1X, 'red', label=condition1)
        plt.errorbar(range(101), condition1X, yerr=condition1SEM,
                    color='red', alpha=.3)
        plt.legend(loc="upper left")
        plt.ylabel("X axis position")
        plt.xlabel("Normalized time")
        plt.title("Average trajectories")
        plt.show()
