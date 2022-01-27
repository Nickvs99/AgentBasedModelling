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
        print(f"\r Calculating {attribute} for similar_wanted = {similar_wanted:.3f}", end="")

        avg, std = collect_avg_and_std(
            attribute,
            width=20, height=20,
            init_positive=190,
            init_negative=190,
            init_neutral=0,
            similar_wanted=similar_wanted,
            n_iterations=n_iterations
        )

        avgs.append(avg)
        stds.append(std)

    print()

    line_plot(similar_wanted_values, np.array(avgs), np.array(stds),
              xlabel="similar_wanted", ylabel=attribute)

    plt.show()

def run_experiment_neutrals(attribute, ylabel="", n_iterations=10):

    width = height = 20
    area = width * height
    empty_spaces = int(0.05 * area)

    init_neutral_values = np.linspace(0, area / 2, num=10, dtype=int)
    similar_wanted_values = np.linspace(0.375, 0.875, num=9, dtype=float)

    for similar_wanted in similar_wanted_values:
        avgs = []
        stds = []

        for init_neutral in init_neutral_values:
            print(f"\r Calculating {attribute} for similar_wanted = {similar_wanted:.3f} and init_neutral = {init_neutral}", end="")

            init_positive = init_negative = int((area - empty_spaces - init_neutral) / 2)
            
            avg, std = collect_avg_and_std(
                attribute,
                width=width, height=height,
                init_positive=init_positive,
                init_negative=init_negative,
                init_neutral=init_neutral,
                similar_wanted=similar_wanted,
                n_iterations=n_iterations
            )

            avgs.append(avg)
            stds.append(std)

        print()

        line_plot(init_neutral_values, np.array(avgs), np.array(stds),
                xlabel="init_neutral", ylabel=attribute, label=f"similar_wanted = {similar_wanted}")
    
    plt.legend()
    plt.show()


def collect_avg_and_std(attribute, width=20, height=20, init_positive=190, init_negative=190, init_neutral=0, similar_wanted=0.75, n_iterations=10):
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
            similar_wanted=similar_wanted
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
         
    # run_experiment_similar_wanted("happy", ylabel="Happiness level", n_iterations=5)
    # run_experiment_similar_wanted("entropy", ylabel="Entropy", n_iterations=25)

    run_experiment_neutrals("happy", ylabel="Happiness level", n_iterations=5)
    run_experiment_neutrals("entropy", ylabel="Entropy", n_iterations=25)