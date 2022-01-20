import matplotlib.pyplot as plt
import numpy as np

from gridmodel import GridModel

def run_experiment(attribute, ylabel="", n_iterations=10):
    """
    Plot a attribute of the model for different 'similar_wanted' values.
    The attribute has to be a key of the data collector.
    """

    similar_wanted_values = [i/8 for i in range(9)]
    avgs = []
    stds = []

    for similar_wanted in similar_wanted_values:
        print(f"\r Calculating {attribute} for similar_wanted = {similar_wanted:.3f}", end="")

        values = []
        for i in range(n_iterations):

            model = GridModel(
                width=20, height=20,
                init_positive=190,
                init_negative=190,
                init_neutral=0,
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

        avgs.append(np.mean(values))
        stds.append(np.std(values))

    print()

    avgs = np.array(avgs)
    stds = np.array(stds)

    plt.plot(similar_wanted_values, avgs)
    plt.fill_between(similar_wanted_values, avgs - stds, avgs + stds, alpha=.1)
    
    plt.xlabel("Similar wanted")
    plt.ylabel(ylabel)
 
    plt.show()


if __name__ == "__main__": 
    
    # TODO do both entropy and happiness experiment simultaneous
         
    run_experiment("happy", ylabel="Happiness level")
    run_experiment("entropy", ylabel="Entropy", n_iterations=25)