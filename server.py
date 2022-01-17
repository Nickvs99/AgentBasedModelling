from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
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

# You can change this to whatever ou want. Make sure to make the different types
# of agents distinguishable
def agent_portrayal(agent):
    portrayal = {
                #  "Shape": "circle",
                 "Shape": "rect",
                #  "Color": "green",
                 "Filled": "true",
                 "Layer": 0,
                #  "r": 1,
                 "w": 1,
                 "h": 1,
                 }
    
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

# # Create a dynamic linegraph
# chart = ChartModule([{"Label": "Positive",
#                       "Color": "green"},
#                       {"Label": "Negative",
#                       "Color": "red"}],
#                     data_collector_name='datacollector')

init_positive = int(0.27 * width * height)
init_negative = init_positive
init_neutral = int(0.27 * width * height)

# Create the server, and pass the grid and the graph
server = ModularServer(GridModel,
                       [grid],
                       "Segregation Model",
                       {"width":width, "height":height, "init_positive": init_positive, "init_negative": init_negative, "init_neutral": init_neutral})

server.port = 8521

server.launch()
