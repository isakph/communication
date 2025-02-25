from pandas import DataFrame

from model import MemeModel


def run_model(
        N: int = 100,
        seed: int = 2154651,
        p: float = 0.2,
        meme_number: int = 4,
        MEME_LOWER_BOUND: int = 4,
        MEME_UPPER_BOUND: int = 10,
        steps: int = 20
) -> DataFrame:
    """
    Runs a simple model of how memes can spread through a social network. 
    The network is a random graph. 
    The probability for an agent to accept an incoming meme depends on the length of the 
    memes involved, where the shorter meme has a higher chance, and p = 0.5 if equal length.

    When the simulation is over, the DataFrame containing the data of the model is returned.

    Args: 
        N (int): the no. of agents.
        seed (int): the seed for the random methods of the model.
        p (float): the probability of two nodes being connected in the random graph.
        meme_number (int): the no. of memes.
        MEME_LOWER_BOUND (int): the lower bound for the length of a meme.
        MEME_UPPER_BOUND (int): the upper bound for the length of a meme. 
    """
    model = MemeModel(N, seed, p, meme_number, MEME_LOWER_BOUND, MEME_UPPER_BOUND)

    for _ in range(steps):
        model.step()

    data = model.datacollector.get_model_vars_dataframe()
    return data


if __name__ == "__main__":
    data = run_model()
    print(data)