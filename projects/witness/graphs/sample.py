import networkx as nx
import matplotlib.pyplot as plt
G = nx.read_adjlist('puzzle1.graph')

tried = []

# while true:
#     l = list(nx.shortest_simple_paths(G, 'm', 'i'))
#     longest = l[-1]

l = list(nx.shortest_simple_paths(G, 'm', 'i'))
longest = l[-1]
