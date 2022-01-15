import random

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from mesa import Model
from mesa.space import SingleGrid

from agents import Positive, Negative


class GridModel(Model):

    def __init__(self, width = 10, height = 10, init_positive = 40, init_negative = 40, similar_wanted = 0.7):
        
        if init_positive + init_negative > width * height:
            raise Exception("Error. You are trying to add more agents than there are grid cells.")

        self.height = width
        self.width = height
        self.similar_wanted = similar_wanted
        
        self.grid = SingleGrid(self.width, self.height, torus=True)
        
        self.n_agents = 0
        self.agents = []

        self.running = True

        self.populate_grid(init_positive, init_negative)
        
    def new_agent(self, agent_type, pos):
        """ Add a new agent of type 'agent_type' to the grid at the position 'pos'. """

        self.n_agents += 1
        
        new_agent = agent_type(self.n_agents, self, pos)
        
        self.grid.place_agent(new_agent, pos)
        self.agents.append(new_agent)

        return new_agent
        
    def remove_agent(self, agent):
        """ Removes the agent from the grid. """
        
        self.n_agents -= 1
        
        self.grid.remove_agent(agent)        
        self.agents.remove(agent)

    def move_agent(self, agent, new_pos):
        """ Moves the agent to a new position. """

        self.model.grid.move_agent(agent, new_pos)

    def get_random_empty_pos(self):
        """ Return a random unoccupied position. """

        if len(self.grid.empties) == 0:
            raise Exception("Error. No empty spaces are available.")

        return random.choice(sorted(self.grid.empties))

    def populate_grid(self, init_positive, init_negative):
        """ Populates the grid with Positive and Negative agents. """

        for i in range(init_positive):
            self.new_agent(Positive, self.get_random_empty_pos())

        for i in range(init_negative):
            self.new_agent(Negative, self.get_random_empty_pos())

    def step(self):
        '''
        Method that calls the step method for each of the agents.
        '''
        for agent in self.agents:
            agent.step(self.similar_wanted)

        # Save the statistics
        # self.datacollector.collect(self)

    def visualise(self):
        """ Visualises the current grid. """

        fig, ax = plt.subplots()

        # Plot grid
        for i in range(self.width + 1):
            ax.axvline(i, color="black")

        for i in range(self.height + 1):
            ax.axhline(i, color="black")

        # Plot agents
        for agent in self.agents:

            if isinstance(agent, Positive):
                color = "red"
            elif isinstance(agent, Negative):
                color = "green"
            else:
                raise Exception(f"Invalid agent type encountered: {type(agent)}")

            ax.add_patch(Rectangle(agent.pos, 1, 1, color=color))

        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.show()


