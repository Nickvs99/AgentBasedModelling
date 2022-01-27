from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from gridmodel import *
import agents

# Import the implemented classes
import IPython
import os
import sys

# # Change stdout so we can ignore most prints etc.
# orig_stdout = sys.stdout
# sys.stdout = open(os.devnull, 'w')
# IPython.get_ipython().magic("run gridmodel.py")
# sys.stdout = orig_stdout

class HappinessCounter(TextElement):
    """
    Shows the number of happy agents
    """
    def render(self, model):
        return f"Happy agents: {int(sum([agent.happy() for agent in model.schedule.agents]))}/{model.schedule.get_agent_count()}"

class Segregation_Param_Test(TextElement):
    """
    Shows the number of happy agents
    """
    def render(self, model):
        return "Average similar neighbors: " + str(np.mean([agent.similar_neighbors(agent.neighbors()) for agent in model.schedule.agents]))

# You can change this to whatever ou want. Make sure to make the different types
# of agents distinguishable
def agent_portrayal(agent):
    portrayal = {
                #"Shape": "circle",
                # "Shape": "rect",
                #  "Color": "green",
                 "Filled": "true",
                 "Layer": 0,
                #  "r": 1,
                # "w": 1,
                # "h": 1,
                 }
    # happy agents are rect and unhappy circles
    if not agent.happy():
        portrayal["Shape"] = "circle"
        portrayal["r"] = "0.9"
    else:
        portrayal["Shape"] = "rect"
        portrayal["w"] = "1"
        portrayal["h"] = "1"

    if isinstance(agent, agents.Positive):
        portrayal["Color"] = "green"
    elif isinstance(agent, agents.Negative):
        portrayal["Color"] = "red"
    else:
        portrayal["Color"] = "black"

    return portrayal

width = 20
height = 25
resolution = 500
grid = CanvasGrid(agent_portrayal, height, width, resolution*min(1, (height/width)), resolution*min(1, (width/height)))

happy_counter = HappinessCounter()

# Create a dynamic linegraph
chart = ChartModule([{"Label": "happy",
                      "Color": "green"}],
                    data_collector_name='datacollector')

proportion_agents = int(0.27 * width * height)
parameters = {
    "width": width,
    "height": height,
    # proportion agents is starting value, then can slide from 0 to max agents with steps of 1% of agent number
    "init_positive": UserSettableParameter("slider","Number Positive Agents:",proportion_agents, 0, width*height, 0.01*width*height),
    "init_negative": UserSettableParameter("slider","Number Negative Agents:",proportion_agents, 0, width*height, 0.01*width*height), 
    "init_neutral": UserSettableParameter("slider","Number Neutral Agents:",proportion_agents, 0, width*height, 0.01*width*height),
    "similar_wanted": UserSettableParameter("slider","Proportion Similarity Desired:",3/8, 0, 1, 1/8),
    "use_network": UserSettableParameter("slider","Use network?", 0, 0, 1, 1),
    "network_p": UserSettableParameter("slider","Network parameter:",0.02, 0, 0.2, 0.01),
    "randomize_part": UserSettableParameter("slider","Randomize part of network at step:",0.0, 0, 1, 0.05)
}

# Create the server, and pass the grid and the graph
server = ModularServer(GridModel,
                       [grid, happy_counter, Segregation_Param_Test(), chart],
                       "Segregation Model",
                       parameters)

server.port = 8521

server.launch()
