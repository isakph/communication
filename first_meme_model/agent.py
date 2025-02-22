import math
import random

from mesa import Agent, Model

class MemeAgent(Agent):
    """
    A MemeAgent requires a mesa.Model and a list of memes (strings).
    """
    def __init__(self, model: Model, memes: list[str]):
        super().__init__(model)
        self.memes: list[str] = memes
        self.meme: str = self.random.choice(memes)
        self.meme_id: int = self._find_meme_id()


    def _find_meme_id(self):
        """
        Helper method to track which meme an agent holds.
        """
        for n, m in enumerate(self.memes):
            if m == self.meme:
                self.meme_id = n


    def spread_meme(self):
        """
        Defines the step that an agent will take during a step.
        For now, let's stick with one action on a random neighbour.
        """
        neighbors = self.model.grid.get_neighbors(self.unique_id, include_center=False)
        if neighbors:
            neighbor_agent = self.random.choice(neighbors)

            # if there is a neighbor, try to get them to accept your meme:
            neighbor_agent.consider_new_meme(self.meme)


    def consider_new_meme(self, incoming_meme: str) -> bool:
        """
        I'm not sure what kind of mechanism I should go for here. 
        One hypothesis is that simpler memes should be accepted with a given probability.
        If most memes start out being rather long and complex,
        we can track how simple memes spread.
        TODO: Make the interaction more complex. Implement, e.g., confidence? Let's say
        confidence rises when you meet somebody with the same meme, and that confidence
        impacts both acceptance and how persuasive you are. 
        """

        assert(isinstance(incoming_meme, str))

        def acceptance_probability(current_meme: str, incoming_meme: str, alpha=1):
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
            # print(f"changed opinion! replaced {self.meme} by {incoming_meme}") # seems to work
            self.meme = incoming_meme
            self.meme_id = self._find_meme_id()
            return True
        return False


if __name__ == "__main__":
    """
    Just checking for stupid bugs
    """
    memes = ["asdf", "a", "asdfasdf"]
    model = Model()
    agent_1 = MemeAgent(model, memes)
    agent_2 = MemeAgent(model, memes)
    agent_1.consider_new_meme(memes[2])