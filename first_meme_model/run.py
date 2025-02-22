import seaborn as sns

from model import MemeModel
# from server import server # I'll figure this stuff out later

model = MemeModel(seed=2154651)

for _ in range(10):
    model.step()

data = model.datacollector.get_model_vars_dataframe()
print(data)
# for agent in model.agents:
#     print(agent.meme)
# g = sns.lineplot(data=data) # TODO: Visualisation

# if __name__ == "__main__":
#     server.port = 8521  # or any open port
#     server.launch()