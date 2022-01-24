from gridmodel import *

from mesa.batchrunner import BatchRunner
from mesa import Model
from SALib.sample import saltelli
from SALib.analyze import sobol

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import combinations

#One factor at a time local sensitivity analysis

#Define parameters and bounds
problem = {
    'num_vars': 4,
    'names': ['init_positive', 'init_negative', 'init_neutral', 'similar_wanted'],
    'bounds': [[18, 30], [18, 30], [18, 30], [0.1, 0.8]]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 30
max_steps = 100
distinct_samples = 30

# Set the outputs
model_reporters = {"Happy agents": lambda m: int(m.happiness)}

data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)

    

    samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype = int)

    if var == 'similar_wanted':
    	samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype = float)
    
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

    f, axs = plt.subplots(4, figsize=(7, 10))
    
    for i, var in enumerate(problem['names']):
        plot_param_var_conf(axs[i], data[var], var, param, i)

param = "Happy agents"
plot_all_vars(data, param)
plt.show()

             