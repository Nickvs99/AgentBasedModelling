from mesa import Agent

class GeneralAgent(Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos

    def step(self, similar_wanted):
        neighbourhood = self.model.grid.get_neighbors(self.pos, moore=True)
        same_type = sum(1 for neighbour in neighbourhood if type(neighbour) == type(self))

        if len(neighbourhood) >  0 and same_type/len(neighbourhood) < similar_wanted:
            self.model.grid.move_to_empty(self)

class Positive(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

class Negative(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)