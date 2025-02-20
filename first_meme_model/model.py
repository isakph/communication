import random
import string

import mesa
from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx

from agent import MemeAgent


def generate_meme(lower_bound: int = 1, upper_bound: int = 100):
    # Strings can consist of using letters and digits:
    characters = string.ascii_letters + string.digits

    # Choose the length of the meme
    length = random.randint(lower_bound, upper_bound)

    # Generate the random string
    random_string = ''.join(random.choices(characters, k=length))

    return random_string


class MemeModel(Model):
    def __init__(
        self,
        N: int = 100,
        seed: float = None,
        p: float = 0.2 # TODO: Figure out what value to use here
    ):
        super().__init__(seed=seed)
        self.num_agents = N
        self.seed = seed
        if not seed:
            self.seed = self.random.seed()
        self.G = nx.erdos_renyi_graph(n=N, p=p, seed=self.seed)
        self.grid: NetworkGrid = NetworkGrid(self.G)

        # Generate four memes of random length in the interval [1,100]
        memes = [generate_meme() for i in range(4)] 
        # create agents
        for node_id in self.grid.nodes():
            # meme = self.random.choice(memes)
            agent = MemeAgent.create_agents(model=self, memes=memes)
            self.agents.register_agent(agent)
            self.grid.place_agent(agent, node_id)

        self.datacollector = DataCollector(
            {f"meme{n}": 
            lambda m: # here, m.schedule.agents no longer works, because I changed the code above. Figure out what to replace it with.
            # It will be something to do with self.agents, but I'm not quite clear on what.
            sum([1 for a in m.schedule.agents if a.meme == memes[n]]) / m.num_agents for n in memes}
        )