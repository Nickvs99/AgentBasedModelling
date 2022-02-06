from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from gridmodel import *
import agents

class HappinessCounter(TextElement):
    """
    Shows the number of happy agents.
    """
    def render(self, model):
        return f"Happy agents: {int(sum([agent.happy() for agent in model.schedule.agents]))}/{model.schedule.get_agent_count()}"

class Avg_Similar(TextElement):
    """
    Shows the average number of similar neighbors an agent has.
    """
    def render(self, model):
        return "Average similar neighbors: " + str(np.mean([agent.similar_neighbors(agent.neighbors()) for agent in model.schedule.agents]))

def agent_portrayal(agent):
    portrayal = {"Filled": "true",
                 "Layer": 0}

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

    # show a circle in the middle of an agent that gets brighter when its theta has been reduced
    if agent.model.use_network:
        portrayal["text"] = "●"
        enlightened = 1 - agent.theta/agent.model.similar_wanted
        portrayal["text_color"] = "#" + f"{hex(int(255*(max(enlightened, isinstance(agent, agents.Negative))))).split('x')[-1].zfill(2)}{hex(int(255*(1-(1-(enlightened))*(1-0.5*isinstance(agent, agents.Positive))))).split('x')[-1].zfill(2)}{hex(int(255*(enlightened))).split('x')[-1].zfill(2)}" 
    
    return portrayal

size = 20
resolution = 500
grid = CanvasGrid(agent_portrayal, size, size, resolution, resolution)

happy_counter = HappinessCounter()

# create a dynamic linegraph
chart = ChartModule([{"Label": "happy",
                      "Color": "green"},
                      {"Label": "entropy",
                      "Color": "red"}],
                    data_collector_name='datacollector')

parameters = {
    "size": size,
    # proportion agents is starting value, then can slide from 0 to max agents with steps of 1% of agent number
    "density": UserSettableParameter("slider","Density:",0.7, 0, 1, 0.01),
    "init_neutral": UserSettableParameter("slider","Number Neutral Agents:",0.2, 0, 1, 0.01),
    "similar_wanted": UserSettableParameter("slider","Proportion Similarity Desired:",3/8, 0, 1, 1/8),
    "use_network": UserSettableParameter("slider","Use network?", 0, 0, 1, 1),
    "network_p": UserSettableParameter("slider","Network parameter:",0.02, 0, 0.2, 0.01),
    "randomize_part": UserSettableParameter("slider","Randomize part of network at step:",0.0, 0, 1, 0.05),
    "decrease_intolerance": UserSettableParameter("slider","Neutral \"convincing rate\":",0.99, 0.9, 1, 0.001),
    "radius": UserSettableParameter("slider", "Neighbourhood Radius:", 1, 0, 5, 1)
}

# create the server, and pass the grid and the graph
server = ModularServer(GridModel,
                       [grid, happy_counter, Avg_Similar(), chart],
                       "Segregation Model",
                       parameters)

server.port = 8521

server.launch()