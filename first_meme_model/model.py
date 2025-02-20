from mesa import Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx

from agent import MemeAgent

class MemeModel(Model):
    def __init__(self, N=100, p=0.05):
        self.num_agents = N
        self.network = nx.erdos_renyi_graph(n=N, p=p)
        self.grid = NetworkGrid(self.network)
        self.schedule = RandomActivation(self)

        # create agents
        for i, node in enumerate(self.network.nodes()):
