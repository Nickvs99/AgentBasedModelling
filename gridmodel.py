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
    def __init__(self, size = 100, density=0.75, init_neutral = 0.33, similar_wanted = 0.75,
                 use_network = 1, network_p = 0.02, randomize_part = 0.5, decrease_intolerance = 0.99, radius = 1):
        """
        Initialize the GridModel. init_positive, init_negative, and init_neutral are relative
        values, e.g. 5% of the grid needs to have neutral agents then set init_neutral to 0.05.
        """
        
        if not 0 <= density <= 1:
            raise Exception("Error. Invalid density value. density has to be between 0 and 1.")
        
        self.size = size
        self.similar_wanted = similar_wanted
        self.radius = radius
        self.use_network = use_network
        self.n_agents = 0

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(int(self.size), int(self.size), torus=True)
        self.populate_grid(size, density, init_neutral)

        if self.use_network:
            self.randomize_part = randomize_part
            self.decrease_intolerance = decrease_intolerance
            self.G = nx.erdos_renyi_graph(n=self.n_agents, p=network_p)
            self.populate_network()
        
        self.datacollector = DataCollector(
            {"happy": lambda m: self.happiness() / self.n_agents, # model-level count of happiness and entropy
             "entropy": lambda m: self.calc_entropy()},
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        self.running = True
        self.datacollector.collect(self) # needs to be commented out when performing experiments.py
    
    def new_agent(self, agent_type, pos):
        """ 
        Add a new agent of type 'agent_type' to the grid at the position 'pos'. 
        """
        new_agent = agent_type(self.n_agents, self, pos)

        self.grid.place_agent(new_agent, pos)
        self.schedule.add(new_agent)
        self.n_agents += 1

        return new_agent

    def get_random_empty_pos(self):
        """ 
        Return a random unoccupied position. 
        """
        if len(self.grid.empties) == 0:
            raise Exception("Error. No empty spaces are available.")

        return random.choice(sorted(self.grid.empties))

    def populate_grid(self, size, density, init_neutral):
        """ 
        Populates the grid with Positive and Negative agents. 
        """
        total_agents = size * size * density
        
        for _ in range(int(total_agents * (1 - init_neutral) / 2)):
            self.new_agent(Positive, self.get_random_empty_pos())

        for _ in range(int(total_agents * (1 - init_neutral) / 2)):
            self.new_agent(Negative, self.get_random_empty_pos())
        
        for _ in range(int(total_agents * init_neutral)):
            self.new_agent(Neutral, self.get_random_empty_pos())

    def populate_network(self):
        """
        Give each node in the empty network an agent.
        """
        list_of_random_nodes = self.random.sample(self.G.nodes(), self.n_agents)

        for agent in self.schedule.agents:
            node_id = list_of_random_nodes.pop()
            agent.node = node_id
            self.G.nodes[node_id]["agent"] = agent

    def happiness(self):
        """
        Count the number of happy agents currently in the model.
        """
        return int(sum([agent.happy() for agent in self.schedule.agents]))

    def step(self, collect=True):
        """
        Method that executes one step of the simulation.
        """
        self.schedule.step()

        # stop running if all agents are happy
        if self.happiness() == self.schedule.get_agent_count():
            self.running = False

        if collect:
            self.datacollector.collect(self)

        # swap a number of random edges in the social network
        if self.use_network:
            nx.algorithms.swap.double_edge_swap(self.G, nswap=int(self.randomize_part * self.n_agents), max_tries=5000)
        
    def run(self, max_iterations=1000, collect=True):
        """
        Method that runs the model until either all agents are happy
        or until a specific amount of steps is reached.
        """
        for _ in range(max_iterations):
            self.step(collect=collect)
            
            if not self.running:
                break

    def calc_entropy(self):
        """
        Method that quantifies the segregation in the model 
        using leibovici entropy.
        """
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