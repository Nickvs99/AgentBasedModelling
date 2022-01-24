from mesa.batchrunner import BatchRunner
from mesa import Model
import matplotlib.pyplot as plt
from gridmodel import GridModel as model
from SALib.sample import saltelli
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations



#Define parameters and bounds
problem = {
    'num_vars': 4,
    'names': ['init_positive', 'init_negative', 'init_neutral', 'similar_wanted'],
    'bounds': [[0, 33], [0, 33], [0, 33], [0.1, 0.8]]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 8
max_steps = 100
distinct_samples = 8

model_reporters = {"Happy agents": lambda m: int(m.happiness)}

#Get samples
param_values = saltelli.sample(problem, distinct_samples)

batch = BatchRunner(model, 
                    max_steps=max_steps,
                    variable_parameters={name:[] for name in problem['names']},
                    model_reporters=model_reporters)

count = 0
data = pd.DataFrame(index=range(replicates*len(param_values)), 
                                columns=['init_positive', 'init_negative', 'init_neutral', 'similar_wanted'])
data['Run'], data['Happy agents'] = None, None

for i in range(replicates):
    for vals in param_values: 
        # Change parameters that should be integers
        vals = list(vals)
        for i in range(0, 3):
        	vals[i] = int(vals[i])

        variable_parameters = {}
        for name, val in zip(problem['names'], vals):
            variable_parameters[name] = val

        batch.run_iteration(variable_parameters, tuple(vals), count)
        iteration_data = batch.get_model_vars_dataframe().iloc[count]
        iteration_data['Run'] = count # Don't know what causes this, but iteration number is not correctly filled
        data.iloc[count, 0:4] = vals
        data.iloc[count, 4:6] = iteration_data
        count += 1
        
        for i in range(10, 101, 10):
            if count / (len(param_values) * (replicates)) * 100 == i:
                print(f'{i}% done!')

        
        

print(data)

Si = sobol.analyze(problem, data['Happy agents'].values, print_to_console=True)

def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')


order_labels = ['1', '2', 'T']
title_labels = ['First order sensitivity', 'Second order sensitivity', 'Total order sensitivity']    

for i in range(len(order_labels)):
    plot_index(Si, problem['names'], order_labels[i], title_labels[i])
    plt.show()

    




