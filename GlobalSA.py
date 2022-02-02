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
    'num_vars': 8,
    'names': ['density', 'init_neutral', 'similar_wanted', 'radius', 'network_p', 'randomize_part', 'decrease_intolerance','size'],
    'bounds': [[0.5, 0.99], [0.1, 0.90], [0.01, 1], [1, 5], [0.01, 0.2], [0.01, 1], [0.9, 0.99], [10, 100]]
}
# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 5
max_steps = 100
distinct_samples = 8

model_reporters = {"Happy agents": lambda m: m.happiness() / m.n_agents,
                    "Entropy": lambda m: m.calc_entropy()}

#Get samples
param_values = saltelli.sample(problem, distinct_samples, calc_second_order = False)

batch = BatchRunner(model, 
                    max_steps=max_steps,
                    variable_parameters={name:[] for name in problem['names']},
                    model_reporters=model_reporters)

count = 0
data = pd.DataFrame(index=range(replicates*len(param_values)), 
                                columns=['density', 'init_neutral', 'similar_wanted', 'radius', 'network_p', 'randomize_part', 'decrease_intolerance', 'size'])
data['Run'], data['Happy agents'], data['Entropy'] = None, None, None

for i in range(replicates):
    for vals in param_values: 

        variable_parameters = {}
        for name, val in zip(problem['names'], vals):
            if name == 'size' or name == 'radius':
                val = int(val)
            variable_parameters[name] = val

        #Make integer for the size and radius parameters.
        

        batch.run_iteration(variable_parameters, tuple(vals), count)
        iteration_data = batch.get_model_vars_dataframe().iloc[count]
        iteration_data['Run'] = count # Don't know what causes this, but iteration number is not correctly filled
        data.iloc[count, 0:8] = vals
        data.iloc[count, 8:11] = iteration_data
        count += 1
        
        for i in range(10, 101, 10):
            if count / (len(param_values) * (replicates)) * 100 == i:
                print(f'{i}% done!')
print(data)

data.to_csv('GlobalSA_data.csv')

Si_happy_agents = sobol.analyze(problem, data['Happy agents'].values, calc_second_order=False, print_to_console=True)
Si_entropy = sobol.analyze(problem, data['Entropy'].values, calc_second_order=False, print_to_console=True)
Si_data = (Si_happy_agents, Si_entropy)
#total_Si, first_Si = Si.to_df()


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


order_labels = ['1', 'T']
title_labels = ['First order sensitivity', 'Total order sensitivity']  
Si_labels = ['Happy agents', 'Entropy']  

# Very simple code to save the sensivity analysis plots to the desired working directory
save_results_to = 'C:/Users/ysijp/OneDrive/Bureaublad/Agent-Based Modelling/GroupProject/Figures/'

for i in range(len(order_labels)):
    plot_index(Si_happy_agents, problem['names'], order_labels[i], title_labels[i] + " " "(Happy agents)")
    plt.savefig(save_results_to + title_labels[i] + "_Happy agents" + '.png', bbox_inches="tight",  dpi = 300)
    plt.show()

for i in range(len(order_labels)):
    plot_index(Si_entropy, problem['names'], order_labels[i], title_labels[i] + " " "(Entropy)")
    plt.savefig(save_results_to + title_labels[i] + "_Entropy" + '.png', bbox_inches="tight", dpi = 300)
    plt.show()
