from mesa import Agent

class Positive(Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos

class Negative(Agent):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos