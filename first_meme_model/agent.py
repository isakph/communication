import math
import random

from mesa import Agent, Model

class MemeAgent(Agent):
    def __init__(self, unique_id: int, model: Model, meme: str):
        super().__init__(unique_id, model)
        self.meme = meme

    
    def step(self):
        """
        Defines the step that an agent will take during a step.
        For now, let's stick with one action on a random neighbour.
        """
        neighbors = self.model.grid.get_neighbors(self.unique_id, include_center=False)
        if neighbors:
            neighbor_id = self.random.choice(neighbors)
            neighbor_agent = self.model.schedule.agents[neighbor_id]

            # if there is a neighbor, try to get them to accept your meme:
            neighbor_agent.consider_new_meme(self.meme)


    def consider_new_meme(self, incoming_meme: str) -> bool:
        """
        I'm not sure what kind of mechanism I should go for here. 
        One hypothesis is that simpler memes should be accepted with a given probability.
        If most memes start out being rather long and complex,
        we can track how simple memes spread.
        """
        
        def acceptance_probability(current_meme, incoming_meme, alpha=1):
            """
            A helper function that calculates the probability for accepting an incoming meme. 
            If the incoming string is a lot shorter than the current meme, the probability
            for accepting the meme will approach 1.
            """
            L_c = len(current_meme)
            L_i = len(incoming_meme)
            p = 1 / (1 + math.exp(alpha * (L_i - L_c)))
            return p
        
        p = acceptance_probability(self.meme, incoming_meme)

        if random.random() < p:
            self.meme = incoming_meme