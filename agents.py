from mesa import Agent

class GeneralAgent(Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos
        self.node = None
        self.theta = self.model.similar_wanted

    def neighbors(self):
        # a list of the neighbors directly around the agent
        return self.model.grid.get_neighbors(self.pos, moore=True, radius = self.model.radius)

    def network_neighbors(self):
        # a list of the neighbors connected to the agent
        return [self.model.G.nodes[neighbor]["agent"] for neighbor in self.model.G.neighbors(self.node)]

    def similar_neighbors(self, neighborhood):
        if len(neighborhood) == 0:
            return 0

        # counts neutral types as same type as well
        same_type = sum(1 for neighbor in neighborhood if type(neighbor) == type(self) or type(neighbor) == Neutral)
        return same_type/len(neighborhood)

    def happy(self):
        if type(self) == Neutral or self.similar_neighbors(self.neighbors()) >= self.theta: # or (self.model.use_network and self.similar_neighbors(self.network_neighbors()) >= self.theta):
            return True
        
        return False
        
    def step(self):
        if not type(self) == Neutral:
            if not self.happy():
                self.model.grid.move_to_empty(self)

        elif self.model.use_network:
            for neighbor in self.network_neighbors():
                neighbor.theta *= self.model.decrease_intolerance

class Positive(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

class Negative(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

class Neutral(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
