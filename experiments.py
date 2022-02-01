import matplotlib.pyplot as plt
import numpy as np

from gridmodel import GridModel

def run_experiment_similar_wanted(attribute, ylabel="", n_iterations=10):
    """
    Plot a attribute of the model for different 'similar_wanted' values.
    The attribute has to be a key of the data collector.
    """

    similar_wanted_values = [i/8 for i in range(9)]
    avgs = []
    stds = []

    for similar_wanted in similar_wanted_values:
        print(f"\rCalculating {attribute} for similar_wanted = {similar_wanted:.3f}", end="")

        avg, std = collect_avg_and_std(
            attribute,
            width=20, height=20,
            init_positive=0.475,
            init_negative=0.475,
            init_neutral=0,
            similar_wanted=similar_wanted,
            use_network=0,
            n_iterations=n_iterations
        )

        avgs.append(avg)
        stds.append(std)

    print()

    line_plot(similar_wanted_values, np.array(avgs), np.array(stds),
              xlabel="similar_wanted", ylabel=ylabel)

    plt.show()

def run_experiment_network(attribute, ylabel="", n_iterations=10):
    """
    Plot a attribute of the model for different 'enlightenment' values.
    The attribute has to be a key of the data collector.
    """

    values = np.linspace(0.001, 0.18, num=50, dtype=float)
    avgs = []
    stds = []

    for value in values:
        print(f"\rCalculating {attribute} for value = {value:.3f}", end="")

        avg, std = collect_avg_and_std(
            attribute,
            width=20, height=20,
            init_positive=0.4,
            init_negative=0.4,
            init_neutral=value,
            similar_wanted=1,
            n_iterations=n_iterations,
            use_network=1, 
            network_p = 0.04, 
            randomize_part = 0.5,
            decrease_intolerance=0.999
        )

        avgs.append(avg)
        stds.append(std)

    print()

    line_plot(values, np.array(avgs), np.array(stds),
              xlabel="value", ylabel=ylabel)

    plt.show()

def run_experiment_neutrals(attribute, ylabel="", n_iterations=10):

    empty_spaces = 0.05

    init_neutral_values = np.linspace(0, 0.5, num=11, dtype=float)
    similar_wanted_values = np.linspace(0, 1, num=9, dtype=float)

    for similar_wanted in similar_wanted_values:
        avgs = []
        stds = []

        for init_neutral in init_neutral_values:
            print(f"\rCalculating {attribute} for similar_wanted = {similar_wanted:.3f} and init_neutral = {init_neutral:.3f}", end="")

            init_positive = init_negative = (1 - empty_spaces - init_neutral) / 2
            
            avg, std = collect_avg_and_std(
                attribute,
                width=10, height=10,
                init_positive=init_positive,
                init_negative=init_negative,
                init_neutral=init_neutral,
                similar_wanted=similar_wanted,
                use_network=1,
                randomize_part=0.5,
                network_p=0.04,
                n_iterations=n_iterations
            )

            avgs.append(avg)
            stds.append(std)

        print()

        line_plot(init_neutral_values * 100, np.array(avgs), np.array(stds),
                xlabel="init_neutral [%]", ylabel=ylabel, label=f"similar_wanted = {similar_wanted}")
    
    plt.legend()
    plt.show()

def collect_avg_and_std(attribute, width=20, height=20, init_positive=190, init_negative=190, init_neutral=0, similar_wanted=0.75, 
                        use_network = 0, network_p = 0.04, randomize_part = 0.2, decrease_intolerance = 0.99, n_iterations=10):
    """
    Run a model with the given parameters n times. Returns the average and standard
    deviation of the attribute.
    """

    values = []
    
    for i in range(n_iterations):
        
        model = GridModel(
            width=width, height=height,
            init_positive=init_positive,
            init_negative=init_negative,
            init_neutral=init_neutral,
            similar_wanted=similar_wanted, 
            use_network = use_network, 
            network_p = network_p, 
            randomize_part = randomize_part, 
            decrease_intolerance = decrease_intolerance
        )
        model.run(collect=False)

        # It could be that the model is not able to finish, then we run the model for
        # n steps more and take the average over those n steps
        if model.running:
            model.run(collect=True, max_iterations=10)

        # If the model has finished, simply collect the values
        else:
            model.collect()

        temp_values = model.datacollector.model_vars[attribute]
        values.append(np.mean(temp_values))

    return np.mean(values), np.std(values)

def line_plot(x_values, y_avgs, y_stds, xlabel="", ylabel="", title="", label=""):
    
    plt.plot(x_values, y_avgs, label=label)
    plt.fill_between(x_values, y_avgs - y_stds, y_avgs + y_stds, alpha=.1)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.title(title)
 

if __name__ == "__main__": 
    
    # TODO do both entropy and happiness experiment simultaneous
         
    # run_experiment_similar_wanted("happy", ylabel="Happiness level", n_iterations=25)
    # run_experiment_similar_wanted("entropy", ylabel="Entropy", n_iterations=25)

    # run_experiment_neutrals("happy", ylabel="Happiness level", n_iterations=25)
    # run_experiment_neutrals("entropy", ylabel="Entropy", n_iterations=25)

    run_experiment_network("happy", ylabel="Happiness level", n_iterations=25)
    run_experiment_network("entropy", ylabel="Entropy", n_iterations=25)