from mesa import Agent

class GeneralAgent(Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos

    def step(self, similar_wanted):
        # wat doet de get_neighbors met vakken waar niemand is? is dan de lengte te lang voor de proportie similar wanted
        neighbourhood = self.model.grid.get_neighbors(self.pos, moore=True)
        # counts neutral types as same type as well
        same_type = sum(1 for neighbour in neighbourhood if type(neighbour) == type(self) or type(neighbour) == Neutral)
        if len(neighbourhood) >  0 and same_type/len(neighbourhood) < similar_wanted:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happiness += 1

class Positive(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

class Negative(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

class Neutral(GeneralAgent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
