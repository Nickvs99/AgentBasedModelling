from gridmodel import *

from mesa.batchrunner import BatchRunner
from mesa import Model
from SALib.sample import saltelli
from SALib.analyze import sobol

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import combinations

# one factor at a time local sensitivity analysis

# define parameters and bounds
problem = {
    'num_vars': 8,
    'names': ['density', 'init_neutral', 'similar_wanted', 'radius', 'network_p', 'randomize_part', 'decrease_intolerance', 'size'],
    'bounds': [[0.5, 0.99], [0.1, 0.90], [0.01, 1], [1, 5], [0.01, 0.2], [0.01, 1], [0.9, 0.99], [10, 100]]
}

# set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
max_steps = 1000
distinct_samples = 10
    
# set the outputs
model_reporters = {"Happy agents": lambda m: m.happiness() / m.n_agents,
                    "Entropy": lambda m: m.calc_entropy()}

data = {}

for i, var in enumerate(problem['names']):
    
    # get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
    if var == 'radius': #var == 'size'or 
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype=int)

    else:
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype = float) 
    
    # remove sample values who are present multiple times. No need to test them several times
    samples = np.unique(samples)

    batch = BatchRunner(GridModel, 
                        max_steps=max_steps,
                        iterations=replicates,
                        variable_parameters={var: samples},
                        model_reporters=model_reporters,
                        display_progress=True)
    
    batch.run_all()
    
    data[var] = batch.get_model_vars_dataframe()


"-------------------------------Plot the influence of the parameters-------------------------------------------"

def plot_param_var_conf(ax, df, var, param, i):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        var: variables to be taken from the dataframe
        param: which output variable to plot
    """
    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

    ax.set_xlabel(var)
    ax.set_ylabel(param)

def plot_all_vars(df, param):
    """
    Plots the parameters passed vs each of the output variables.

    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """

    f, axs = plt.subplots(7, figsize=(8, 10))
    
    for i, var in enumerate(problem['names']):
        plot_param_var_conf(axs[i], data[var], var, param, i)

plot_all_vars(data, "Happy agents")
plot_all_vars(data, "Entropy")
plt.show()