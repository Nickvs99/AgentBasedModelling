from pyexpat import model
import random
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from spatialentropy import leibovici_entropy, altieri_entropy
import networkx as nx

from agents import Positive, Negative, Neutral


class GridModel(Model):
    def __init__(self, width = 10, height = 10, init_positive = 33, init_negative = 33, init_neutral = 33, 
    similar_wanted = 0.75, use_network = 0, network_p = 0.02, randomize_part = 0.0, decrease_intolerance = 0.99):
        
        if init_positive + init_negative + init_neutral > width * height:
            raise Exception("Error. You are trying to add more agents than there are grid cells.")

        self.height = width
        self.width = height
        self.neutral = init_neutral
        self.similar_wanted = similar_wanted

        # shows happiness 0 before model starts
        # self.happiness = 0
        self.entropy = 0       

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(self.width, self.height, torus=True)

        self.n_agents = 0

        self.running = True

        self.populate_grid(init_positive, init_negative, init_neutral)

        self.use_network = use_network
        if self.use_network:
            self.network_p = network_p
            self.G = nx.erdos_renyi_graph(n=self.n_agents, p=self.network_p)
            self.populate_network()
            self.randomize_part = randomize_part
            self.decrease_intolerance = decrease_intolerance
        
        # counts number happy agents upon initialization
        # for agent in self.schedule.agents:
        #     if agent.happy():
        #         self.happiness += 1

        self.datacollector = DataCollector(
            {"happy": lambda m: self.happiness(), # Model-level count of happy agents
             "entropy": "entropy"},
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )
        self.collect()
        
    def new_agent(self, agent_type, pos):
        """ Add a new agent of type 'agent_type' to the grid at the position 'pos'. """

        new_agent = agent_type(self.n_agents, self, pos)

        self.n_agents += 1
        
        self.grid.place_agent(new_agent, pos)
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

    def populate_network(self):
        list_of_random_nodes = self.random.sample(self.G.nodes(), self.n_agents)

        for agent in self.schedule.agents:
            node_id = list_of_random_nodes.pop()
            agent.node = node_id
            self.G.nodes[node_id]["agent"] = agent

    def happiness(self):
        return int(sum([agent.happy() for agent in self.schedule.agents]))

    def step(self, collect=True):
        '''
        Method that calls the step method for each of the agents.
        '''

        self.schedule.steps += 1 # Needed for OFAT

        # happiness counter always includes neutral agents
        # self.happiness = self.neutral
        
        # neutral agents don't move (always happy) so skip step if neutral
        for agent in self.schedule.agents:
            if type(agent) == Neutral:
                continue
            agent.step()

        if self.happiness() == self.schedule.get_agent_count():
            self.running = False

        if collect:
            self.collect()

        if self.use_network:
            nx.algorithms.swap.double_edge_swap(self.G, nswap=int(self.randomize_part * self.n_agents), max_tries=1000)

    def collect(self):
        self.entropy = self.calc_entropy()

        # Save the statistics (need to import as well)
        self.datacollector.collect(self)
        
    def run(self, max_iterations=1000, collect=True):
        iteration_count = 0

        while iteration_count < max_iterations:

            self.step(collect=collect)
            
            if not self.running:
                return

            iteration_count += 1

    def calc_entropy(self):
        points = []
        types = []

        for agent in self.schedule.agents:
            # Neutrals are ignored in the entropy calculations
            if isinstance(agent, Neutral):
                continue
            elif isinstance(agent, Positive):
                type_value = 0
            else:
                type_value = 1

            points.append(list(agent.pos))
            types.append(type_value)

        return leibovici_entropy(points, types, d=1.5).entropy