from mesa import Agent

class GeneralAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos
        self.node = None
        self.theta = self.model.similar_wanted

    def neighbors(self):
        """ 
        Returns a list of the neighbors directly around the agent 
        """
        return self.model.grid.get_neighbors(self.pos, moore=True, radius=self.model.radius)

    def social_contacts(self):
        """ 
        Returns a list of the agents connected to this agent in the social network. 
        """
        return [self.model.G.nodes[neighbor]["agent"] for neighbor in self.model.G.neighbors(self.node)]

    def similar_neighbors(self, neighborhood):
        """ 
        Given a neighborhood, returns the fraction of neighbors 
        that are the same type as this agent or Neutral.
        """
        if len(neighborhood) == 0:
            return 0

        # count the number neighbors that are the same type as this agent *or* Neutral
        # since all agents are happy with Neutral neighbors
        same_type = sum(1 for neighbor in neighborhood if type(neighbor) == type(self) or type(neighbor) == Neutral)
        return same_type/len(neighborhood)

class PolarizedAgent(GeneralAgent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def happy(self):
        """ 
        Returns whether or not this agent is happy with its neighbors. 
        """
        if self.similar_neighbors(self.neighbors()) >= self.theta:
            return True
        
        return False

    def step(self):
        '''
        Unhappy agents move to a new position.
        '''
        if not self.happy():
            self.model.grid.move_to_empty(self)

class Neutral(GeneralAgent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def happy(self):
        """ 
        Neutral agents are always happy where they are. 
        This function is necessary to count the number of happy agents in the model.
        """
        return True

    def step(self):
        '''
        Neutral agents decrease their neighbors' theta.
        '''
        if self.model.use_network:
            for neighbor in self.social_contacts():
                neighbor.theta *= self.model.decrease_intolerance

class Positive(PolarizedAgent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

class Negative(PolarizedAgent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)