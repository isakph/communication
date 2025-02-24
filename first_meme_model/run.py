from model import MemeModel
from server import server # I'll figure this stuff out later

model = MemeModel(seed=2154651, meme_number=10)

for _ in range(20):
    model.step()

data = model.datacollector.get_model_vars_dataframe()
print(data)

# if __name__ == "__main__":
#     server.port = 8521  # or any open port
#     server.launch()