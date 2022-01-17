from pyexpat import model
import random

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from agents import Positive, Negative, Neutral


class GridModel(Model):
    # these parameters need to be changed here as well in server.py each time?
    def __init__(self, width = 10, height = 10, init_positive = 27, init_negative = 27, init_neutral = 27, 
    similar_wanted = 0.7):
        
        if init_positive + init_negative + init_neutral > width * height:
            raise Exception("Error. You are trying to add more agents than there are grid cells.")

        self.height = width
        self.width = height
        self.neutral = init_neutral
        self.similar_wanted = similar_wanted
        # shows happiness 0 before model starts
        self.happiness = 0
        
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(self.width, self.height, torus=True)
        
        self.n_agents = 0
        #self.agents = []

        self.running = True

        self.populate_grid(init_positive, init_negative, init_neutral)
        
        
    def new_agent(self, agent_type, pos):
        """ Add a new agent of type 'agent_type' to the grid at the position 'pos'. """

        self.n_agents += 1
        
        new_agent = agent_type(self.n_agents, self, pos)
        
        self.grid.place_agent(new_agent, pos)
        #self.agents.append(new_agent)
        self.schedule.add(new_agent)

        return new_agent
        
    # def remove_agent(self, agent):
    #     """ Removes the agent from the grid. """
        
    #     self.n_agents -= 1
        
    #     self.grid.remove_agent(agent)        
    #     self.agents.remove(agent)

    # def move_agent(self, agent, new_pos):
    #     """ Moves the agent to a new position. """

    #     self.model.grid.move_agent(agent, new_pos)

    def get_random_empty_pos(self):
        """ Return a random unoccupied position. """

        if len(self.grid.empties) == 0:
            raise Exception("Error. No empty spaces are available.")

        return random.choice(sorted(self.grid.empties))

    def populate_grid(self, init_positive, init_negative, init_neutral):
        """ Populates the grid with Positive and Negative agents. """

        for i in range(init_positive):
            self.new_agent(Positive, self.get_random_empty_pos())

        for i in range(init_negative):
            self.new_agent(Negative, self.get_random_empty_pos())
        
        for i in range(init_neutral):
            self.new_agent(Neutral, self.get_random_empty_pos())

    def step(self):
        '''
        Method that calls the step method for each of the agents.
        '''
        #Happiness counter always includes neutral agents
        self.happiness = self.neutral
        # neutral agents don't move (always happy) so skip step if neutral
        for agent in self.schedule.agents:
            if type(agent) == Neutral:
                continue
            agent.step(self.similar_wanted)
        if self.happiness == self.schedule.get_agent_count():
            self.running = False

        # Save the statistics (need to import as well)
        # self.datacollector.collect(self)

    # def visualise(self):
    #     """ Visualises the current grid. """

    #     fig, ax = plt.subplots()

    #     # Plot grid
    #     for i in range(self.width + 1):
    #         ax.axvline(i, color="black")

    #     for i in range(self.height + 1):
    #         ax.axhline(i, color="black")

    #     # Plot agents
    #     for agent in self.agents:

    #         if isinstance(agent, Positive):
    #             color = "red"
    #         elif isinstance(agent, Negative):
    #             color = "green"
    #         elif isinstance(agent, Neutral):
    #             color = "black"
    #         else:
    #             raise Exception(f"Invalid agent type encountered: {type(agent)}")

    #         ax.add_patch(Rectangle(agent.pos, 1, 1, color=color))

    #     plt.xlim(0, self.width)
    #     plt.ylim(0, self.height)
    #     plt.show()


