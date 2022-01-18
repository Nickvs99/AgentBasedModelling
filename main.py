from gridmodel import GridModel
import matplotlib.pyplot as plt

def main():
    width, height = 20, 25
    init_positive, init_negative, init_neutral = 27, 27, 27

    model = GridModel(width, height, init_positive, init_negative, init_neutral)
    #model.visualise()

    # potentially use this from datacollector
    # model.run_model()
    # data = model.datacollector.get_model_vars_dataframe()
    #data = model.datacollector.get_agent_vars_dataframe()
    # data.plot()


if __name__ == "__main__":
    main()
    