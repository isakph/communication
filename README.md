# communication
Defining and modelling communication in various ways. 

To begin with, I would quite simply like to learn how to model simple social systems, such as social networks with agent-based modelling. 
Later on, a desideratum is to model advanced things like Niklas Luhmann's conception of social systems, and so on, possibly by making the agents [anticipatory](https://jasss.soc.surrey.ac.uk/8/2/7.html). 
We will see, though. 

Since the law is a social system according to this view, I will also look into how I can simulate legal interactions and the like. 

### First Meme Model
Use `first_meme_model/run.py` to run the model.
`server.py` is currently just some garbled copy-paste from earlier Mesa versions that I have to fix;
currently, it neither works nor sees any use. 

This is the first simulation that I am doing here.
(Visualization is not yet implemented.)
The model is a simple network, a random graph. 
The memes are strings of varying length.
When the model makes a step, the agents interact, in a random order, with a neighbour. 
A neighbour is a node that they are connected two. 

There are 100 nodes and 100 agents, one for each node. 
The probability that two nodes are connected is $p = 0.2$.
When agents interact, they try to spread the meme that they currently hold. 
The agent that they reach out to accepts the incoming meme with a probability of

![Logistic Function](https://latex.codecogs.com/png.latex?p%20%3D%20%5Cfrac%7B1%7D%7B1%20%2B%20e%5E%7B%5Calpha%20%28L_i%20-%20L_c%29%7D%7D)

where $L_i$ is the length of the incoming string and $L_c$ is the length of the current string.
$\alpha$ is set to $1$.
This means that when the two memes are of equal length, the exponent becomes zero and we get $p = 0.5$, meaning that it's a toss up whether the agent chooses to keep the meme they already have or to adapt the incoming one. 
When the difference in length is large, the shorter meme is preferred by a commensurate amount.

There's a chance that I implement some more refined interaction and stuff after I have figured the visualization bits out.
I imagine that the visualizations should at least include how the network looks and the graphs for the relative frequencies of the memes throughout the simulation. 
