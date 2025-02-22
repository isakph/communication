import random
import string

from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx

from agent import MemeAgent


class MemeModel(Model):
    def __init__(
        self,
        N: int = 100,
        seed: int = None,
        p: float = 0.2, # TODO: Figure out what value to use here
        meme_number: int = 4
    ):
        super().__init__(seed=seed)
        self.num_agents = N
        self.seed = seed
        if not seed:
            self.seed = self.random.seed()
        self.G = nx.erdos_renyi_graph(n=N+1, p=p, seed=self.seed)
        self.grid: NetworkGrid = NetworkGrid(self.G)

        # Generate a number of memes of random length in the interval [1,100]
        memes = [self.generate_meme() for _ in range(meme_number)] 

        # create and place agents
        agents = MemeAgent.create_agents(model=self, n=N, memes=memes)
        for a in agents:
            self.grid.place_agent(a, a.unique_id) # not sure if this does what I want

        # TODO: This doesn't work or do anything
        self.datacollector = DataCollector(
            # model_reporters = {f"meme{n}": lambda m: sum([1 for a in m.agents if a.meme == memes[n]]) / m.num_agents for n in range(len(memes))}
            # model_reporters = {memes[n]: lambda m: sum([1 for a in m.agents if a.meme == memes[n]]) / m.num_agents for n in range(len(memes))}
            model_reporters = {
                memes[0]: lambda m: sum([1 for a in m.agents if a.meme == memes[0]]) / m.num_agents, 
                memes[1]: lambda m: sum([1 for a in m.agents if a.meme == memes[1]]) / m.num_agents, 
                memes[2]: lambda m: sum([1 for a in m.agents if a.meme == memes[2]]) / m.num_agents, 
                memes[3]: lambda m: sum([1 for a in m.agents if a.meme == memes[3]]) / m.num_agents
            }
            # {"agent_count": lambda m: len(m.agents)}
            # TODO: here, m.schedule.agents no longer works, because I changed the code above. Figure out what to replace it with.
            # It will be something to do with self.agents, but I'm not quite clear on what.
        )


    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("spread_meme") # not sure if do() or shuffle_do() makes more sense


    @staticmethod
    def generate_meme(lower_bound: int = 1, upper_bound: int = 10):
        """
        Generates a random string of letters and digits with a random length
        in the interval given as lower and upper bounds.
        TODO: Consider replacing random with NumPy
        """
        # Strings consist of letters and digits:
        characters = string.ascii_letters + string.digits

        # Choose a random length in the interval
        length = random.randint(lower_bound, upper_bound)

        # Generate the random string
        random_string = ''.join(random.choices(characters, k=length))

        return random_string