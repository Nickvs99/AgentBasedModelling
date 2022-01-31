
# AgentBasedModelling

### Introduction
This model is an extension of Schellings segregation model. Schelling originally showed that a small bias in neighbour preference can have a significant effect on the segregation proportion in a large population. In this model we will be researching what the effects of neutral agents have on this effect originally found by Schelling.

To do this the research question will be answered:
``` Does the introduction of neutral agents in a Schelling segregation model yield  increased entropy in comparison to a Schelling segregation model without neutral agents?``` 

To run this model type the following command in the AgentBasedModelling folder:
``` ipython server.py``` 
Legend for the model:
<ul>
  <li>:green_square: = Happy Positive agents</li>
  <li>:green_circle: = Unhappy Positive agents</li>
  <li>:red_square: = Happy Negative agents</li>
  <li>:red_circle: = Unhappy Negative agents</li>
  <li>:black_large_square: = Happy Neutral agents</li>
  <li>:white_large_square: = Unallocated living space </li>
</ul>

### Model
Like Schelling if an agent is unhappy due the lack of similarity of the surrounding neighbours, the agents will decide to move. However now the model also consists of neutral agents, which are always happy with the location they live and other agents consider neutral agents similar as well. Futhermore a social network has been added. This social network influences the preferences the agents have on the desired similarity in neighbours.
The model consists of the changeable variables:
<ul>
  <li>Number of Positive, Negative and Neutral agents</li>
  <li>Preferred number of similar neighbours</li>
  <li>Social network influence </li>
</ul>

### Analysis
Segregation is measured as the amount of entropy and the influence of the parameters in computed in the sensitivity analysis.
