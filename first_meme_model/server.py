from mesa.visualization.modules import NetworkModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from model import MemeModel


color_palette = [
    "Red", "Green", "Blue", "Cyan", "Magenta", "Yellow", 
    "Orange", "Purple", "Brown", "Gray"
]
color_map = {}  # meme_string -> color

def get_node_color(agent):
    """
    Assign colors to memes in a first-come, first-served manner,
    cycling through color_palette if needed.
    """
    meme = agent.meme
    if meme not in color_map:
        # Assign the next color (cycling back if we go past the end)
        assigned_color = color_palette[len(color_map) % len(color_palette)]
        color_map[meme] = assigned_color

    return color_map[meme]


def network_portrayal(G):
    """
    G is the NetworkX Graph. Each node can have multiple agents,
    but typically there's only one agent per node in this model.
    We'll color nodes according to the agent's meme.
    """

    portrayal = dict()
    nodes_list = []
    for (node_id, agents) in G.nodes.data("agent"):
        # The following assumes only one agent per node, will have to 
        # do something about that in the future
        agent = agents[0] if agents else None
        color = "Gray"
        label = ""
        if agent:
            color = get_node_color(agent)
            label = f"{agent.meme}"

        nodes_list.append({
            "id": node_id,
            "color": color,
            "size": 6,
            "shape": "circle",
            "label": label,
        })

    # Edges: just store source and target
    edges_list = []
    for (source, target) in G.edges:
        edges_list.append({"source": source, "target": target})

    portrayal["nodes"] = nodes_list
    portrayal["edges"] = edges_list
    return portrayal

# Create the network visualization module
network_module = NetworkModule(network_portrayal, 500, 500)

# Create a chart to track fraction of each meme over time
chart = ChartModule([
    {"Label": "Meme_A_Frac", "Color": "Red"},
    {"Label": "Meme_B_Frac", "Color": "Green"},
    {"Label": "Meme_C_Frac", "Color": "Blue"},
])

# The ModularServer ties everything together.
server = ModularServer(
    MemeModel,
    [network_module, chart],
    "Meme Spread Model",
    {
        "N": 20,  # Default number of agents (nodes)
        "p": 0.2  # Default probability for edges in Erdos-Renyi
    }
)
server.port = 8521  # You can change this port if needed
