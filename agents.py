from mesa import Agent

class GeneralAgent(Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos
        self.node = None
        # self.happy = True

    def similar_network_neighbors(self):
        # neighbourhood is a list of the neighbours directly around the agent
        neighbourhood = [self.model.G.nodes[neighbour]["agent"][0] for neighbour in self.model.G.neighbors(self.node)]
        
        if len(neighbourhood) == 0:
            return 0

        # counts neutral types as same type as well
        same_type = sum(1 for neighbour in neighbourhood if type(neighbour) == type(self) or type(neighbour) == Neutral)
        return same_type/len(neighbourhood)

    def similar_neighbors(self):
        # neighbourhood is a list of the neighbours directly around the agent
        neighbourhood = self.model.grid.get_neighbors(self.pos, moore=True, radius = 1)

        if len(neighbourhood) == 0:
            return 0

        # counts neutral types as same type as well
        same_type = sum(1 for neighbour in neighbourhood if type(neighbour) == type(self) or type(neighbour) == Neutral)
        return same_type/len(neighbourhood)

    def happy(self):
        if type(self) == Neutral or self.similar_neighbors() >= self.model.similar_wanted or (self.model.use_network and self.similar_network_neighbors() >= self.model.similar_wanted):
            return True
        
        return False
        
    def step(self): #, similar_wanted):
        if not self.happy():
            self.model.grid.move_to_empty(self)
            # return False
        else:
            self.model.happiness += 1
            # return True

class Positive(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

class Negative(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

class Neutral(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
